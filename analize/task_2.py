import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as sps
from scipy.stats import kstest
from data import DATA_1_3
from pr_1 import VariationalSeriesAndGist
from pr_2 import EvaluationStatisticalCharacteristics


def identify_relay(data):
    df = VariationalSeriesAndGist(data).get_variational_series()
    df['F(x)'] = [sum(df['Віндосна частота p'][:i + 1]) for i in range(len(df['Віндосна частота p']))]
    df = df[df['F(x)'] < 1.0]

    df['t'] = df['Варіанта x']
    df['z'] = np.sqrt([2 * np.log(1 / (1 - df['F(x)']))])[0]
    df.plot.scatter(x='t', y='z')
    plt.show()


def parametric_recovery_distribution(data):
    """Параметричне відновлення розподілу."""

    ev = EvaluationStatisticalCharacteristics(data)
    m, q = ev.average, ev.S
    df = pd.DataFrame({'x': sorted(list(set(ev.data)))})

    df['f(x)'] = 1 / (q * math.pow(2 / math.pi, 1 / 2)) * np.exp(-((df['x'] - m) ** 2 / (2 * q * q)))
    df['u'] = (df['x'] - m) / q

    def fi(u):
        p = 0.2316419
        t = 1 / (1 + p * u)
        b1 = 0.31938153
        b2 = -0.356563782
        b3 = 1.781477937
        b4 = -1.821255978
        b5 = 1.330274429

        return 1 - 1 / math.pow(2 * math.pi, 1 / 2) * np.exp(-(u ** 2) / 2) * (
                b1 * t + b2 * t ** 2 + b3 * t ** 3 + b4 * t ** 4 + b5 * t ** 5)

    df['F(x)'] = np.where(df['u'] >= 0, fi(df['u']), 1 - fi(abs(df['u'])))

    plt.plot(df['x'], df['f(x)'], label='f(x)')
    plt.show()
    plt.plot(df['x'], df['F(x)'], label='F(x)')
    plt.show()
    return df


def a(data):
    df = parametric_recovery_distribution(data)
    print(1)


if __name__ == '__main__':
    # from scipy.stats import norm

    a(DATA_1_3)
