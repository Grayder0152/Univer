import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from pr_10 import EstimationLinearRegressionParameters


class ConfidenceEstRegAndPredictionValue:
    """CONFIDENCE ESTIMATION OF REGRESSION AND PREDICTIVE VALUES"""

    def __init__(self, x: list, y: list):
        self.df = pd.DataFrame({
            'x': x,
            'y': y
        })
        self.reg = EstimationLinearRegressionParameters(x, y)
        self.df['q{y_mean(x)}'] = (self.reg.S2_e / self.reg.corr.N + (self.reg.q_b * (self.df['x'] - self.reg.corr.x_mean)) ** 2) ** (1 / 2)
        self.df['y_mean_min'] = self.reg.df['f(x)'] - self.reg.corr.t_st * self.df['q{y_mean(x)}']
        self.df['y_mean_max'] = self.reg.df['f(x)'] + self.reg.corr.t_st * self.df['q{y_mean(x)}']

        self.df['q{y(x)}'] = (self.df['q{y_mean(x)}'] ** 2 + self.reg.S2_e) ** (1 / 2)
        self.df['y_min'] = self.reg.df['f(x)'] - self.reg.corr.t_st * self.df['q{y(x)}']
        self.df['y_max'] = self.reg.df['f(x)'] + self.reg.corr.t_st * self.df['q{y(x)}']


if __name__ == '__main__':
    from data import X, Y

    con = ConfidenceEstRegAndPredictionValue(X, Y)

    sns.regplot(x="x", y="y", data=con.df, label='reg')
    plt.plot(con.df['x'], con.df['y_max'], '.', label='y_max')
    plt.plot(con.df['x'], con.df['y_min'], '.', label='y_min')
    plt.plot(con.df['x'], con.df['y_mean_max'], '.', label='y_mean_max')
    plt.plot(con.df['x'], con.df['y_mean_min'], '.', label='y_mean_min')

    plt.legend()
    plt.show()
