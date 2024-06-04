import itertools
import time
import tqdm

n = 100
d = 0.02

# for i in tqdm.tqdm(range(n)):
#     time.sleep(d)
#
# for i in tqdm.tqdm([f'a{_}' for _ in range(n)]):
#     time.sleep(d)

p, q = 20, 20
for x, y in tqdm.tqdm(list(itertools.product(range(p), range(q)))):
    time.sleep(d)
