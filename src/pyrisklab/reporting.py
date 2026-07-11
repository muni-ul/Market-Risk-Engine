from __future__ import annotations

import hashlib
import json
import math
import platform
import shutil
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from pyrisklab import __version__
from pyrisklab.exceptions import ReportingError, RunError
from pyrisklab.models import RunConfig


def prepare_output_dir(output_dir: Path, run_name: str, overwrite: bool = False) -> Path:
    run_dir = output_dir / run_name
    if run_dir.exists():
        if not overwrite:
            raise RunError(f"{run_dir} already exists. Use --overwrite or choose a different run_name.")
        try:
            shutil.rmtree(run_dir)
        except OSError as exc:
            raise RunError(
                f"could not overwrite {run_dir}. Check folder permissions."
            ) from exc
    try:
        run_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RunError(
            f"could not create {run_dir}. Check folder permissions."
        ) from exc
    return run_dir


def save_config_copy(config_path: Path, run_dir: Path) -> Path:
    target = run_dir / "config_used.yaml"
    try:
        shutil.copy2(config_path, target)
    except OSError as exc:
        raise RunError(
            f"could not copy config_used.yaml to {run_dir}. Check folder permissions."
        ) from exc
    return target


def save_csv_outputs(run_dir: Path, outputs: dict[str, pd.DataFrame]) -> list[Path]:
    paths = []
    for filename, df in outputs.items():
        df = _require_dataframe(df, filename)
        path = run_dir / filename
        try:
            df.to_csv(path, index=False)
        except OSError as exc:
            raise RunError(
                f"could not write {filename} to {run_dir}. Check folder permissions."
            ) from exc
        paths.append(path)
    return paths


def write_run_metadata(
    run_dir: Path,
    config: RunConfig,
    config_path: Path,
    outputs: dict[str, pd.DataFrame],
) -> Path:
    path = run_dir / "run_metadata.json"
    metadata = {
        "schema_version": 1,
        "project": "PyRiskLab",
        "project_version": __version__,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "run_name": config.run_name,
        "seed": config.seed,
        "config_path": config_path.as_posix(),
        "config_sha256": _sha256_file(config_path),
        "output_dir": run_dir.as_posix(),
        "execution_enabled": config.execution.enabled,
        "benchmark_enabled": config.benchmark.enabled,
        "simulation_only": True,
        "csv_row_counts": _csv_row_counts(outputs),
        "generated_artifacts": _artifact_names(run_dir),
    }
    try:
        path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise RunError(
            f"could not write run_metadata.json to {run_dir}. Check folder permissions."
        ) from exc
    return path


def generate_charts(run_dir: Path, outputs: dict[str, pd.DataFrame]) -> list[Path]:
    return [
        plot_market_path(_required_output(outputs, "market_path.csv"), run_dir),
        plot_option_price(_required_output(outputs, "pricing_history.csv"), run_dir),
        plot_greeks(_required_output(outputs, "greeks_history.csv"), run_dir),
        plot_portfolio_value(_required_output(outputs, "portfolio_history.csv"), run_dir),
        plot_drawdown(_required_output(outputs, "portfolio_history.csv"), run_dir),
    ]


def plot_market_path(market_path: pd.DataFrame, run_dir: Path) -> Path:
    _require(market_path, {"step", "underlying_price"}, "market_path")
    return _line(run_dir / "market_path.png", market_path["step"], market_path["underlying_price"], "Synthetic Market Path", "Simulation Step", "Underlying Price")


def plot_option_price(pricing_history: pd.DataFrame, run_dir: Path) -> Path:
    _require(pricing_history, {"step", "option_price"}, "pricing_history")
    return _line(run_dir / "option_price.png", pricing_history["step"], pricing_history["option_price"], "Black-Scholes Option Price", "Simulation Step", "Option Price")


def plot_greeks(greeks_history: pd.DataFrame, run_dir: Path) -> Path:
    _require(greeks_history, {"step", "delta", "gamma", "vega", "theta", "rho"}, "greeks_history")
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in ["delta", "gamma", "vega", "theta", "rho"]:
        ax.plot(greeks_history["step"], greeks_history[column], label=column)
    ax.set_title("Option Greeks Across Simulated Path")
    ax.set_xlabel("Simulation Step")
    ax.set_ylabel("Greek Value")
    ax.legend()
    fig.tight_layout()
    path = run_dir / "greeks.png"
    return _save_figure(fig, path)


def plot_portfolio_value(portfolio_history: pd.DataFrame, run_dir: Path) -> Path:
    _require(portfolio_history, {"step", "total_value"}, "portfolio_history")
    return _line(run_dir / "portfolio_value.png", portfolio_history["step"], portfolio_history["total_value"], "Simulated Portfolio Value", "Simulation Step", "Portfolio Value ($)")


def plot_drawdown(portfolio_history: pd.DataFrame, run_dir: Path) -> Path:
    _require(portfolio_history, {"step", "drawdown_pct"}, "portfolio_history")
    return _line(run_dir / "drawdown.png", portfolio_history["step"], portfolio_history["drawdown_pct"] * 100, "Portfolio Drawdown", "Simulation Step", "Drawdown (%)")


def write_summary_report(run_dir: Path, config: RunConfig, outputs: dict[str, pd.DataFrame]) -> Path:
    market = _required_output(outputs, "market_path.csv")
    pricing = _required_output(outputs, "pricing_history.csv")
    trades = _required_output(outputs, "trades.csv")
    portfolio = _required_output(outputs, "portfolio_history.csv")
    risk_events = _required_output(outputs, "risk_events.csv")
    benchmark = _optional_output(outputs, "benchmark.csv")
    _require_summary_frame(market, {"underlying_price"}, "market_path")
    _require_summary_frame(pricing, {"option_price"}, "pricing_history")
    _require_summary_frame(portfolio, {"total_value", "drawdown_pct"}, "portfolio_history")
    initial_underlying = _summary_float(
        market["underlying_price"].iloc[0],
        "market_path.underlying_price",
    )
    final_underlying = _summary_float(
        market["underlying_price"].iloc[-1],
        "market_path.underlying_price",
    )
    final_value = _summary_float(portfolio["total_value"].iloc[-1], "portfolio_history.total_value")
    max_drawdown = _summary_float(portfolio["drawdown_pct"].max(), "portfolio_history.drawdown_pct")
    initial_option_price = _summary_float(
        pricing["option_price"].iloc[0],
        "pricing_history.option_price",
    )
    final_option_price = _summary_float(
        pricing["option_price"].iloc[-1],
        "pricing_history.option_price",
    )
    signals = _optional_output(outputs, "signals.csv")
    orders = _optional_output(outputs, "orders.csv")
    if not config.execution.enabled:
        trade_note = "Fake execution was disabled in the config, so proposed orders were not filled."
    elif trades.empty:
        trade_note = "No simulated trades were executed in this run."
    else:
        trade_note = f"{len(trades)} simulated trades were executed."
    risk_note = "No risk events were triggered in this run." if risk_events.empty else f"{len(risk_events)} risk events were recorded."
    benchmark_text = "Benchmark was disabled or skipped."
    if not benchmark.empty:
        _require(benchmark, {"method", "speedup_vs_loop"}, "benchmark")
        vector_rows = benchmark.loc[benchmark["method"] == "numpy_vectorized"]
        if vector_rows.empty:
            raise ReportingError("benchmark DataFrame must include a numpy_vectorized row when benchmark output is not empty.")
        vector = vector_rows.iloc[0]
        speedup = _summary_float(
            vector["speedup_vs_loop"],
            "benchmark.speedup_vs_loop",
        )
        benchmark_text = (
            f"Vectorized NumPy pricing ran {speedup:.2f}x faster "
            "than the Python loop on this machine. Benchmark results vary by hardware, "
            "Python version, and input size."
        )
    artifact_list = "\n".join(f"- `{name}`" for name in _artifact_names(run_dir))
    text = f"""# PyRiskLab Run Summary

Run name: `{config.run_name}`
Seed: `{config.seed}`
Output directory: `{run_dir.as_posix()}`

## Simulation Only

This is a local simulation only. It does not use live market data, place real trades, connect to a brokerage, provide investment advice, or make profitability claims.

## Market Simulation

- Initial underlying price: ${initial_underlying:.2f}
- Final underlying price: ${final_underlying:.2f}
- Generated steps: {len(market)}
- Model: geometric Brownian motion with synthetic data
- Drift assumption: {config.market.drift:.2%}
- Volatility assumption: {config.market.volatility:.2%}
- Trading days per year: {config.market.trading_days}

## Option Contract

- Symbol: `{config.option.symbol}`
- Type: `{config.option.option_type}`
- Strike: ${config.option.strike:.2f}
- Initial days to expiry: {config.option.days_to_expiry}
- Initial model price: ${initial_option_price:.2f}
- Final model price: ${final_option_price:.2f}

## Strategy Signals

- Total signal rows: {len(signals)}
- Proposed simulated orders: {len(orders)}

## Portfolio Results

- Starting cash: ${config.risk.starting_cash:,.2f}
- Number of simulated trades: {len(trades)}
- Final portfolio value: ${final_value:,.2f}
- Max drawdown: {max_drawdown:.2%}
- Risk events: {len(risk_events)}

## Fake Execution

{trade_note}

## Risk Events

{risk_note}

## Benchmark

{benchmark_text}

## Generated Artifacts

{artifact_list}

## Limitations

PyRiskLab uses synthetic paths and a simplified fake execution model. It does not model liquidity, spreads, order books, slippage, taxes, margin, assignment, or real market behavior.
"""
    path = run_dir / "summary_report.md"
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise RunError(
            f"could not write summary_report.md to {run_dir}. Check folder permissions."
        ) from exc
    return path


def generate_reports(run_dir: Path, config: RunConfig, config_path: Path, outputs: dict[str, pd.DataFrame]) -> list[Path]:
    paths = [save_config_copy(config_path, run_dir)]
    paths.extend(save_csv_outputs(run_dir, outputs))
    paths.extend(generate_charts(run_dir, outputs))
    paths.append(write_run_metadata(run_dir, config, config_path, outputs))
    paths.append(write_summary_report(run_dir, config, outputs))
    return paths


def _line(path: Path, x, y, title: str, xlabel: str, ylabel: str) -> Path:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    return _save_figure(fig, path)


def _save_figure(fig, path: Path) -> Path:
    try:
        fig.savefig(path, dpi=140)
    except OSError as exc:
        raise RunError(
            f"could not write {path.name} to {path.parent}. Check folder permissions."
        ) from exc
    finally:
        plt.close(fig)
    return path


def _require(df: pd.DataFrame, columns: set[str], name: str) -> None:
    missing = columns - set(df.columns)
    if missing:
        raise ReportingError(f"{name} DataFrame must include: {', '.join(sorted(missing))}.")


def _require_summary_frame(df: pd.DataFrame, columns: set[str], name: str) -> None:
    _require(df, columns, name)
    if df.empty:
        raise ReportingError(f"{name} DataFrame must include at least one row for summary_report.md.")


def _required_output(outputs: dict[str, pd.DataFrame], filename: str) -> pd.DataFrame:
    try:
        output = outputs[filename]
    except KeyError as exc:
        raise ReportingError(f"required pipeline output is missing: {filename}") from exc
    return _require_dataframe(output, filename)


def _optional_output(outputs: dict[str, pd.DataFrame], filename: str) -> pd.DataFrame:
    if filename not in outputs:
        return pd.DataFrame()
    return _require_dataframe(outputs[filename], filename)


def _csv_row_counts(outputs: dict[str, pd.DataFrame]) -> dict[str, int]:
    return {
        filename: int(len(_require_dataframe(frame, filename)))
        for filename, frame in sorted(outputs.items())
    }


def _require_dataframe(value, filename: str) -> pd.DataFrame:
    if not isinstance(value, pd.DataFrame):
        raise ReportingError(
            f"{filename} pipeline output must be a pandas DataFrame. "
            f"Received {type(value).__name__}."
        )
    return value


def _summary_float(value, field_name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ReportingError(
            f"{field_name} must be numeric for summary_report.md. Received {value!r}."
        ) from exc
    if not math.isfinite(parsed):
        raise ReportingError(
            f"{field_name} must be finite for summary_report.md. Received {value!r}."
        )
    return parsed


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise RunError(
            f"could not read config file for metadata hashing: {path}"
        ) from exc
    return digest.hexdigest()


def _artifact_names(run_dir: Path) -> list[str]:
    try:
        names = {path.name for path in run_dir.iterdir() if path.is_file()}
    except OSError as exc:
        raise RunError(
            f"could not list generated artifacts in {run_dir}. Check folder permissions."
        ) from exc
    names.update({"run_metadata.json", "summary_report.md"})
    return sorted(names)
