from __future__ import annotations

from pathlib import Path

import pandas as pd

from pyrisklab.benchmark import run_pricing_benchmark
from pyrisklab.config import load_config
from pyrisklab.execution import create_orders_from_signals, execute_orders
from pyrisklab.greeks import calculate_greeks_for_market_path
from pyrisklab.market import simulate_gbm_path
from pyrisklab.models import RunResult
from pyrisklab.portfolio import Portfolio, build_portfolio_history
from pyrisklab.pricing import price_market_path, to_contract
from pyrisklab.reporting import generate_reports, prepare_output_dir
from pyrisklab.risk import RiskManager, risk_events_frame
from pyrisklab.strategy import generate_signals


def run_simulation(config_path: str | Path, overwrite: bool = False, progress=None) -> RunResult:
    _emit(progress, "[1/7] Loading config...")
    path = Path(config_path)
    config = load_config(path)
    run_dir = prepare_output_dir(Path(config.output_dir), config.run_name, overwrite)

    _emit(progress, "[2/7] Simulating market path...")
    market_path = simulate_gbm_path(config.market, config.seed)
    option = to_contract(config.option)

    _emit(progress, "[3/7] Pricing option and calculating Greeks...")
    pricing_history = price_market_path(market_path, option, config.market.trading_days)
    greeks_history = calculate_greeks_for_market_path(market_path, option, config.market.trading_days)

    _emit(progress, "[4/7] Running strategy, risk checks, and fake execution...")
    signals = generate_signals(pricing_history, greeks_history, config.strategy)
    orders = create_orders_from_signals(signals, pricing_history)
    audited_orders, approved_orders, risk_events = _apply_risk(orders, config)
    trades = execute_orders(
        approved_orders,
        commission_per_contract=config.execution.commission_per_contract,
        contract_multiplier=config.execution.contract_multiplier,
        fill_model=config.execution.fill_model,
    )

    _emit(progress, "[5/7] Tracking portfolio value and drawdown...")
    portfolio_history = build_portfolio_history(
        trades,
        pricing_history,
        config.risk.starting_cash,
        config.execution.contract_multiplier,
    )

    _emit(progress, "[6/7] Running benchmark...")
    benchmark = run_pricing_benchmark(config.benchmark)

    outputs = {
        "market_path.csv": market_path,
        "pricing_history.csv": pricing_history,
        "greeks_history.csv": greeks_history,
        "signals.csv": signals,
        "orders.csv": audited_orders,
        "trades.csv": trades,
        "portfolio_history.csv": portfolio_history,
        "risk_events.csv": risk_events,
        "benchmark.csv": benchmark,
    }

    _emit(progress, "[7/7] Saving reports...")
    generate_reports(run_dir, config, path, outputs)
    return RunResult(config.run_name, run_dir, path, "completed")


def _emit(progress, message: str) -> None:
    if progress is not None:
        progress(message)


def _apply_risk(orders: pd.DataFrame, config) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    manager = RiskManager(config.risk, config.execution.contract_multiplier)
    risk_portfolio = Portfolio(config.risk.starting_cash, config.execution.contract_multiplier)
    audited = []
    approved = []
    for row in orders.itertuples(index=False):
        snapshot = risk_portfolio.mark_to_market(int(row.step), str(row.symbol), float(row.requested_price))
        current_position = risk_portfolio.current_quantity(str(row.symbol))
        result = manager.validate_order(
            row,
            current_position,
            snapshot.total_value,
            snapshot.drawdown_pct,
            risk_portfolio.cash,
            config.execution.commission_per_contract * int(row.quantity),
        )
        order_record = row._asdict()
        if result.allowed:
            order_record["status"] = "APPROVED"
            order_record["risk_reason"] = ""
            approved_order = row._asdict()
            approved.append(approved_order)
            trade = execute_orders(
                pd.DataFrame([approved_order], columns=orders.columns),
                commission_per_contract=config.execution.commission_per_contract,
                contract_multiplier=config.execution.contract_multiplier,
                fill_model=config.execution.fill_model,
            ).iloc[0]
            risk_portfolio.apply_trade(trade)
        else:
            order_record["status"] = "BLOCKED"
            order_record["risk_reason"] = result.events[0].reason if result.events else "Blocked by risk manager."
        audited.append(order_record)
    audited_columns = [*orders.columns, "status", "risk_reason"]
    return (
        pd.DataFrame(audited, columns=audited_columns),
        pd.DataFrame(approved, columns=orders.columns),
        risk_events_frame(manager.events),
    )
