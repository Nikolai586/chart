from sys import exit
import matplotlib.pyplot as plt
import numpy as np


def plot_four_series(
    x,
    y1, y2, y3, y4,
    labels=("Ряд 1", "Ряд 2", "Ряд 3", "Ряд 4"),
    styles=None,
    title="График с 4 последовательностями",
    xlabel="X",
    ylabel="Y",
    figsize=(10, 6),
    grid=True
):
    """
    Строит график с 4 последовательностями данных и настраиваемыми стилями.

    Параметры
    ---------
    x : последовательность
        Общая ось X.
    y1..y4 : последовательности
        Четыре ряда данных.
    labels : tuple[str, str, str, str]
        Подписи для легенды.
        Если None — используются стили по умолчанию.
    """

    default_styles = [
        {"color": "tab:blue",   "linestyle": "-",  "linewidth": 2, "marker": "o", "markersize": 4},
        {"color": "tab:orange", "linestyle": "--", "linewidth": 2, "marker": "s", "markersize": 4},
        {"color": "tab:green",  "linestyle": "-.", "linewidth": 2, "marker": "^", "markersize": 4},
        {"color": "tab:red",    "linestyle": ":",  "linewidth": 2, "marker": "D", "markersize": 4},
    ]

    if styles is None:
        styles = default_styles
    else:
        styles = [{**default_styles[i], **(styles[i] if i < len(styles) else {})}
                  for i in range(4)]
    fig, ax = plt.subplots(figsize=figsize)
    series = [y1, y2, y3, y4]

    for y, label, style in zip(series, labels, styles):
        ax.plot(x, y, label=label, **style)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if grid:
        ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="best", frameon=True)
    fig.tight_layout()
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
        print(f"❌ Ошибка: нужно ввести ровно 3 числа, а вы ввели {len(data)}. Попробуйте снова.\n")
        exit(0)

    try:
        numbers = [int(i) for i in data]
    except ValueError:
        print("❌ Ошибка: все введённые значения должны быть числами. Попробуйте снова.\n")
        exit(0)
    return numbers
        


if __name__ == "__main__":
    user_input = input_data()
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
    plot_four_series(
        x, y1, y2, y3, y4,
        labels=("sin(x)", "cos(x)", "sin(x)·e^(-x/5)", "ln(1+x)"),
        styles=my_styles,
        title="Четыре последовательности данных",
        xlabel="x",
        ylabel="y",
        grid=True,
    )
