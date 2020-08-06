import xpbt.core
from xpbt.genomes.fastq import FastQ


class ReadLazyStitcher(xpbt.core.ReadLazyStitcher):
    def __init__(self, minNumOfOverlappingBases: int = 20, maxHammingDistance: int = 1,
                 allow3PrimeOverhang: bool = False):
        """
        A stitcher that do Lazy stitch. lazy means as long as the minimum overlapping length is reached and the
        maxHammingDistance is satisfied, the two reads are stitched together.
        :param minNumOfOverlappingBases: minimum overlapping bases to stitch the reads
        :param maxHammingDistance: maximum allowed hamming distance allowed in the overlapping region
        :param allow3PrimeOverhang: whether allow 3 prime overhang when stitch the two reads
        """
        super(ReadLazyStitcher, self).__init__(minNumOfOverlappingBases, maxHammingDistance, allow3PrimeOverhang)

    def stitch(self, read1: FastQ, read2: FastQ, newId: str = "stitched") -> FastQ:
        """
            Stitch Read1 and Read2 based on their sequence.
            It is a lazy stitching, which means as long as read1 and read2 have a common region of length>=minNumOfOverlappingBases
            they are stitched together. Here is how it works:
            - starts from minNumOfOverlappingBases
            - sliding inwards
            - if the hamming distance of the overlapping part <= maxHammingDistance, the overlapping part is stitched
            (highest qual base is used when there is a discrepancy)

                         read1Begin                          read1End
                             |     minNumOfOverlappingBases     |
            read1 ---------------------------------------------->
                             <---------------------------------------------- read2
                             |                                  |
                         read2End                          read2Begin
         * @param r1
         * @param r2
         * @return the stitched FastQ or an empty FastQ if fail to stitch

        :param read1:
        :param read2:
        :param newId: the new ID of the stitched FastQ
        :return: stitched FastQ
        :raise: ValueError if not able to stitch
        """
        return super(ReadLazyStitcher, self).stitch(read1, read2, newId)
