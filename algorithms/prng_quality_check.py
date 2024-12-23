import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import chisquare
from statsmodels.tsa.stattools import acf


class PRNGQualityChecker:
    def __init__(self, generator_function, num_samples=10000):
        self.generator_function = generator_function
        self.num_samples = num_samples
        self.samples = None

    def generate_samples(self):
        self.samples = np.array([self.generator_function() for _ in range(self.num_samples)])

    def frequency_test(self):
        if self.samples is None:
            raise ValueError("Samples have not been generated yet.")

        counts = np.bincount(self.samples)
        chi2, p = chisquare(counts)
        return {
            "chi2": chi2,
            "p_value": p,
            "uniform": p > 0.05
        }

    def autocorrelation_test(self, lags=20):
        if self.samples is None:
            raise ValueError("Samples have not been generated yet.")

        autocorr = acf(self.samples, nlags=lags, fft=True)
        return autocorr

    def visualize_samples(self):
        if self.samples is None:
            raise ValueError("Samples have not been generated yet.")

        plt.figure(figsize=(10, 5))
        plt.plot(self.samples[:100], marker='o', linestyle='-', label="Random Numbers")
        plt.title("Visualization of Random Numbers")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.legend()
        plt.grid()
        plt.show()

    def scatter_plot(self):
        if self.samples is None:
            raise ValueError("Samples have not been generated yet.")

        x = self.samples[:self.num_samples // 2]
        y = self.samples[self.num_samples // 2:self.num_samples]

        plt.figure(figsize=(6, 6))
        plt.scatter(x, y, alpha=0.6)
        plt.title("Scatter Plot of Random Numbers")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid()
        plt.show()


if __name__ == "__main__":
    rng = lambda: np.random.randint(0, 2)
    checker = PRNGQualityChecker(rng, num_samples=10000)
    checker.generate_samples()

    frequency_results = checker.frequency_test()
    print("Frequency Test Results:", frequency_results)

    autocorr_results = checker.autocorrelation_test(lags=20)
    print("Autocorrelation Test Results:", autocorr_results)

    checker.visualize_samples()
    checker.scatter_plot()
