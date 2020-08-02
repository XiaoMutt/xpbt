import xpbt.core
import typing as tp


class DnaKmerBloomFilter(xpbt.core.DnaKmerBloomFilter):
    def __init__(self, kmerLengthOrFileName: tp.Union[int, str],
                 falsePositiveRateOrNumOfKmers: tp.Union[float, int, None] = None,
                 storageBitWidth: tp.Optional[int] = None):
        """
        A Bloom Filter for DNA Kmers.
        Bloom Filter is a high-speed and memory-efficient "memorization" unit. It is based on probabilities and will
        have a controlled false positive rate. However, it has no false negatives. The false positive rate is affected
        by the storage space and number of kmers stored in the Bloom Filter.

        The arguments are valid in the following cases:
        * FileName: str, None, None (load from a file)
        * kmerLength: int, falsePositiveRate: float, storageBitWidth: int
        * kmerLength: int, NumOfKmers: int, storageBitWidth: int
        :param kmerLengthOrFileName: the DNA Kmer Length. Or the File Name to load and reconstruct a DnaKmerBloomFilter
        :param falsePositiveRateOrNumOfKmers: desired falsePositiveRate or Expected maximum Number of Kmers to add
        :param storageBitWidth: the storage space of the Bloom filter is 2^storageBitWith/8 bytes. This must be [4, 32]

        """
        if type(kmerLengthOrFileName) is str and falsePositiveRateOrNumOfKmers is None and storageBitWidth is None:
            super(DnaKmerBloomFilter, self).__init__(kmerLengthOrFileName)
        elif type(kmerLengthOrFileName) is int and type(falsePositiveRateOrNumOfKmers) is not None \
                and type(storageBitWidth) is not None:
            super(DnaKmerBloomFilter, self).__init__(kmerLengthOrFileName, falsePositiveRateOrNumOfKmers,
                                                     storageBitWidth)
        else:
            raise Exception(f"Cannot understand the arguments "
                            f"{kmerLengthOrFileName}, {falsePositiveRateOrNumOfKmers}, {storageBitWidth}")

    def add(self, dnaKmer: str) -> bool:
        """
        Add the DNA Kmer in to the Bloom filter.
        :param dnaKmer: The DNA Kmer to be added to the Bloom Filter.
        The length of the dna must be the same as kmerLength set by the constructor.
        :return: True if the Bloom Filter did not contain this dna and it has been successfully added.
        False if the Bloom Filter already contains this dna and there is no need to add it.
        """

        return super(DnaKmerBloomFilter, self).add(dnaKmer)

    def contains(self, dnaKmer: str) -> bool:
        """
        Check if the Bloom Filter contains this dnaKmer
        :param dnaKmer: the dnaKmer to check.
        The length of the dna must be the same as kmerLength set by the constructor.
        :return: return True if the Bloom filter contains the dna; otherwise False.
        """
        return super(DnaKmerBloomFilter, self).contains(dnaKmer)

    def getKmerK(self) -> int:
        """
        :return: the set length of the DNA Kmer
        """
        return super(DnaKmerBloomFilter, self).getKmerK()

    def getFalsePositiveRate(self) -> float:
        """
        :return: the false positive rate of the Bloom filter
        """
        return super(DnaKmerBloomFilter, self).getFalsePositiveRate()

    def getMaxCapacity(self) -> int:
        """

        :return: the max number of Kmers can be added to the Bloom filter
        under the constrain of the falsePositiveRate and the storageBitWidth.
        """
        return super(DnaKmerBloomFilter, self).getMaxCapacity()

    def getStorageBitSize(self) -> int:
        """

        :return: the storage size of the Bloom filter in bits
        """
        return super(DnaKmerBloomFilter, self).getStorageBitSize()

    def saveToFile(self, fileName: str):
        """
        Save the Bloom to the fileName. The file can be used to reconstruct the Bloom Filter.
        :param fileName:
        :return: None
        """
        super(DnaKmerBloomFilter, self).saveToFile(fileName)

    def getNumOfHashers(self) -> int:
        """
        :return: Number of Hashers used by this Bloom Filter
        """
        return super(DnaKmerBloomFilter, self).getNumOfHashers()
