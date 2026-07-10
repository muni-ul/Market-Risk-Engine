from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from pyrisklab.exceptions import PricingError
from pyrisklab.models import OptionContract


def to_contract(option) -> OptionContract:
    return OptionContract(
        option.underlying_symbol,
        option.symbol,
        option.option_type,
        option.strike,
        option.risk_free_rate,
        option.volatility,
        option.days_to_expiry,
    )


def intrinsic_value(spot, strike: float, option_type: str):
    prices = np.asarray(spot, dtype=float)
    if option_type == "call":
        result = np.maximum(prices - strike, 0.0)
    elif option_type == "put":
        result = np.maximum(strike - prices, 0.0)
    else:
        raise PricingError(f"option_type must be 'call' or 'put'. Received {option_type!r}.")
    return _scalar_if_scalar(result)


def black_scholes_price(spot, strike: float, time_to_expiry, risk_free_rate: float, volatility: float, option_type: str):
    if option_type not in {"call", "put"}:
        raise PricingError(f"option_type must be 'call' or 'put'. Received {option_type!r}.")
    if not np.isfinite(strike) or strike <= 0:
        raise PricingError(f"strike must be greater than 0. Received {strike}.")
    if not np.isfinite(risk_free_rate):
        raise PricingError(f"risk_free_rate must be finite. Received {risk_free_rate}.")
    if not np.isfinite(volatility) or volatility < 0:
        raise PricingError(f"volatility must be >= 0. Received {volatility}.")

    s = np.asarray(spot, dtype=float)
    t = np.asarray(time_to_expiry, dtype=float)
    s, t = np.broadcast_arrays(s, t)
    if not np.isfinite(s).all() or (s <= 0).any():
        raise PricingError("underlying_price must be finite and greater than 0.")
    if not np.isfinite(t).all() or (t < 0).any():
        raise PricingError("time_to_expiry must be finite and >= 0.")

    prices = np.zeros_like(s, dtype=float)
    expired = t <= 0
    if expired.any():
        prices[expired] = intrinsic_value(s[expired], strike, option_type)

    active = ~expired
    if active.any():
        if volatility == 0:
            discounted_strike = strike * np.exp(-risk_free_rate * t[active])
            if option_type == "call":
                prices[active] = np.maximum(s[active] - discounted_strike, 0.0)
            else:
                prices[active] = np.maximum(discounted_strike - s[active], 0.0)
        else:
            sqrt_t = np.sqrt(t[active])
            d1 = (np.log(s[active] / strike) + (risk_free_rate + 0.5 * volatility**2) * t[active]) / (volatility * sqrt_t)
            d2 = d1 - volatility * sqrt_t
            if option_type == "call":
                prices[active] = s[active] * norm.cdf(d1) - strike * np.exp(-risk_free_rate * t[active]) * norm.cdf(d2)
            else:
                prices[active] = strike * np.exp(-risk_free_rate * t[active]) * norm.cdf(-d2) - s[active] * norm.cdf(-d1)
    return _scalar_if_scalar(prices)


def price_market_path(market_path: pd.DataFrame, option: OptionContract, trading_days: int) -> pd.DataFrame:
    _require_columns(market_path, {"step", "time_years", "underlying_price"}, "market path")
    if market_path.empty:
        raise PricingError("market path is empty. Run market simulation before pricing options.")
    if trading_days <= 0:
        raise PricingError(f"trading_days must be > 0. Received {trading_days}.")
    time_to_expiry = np.maximum((option.initial_days_to_expiry - market_path["step"].to_numpy()) / trading_days, 0.0)
    option_price = black_scholes_price(
        market_path["underlying_price"].to_numpy(),
        option.strike,
        time_to_expiry,
        option.risk_free_rate,
        option.volatility,
        option.option_type,
    )
    return pd.DataFrame(
        {
            "step": market_path["step"],
            "time_years": market_path["time_years"],
            "underlying_price": market_path["underlying_price"],
            "time_to_expiry": time_to_expiry,
            "symbol": option.symbol,
            "option_symbol": option.symbol,
            "option_type": option.option_type,
            "strike": option.strike,
            "risk_free_rate": option.risk_free_rate,
            "volatility": option.volatility,
            "option_price": option_price,
        }
    )


def _require_columns(df: pd.DataFrame, columns: set[str], name: str) -> None:
    missing = columns - set(df.columns)
    if missing:
        raise PricingError(f"{name} must include columns: {', '.join(sorted(missing))}.")


def _scalar_if_scalar(result: np.ndarray):
    array = np.asarray(result)
    if array.ndim == 0:
        return float(array)
    return result
