from __future__ import annotations

import math
from collections.abc import Callable
from numbers import Real
from pathlib import Path

import pandas as pd

from pyrisklab.benchmark import run_pricing_benchmark
from pyrisklab.config import load_config
from pyrisklab.execution import TRADE_COLUMNS, create_orders_from_signals, execute_orders
from pyrisklab.exceptions import RunError
from pyrisklab.greeks import calculate_greeks_for_market_path
from pyrisklab.market import simulate_gbm_path
from pyrisklab.models import (
    ORDER_AUDIT_COLUMNS,
    ORDER_RISK_REASON_COLUMN,
    ORDER_STATUS_APPROVED,
    ORDER_STATUS_BLOCKED,
    ORDER_STATUS_COLUMN,
    ORDER_STATUS_SKIPPED,
    RunResult,
)
from pyrisklab.portfolio import Portfolio, build_portfolio_history
from pyrisklab.pricing import price_market_path, to_contract
from pyrisklab.reporting import generate_reports, prepare_output_dir
from pyrisklab.risk import RiskManager, risk_events_frame
from pyrisklab.strategy import generate_signals


ProgressCallback = Callable[[str], None]


def run_simulation(
    config_path: str | Path,
    overwrite: bool = False,
    progress: ProgressCallback | None = None,
) -> RunResult:
    _emit(progress, "[1/7] Loading config...")
    path = Path(config_path)
    config = load_config(path)
    run_dir = prepare_output_dir(Path(config.output_dir), config.run_name, overwrite)

    _emit(progress, "[2/7] Simulating market path...")
    market_path = simulate_gbm_path(config.market, config.seed)
    option = to_contract(config.option)

    _emit(progress, "[3/7] Pricing option and calculating Greeks...")
    pricing_history = price_market_path(market_path, option, config.market.trading_days)
    greeks_history = calculate_greeks_for_market_path(
        market_path,
        option,
        config.market.trading_days,
    )

    _emit(progress, "[4/7] Running strategy, risk checks, and fake execution...")
    signals = generate_signals(pricing_history, greeks_history, config.strategy)
    orders = create_orders_from_signals(signals, pricing_history)
    if config.execution.enabled:
        audited_orders, approved_orders, risk_events = _apply_risk(orders, config)
        trades = execute_orders(
            approved_orders,
            commission_per_contract=config.execution.commission_per_contract,
            contract_multiplier=config.execution.contract_multiplier,
            fill_model=config.execution.fill_model,
        )
    else:
        audited_orders = _skip_execution(orders)
        risk_events = risk_events_frame([])
        trades = pd.DataFrame(columns=TRADE_COLUMNS)

    _emit(progress, "[5/7] Tracking portfolio value and drawdown...")
    portfolio_history = build_portfolio_history(
        trades,
        pricing_history,
        config.risk.starting_cash,
        config.execution.contract_multiplier,
    )

    if config.benchmark.enabled:
        _emit(progress, "[6/7] Running benchmark...")
    else:
        _emit(progress, "[6/7] Benchmark disabled by config. Skipping...")
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


def _emit(progress: ProgressCallback | None, message: str) -> None:
    if progress is not None:
        progress(message)


def _apply_risk(orders: pd.DataFrame, config) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    manager = RiskManager(config.risk, config.execution.contract_multiplier)
    risk_portfolio = Portfolio(config.risk.starting_cash, config.execution.contract_multiplier)
    audited = []
    approved = []
    for row in orders.itertuples(index=False):
        snapshot = risk_portfolio.mark_to_market(
            int(row.step),
            str(row.symbol),
            float(row.requested_price),
        )
        current_position = risk_portfolio.current_quantity(str(row.symbol))
        result = manager.validate_order(
            row,
            current_position,
            snapshot.total_value,
            snapshot.drawdown_pct,
            risk_portfolio.cash,
            config.execution.commission_per_contract * _as_order_quantity(row.quantity),
        )
        order_record = row._asdict()
        if result.allowed:
            order_record[ORDER_STATUS_COLUMN] = ORDER_STATUS_APPROVED
            order_record[ORDER_RISK_REASON_COLUMN] = ""
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
            order_record[ORDER_STATUS_COLUMN] = ORDER_STATUS_BLOCKED
            order_record[ORDER_RISK_REASON_COLUMN] = (
                result.events[0].reason if result.events else "Blocked by risk manager."
            )
        audited.append(order_record)
    audited_columns = [*orders.columns, *ORDER_AUDIT_COLUMNS]
    return (
        pd.DataFrame(audited, columns=audited_columns),
        pd.DataFrame(approved, columns=orders.columns),
        risk_events_frame(manager.events),
    )


def _skip_execution(orders: pd.DataFrame) -> pd.DataFrame:
    audited = orders.copy()
    audited[ORDER_STATUS_COLUMN] = ORDER_STATUS_SKIPPED
    audited[ORDER_RISK_REASON_COLUMN] = "Fake execution disabled by config."
    return audited.reindex(columns=[*orders.columns, *ORDER_AUDIT_COLUMNS])


def _as_order_quantity(value) -> int:
    if isinstance(value, bool):
        raise RunError(
            f"order quantity must be an integer before risk orchestration. Received {value!r}."
        )
    if isinstance(value, Real):
        numeric = float(value)
        if not math.isfinite(numeric):
            raise RunError(
                "order quantity must be a finite integer before risk orchestration. "
                f"Received {value!r}."
            )
        if not numeric.is_integer():
            raise RunError(
                f"order quantity must be an integer before risk orchestration. Received {value!r}."
            )
    try:
        quantity = int(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise RunError(
            f"order quantity must be an integer before risk orchestration. Received {value!r}."
        ) from exc
    if quantity <= 0:
        raise RunError(
            f"order quantity must be > 0 before risk orchestration. Received {quantity}."
        )
    return quantity
