import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


class AnalysisCorrelation:
    """Аналіз кореляційного поля. Оцінення коєф. кореляції Пірсона"""

    t_st = 2.10  # n = 20
    u = 1.96

    def __init__(self, x: tuple, y: tuple):
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
    def mean(seq: tuple) -> float:
        return sum(seq) / len(seq)


if __name__ == '__main__':
    X = (
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
        12, 13, 14, 15, 16, 17, 18, 19, 20
    )
    Y = (
        93.1, 92, 87.3, 91.4, 81.8, 76.1, 74.5, 77.4, 74.4, 64.7,
        61.4, 60.9, 70.5, 63.3, 57.1, 47.2, 45.4, 44.5, 43.8, 43.7
    )
    ac = AnalysisCorrelation(X, Y)
    print(ac)
    df = pd.DataFrame({
        'x': X,
        'y': Y
    })
    sns.scatterplot(x="x", y="y", data=df)
    plt.show()
    # print(stats.pearsonr(X, Y).statistic, stats.pearsonr(X, Y).pvalue)
