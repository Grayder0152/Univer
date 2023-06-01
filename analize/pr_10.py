import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from pr_8 import AnalysisCorrelation


class EstimationLinearRegressionParameters:
    """ESTIMATION OF LINEAR REGRESSION PARAMETERS."""

    def __init__(self, x: list, y: list) -> None:
        self.df = pd.DataFrame({
            'x': x,
            'y': y
        })
        self.corr = AnalysisCorrelation(x, y)
        self.b = self.corr.r * (self.corr.S_y / self.corr.S_x)
        self.a = self.corr.y_mean - self.b * self.corr.x_mean

        self.df['f(x)'] = self.a + self.b * self.df['x']
        self.df['e'] = self.df['y'] - self.df['f(x)']
        self.df['e^2'] = self.df['e'] ** 2

        self.S2_e = (sum(self.df['e^2']) / (self.corr.N - 2))

        self.q_a = ((self.S2_e * (1 + self.corr.x_mean ** 2 / self.corr.S_x ** 2)) / (self.corr.N)) ** (1 / 2)
        self.q_b = (self.S2_e / (self.corr.N * self.corr.S_x ** 2)) ** (1 / 2)

        self.a_interval = self.a - self.corr.t_st * self.q_a, self.a + self.corr.t_st * self.q_a
        self.b_interval = self.b - self.corr.t_st * self.q_b, self.b + self.corr.t_st * self.q_b

        self.t_a = self.a / self.q_a
        self.t_b = self.b / self.q_b

    def __str__(self):
        return (
            f"Параметр `a` - {'незначущий' if abs(self.t_a) <= self.corr.t_st else 'значущий'}\n"
            f"Параметр `b` - {'незначущий' if abs(self.t_b) <= self.corr.t_st else 'значущий'}"
        )


if __name__ == '__main__':
    from data import X, Y

    est = EstimationLinearRegressionParameters(X, Y)
    print(est)

    sns.regplot(x="x", y="y", data=est.df)
    plt.show()
