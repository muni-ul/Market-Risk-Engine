from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
import pandas as pd

from pyrisklab.analytics import path_analytics
from pyrisklab.greeks import calculate_greeks
from pyrisklab.pricing import black_scholes_price
from pyrisklab.scenarios import ScenarioInputs


@dataclass(frozen=True)
class ScenarioResult:
    inputs: ScenarioInputs
    dates: pd.DatetimeIndex
    portfolio_paths: np.ndarray
    stock_paths: np.ndarray
    summary: dict[str, float]
    analytics: dict[str, object]
    representative: pd.DataFrame
    risk_decisions: pd.DataFrame
    greeks: dict[str, float]
    reconciliation: dict[str, float]

    def paths_frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.portfolio_paths, index=self.dates)


def run_portfolio_scenario(inputs: ScenarioInputs) -> ScenarioResult:
    errors = inputs.validate()
    if errors:
        raise ValueError(" ".join(errors))
    steps = inputs.horizon_days
    rng = np.random.default_rng(inputs.seed)
    dt = 1 / 252
    shocks = rng.standard_normal((steps, inputs.paths))
    increments = (inputs.drift - inputs.volatility**2 / 2) * dt
    increments += inputs.volatility * np.sqrt(dt) * shocks
    stocks = np.vstack(
        [
            np.full(inputs.paths, inputs.initial_price),
            inputs.initial_price * np.exp(np.cumsum(increments, axis=0)),
        ]
    )
    cash = inputs.starting_capital * inputs.cash_pct / 100
    stock_dollars = inputs.starting_capital * inputs.stock_pct / 100
    option_dollars = inputs.starting_capital * inputs.option_pct / 100
    shares = stock_dollars / inputs.initial_price  # fractional shares are supported
    initial_option_price = float(
        black_scholes_price(
            inputs.initial_price,
            inputs.strike,
            inputs.option_expiry_days / 252,
            inputs.risk_free_rate,
            inputs.option_volatility,
            inputs.option_type,
        )
    )
    contracts = option_dollars / (initial_option_price * 100) if initial_option_price > 0 else 0
    remaining_days = np.maximum(inputs.option_expiry_days - np.arange(steps + 1), 0) / 252
    option_prices = black_scholes_price(
        stocks,
        inputs.strike,
        remaining_days[:, None],
        inputs.risk_free_rate,
        inputs.option_volatility,
        inputs.option_type,
    )
    values = cash + shares * stocks + contracts * 100 * option_prices
    analytics = path_analytics(values)
    rep = int(analytics["representative_id"])
    dates = pd.date_range(date.today(), date.today() + timedelta(days=steps), periods=steps + 1)
    representative = pd.DataFrame(
        {
            "date": dates,
            "portfolio_value": values[:, rep],
            "stock_price": stocks[:, rep],
            "cash": cash,
            "stock_value": shares * stocks[:, rep],
            "option_value": contracts * 100 * option_prices[:, rep],
            "drawdown": analytics["drawdowns"],
        }
    )
    ending = np.asarray(analytics["ending"])
    summary = {
        "starting_capital": inputs.starting_capital,
        "median_ending": float(np.median(ending)),
        "median_return": float(np.median(ending) / inputs.starting_capital - 1),
        "probability_below_start": float(np.mean(ending < inputs.starting_capital)),
        "max_drawdown": float(analytics["max_drawdown"]),
        "p10_ending": float(np.quantile(ending, 0.1)),
        "p90_ending": float(np.quantile(ending, 0.9)),
    }
    proposed = stock_dollars + option_dollars
    blocked = proposed > inputs.max_trade_notional
    risk = pd.DataFrame(
        [
            {
                "date": dates[0],
                "action": "Initial allocation",
                "side": "BUY",
                "quantity": round(shares, 3) + round(contracts, 3),
                "notional": proposed,
                "status": "BLOCKED" if blocked else "ACCEPTED",
                "limit": "Maximum trade notional",
                "observed": proposed,
                "explanation": (
                    f"Proposed allocation exceeds the ${inputs.max_trade_notional:,.0f} limit."
                    if blocked
                    else "Initial simulated allocation passed configured risk limits."
                ),
            }
        ]
    )
    current_greeks = {
        k: float(v)
        for k, v in calculate_greeks(
            inputs.initial_price,
            inputs.strike,
            inputs.option_expiry_days / 252,
            inputs.risk_free_rate,
            inputs.option_volatility,
            inputs.option_type,
        ).items()
    }
    final = representative.iloc[-1]
    reconciliation = {
        "cash": cash,
        "stock_value": float(final.stock_value),
        "option_value": float(final.option_value),
        "shares": shares,
        "contracts": contracts,
        "ending_value": float(final.portfolio_value),
    }
    return ScenarioResult(
        inputs,
        dates,
        values,
        stocks,
        summary,
        analytics,
        representative,
        risk,
        current_greeks,
        reconciliation,
    )
