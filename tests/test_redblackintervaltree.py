from xpbt.xpbt import RedBlackIntervalTree
from random import randint
from tqdm import tqdm

rbit = RedBlackIntervalTree()
for _ in tqdm(range(1000000)):
    low = randint(-1000000, 1000000)
    high = low + randint(0, 1000)
    rbit.insert(low, high)
rbit.check()
