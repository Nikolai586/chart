from sys import exit
import logging
from logging.handlers import RotatingFileHandler
import matplotlib.pyplot as plt
import numpy as np


handler = RotatingFileHandler(
    "app.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=10,
    encoding="utf-8",
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def plot_four_series_interactive(
    x,
    y1, y2, y3, y4,
    labels=("Ряд 1", "Ряд 2", "Ряд 3", "Ряд 4"),
    styles=None,
    title="График с 4 последовательностями",
    xlabel="X",
    ylabel="Y",
    figsize=(11, 6),
    grid=True,
    snap_tolerance=0.15,
    save_path=None,
):
    x = np.asarray(x, dtype=float)
    series = [np.asarray(y, dtype=float) for y in (y1, y2, y3, y4)]
    default_styles = [
        {"color": "tab:blue",   "linestyle": "-",  "linewidth": 2, "marker": "o"},
        {"color": "tab:orange", "linestyle": "--", "linewidth": 2, "marker": "s"},
        {"color": "tab:green",  "linestyle": "-.", "linewidth": 2, "marker": "^"},
        {"color": "tab:red",    "linestyle": ":",  "linewidth": 2, "marker": "D"},
    ]

    if styles is None:
        styles = default_styles
    else:
        styles = [{**default_styles[i], **(styles[i] if i < len(styles) else {})}
                  for i in range(4)]
    fig, ax = plt.subplots(figsize=figsize)
    lines = []

    for y, label, style in zip(series, labels, styles):
        s = {**style, "markersize": 4}
        (ln,) = ax.plot(x, y, label=label, **s)
        lines.append(ln)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if grid:
        ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="best")
    highlight_pts = [
        ax.plot([], [], "o", color=styles[i]["color"],
                markersize=12, markeredgecolor="black",
                markeredgewidth=1.5, zorder=5, visible=False)[0]
        for i in range(4)
    ]
    vline = ax.axvline(0, color="gray", linestyle=":", linewidth=1,
                       alpha=0.8, visible=False, zorder=1)
    annot = ax.annotate(
        "", xy=(0, 0), xytext=(12, 12), textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.4", fc="lightyellow", ec="gray", alpha=0.95),
        fontsize=9, zorder=10, visible=False,
    )
    x_min, x_max = float(x.min()), float(x.max())
    tolerance = (x_max - x_min) * snap_tolerance

    def on_move(event):
        if event.inaxes is not ax or event.xdata is None:
            _hide()
            fig.canvas.draw_idle()
            return
        idx = int(np.argmin(np.abs(x - event.xdata)))

        if abs(x[idx] - event.xdata) > tolerance:
            _hide()
            fig.canvas.draw_idle()
            return
        x_hit = x[idx]
        y_vals = [s[idx] for s in series]

        for pt, yv in zip(highlight_pts, y_vals):
            pt.set_data([x_hit], [yv])
            pt.set_visible(True)
        vline.set_xdata([x_hit, x_hit])
        vline.set_visible(True)
        lines_txt = [f"x = {x_hit:.4g}"]

        for label, yv in zip(labels, y_vals):
            lines_txt.append(f"{label}: {yv:.4g}")
        annot.xy = (x_hit, max(y_vals))
        annot.set_text("\n".join(lines_txt))
        annot.set_visible(True)
        fig.canvas.draw_idle()

    def _hide():
        for pt in highlight_pts:
            pt.set_visible(False)
        vline.set_visible(False)
        annot.set_visible(False)

    fig.canvas.mpl_connect("motion_notify_event", on_move)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    return fig, ax


def input_data() -> list[int]:
    '''
    Ввод данных пользователем.
    Проверка на тип данных и колличество значений.
    '''
    user_input = input('Введите три числа через пробел: ').strip()
    data = user_input.split()

    if len(data) != 3:
        raise ValueError("❌ Ошибка: нужно ввести ровно 3 числа, а вы ввели {len(data)}. Попробуйте снова.\n")

    try:
        numbers = [int(i) for i in data]
    except:
        raise ValueError("❌ Ошибка: все введённые значения должны быть числами. Попробуйте снова.\n")
    return numbers
        


if __name__ == "__main__":
    try:
        user_input = input_data()
    except ValueError as er:
        logger.error(er)
        exit(0)
    x = np.linspace(*user_input)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.exp(-x / 5)
    y4 = np.log1p(x)
    my_styles = [
        {"color": "crimson",   "linestyle": "-",  "linewidth": 2.5, "marker": "o", "markersize": 3, "alpha": 0.9},
        {"color": "navy",      "linestyle": "--", "linewidth": 2,   "marker": "s", "markersize": 3, "alpha": 0.9},
        {"color": "darkgreen", "linestyle": "-.", "linewidth": 2,   "marker": "^", "markersize": 3, "alpha": 0.9},
        {"color": "orange",    "linestyle": ":",  "linewidth": 2.5, "marker": "D", "markersize": 3, "alpha": 0.9},
    ]
    plot_four_series_interactive(
        x, y1, y2, y3, y4,
        labels=("sin(x)", "cos(x)", "sin(x)·e^(-x/5)", "ln(1+x)"),
        styles=my_styles,
        title="Наведите мышь — подсветятся общие точки",
        snap_tolerance=0.05
    )
