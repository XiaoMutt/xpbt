from xpbt.genome.coordinates import Zeronate
from xpbt.algorithm.red_black_tree import RedBlackIntervalTree
from xpbt.ngs.cigar import Cigarette, CIGAR

z = Zeronate.parse("chr1:123-133,-")
print(z.chr)
print(z.start)
print(z.stop)
print(z.strand)
print(z.thisown)

cig = Cigarette(0, 10, z, CIGAR.CODE.M)

rbit = RedBlackIntervalTree()
rbit.insert(cig)
rbit.check()
