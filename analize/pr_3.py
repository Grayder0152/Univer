from data import DATA_1_3
from pr_1 import VariationalSeriesAndGist

import matplotlib.pyplot as plt
import scipy.stats


class IdentificationNormalDistribution:
    """Ідентифікація нормального росподілу."""

    def __init__(self, data: list[float]):
        var_series = VariationalSeriesAndGist(data)
        self.df = var_series.get_variational_series()
        self.identification_based_on_probability_paper()

    def identification_based_on_probability_paper(self):
        self.df = self.df.sort_values(by=['Варіанта x'], ignore_index=True)
        self.df['Fn(x)'] = [sum(self.df['Віндосна частота p'][:i + 1]) for i in
                            range(len(self.df['Віндосна частота p']))]
        r = []
        for x, f in self.df[['Варіанта x', 'Fn(x)']].values:
            if f == 1:
                r.append(None)
            else:
                r.append(x)
        self.df['x'] = r
        self.df = self.df.dropna()
        self.df['u'] = scipy.stats.norm.ppf(self.df['Fn(x)']).round(2)

    def show_qq(self):
        self.df.plot.scatter(x='x', y='u')
        plt.show()


if __name__ == '__main__':
    iden = IdentificationNormalDistribution(DATA_1_3)
    iden.show_qq()
