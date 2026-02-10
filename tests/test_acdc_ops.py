import numpy as np

from harmony.ops.acdc import ac_power, ac_power_trend, acdc_split, dc_slope, ema_lpf


def test_ema_lpf_and_split_empty() -> None:
    empty = np.array([])
    assert ema_lpf(empty).size == 0
    dc, ac = acdc_split(empty)
    assert dc.size == 0
    assert ac.size == 0


def test_ac_power_and_trend_small() -> None:
    assert ac_power(np.array([])) == 0.0
    assert ac_power_trend(np.array([1.0, 2.0, 3.0]), np.array([0.0, 1.0, 2.0])) == 0.0


def test_ac_power_trend_increasing() -> None:
    x_ac = np.array([0.5, 0.5, 0.5, 1.5, 1.5, 1.5])
    t = np.arange(len(x_ac))
    trend = ac_power_trend(x_ac, t)
    assert trend > 0


def test_dc_slope_short_series() -> None:
    assert dc_slope(np.array([1.0]), np.array([0.0])) == 0.0
    slope = dc_slope(np.array([0.0, 2.0]), np.array([0.0, 1.0]))
    assert abs(slope - 2.0) < 1e-12
