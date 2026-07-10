from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from pyrisklab.exceptions import GreeksError
from pyrisklab.models import OptionContract


def calculate_greeks(spot, strike: float, time_to_expiry, risk_free_rate: float, volatility: float, option_type: str) -> dict[str, object]:
    if option_type not in {"call", "put"}:
        raise GreeksError(f"option_type must be 'call' or 'put'. Received {option_type!r}.")
    _reject_bool_scalar(spot, "underlying_price")
    _reject_bool_scalar(time_to_expiry, "time_to_expiry")
    _reject_bool_scalar(strike, "strike")
    _reject_bool_scalar(risk_free_rate, "risk_free_rate")
    _reject_bool_scalar(volatility, "volatility")
    if not np.isfinite(strike) or strike <= 0:
        raise GreeksError(f"strike must be greater than 0. Received {strike}.")
    if not np.isfinite(risk_free_rate):
        raise GreeksError(f"risk_free_rate must be finite. Received {risk_free_rate}.")
    if not np.isfinite(volatility) or volatility < 0:
        raise GreeksError(f"volatility must be >= 0. Received {volatility}.")

    s = np.asarray(spot, dtype=float)
    t = np.asarray(time_to_expiry, dtype=float)
    s, t = np.broadcast_arrays(s, t)
    if not np.isfinite(s).all() or (s <= 0).any():
        raise GreeksError("underlying_price must be finite and greater than 0.")
    if not np.isfinite(t).all() or (t < 0).any():
        raise GreeksError("time_to_expiry must be finite and >= 0.")

    delta = np.zeros_like(s, dtype=float)
    gamma = np.zeros_like(s, dtype=float)
    vega = np.zeros_like(s, dtype=float)
    theta = np.zeros_like(s, dtype=float)
    rho = np.zeros_like(s, dtype=float)

    boundary = (t <= 0) | (volatility == 0)
    if boundary.any():
        fwd_strike = strike * np.exp(-risk_free_rate * t[boundary])
        if option_type == "call":
            delta[boundary] = np.where(s[boundary] > fwd_strike, 1.0, np.where(s[boundary] < fwd_strike, 0.0, 0.5))
        else:
            delta[boundary] = np.where(s[boundary] < fwd_strike, -1.0, np.where(s[boundary] > fwd_strike, 0.0, -0.5))

    active = ~boundary
    if active.any():
        sqrt_t = np.sqrt(t[active])
        d1 = (np.log(s[active] / strike) + (risk_free_rate + 0.5 * volatility**2) * t[active]) / (volatility * sqrt_t)
        d2 = d1 - volatility * sqrt_t
        pdf = norm.pdf(d1)
        gamma[active] = pdf / (s[active] * volatility * sqrt_t)
        vega[active] = s[active] * pdf * sqrt_t / 100.0
        if option_type == "call":
            delta[active] = norm.cdf(d1)
            theta[active] = (-(s[active] * pdf * volatility) / (2 * sqrt_t) - risk_free_rate * strike * np.exp(-risk_free_rate * t[active]) * norm.cdf(d2)) / 365.0
            rho[active] = strike * t[active] * np.exp(-risk_free_rate * t[active]) * norm.cdf(d2) / 100.0
        else:
            delta[active] = norm.cdf(d1) - 1
            theta[active] = (-(s[active] * pdf * volatility) / (2 * sqrt_t) + risk_free_rate * strike * np.exp(-risk_free_rate * t[active]) * norm.cdf(-d2)) / 365.0
            rho[active] = -strike * t[active] * np.exp(-risk_free_rate * t[active]) * norm.cdf(-d2) / 100.0
    return {key: _scalar_if_scalar(value) for key, value in {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}.items()}


def calculate_greeks_for_market_path(market_path: pd.DataFrame, option: OptionContract, trading_days: int) -> pd.DataFrame:
    required = {"step", "time_years", "underlying_price"}
    missing = required - set(market_path.columns)
    if missing:
        raise GreeksError(f"market path must include columns: {', '.join(sorted(missing))}.")
    if market_path.empty:
        raise GreeksError("market path is empty. Run market simulation before calculating Greeks.")
    if trading_days <= 0:
        raise GreeksError(f"trading_days must be > 0. Received {trading_days}.")
    time_to_expiry = np.maximum((option.initial_days_to_expiry - market_path["step"].to_numpy()) / trading_days, 0.0)
    greeks = calculate_greeks(
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
            **greeks,
        }
    )


def _scalar_if_scalar(result: np.ndarray):
    array = np.asarray(result)
    if array.ndim == 0:
        return float(array)
    return result


def _reject_bool_scalar(value, field_name: str) -> None:
    if isinstance(value, bool):
        raise GreeksError(f"{field_name} must be numeric. Received {value!r}.")
