import numpy as np


def _require_matplotlib():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "matplotlib is required for plotting. Install it or skip plotting."
        ) from exc
    return plt


def plot_signals(t: np.ndarray, signals: dict[str, np.ndarray], title: str = "Signals") -> None:
    plt = _require_matplotlib()
    fig, ax = plt.subplots(figsize=(12, 4))
    for name, data in signals.items():
        ax.plot(t, data, label=name)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    fig.tight_layout()


def plot_phases(t: np.ndarray, phases: dict[str, np.ndarray], title: str = "Phases") -> None:
    plt = _require_matplotlib()
    fig, ax = plt.subplots(figsize=(12, 4))
    for name, data in phases.items():
        ax.plot(t, data, label=name)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Phase (rad)")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    fig.tight_layout()


def plot_metrics(
    t: np.ndarray, metrics: dict[str, np.ndarray], title: str = "Metrics"
) -> None:
    plt = _require_matplotlib()
    fig, ax = plt.subplots(figsize=(12, 4))
    for name, data in metrics.items():
        ax.plot(t, data, label=name)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
