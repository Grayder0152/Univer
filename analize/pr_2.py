import math
from statistics import mean, median

import pandas
import pandas as pd


class EvaluationStatisticalCharacteristics:
    """Оцінювання статистичних характеристик."""

    def __init__(self, data):
        self.data = sorted(data)
        self.N = len(data)
        self.a = 0.05
        self.t = 2.0  # N = 60
        self.u = 1.96

        self.med: float | None = None  # медіана
        self.average: float | None = None  # середнє арифметичне
        self.S: float | None = None  # середньоквадратичне відхилення зсунене
        self.S_: float | None = None  # середньоквадратичне відхилення незсунене
        self.W: float | None = None  # коефіцієнт варіації Пірсона
        self.A: float | None = None  # коефіцієнт асиметрії зсунений
        self.A_: float | None = None  # коефіцієнт асиметрії незсунений
        self.E: float | None = None  # коефіцієнт ексцесу зсунений
        self.E_: float | None = None  # коефіцієнт ексцесу незсунений
        self.X: float | None = None  # коефіцієнт контрексцесу

        self.q_average: float | None = None  # середньоквадратичке відхилення параметра
        self.q_S_: float | None = None  # середньоквадратичке відхилення параметра
        self.q_W: float | None = None  # середньоквадратичке відхилення параметра
        self.q_A: float | None = None  # середньоквадратичке відхилення параметра
        self.q_A_: float | None = None  # середньоквадратичке відхилення параметра
        self.q_E: float | None = None  # середньоквадратичке відхилення параметра
        self.q_E_: float | None = None  # середньоквадратичке відхилення параметра

        self.med_r: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.average_r: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.S__r: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.W_r: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.A_r: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.A__r: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.E_r: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.E__r: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.normal_value: tuple[float, float] | None = None  # інтервал нормальних значень параметра
        self.results: list[pd.DataFrame] = []

        self.calculation()

    def calculation(self):
        self.average = mean(self.data)
        self.med = median(self.data)

        s2 = self.get_sample_variance(degree=2)
        s2_ = self.get_sample_variance(degree=2, shifted=False)

        self.S = math.pow(s2, 1 / 2)
        self.S_ = math.pow(s2_, 1 / 2)
        self.W = self.S_ / self.average
        self.A = self.sum_div(3) / (self.N * math.pow(self.S, 3))
        self.A_ = (math.pow(self.N * (self.N - 1), 1 / 2) * self.A) / (self.N - 2)
        self.E = self.sum_div(4) / (self.N * math.pow(self.S, 4)) - 3
        self.E_ = ((self.N * self.N - 1) / ((self.N - 2) * (self.N - 3))) * (self.E + 6 / (self.N + 1))
        self.X = 1 / (math.pow(self.E + 3, 1 / 2))

        self._calculation_of_mean_square_deviation_parameters()
        self._calculation_range_of_normal_values()
        self.results.append(self.get_result())

        normal_values = list(filter(lambda x: self.normal_value[1] >= x >= self.normal_value[0], self.data))

        if len(normal_values) != len(self.data) and len(normal_values) > 20:
            self.data = sorted(normal_values)
            self.calculation()

    def _calculation_of_mean_square_deviation_parameters(self):
        """Обчислення середньоквадратичного відхилення параметрів"""

        self.q_average = self.S_ / math.pow(self.N, 1 / 2)
        self.q_S_ = self.S_ / math.pow(2 * self.N, 1 / 2)
        self.q_W = self.W * math.pow((1 + 2 * math.pow(self.W, 2)) / (2 * self.N), 1 / 2)
        self.q_A = math.pow((6 * (self.N - 2)) / ((self.N + 1) * (self.N + 3)), 1 / 2)
        self.q_A_ = math.pow((6 * self.N * (self.N - 1)) / ((self.N - 2) * (self.N + 1) * (self.N + 3)), 1 / 2)

        self.q_E = math.pow(
            (24 * self.N * (self.N - 2) * (self.N - 3)) / (math.pow(self.N + 1, 2) * (self.N + 3) * (self.N + 5)),
            1 / 2
        )
        self.q_E_ = math.pow(
            (24 * self.N * math.pow(self.N - 1, 2)) / ((self.N - 3) * (self.N - 2) * (self.N + 3) * (self.N + 5)),
            1 / 2
        )

    def _calculation_range_of_normal_values(self):
        """Обчислення інтервалу значень. Значення, які не входять в цей інтервал - аномальні."""

        self.med_r = (
            self.data[round(self.N / 2 - self.u * (math.pow(self.N, 1 / 2) / 2)) - 1],
            self.data[round(self.N / 2 + 1 + self.u * (math.pow(self.N, 1 / 2) / 2)) - 1]
        )
        self.average_r = self.get_range_of_normal_values(self.average, self.q_average)
        self.S__r = self.get_range_of_normal_values(self.S_, self.q_S_)
        self.W_r = self.get_range_of_normal_values(self.W, self.q_W)
        self.A_r = self.get_range_of_normal_values(self.A, self.q_A)
        self.A__r = self.get_range_of_normal_values(self.A_, self.q_A_)
        self.E_r = self.get_range_of_normal_values(self.E, self.q_E)
        self.E__r = self.get_range_of_normal_values(self.E_, self.q_E_)
        self.normal_value = (self.average - self.u * self.S_, self.average + self.u * self.S_)

    def get_range_of_normal_values(self, value: float, q: float) -> tuple[float, float]:
        return value - self.t * q, value + self.t * q

    def sum_div(self, degree: int) -> float:
        return sum(math.pow(i - self.average, degree) for i in self.data)

    def get_sample_variance(self, degree: int = 2, shifted: bool = True) -> float:
        return self.sum_div(degree) / (self.N - (0 if shifted else 1))

    def get_result(self) -> pd.DataFrame:
        re = {
            "Оцінка": [self.average, self.med, self.S_, self.W, self.A, self.A_, self.E, self.E_, self.X],
            "Середньоквадратичного відхилення": [self.q_average, None, self.q_S_, self.q_W, self.q_A, self.q_A_,
                                                 self.q_E, self.q_E_, None],
            "Інтервал нижній": [self.average_r[0], self.med_r[0], self.S__r[0], self.W_r[0], self.A_r[0], self.A__r[0],
                                self.E_r[0],
                                self.E__r[0], None],
            "Інтервал верхній": [self.average_r[1], self.med_r[1], self.S__r[1], self.W_r[1], self.A_r[1], self.A__r[1],
                                 self.E_r[1],
                                 self.E__r[1], None],
        }
        df = pandas.DataFrame(re, index=[
            'Середнє арифметичне', 'Медіана', 'Середньоквадратичне відхилення',
            'Коефіцієнт варіації Пірсона', 'Коефіцієнт асиметрії зсунений',
            'Коефіцієнт асиметрії незсунений', 'Коефіцієнт ексцесу зсунений',
            'Коефіцієнт ексцесу незсунений', 'Коефіцієнт контрексцесу'])
        df["Оцінка"] = df["Оцінка"].round(2)
        df["Середньоквадратичного відхилення"] = df["Середньоквадратичного відхилення"].round(2)
        df["Інтервал нижній"] = df["Інтервал нижній"].round(2)
        df["Інтервал верхній"] = df["Інтервал верхній"].round(2)

        return df


if __name__ == '__main__':
    DATA = (
        3.8, 5, 7, 7.1, 7.2, 7.4, 7.6, 7.6, 7.7, 7.9, 8.1, 8.2, 8.2, 8.3,
        8.4, 8.4, 8.5, 8.5, 8.7, 8.7, 8.8, 8.8, 8.8, 8.9, 9.2, 9.5, 10.2
    )
    s = EvaluationStatisticalCharacteristics(DATA)
    r = s.results
    print("Статистичні характеристики вибірки")
    print(r[0].to_string())
    print("Статистичні характеристики вибірки після вилучення аномальніз значень")
    print(r[1].to_string())
