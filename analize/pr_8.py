import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class AnalysisCorrelation:
    """Аналіз кореляційного поля. Оцінення коєф. кореляції Пірсона"""

    # t_st = 2.10  # n = 20
    t_st = 2.16  # n = 15

    u = 1.96

    def __init__(self, x: list, y: list):
        self.N = len(x)
        self.x_mean = self.mean(x)
        self.y_mean = self.mean(y)
        self.xy_mean = sum(x_i * y_i for x_i, y_i in zip(x, y)) / self.N
        self.S_x = (sum((x_i - self.x_mean) ** 2 for x_i in x) / self.N) ** (1 / 2)
        self.S_y = (sum((y_i - self.y_mean) ** 2 for y_i in y) / self.N) ** (1 / 2)

        self.r = (self.xy_mean - self.x_mean * self.y_mean) / (self.S_x * self.S_y)
        self.t = (self.r * (self.N - 2) ** (1 / 2)) / ((1 - self.r ** 2) ** (1 / 2))
        self.interval = self.get_interval()

    def get_interval(self) -> tuple:
        k = self.u * (1 - self.r ** 2) / ((self.N - 1) ** (1 / 2))
        r = self.r + (self.r * (1 - self.r ** 2)) / (2 * self.N)
        return r - k, r + k

    def __str__(self):
        if abs(self.t) <= self.t_st:
            return "Лінійний зв'язок між показниками відсутній."
        return "Між показниками існує ліінйний зв'язок."

    @staticmethod
    def mean(seq: list) -> float:
        return sum(seq) / len(seq)

    def show_result(self) -> str:
        result = f"""
        Коефіцієнт Пірсона(r) = {self.r}
        Статистика(t) = {self.t}
        Інтервальна оцінка = {self.get_interval()}
        """
        return result


if __name__ == '__main__':
    from data import X, Y

    ac = AnalysisCorrelation(X, Y)
    print(ac.show_result())
    df = pd.DataFrame({
        'x': X,
        'y': Y
    })
    sns.scatterplot(x="x", y="y", data=df)
    plt.show()
