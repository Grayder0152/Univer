import math
from abc import ABC, abstractmethod
from statistics import mean


class EqualityMeansAndVarianceTwoSamples(ABC):
    def __init__(self, data_x: list[float], data_y: list[float], t_a: float = 2.0, f_a: float = 1.53):
        self.data_x: list[float] = data_x
        self.data_y: list[float] = data_y

        self.t_a: float = t_a  # квантиль розподілу Стьюдента
        self.f_a: float = f_a  # квантиль розподілу Фішера

        self.x_average: float | None = None
        self.y_average: float | None = None

        self.S2__x: float | None = None
        self.S2__y: float | None = None

        self.t: float | None = None
        self.f: float | None = None

        self.calculation()

    @abstractmethod
    def calculate_t(self) -> float:
        pass

    @abstractmethod
    def calculate_f(self) -> float:
        pass

    def calculation(self):
        self.x_average = mean(self.data_x)
        self.y_average = mean(self.data_y)

        self.S2__x = self.get_variance(self.data_x, self.x_average)
        self.S2__y = self.get_variance(self.data_y, self.y_average)

        self.t = self.calculate_t()
        self.f = self.calculate_f()

    @staticmethod
    def sum_div(data: list[float], average: float, degree: int) -> float:
        return sum(math.pow(i - average, degree) for i in data)

    def get_variance(self, data: list[float], average: float, degree: int = 2, shifted: bool = True) -> float:
        return self.sum_div(data, average, degree) / (len(data) - (0 if shifted else 1))

    def get_result(self) -> str:
        result = ""
        if abs(self.t) <= self.t_a:
            result += "Гіпотеза про рівність середніх значень сукупностей справджена!\n"
        else:
            result += "Середні значення істотно відрізняються\n"

        if self.f <= self.f_a:
            result += "Дисперсії генеральних сукупностей збігаються!\n"
        else:
            result += "Дисперсії генеральних сукупностей відмінні!\n"

        return result


class DependentEqualityMeansAndVarianceTwoSamples(EqualityMeansAndVarianceTwoSamples):
    """Перевірка рівностей середніх та дисперсії у випадку двох ЗАЛЕЖНИХ вибірок."""

    def __init__(self, data_x: list[float], data_y: list[float], t_a: float = 2.0, f_a: float = 1.53):
        self.data_z: list[float] = [x - y for x, y in zip(data_x, data_y)]

        self.N: int = len(self.data_z)
        self.z_average: float | None = None
        self.S__z: float | None = None

        super().__init__(data_x, data_y, t_a, f_a)

    def calculation(self):
        self.z_average = mean(self.data_z)
        self.S__z = math.pow(
            self.get_variance(self.data_z, self.z_average),
            1 / 2
        )
        super().calculation()

    def calculate_t(self) -> float:
        return (self.z_average * math.pow(self.N, 1 / 2)) / self.S__z

    def calculate_f(self) -> float:
        return self.S2__x / self.S2__y if self.S2__x >= self.S2__y else self.S2__y / self.S2__x

    def __str__(self):
        return f"""Перевірка рівностей середніх та дисперсії у випадку двох ЗАЛЕЖНИХ вибірок: t={self.t}, f={self.f}"""


class IndependentEqualityMeansAndVarianceTwoSamples(EqualityMeansAndVarianceTwoSamples):
    """Перевірка рівностей середніх та дисперсії у випадку двох НЕЗАЛЕЖНИХ вибірок."""

    def __init__(self, data_x: list[float], data_y: list[float], t_a: float = 2.0, f_a: float = 1.53):
        self.N_x: int = len(data_x)
        self.N_y: int = len(data_y)

        super().__init__(data_x, data_y, t_a, f_a)

    def calculate_t(self) -> float:
        s = ((self.N_x - 1) * self.S2__x + (self.N_y - 1) * self.S2__y) / self.N_x + self.N_y - 2
        return (self.x_average - self.y_average) / math.pow((s / self.N_x) + (s / self.N_y), 1 / 2)

    def calculate_f(self) -> float:
        return self.S2__x / self.S2__y if self.S2__x >= self.S2__y else self.S2__y / self.S2__x

    def __str__(self):
        return f"""Перевірка рівностей середніх та дисперсії у випадку двох НЕЗАЛЕЖНИХ вибірок: t={self.t}, f={self.f}"""


if __name__ == '__main__':
    from data import (
        DATA_DEP_4_7_1, DATA_DEP_4_7_2,
        DATA_INDEP_4_7_1, DATA_INDEP_4_7_2
    )

    d = DependentEqualityMeansAndVarianceTwoSamples(DATA_DEP_4_7_1, DATA_DEP_4_7_2)
    print(d)
    print(d.get_result())
    print('-' * 100)
    i = IndependentEqualityMeansAndVarianceTwoSamples(DATA_INDEP_4_7_1, DATA_INDEP_4_7_2)
    print(i)
    print(i.get_result())