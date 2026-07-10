class PyRiskLabError(Exception):
    """Base exception for expected PyRiskLab errors."""


class ConfigError(PyRiskLabError):
    """Raised for invalid config files or config values."""


class PricingError(PyRiskLabError):
    """Raised when option pricing cannot be completed."""


class GreeksError(PyRiskLabError):
    """Raised when Greek calculation cannot be completed."""


class StrategyError(PyRiskLabError):
    """Raised when strategy signal generation fails."""


class ExecutionError(PyRiskLabError):
    """Raised when fake execution cannot create valid orders or trades."""


class MarketSimulationError(PyRiskLabError):
    """Raised when market simulation cannot be completed."""


class PortfolioError(PyRiskLabError):
    """Raised when portfolio state cannot be updated safely."""


class RiskError(PyRiskLabError):
    """Raised when risk validation cannot be completed safely."""


class ReportingError(PyRiskLabError):
    """Raised when report content cannot be generated from pipeline outputs."""


class BenchmarkError(PyRiskLabError):
    """Raised when benchmark execution or validation fails."""


class RunError(PyRiskLabError):
    """Raised for run setup, orchestration, and output artifact problems."""
