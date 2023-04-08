import math
from abc import ABC

import pandas as pd


class RankSumCriteria(ABC):
    def __init__(self, data_x: list[float], data_y: list[float], u_a: float = 1.96):
        self.u_a: float = u_a
        self.N_x: int = len(data_x)
        self.N_y: int = len(data_y)
        self.E: float | None = None
        self.D: float | None = None
        self.u: float | None = None

    def calculation(self):
        pass

    def get_result(self) -> str:
        if abs(self.u) <= self.u_a:
            return "Зсуву у функціях розподілу немає!"
        return "Функції розподілу зсунені одна відносно іншої!"


class WilcoxonRankSumCriteria(RankSumCriteria):
    """Критерії суми рангів Вілкоксона."""

    def __init__(self, data_x: list[float], data_y: list[float], u_a: float = 1.96):
        super().__init__(data_x, data_y, u_a)

        self.df = pd.DataFrame({
            'x,y': data_x + data_y
        })
        self.df['data'] = list('x' * self.N_x + 'y' * self.N_y)
        self.W: float | None = None
        self.calculation()

    def calculation(self):
        self.df['sorted'] = self.df['x,y'].sort_values().values
        self.df['index'] = self.df['sorted'].index + 1

        sorted_el = self.df['sorted'].to_list()
        rang = []
        for el in self.df['x,y']:
            el_count = sorted_el.count(el)
            el_index = sorted_el.index(el) + 1
            rang.append(sum(range(el_index, el_index + el_count)) / el_count if el_count > 1 else el_index)

        self.df['r'] = rang

        self.W = self.df[self.df['data'] == 'x']['r'].sum()
        self.E = (self.N_x * (self.N_x + self.N_y + 1)) / 2
        self.D = (self.N_x * self.N_y * (self.N_x + self.N_y + 1)) / 12
        self.u = (self.W - self.E) / (math.pow(self.D, 1 / 2))

    def __str__(self):
        return f"""Критерії суми рангів Вілкоксона: W={self.W}, E={self.E}, D={self.D}, u={self.u}"""


class MannaRankSumCriteria(RankSumCriteria):
    """Критерії суми рангів Манна."""

    def __init__(self, data_x: list[float], data_y: list[float], u_a: float = 1.96):
        super().__init__(data_x, data_y, u_a)

        self.data_x = data_x
        self.data_y = data_y

        self.V: float | None = None
        self.calculation()

    def calculation(self):
        v_i = []
        for el_x in self.data_x:
            v = 0
            for el_y in self.data_y:
                if el_x > el_y:
                    v += 1
                elif el_x < el_y:
                    v += 0
                else:
                    v += 0.5
            v_i.append(v)

        self.V = sum(v_i)
        self.E = (self.N_x * self.N_y) / 2
        self.D = (self.N_x * self.N_y * (self.N_x + self.N_y + 1)) / 12
        self.u = (self.V - self.E) / math.pow(self.D, 1 / 2)

    def __str__(self):
        return f"""Критерії суми рангів Манна: V={self.V}, E={self.E}, D={self.D}, u={self.u}"""


if __name__ == '__main__':
    from data import DATA_INDEP_4_7_1, DATA_INDEP_4_7_2

    # x = [102.9, 142.0, 353.1, 253.3, 169.9, 234.4, 277.9, 175.8]
    # y = [424.9, 353.1, 310.2, 422.0, 454.2, 390.6, 372.4]

    w = WilcoxonRankSumCriteria(DATA_INDEP_4_7_1, DATA_INDEP_4_7_2)
    m = MannaRankSumCriteria(DATA_INDEP_4_7_1, DATA_INDEP_4_7_2)
    print(w)
    print(w.get_result())
    print('-'*100)
    print(m)
    print(m.get_result())
