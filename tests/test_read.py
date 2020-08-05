from xpbt.genomes.read import ReadLazyStitcher, AlignedRead
from xpbt.genomes.fastq import FastQ
from xpbt.genomes.coordinates import Zeronate
from xpbt.genomes.cigar import CIGAR
from unittest import TestCase


class TestRead(TestCase):
    def test_fastq_stitcher(self):
        rs = ReadLazyStitcher()

        read1 = FastQ("read1",
                      "CTCTTGAGTAGCTGGGATTACAGCATGCCACCATGCCTGGCTAATTTTT",
                      "",
                      "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        read2 = FastQ("read2",
                      "TGAAACCCCATCTCTACTAAAAATACAAAAATTAGCCAGGCATGGT",
                      "",
                      "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

        read = rs.stitch(read1, read2, "stitched")
        self.assertEqual("CTCTTGAGTAGCTGGGATTACAGCATGCCACCATGCCTGGCTAATTTTTGTATTTTTAGTAGAGATGGGGTTTCA",
                         read.seq)
        self.assertEqual("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAKKKKKKKKKKKKKKKKKKKKBBBBBBBBBBBBBBBBBBBBBBBBBB",
                         read.qual)

        # one base miss-match
        read2 = FastQ("read2",
                      "TGAAACCCCATCTCTACTAAAAATACAAAAATTAGCCACGCATGGT",
                      "",
                      "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        read = rs.stitch(read1, read2, "stitched")
        self.assertEqual("CTCTTGAGTAGCTGGGATTACAGCATGCCACCATGCGTGGCTAATTTTTGTATTTTTAGTAGAGATGGGGTTTCA",
                         read.seq)
        self.assertEqual("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAKKKKKKK$KKKKKKKKKKKKBBBBBBBBBBBBBBBBBBBBBBBBBB",
                         read.qual)

        # cannot stitch
        read2 = FastQ("read2",
                      "TGAAACCCCATCTCTACTAAAAATACAAAATTTAGCCACGCATGGT",
                      "",
                      "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

        with self.assertRaises(ValueError):
            rs.stitch(read1, read2, "unableToStitch")

        # allow overhange
        read1 = FastQ("read1",
                      "AGCATGCCACCATGCCTGGCTAATTTTTGTATTTTTAGTAGAGATGGGGTTTCA",
                      "",
                      "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        read2 = FastQ("read2",
                      "AAATACAAAAATTAGCCAGGCATGGTGGCATGCTGTAATCCCAGCTACTCAAGAG",
                      "",
                      "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

        rs = ReadLazyStitcher(20, 1, True)
        read = rs.stitch(read1, read2, "stitched")

        self.assertEqual("CTCTTGAGTAGCTGGGATTACAGCATGCCACCATGCCTGGCTAATTTTTGTATTTTTAGTAGAGATGGGGTTTCA",
                         read.seq)
        self.assertEqual("BBBBBBBBBBBBBBBBBBBBBKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKAAAAAAAAAAAAAAAAAAAA",
                         read.qual)

        rs = ReadLazyStitcher(20, 1, False)
        with self.assertRaises(ValueError):
            rs.stitch(read1, read2, "unableToStitch")

    def test_aligned_read(self):
        ar = AlignedRead("test")
        ar.insertAlignedSegment(0, Zeronate("chr2", 3, 41, False), CIGAR.cigarString2TuplePairs("8M7D6M2I2M11D7M"))
        ar.insertAlignedSegment(200, Zeronate("chrY", 3, 24, False), CIGAR.cigarString2TuplePairs("3S10M2D8I9M20H"))
        ar.insertAlignedSegment(0, Zeronate("chr1", 10, 30, False), CIGAR.cigarString2TuplePairs("20M"))
        ar.insertAlignedSegment(100, Zeronate("chr4", 5, 26, False), CIGAR.cigarString2TuplePairs("3S10M2D8I9M20H"))
        ar.insertAlignedSegment(0, Zeronate("chr5", 59, 100, True), CIGAR.cigarString2TuplePairs("8M7D6M2I2M11D3M"))
        ar.insertAlignedSegment(100, Zeronate("chr5", 75, 100, True), CIGAR.cigarString2TuplePairs("4H5M1I10M1D10M"))

        res = ar.map(4)
        self.assertEqual(3, len(res))
        self.assertEqual(
            tuple(sorted(["chr2:7_8,+", "chr1:14_15,+", "chr5:84_85,-"])),
            tuple(sorted([z.str() for z in res]))
        )

        res = ar.map(110)
        self.assertEqual(2, len(res))
        self.assertEqual(
            tuple(sorted(["chr4:12_13,+", "chr5:88_89,-"])),
            tuple(sorted([z.str() for z in res]))
        )

        res = ar.map(300)
        self.assertEqual(0, len(res))
