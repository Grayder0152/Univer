"""Побудова варіаційного ряду і гістограми"""

import math
from typing import Sequence

import matplotlib.pyplot as plt
import pandas as pd

from data import DATA_1_3


class VariationalSeriesAndGist:
    """Побудова варіаційного ряду і густограми."""

    def __init__(self, data: Sequence[float | int]):
        self.data = sorted(data)
        self.unique_data = set(self.data)
        self.N = len(data)  # count of data
        self.max_value = max(self.unique_data)
        self.min_value = min(self.unique_data)

    def get_count_of_class(self) -> int:
        m = round(math.pow(self.N, 1 / 2 if self.N < 100 else 1 / 3))
        if m % 2 == 0:
            m -= 1
        return m

    def get_weight_of_class(self) -> float:
        return (self.max_value - self.min_value) / self.get_count_of_class()

    def get_classes(self, weight: float) -> list[tuple[float, float]]:
        i = 0
        d = []
        x = self.min_value
        while x < self.max_value:
            x = self.min_value + weight * i
            i += 1
            d.append(round(x, 2))

        return [(d[i], d[i + 1]) for i in range(len(d) - 1)]

    def get_variational_series_with_class(self) -> pd.DataFrame:
        h = self.get_weight_of_class()
        classes = self.get_classes(h)

        n = [len(list((filter(lambda x: cl[1] > x > cl[0], self.data)))) for cl in classes]
        # 'Класс': [str(classes[i]).replace('(', '[').replace(')', ']', 0 if i != len(classes) - 1 else 1) for i in range(len(classes))],
        return pd.DataFrame({
            'Класс': [f"{cl[0]}-{cl[1]}" for cl in classes],
            'Частота n': n,
            'Віндосна частота p': [i / self.N for i in n]
        })

    def get_variational_series(self):
        return pd.DataFrame({
            'Варіанта x': list(self.unique_data),
            'Частота n': [self.data.count(i) for i in self.unique_data],
            'Віндосна частота p': [self.data.count(i) / self.N for i in self.unique_data]
        })

    def show_hist(self) -> pd.DataFrame:
        variational_series_with_class = self.get_variational_series_with_class()
        variational_series_with_class.plot.bar(x='Класс', y='Віндосна частота p', rot=0, width=1)
        plt.show()
        return variational_series_with_class


if __name__ == '__main__':
    v = VariationalSeriesAndGist(DATA_1_3)
    df = v.get_variational_series()
    print(df)

    df_cl = v.show_hist()
    print("Ідентифіковано нормальний розподіл.")
