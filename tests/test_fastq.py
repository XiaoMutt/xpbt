from xpbt.genomes.fastq import FastQ
from xpbt.genomes.fastq import FastQIntegrator
from xpbt.genomes.read import ReadStitcher
from xpbt.genomes import fastq
from unittest import TestCase


class TestFastQ(TestCase):
    def test_fastq_integrator(self):
        fi = FastQIntegrator()
        record1 = FastQ("record1",
                        "CATTCTTCACGTAGTTCTCGAGC",
                        "",
                        "$$$$$$$$$$$$$$$$$$$$$$$")
        for _ in range(3):
            fi.add(record1)
        result = fi.integrate("merged")
        self.assertEqual("merged", result.id)
        self.assertEqual("CATTCTTCACGTAGTTCTCGAGC", result.seq)
        self.assertEqual("#######################", result.desc)
        self.assertEqual("***********************", result.qual)

        record2 = FastQ("record2",
                        "CATTCTTCACGTAGTTCTCGAGCT",
                        "",
                        "$$$$$$$$$$$$$$$$$$$$$$$;")

        fi.add(record2)

        result = fi.integrate("merged")
        self.assertEqual("merged", result.id)
        self.assertEqual("CATTCTTCACGTAGTTCTCGAGCT", result.seq)
        self.assertEqual("$$$$$$$$$$$$$$$$$$$$$$$!", result.desc)
        self.assertEqual("///////////////////////;", result.qual)

    def test_fastq_stitcher(self):
        rs = ReadStitcher()

        read1 = FastQ("read1",
                      "CTCTTGAGTAGCTGGGATTACAGCATGCCACCATGCCTGGCTAATTTTT",
                      "",
                      "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        read2 = FastQ("read2",
                      "TGAAACCCCATCTCTACTAAAAATACAAAAATTAGCCAGGCATGGT",
                      "",
                      "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

        read = rs.lazyStitch("stitched", read1, read2)
        self.assertEqual("CTCTTGAGTAGCTGGGATTACAGCATGCCACCATGCCTGGCTAATTTTTGTATTTTTAGTAGAGATGGGGTTTCA",
                         read.seq)
        self.assertEqual("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAKKKKKKKKKKKKKKKKKKKKBBBBBBBBBBBBBBBBBBBBBBBBBB",
                         read.qual)

        # one base miss-match
        read2 = FastQ("read2",
                      "TGAAACCCCATCTCTACTAAAAATACAAAAATTAGCCACGCATGGT",
                      "",
                      "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        read = rs.lazyStitch("stitched", read1, read2)
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
            rs.lazyStitch("unableToStitch", read1, read2)

        # allow overhange
        read1 = FastQ("read1",
                      "AGCATGCCACCATGCCTGGCTAATTTTTGTATTTTTAGTAGAGATGGGGTTTCA",
                      "",
                      "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        read2 = FastQ("read2",
                      "AAATACAAAAATTAGCCAGGCATGGTGGCATGCTGTAATCCCAGCTACTCAAGAG",
                      "",
                      "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

        rs = ReadStitcher(20, 1, True)
        read = rs.lazyStitch("stitched", read1, read2)

        self.assertEqual("CTCTTGAGTAGCTGGGATTACAGCATGCCACCATGCCTGGCTAATTTTTGTATTTTTAGTAGAGATGGGGTTTCA",
                         read.seq)
        self.assertEqual("BBBBBBBBBBBBBBBBBBBBBKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKAAAAAAAAAAAAAAAAAAAA",
                         read.qual)

        rs = ReadStitcher(20, 1, False)
        with self.assertRaises(ValueError):
            rs.lazyStitch("unableToStitch", read1, read2)
