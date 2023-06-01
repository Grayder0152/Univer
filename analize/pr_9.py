from abc import abstractmethod, ABC
from math import sqrt
from typing import Optional

import pandas as pd


class RankCorrelation(ABC):
    a = 0.05
    t_st = 2.10  # n = 20
    u_st = 1.96

    def __init__(self, x: list, y: list):
        self.x_df = pd.DataFrame({
            'x': x
        })
        self.y_df = pd.DataFrame({
            'y': y
        })
        self.x_df = self.x_df.sort_values(by=['x'])
        self.y_df = self.y_df.sort_values(by=['y'])
        self.x_df['rx'] = self.get_rank(self.x_df['x'].to_list())
        self.y_df['ry'] = self.get_rank(self.y_df['y'].to_list())

        self.df = self.x_df.join(self.y_df).sort_index()
        self.df = self.df.sort_values(['rx'], ignore_index=True)
        self.n = len(x)

        self.coeff = None

    @staticmethod
    def get_rank(sorted_el: list) -> list:
        rang = []
        for el in sorted_el:
            el_count = sorted_el.count(el)
            el_index = sorted_el.index(el) + 1
            rang.append(sum(range(el_index, el_index + el_count)) / el_count if el_count > 1 else el_index)
        return rang

    @staticmethod
    def get_a_b(rang: list) -> float:
        refs = [r for r in rang if rang.count(r) > 1]

        return sum(
            (refs.count(j) ** 3 - refs.count(j)) for j in set(refs)
        ) / 12

    def calc(self):
        if self.df['rx'].dtypes == 'float64' or self.df['ry'].dtypes == 'float64':
            print("Є зв'язні ранги!")
            self.calc_with_viscous()
        else:
            print("Зв'язних рангів немає!")
            self.calc_without_viscous()

    @abstractmethod
    def calc_with_viscous(self):
        pass

    @abstractmethod
    def calc_without_viscous(self):
        pass


class SpearmanRankCorrelation(RankCorrelation):
    def __init__(self, x: list, y: list):
        super().__init__(x, y)
        self.A = 0
        self.B = 0
        self.t = None

    def calc_with_viscous(self):
        n = self.n
        rx_list = self.df['rx'].to_list()
        ry_list = self.df['ry'].to_list()

        if self.df['rx'].dtypes == 'float64':
            self.A = self.get_a_b(rx_list)
        if self.df['ry'].dtypes == 'float64':
            self.B = self.get_a_b(ry_list)

        self.coeff = (
                (
                        (n / 6) * (n ** 2 - 1) -
                        sum((rx - ry) ** 2 for rx, ry in zip(rx_list, ry_list)) -
                        self.A - self.B
                ) /
                sqrt(
                    ((n / 6) * (n ** 2 - 1) - 2 * self.A) *
                    ((n / 6) * (n ** 2 - 1) - 2 * self.B)
                )
        )
        self.t = self.get_t(self.coeff)

    def calc_without_viscous(self):
        n = self.n
        self.coeff = (
                1 - (6 / (n * (n ** 2 - 1))) *
                sum(
                    (rx - ry) ** 2 for rx, ry in zip(
                        self.df['rx'].to_list(), self.df['ry'].to_list()
                    )
                )
        )
        self.t = self.get_t(self.coeff)

    def get_t(self, coeff: float):
        n = self.n
        return (coeff * sqrt(n - 2)) / sqrt(1 - coeff ** 2)

    def __str__(self):
        if self.t_st >= abs(self.t):
            return "Між показниками ВІДСУТНЯ монотонна залежність!(за Спірмена)"
        return "Між показниками ІСНУЄ монотонна залежність!(за Спірмена)"

    def show_result(self) -> str:
        result = f"""Коефіцієнт Спірмена(r) = {self.coeff}\nСтатистика(t) = {self.t}"""
        return result


class KendallRankCorrelation(RankCorrelation):
    def __init__(self, x: list, y: list):
        super().__init__(x, y)
        self.C = 0
        self.D = 0

        self.v = None
        self.S = None
        self.u = None

    @staticmethod
    def get_c_d(rang: list) -> float:
        refs = [r for r in rang if rang.count(r) > 1]

        return sum(
            refs.count(j) * (refs.count(j) - 1) for j in set(refs)
        ) / 2

    def calc_with_viscous(self):
        n = self.n
        rx_list = self.df['rx'].to_list()
        ry_list = self.df['ry'].to_list()
        self.v = self.get_v(ry_list, rx_list)
        self.S = sum(self.v)
        if self.df['rx'].dtypes == 'float64':
            self.C = self.get_c_d(rx_list)
        if self.df['ry'].dtypes == 'float64':
            self.D = self.get_c_d(ry_list)

        self.coeff = self.S / sqrt(
            ((n / 2) * (n - 1) - self.C) * ((n / 2) * (n - 1) - self.D)
        )
        self.u = self.get_u(self.coeff)

    def calc_without_viscous(self):
        ry_list = self.df['ry'].to_list()
        self.v = self.get_v(ry_list)
        self.S = sum(self.v)
        self.coeff = (2 * self.S) / (self.n * (self.n - 1))
        self.u = self.get_u(self.coeff)

    def get_u(self, coeff: float):
        n = self.n
        return (3 * coeff * sqrt(n * (n - 1))) / sqrt(2 * (2 * n + 5))

    @staticmethod
    def get_v(ry: list, rx: Optional[list] = None) -> list:
        v = []
        for i in range(len(ry)):
            for j in range(i + 1, len(ry)):
                if rx is None:
                    vi = 1 if ry[i] < ry[j] else -1
                else:
                    if rx[i] == rx[j] or ry[i] == ry[j]:
                        vi = 0
                    else:
                        vi = 1 if ry[i] < ry[j] else -1
                v.append(vi)
        return v

    def __str__(self):
        if self.u_st >= abs(self.u):
            return "Між показниками ВІДСУТНЯ монотонна залежність!(за Кенделла)"
        return "Між показниками ІСНУЄ монотонна залежність!(за Кенделла)"

    def show_result(self) -> str:
        result = f"""Коефіцієнт Кенделла(r) = {self.coeff}\nСтатистика(u) = {self.u}"""
        return result


if __name__ == '__main__':
    from data import X, Y

    print("За Спірмена")
    s = SpearmanRankCorrelation(X, Y)
    s.calc()
    print(s.show_result())
    print(s)

    print()
    print("За Кендела")
    k = KendallRankCorrelation(X, Y)
    k.calc()
    print(k.show_result())
    print(k)
