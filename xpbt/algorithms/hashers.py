import xpbt.core
import typing as tp


class DnaKmerHasher(xpbt.core.DnaKmerHasher):
    def __init__(self, kmerLengthOrString: tp.Union[int, str], bitWidth: int = None):
        """
        Hash a DNA Kmer to a positive integer uniformly distributed in [0, 2^bitWidth-1)
        :param kmerLengthOrString: the length of the K-mer, i.e. the K, or a string to load from to create a DnaKmerHasher
        :param bitWidth:  the K-mer will be hashed to an integer uniformly distributed in [0, 2^bitWidth-1)
        """
        if type(kmerLengthOrString) is int and bitWidth is not None:
            super(DnaKmerHasher, self).__init__(kmerLengthOrString, bitWidth)
        elif type(kmerLengthOrString) is str and bitWidth is None:
            super(DnaKmerHasher, self).__init__(kmerLengthOrString)
        else:
            raise Exception(f"Cannot understand the parameters: {kmerLengthOrString} and {bitWidth}")

    def str(self) -> str:
        """

        :return: a string representation of the DnaKmerHasher. It can be used to recreate the DnaKmerHashser
        """
        return super(DnaKmerHasher, self).str()

    def hash(self, kmer: str) -> int:
        """
        Hash the kmer to an integer. The length of the kmer must equal to the kmerLength set in the __init__
        :param kmer: the DNA Kmer
        :return: the hashed integer
        """
        return super(DnaKmerHasher, self).hash(kmer)

    def getIndexPermutations(self) -> list:
        """
        Get the index permutations. This is for debugging purpose. No other practical use.
        :param result:
        :return: (list) the list of index permutations.
        """
        result=xpbt.core.IntVector()
        super(DnaKmerHasher, self).getIndexPermutations(result)
        return list(result)
