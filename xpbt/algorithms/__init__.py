import xpbt.core


class DnaKmerHasher(xpbt.core.DnaKmerHasher):

    def getIndexPermutations(self):
        res = xpbt.core.IntVector()
        super(DnaKmerHasher, self).getIndexPermutations(res)
        return res


