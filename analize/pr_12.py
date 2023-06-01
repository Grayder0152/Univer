import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from pr_10 import EstimationLinearRegressionParameters


class VerSignificanceAdequacyReg:
    """VERIFICATION OF SIGNIFICANCE AND ADEQUACY OF REGRESSION"""

    def __init__(self, x: list, y: list):
        self.df = pd.DataFrame({
            'x': x,
            'y': y
        })
        self.f = 4.41
        self.reg = EstimationLinearRegressionParameters(x, y)

        self.F = sum((y_mean_x - self.reg.corr.y_mean) ** 2 for y_mean_x in self.reg.df['f(x)']) / self.reg.S2_e
        self.R_2 = self.reg.corr.r ** 2 * 100

    def __str__(self):
        return f"Регресія {'значуща' if self.F > self.f else 'незначуща'}. Адекватність: {self.R_2}%."


if __name__ == '__main__':
    from data import X, Y

    con = VerSignificanceAdequacyReg(X, Y)
    plt.plot(con.reg.df['f(x)'], con.reg.df['e'], '.')
    plt.plot(con.reg.df['f(x)'], [0 for _ in range(20)])
    plt.show()

    print(con)
