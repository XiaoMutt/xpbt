from xpbt.genomes.fastq import FastQ
from xpbt.genomes.fastq import FastQIntegrator
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
        del record1
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


