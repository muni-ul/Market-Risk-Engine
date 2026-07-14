from __future__ import annotations

import numpy as np


def path_analytics(values: np.ndarray) -> dict[str, object]:
    """Calculate display analytics once, independently of chart rendering."""
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 1:
        raise ValueError("values must contain at least two dates and one path")
    quantiles = np.quantile(values, [0.1, 0.5, 0.9], axis=1)
    ending = values[-1]
    representative_id = int(np.argmin(np.abs(ending - np.median(ending))))
    representative = values[:, representative_id]
    peaks = np.maximum.accumulate(representative)
    drawdowns = representative / peaks - 1.0
    trough = int(np.argmin(drawdowns))
    peak = int(np.argmax(representative[: trough + 1]))
    return {
        "p10": quantiles[0],
        "median": quantiles[1],
        "p90": quantiles[2],
        "ending": ending,
        "representative_id": representative_id,
        "representative": representative,
        "drawdowns": drawdowns,
        "high_idx": int(np.argmax(representative)),
        "low_idx": int(np.argmin(representative)),
        "drawdown_peak_idx": peak,
        "drawdown_trough_idx": trough,
        "max_drawdown": float(drawdowns[trough]),
    }
