import xpbt.core


class DnaKmerHasher(xpbt.core.DnaKmerHasher):
    def getIndexPermutations(self, result=xpbt.core.IntVector()):
        super(DnaKmerHasher, self).getIndexPermutations(result)
        return result
