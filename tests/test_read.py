from xpbt.genomes.read import ReadLazyStitcher
from xpbt.genomes.fastq import FastQ
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
