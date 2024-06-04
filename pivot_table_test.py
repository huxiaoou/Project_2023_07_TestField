import numpy as np
import pandas as pd

n = 20
m = 5
k = 3

df = pd.DataFrame({
    "T": [_ for g in [[f"T{_:03d}"] * m for _ in range(n)] for _ in g],
    "C": [f"C{_}" for _ in range(m)] * n,
    "I": (["I0"] * k + ["I1"] * (m - k)) * n,
    "volume": np.random.randint(0, 100, size=n * m),
    "amount": np.random.randint(0, 1000, size=n * m),
    "oi": np.random.randint(0, 500, size=n * m)
}).sort_values("T")
print(df)

sum_df = pd.pivot_table(data=df, index=["T", "I"], values=["volume", "amount", "oi"], aggfunc=sum)

print(sum_df)
