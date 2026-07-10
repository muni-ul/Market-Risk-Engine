from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from pyrisklab.exceptions import ConfigError
from pyrisklab.models import (
    BenchmarkConfig,
    ExecutionConfig,
    MarketConfig,
    OptionConfig,
    RiskConfig,
    RunConfig,
    StrategyConfig,
)

RUN_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def load_config(config_path: str | Path) -> RunConfig:
    path = Path(config_path)
    if not path.exists():
        raise ConfigError(f"config file not found: {path}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"could not parse YAML in {path}. Check indentation and syntax.") from exc
    if not raw:
        raise ConfigError("config file is empty.")
    if not isinstance(raw, dict):
        raise ConfigError("config root must be a mapping.")
    return validate_config(raw)


def validate_config(raw: dict[str, Any]) -> RunConfig:
    for section in ("market", "option", "strategy", "risk", "benchmark"):
        _require(raw, section)

    run_name = str(_require(raw, "run_name")).strip()
    if not run_name:
        raise ConfigError("run_name must not be empty.")
    if not RUN_NAME_RE.match(run_name):
        raise ConfigError(f"run_name must use only letters, numbers, underscores, or hyphens. Received {run_name!r}.")

    seed = _as_int(_require(raw, "seed"), "seed")
    output_dir = str(raw.get("output_dir", "results"))

    market_raw = _section(raw, "market")
    option_raw = _section(raw, "option")
    strategy_raw = _section(raw, "strategy")
    risk_raw = _section(raw, "risk")
    benchmark_raw = _section(raw, "benchmark")
    execution_raw = raw.get("execution", {}) or {}

    market = MarketConfig(
        initial_price=_positive(market_raw, "market.initial_price"),
        drift=_as_float(_require(market_raw, "drift", "market.drift"), "market.drift"),
        volatility=_nonnegative(market_raw, "market.volatility"),
        trading_days=_positive_int(market_raw, "market.trading_days"),
        steps=_positive_int(market_raw, "market.steps"),
        paths=_min_int(market_raw, "market.paths", 1),
    )

    option_type = str(_require(option_raw, "option_type", "option.option_type")).lower()
    if option_type not in {"call", "put"}:
        raise ConfigError(f"option.option_type must be 'call' or 'put'. Received {option_type!r}.")
    option = OptionConfig(
        underlying_symbol=_nonempty_str(option_raw, "option.underlying_symbol"),
        symbol=_nonempty_str(option_raw, "option.symbol"),
        option_type=option_type,
        strike=_positive(option_raw, "option.strike"),
        risk_free_rate=_as_float(_require(option_raw, "risk_free_rate", "option.risk_free_rate"), "option.risk_free_rate"),
        volatility=_nonnegative(option_raw, "option.volatility"),
        days_to_expiry=_min_int(option_raw, "option.days_to_expiry", 0),
    )

    strategy = StrategyConfig(
        name=_nonempty_str(strategy_raw, "strategy.name"),
        buy_delta_below=_as_float(_require(strategy_raw, "buy_delta_below", "strategy.buy_delta_below"), "strategy.buy_delta_below"),
        sell_delta_above=_as_float(_require(strategy_raw, "sell_delta_above", "strategy.sell_delta_above"), "strategy.sell_delta_above"),
        trade_quantity=_positive_int(strategy_raw, "strategy.trade_quantity"),
        min_steps_between_trades=_as_int(strategy_raw.get("min_steps_between_trades", 0), "strategy.min_steps_between_trades"),
    )
    if strategy.name != "simple_delta_rule":
        raise ConfigError(f"strategy.name must be 'simple_delta_rule'. Received {strategy.name!r}.")
    if not -1 <= strategy.buy_delta_below <= 1:
        raise ConfigError(f"strategy.buy_delta_below must be between -1 and 1. Received {strategy.buy_delta_below}.")
    if not -1 <= strategy.sell_delta_above <= 1:
        raise ConfigError(f"strategy.sell_delta_above must be between -1 and 1. Received {strategy.sell_delta_above}.")
    if strategy.buy_delta_below >= strategy.sell_delta_above:
        raise ConfigError(
            "strategy.buy_delta_below must be less than strategy.sell_delta_above. "
            f"Received {strategy.buy_delta_below} and {strategy.sell_delta_above}."
        )
    if strategy.min_steps_between_trades < 0:
        raise ConfigError(f"strategy.min_steps_between_trades must be >= 0. Received {strategy.min_steps_between_trades}.")

    execution = ExecutionConfig(
        enabled=_as_bool(execution_raw.get("enabled", True), "execution.enabled"),
        fill_model=str(execution_raw.get("fill_model", "deterministic_mid")),
        commission_per_contract=_as_float(execution_raw.get("commission_per_contract", 0.0), "execution.commission_per_contract"),
        contract_multiplier=_as_int(execution_raw.get("contract_multiplier", 100), "execution.contract_multiplier"),
    )
    if execution.fill_model != "deterministic_mid":
        raise ConfigError(f"execution.fill_model must be 'deterministic_mid'. Received {execution.fill_model!r}.")
    if execution.commission_per_contract < 0:
        raise ConfigError(f"execution.commission_per_contract must be >= 0. Received {execution.commission_per_contract}.")
    if execution.contract_multiplier <= 0:
        raise ConfigError(f"execution.contract_multiplier must be > 0. Received {execution.contract_multiplier}.")

    risk = RiskConfig(
        starting_cash=_positive(risk_raw, "risk.starting_cash"),
        max_position_quantity=_min_int(risk_raw, "risk.max_position_quantity", 0),
        max_trade_notional=_nonnegative(risk_raw, "risk.max_trade_notional"),
        max_drawdown_pct=_nonnegative(risk_raw, "risk.max_drawdown_pct"),
        max_loss_pct=_nonnegative(risk_raw, "risk.max_loss_pct"),
        stop_trading_on_breach=_as_bool(risk_raw.get("stop_trading_on_breach", True), "risk.stop_trading_on_breach"),
    )
    if risk.max_drawdown_pct > 1:
        raise ConfigError(f"risk.max_drawdown_pct must be <= 1. Received {risk.max_drawdown_pct}.")
    if risk.max_loss_pct > 1:
        raise ConfigError(f"risk.max_loss_pct must be <= 1. Received {risk.max_loss_pct}.")

    enabled = _as_bool(_require(benchmark_raw, "enabled", "benchmark.enabled"), "benchmark.enabled")
    benchmark = BenchmarkConfig(
        enabled=enabled,
        num_prices=_positive_int(benchmark_raw, "benchmark.num_prices") if enabled else _as_int(benchmark_raw.get("num_prices", 1), "benchmark.num_prices"),
        seed=_as_int(benchmark_raw.get("seed", seed), "benchmark.seed"),
        tolerance=_as_float(benchmark_raw.get("tolerance", 1e-8), "benchmark.tolerance"),
    )
    if benchmark.tolerance <= 0:
        raise ConfigError(f"benchmark.tolerance must be > 0. Received {benchmark.tolerance}.")

    return RunConfig(run_name, seed, output_dir, market, option, strategy, execution, risk, benchmark)


def _section(raw: dict[str, Any], name: str) -> dict[str, Any]:
    value = _require(raw, name)
    if not isinstance(value, dict):
        raise ConfigError(f"{name} section must be a mapping.")
    return value


def _require(raw: dict[str, Any], key: str, field: str | None = None) -> Any:
    if key not in raw:
        raise ConfigError(f"missing required field: {field or key}")
    return raw[key]


def _as_float(value: Any, field: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{field} must be numeric. Received {value!r}.") from exc
    return parsed


def _as_int(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise ConfigError(f"{field} must be an integer. Received {value!r}.")
    if isinstance(value, float) and not value.is_integer():
        raise ConfigError(f"{field} must be an integer. Received {value!r}.")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"{field} must be an integer. Received {value!r}.") from exc
    return parsed


def _as_bool(value: Any, field: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    raise ConfigError(f"{field} must be true or false. Received {value!r}.")


def _positive(raw: dict[str, Any], field: str) -> float:
    key = field.split(".")[-1]
    value = _as_float(_require(raw, key, field), field)
    if value <= 0:
        raise ConfigError(f"{field} must be > 0. Received {value}.")
    return value


def _nonnegative(raw: dict[str, Any], field: str) -> float:
    key = field.split(".")[-1]
    value = _as_float(_require(raw, key, field), field)
    if value < 0:
        raise ConfigError(f"{field} must be >= 0. Received {value}.")
    return value


def _positive_int(raw: dict[str, Any], field: str) -> int:
    key = field.split(".")[-1]
    value = _as_int(_require(raw, key, field), field)
    if value <= 0:
        raise ConfigError(f"{field} must be > 0. Received {value}.")
    return value


def _min_int(raw: dict[str, Any], field: str, minimum: int) -> int:
    key = field.split(".")[-1]
    value = _as_int(_require(raw, key, field), field)
    if value < minimum:
        raise ConfigError(f"{field} must be >= {minimum}. Received {value}.")
    return value


def _nonempty_str(raw: dict[str, Any], field: str) -> str:
    key = field.split(".")[-1]
    value = str(_require(raw, key, field)).strip()
    if not value:
        raise ConfigError(f"{field} must not be empty.")
    return value
