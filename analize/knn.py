import math
import pandas as pd


class Knn:
    def __init__(self, k: int = 1):
        self.k = k
        self.study_df = pd.DataFrame({
            'x1': [9.2, 6.3, 10.0, 8.5, 3.0, 7.3, 5.3, 4.2, 7.0, 10.3, 4.4, 9.4, 3.4, 9.3, 10.2, 6.3],
            'x2': [8.2, 9.3, 9.0, 7.3, 6.3, 11.0, 10.4, 7.5, 6.1, 6.5, 8.5, 6.3, 7.2, 10.5, 11.3, 7.2],
            'y': [2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 2]
        }, index=[f"S{i}" for i in range(16)])

        self.test_df = pd.DataFrame({
            'x1': [2.6, 5.0, 3.1, 9.1, 7.7, 5.4, 1.4, 7.4, 8.3, 2.8],
            'x2': [9.4, 5.4, 1.3, 7.2, 0.4, 1.2, 5.6, 4.3, 1.9, 6.1],
            'y': [1, 1, 1, 2, 2, 2, 1, 2, 2, 1]
        }, index=[f"T{i}" for i in range(10)])

        self.accuracy = None
        self.confusion_matrix = None

    def calc(self) -> None:
        for tx1, tx2, inx in zip(self.test_df['x1'].values, self.test_df['x2'].values, self.test_df.index):
            self.study_df[f"dist_{inx}"] = [
                math.sqrt(math.pow(sx1 - tx1, 2) + math.pow(sx2 - tx2, 2))
                for sx1, sx2 in self.study_df[['x1', 'x2']].values
            ]
            # self.study_df[f"dist_{inx}"] = [
            #     abs(sx1 - tx1) + abs(sx2 - tx2)
            #     for sx1, sx2 in self.study_df[['x1', 'x2']].values
            # ]

        self.test_df['min_dis'] = [
            self.study_df[f'dist_T{i}'].sort_values().iloc[:self.k].index.to_list()
            for i in range(self.test_df.shape[0])
        ]
        self.test_df['y_pred'] = [
            self.study_df.loc[loc]['y'].value_counts().index[0]
            for loc in self.test_df['min_dis'].values
        ]
        self.test_df['is_eq'] = self.test_df['y'] == self.test_df['y_pred']
        self.accuracy = self.test_df[self.test_df.is_eq].shape[0] / self.test_df.shape[0] * 100

        self.confusion_matrix = pd.DataFrame({
            i: [
                self.test_df[(self.test_df.y == i) & (self.test_df.y_pred == j)].shape[0]
                for j in self.test_df['y'].unique()
            ] for i in self.test_df['y_pred'].unique()
        }, index=[i for i in self.test_df['y'].unique()])


if __name__ == '__main__':
    k = Knn(1)
    k.calc()
    print(k.study_df)
    print(k.test_df)
    print(k.confusion_matrix)
