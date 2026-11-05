"""Small-sample statistics for eval claims: bootstrap CIs and paired tests.

Deliberately dependency-free (stdlib only) and seeded, so a reported interval
is reproducible. These are the routines behind the "don't call a 3-point
swing a win" rule in the ``llm-evaluation`` skill.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Interval:
    point: float
    low: float
    high: float
    n: int
    method: str = "percentile-bootstrap"
    confidence: float = 0.95

    def __str__(self) -> str:
        return f"{self.point:.3f} [{self.low:.3f}, {self.high:.3f}] n={self.n}"


def bootstrap_ci(
    values: Sequence[float],
    *,
    statistic: Callable[[Sequence[float]], float] = lambda xs: sum(xs) / len(xs),
    n_boot: int = 2000,
    confidence: float = 0.95,
    seed: int = 0,
) -> Interval:
    """Percentile bootstrap CI. Uses a fixed seed for reproducibility."""
    n = len(values)
    if n == 0:
        return Interval(0.0, 0.0, 0.0, 0, confidence=confidence)
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        stats.append(statistic(sample))
    stats.sort()
    alpha = (1.0 - confidence) / 2.0
    low = stats[max(0, int(math.floor(alpha * n_boot)))]
    high = stats[min(n_boot - 1, int(math.ceil((1 - alpha) * n_boot)) - 1)]
    return Interval(statistic(values), low, high, n, confidence=confidence)


def mcnemar(
    a: Sequence[float], b: Sequence[float], *, threshold: float = 0.5
) -> Tuple[float, float, int, int]:
    """Exact-ish McNemar test for paired binary outcomes.

    ``a`` and ``b`` are per-sample scores for the same cases under two systems.
    Returns ``(statistic, p_value, b01, b10)`` where ``b01`` = a passes & b
    fails and ``b10`` = a fails & b passes. ``p_value`` comes from the
    chi-square approximation with continuity correction (df=1), which is the
    standard for n >= 25; below that treat the p-value as indicative only.
    """
    if len(a) != len(b):
        raise ValueError("paired test needs equal-length sequences")
    b01 = sum(1 for x, y in zip(a, b) if x >= threshold and y < threshold)
    b10 = sum(1 for x, y in zip(a, b) if x < threshold and y >= threshold)
    if b01 + b10 == 0:
        return 0.0, 1.0, b01, b10
    stat = (abs(b01 - b10) - 1) ** 2 / (b01 + b10)
    # Survival function of chi-square with 1 dof = erfc(sqrt(stat/2)).
    p = math.erfc(math.sqrt(stat / 2.0))
    return stat, p, b01, b10


def wilson_interval(successes: int, n: int, confidence: float = 0.95) -> Interval:
    """Wilson score interval for a proportion; stable at n<50 and p near 0/1."""
    if n == 0:
        return Interval(0.0, 0.0, 0.0, 0, "wilson", confidence)
    z = _z_for(confidence)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return Interval(p, max(0.0, centre - half), min(1.0, centre + half), n, "wilson", confidence)


_Z_TABLE = {0.8: 1.2816, 0.9: 1.6449, 0.95: 1.9600, 0.98: 2.3263, 0.99: 2.5758}


def _z_for(confidence: float) -> float:
    if confidence in _Z_TABLE:
        return _Z_TABLE[confidence]
    # Acklam's inverse normal CDF approximation (good to ~1e-9).
    p = 1.0 - (1.0 - confidence) / 2.0
    return _inv_normal_cdf(p)


def _inv_normal_cdf(p: float) -> float:
    a = [-39.69683028665376, 220.9460984245205, -275.9285104469687,
         138.3577518672690, -30.66479806614716, 2.506628277459239]
    b = [-54.47609879822406, 161.5858368580409, -155.6989798598866,
         66.80131188771972, -13.28068155288572]
    c = [-0.007784894002430293, -0.3223964580411365, -2.400758277161838,
         -2.549732539343734, 4.374664141464968, 2.938163982698783]
    d = [0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (
        ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def is_significant(p_value: float, alpha: float = 0.05) -> bool:
    return p_value < alpha


def minimum_detectable_effect(n: int, baseline: float = 0.5, z: float = 1.96) -> float:
    """Rough absolute effect (in pass-rate points) detectable at 95% / 80% power."""
    if n <= 0:
        return 1.0
    return z * math.sqrt(2 * baseline * (1 - baseline) / n)
