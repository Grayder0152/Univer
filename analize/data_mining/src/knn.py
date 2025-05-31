from collections import Counter
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from sklearn.model_selection import train_test_split

from extranction import extract


class KNNClassifier:
    def __init__(self, k: int = 3, distance: Literal['euclidean', 'manhattan'] = 'euclidean'):
        self.k = k
        self.distance = distance
        self.X_train = None
        self.y_train = None

    def fit(self, x: np.ndarray, y: np.ndarray):
        self.X_train = x
        self.y_train = y

    def _compute_distance(self, x1: np.ndarray, x2: np.ndarray) -> float:
        if self.distance == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif self.distance == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        else:
            raise ValueError(f"Невідома метрика: {self.distance}")

    def _predict_point(self, x: np.ndarray) -> int:
        distances = [self._compute_distance(x, train_x) for train_x in self.X_train]
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = self.y_train[k_indices]
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

    def predict(self, x_arr: np.ndarray) -> np.ndarray:
        return np.array([self._predict_point(x) for x in x_arr])

    def score(self, x_test: np.ndarray, y_test: np.ndarray) -> float:
        y_pred = self.predict(x_test)
        return np.mean(y_pred == y_test)

    @staticmethod
    def visualize(x_test: np.ndarray, y_pred: np.ndarray, title: str = "KNN Classification Result"):
        """
        Побудова графіка результатів класифікації в 2D.
        """
        if x_test.shape[1] != 2:
            raise ValueError("Візуалізація можлива лише для 2D даних.")

        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(x_test[:, 0], x_test[:, 1], c=y_pred, cmap='tab10', edgecolor='k', s=60)
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.title(title)
        plt.legend(*scatter.legend_elements(), title="Класи")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    df = extract('clustered_data_3.csv')

    X = df[["col1", "col2"]].to_numpy()
    y = df["cluster"].to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    results = []
    for k in [3, 5, 7]:
        for metric in ['euclidean', 'manhattan']:
            clf = KNNClassifier(k=k, distance=metric)
            clf.fit(X_train, y_train)
            acc = clf.score(X_test, y_test)
            results.append((k, metric, acc))

    results_df = pl.DataFrame({
        "k": [r[0] for r in results],
        "distance": [r[1] for r in results],
        "accuracy": [r[2] for r in results],
    })

    plot_df = results_df.to_pandas()
    pivot_df = plot_df.pivot(index="k", columns="distance", values="accuracy")

    plt.figure(figsize=(8, 5))
    for metric in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[metric], marker='o', label=metric.capitalize())

    plt.title("Вплив метрики відстані на точність класифікації KNN")
    plt.xlabel("Кількість сусідів (k)")
    plt.ylabel("Accuracy")
    plt.xticks(pivot_df.index)
    plt.ylim(0.0, 1.05)
    plt.grid(True)
    plt.legend(title="Метрика")
    plt.tight_layout()
    plt.show()
