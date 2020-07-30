from xpbt.xpbt import Zeronate
from unittest import TestCase
from xpbt.xpbt import RedBlackIntervalTree
from random import randint
from tqdm import tqdm

z = Zeronate.parse("chr1:123-125,-")
print(z.chr)
print(z.start)
print(z.stop)
print(z.strand)
print(z.thisown)

