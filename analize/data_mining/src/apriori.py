import pandas as pd
from itertools import combinations
from collections import defaultdict


class Apriori:
    def __init__(self, min_support: float = 0.2, min_confidence: float = 0.6):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = {}
        self.rules = []
        self.transactions = []

    def fit(self, transactions: list[set]):
        self.transactions = transactions
        self._generate_frequent_itemsets()
        self._generate_association_rules()

    def _generate_frequent_itemsets(self):
        total = len(self.transactions)
        itemset_counts = defaultdict(int)

        # 1-елементні набори
        for transaction in self.transactions:
            for item in transaction:
                itemset_counts[frozenset([item])] += 1

        self.frequent_itemsets = {
            item: count for item, count in itemset_counts.items()
            if count / total >= self.min_support
        }

        k = 2
        current_frequent = list(self.frequent_itemsets.keys())

        while current_frequent:
            candidates = list(set(
                frozenset(i.union(j))
                for i in current_frequent
                for j in current_frequent
                if len(i.union(j)) == k
            ))

            itemset_counts = defaultdict(int)
            for transaction in self.transactions:
                for candidate in candidates:
                    if candidate.issubset(transaction):
                        itemset_counts[candidate] += 1

            current_frequent = [
                item for item in itemset_counts
                if itemset_counts[item] / total >= self.min_support
            ]
            self.frequent_itemsets.update({
                item: itemset_counts[item] for item in current_frequent
            })
            k += 1

    def _generate_association_rules(self):
        total = len(self.transactions)
        self.rules = []

        for itemset in self.frequent_itemsets:
            if len(itemset) < 2:
                continue

            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent

                    support_itemset = self.frequent_itemsets[itemset] / total
                    support_antecedent = self.frequent_itemsets.get(antecedent, 0) / total

                    if support_antecedent == 0:
                        continue

                    confidence = support_itemset / support_antecedent
                    if confidence >= self.min_confidence:
                        self.rules.append({
                            "antecedent": antecedent,
                            "consequent": consequent,
                            "support": round(support_itemset, 3),
                            "confidence": round(confidence, 3)
                        })

    def get_frequent_itemsets(self) -> pd.DataFrame:
        total = len(self.transactions)
        return pd.DataFrame([
            {"itemset": ', '.join(item), "support": round(count / total, 3)}
            for item, count in self.frequent_itemsets.items()
        ])

    def get_rules(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "antecedent": ', '.join(rule["antecedent"]),
                "consequent": ', '.join(rule["consequent"]),
                "support": rule["support"],
                "confidence": rule["confidence"]
            }
            for rule in self.rules
        ])


if __name__ == '__main__':
    df = pd.read_csv("../datasets/unique_transactions_100.csv")
    transactions = df.apply(lambda row: set(row.dropna()), axis=1).tolist()

    ap = Apriori(min_support=0.2, min_confidence=0.6)
    ap.fit(transactions)

    print('Частота наборів товару:')
    print(ap.get_frequent_itemsets().head(20))
    print('Асоціативні правила:')
    print(ap.get_rules().head(20))
