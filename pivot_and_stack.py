import numpy as np
import pandas as pd


def sum_nan(x: pd.Series):
    return x.dropna().sum()


df = pd.DataFrame({
    "A": ['a', 'a', 'a', 'b', 'c', 'c', 'd', 'd', 'd'],
    "B": ['x', 'y', 'z', 'x', 'x', 'z', 'x', 'y', 'z'],
    "C": [1, 2, 3, 4, 5, 6, 7, 8, 9],
})
print("\n", df)

p = pd.pivot_table(data=df, index="A", columns="B", values="C")
print("\n", p)

s = p.stack(dropna=False)
print("\n", s)

m = s.rolling(window=2, min_periods=1).mean()
print("\n", m)

x = s / m - 1
print("\n", x)

df0 = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [3.14, 6, 5, np.nan, -1]})
df1 = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [3.14, 6, 5, 2023, -1]})
df2 = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [3.14, 6, 5, np.inf, -1]})

print("\n" + "-" * 60)
print(df0.corr(method="pearson").at["A", "B"])
print(df1.corr(method="pearson").at["A", "B"])
print(df2.corr(method="pearson").at["A", "B"])

print("\n" + "-" * 60)
print(df0.corr(method="spearman").at["A", "B"])
print(df1.corr(method="spearman").at["A", "B"])
print(df2.corr(method="spearman").at["A", "B"])
