import math

import pandas as pd


class WilcoxonSignRankCriteria:
    """Застосування критерії знакових рангів Вікоксона до двох залежних вибірок."""

    def __init__(self, data_x: list[float], data_y: list[float], u_a: float = 1.96):
        self.df = pd.DataFrame({
            'x': data_x,
            'y': data_y
        })
        self.u_a: float = u_a
        self.N: int | None = None
        self.T: float | None = None
        self.E_T: float | None = None
        self.D_T: float | None = None
        self.u: float | None = None

        self.calculation()

    def calculation(self):
        self.df['z'] = self.df['x'] - self.df['y']
        self.df = self.df[self.df['z'] != 0]
        self.df['s'] = self.df['z'] > 0
        self.N = len(self.df['s'])
        self.df['|z|'] = abs(self.df['z'])
        self.df = self.df.sort_values(by=['|z|'], ignore_index=True)

        sorted_el = self.df['|z|'].to_list()
        rang = []
        for el in self.df['|z|']:
            el_count = sorted_el.count(el)
            el_index = sorted_el.index(el) + 1
            rang.append(sum(range(el_index, el_index + el_count)) / el_count if el_count > 1 else el_index)
        self.df['r'] = rang

        self.df['s*r'] = self.df['s'] * self.df['r']

        self.N = len(self.df['z'])
        self.T = self.df['s*r'].sum()
        self.E_T = (self.N * (self.N + 1)) / 4
        self.D_T = (self.N * (self.N + 1) * (2 * self.N + 1)) / 24

        self.u = (self.T - self.E_T) / math.pow(self.D_T, 1 / 2)

    def get_result(self) -> str:
        if abs(self.u) <= self.u_a:
            return "Зсуву у функціях розподілу немає!"
        return "Функції розподілу зсунені одна відносно іншої!"

    def __str__(self):
        return f"""Застосування критерії знакових рангів Вікоксона: T={self.T}, E={self.E_T}, D={self.D_T}, u={self.u}"""


if __name__ == '__main__':
    from data import DATA_DEP_4_7_1, DATA_DEP_4_7_2

    w = WilcoxonSignRankCriteria(DATA_DEP_4_7_1, DATA_DEP_4_7_2)
    print(w)
    print(w.get_result())
