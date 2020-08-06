from xpbt.genomes.aligned import AlignedRead, AlignedReference
from xpbt.genomes.cigar import CIGAR
from unittest import TestCase


class TestRead(TestCase):

    def test_aligned_read(self):
        ar = AlignedRead("test")
        ar.insert(0, "chr2", 3, 41, False, CIGAR.cigarString2TuplePairs("8M7D6M2I2M11D7M"))
        ar.insert(200, "chrY", 3, 24, False, CIGAR.cigarString2TuplePairs("3S10M2D8I9M20H"))
        ar.insert(0, "chr1", 10, 30, False, CIGAR.cigarString2TuplePairs("20M"))
        ar.insert(100, "chr4", 5, 26, False, CIGAR.cigarString2TuplePairs("3S10M2D8I9M20H"))
        ar.insert(0, "chr5", 59, 100, True, CIGAR.cigarString2TuplePairs("8M7D6M2I2M11D3M"))
        ar.insert(100, "chr5", 75, 100, True, CIGAR.cigarString2TuplePairs("4H5M1I10M1D10M"))

        res = ar.map(4)
        self.assertEqual(3, len(res))
        self.assertEqual(
            tuple(sorted(["chr2:7_8,+", "chr1:14_15,+", "chr5:84_85,-"])),
            tuple(sorted([None if z is None else z.str() for z in res]))
        )

        res = ar.map(110)
        self.assertEqual(2, len(res))
        self.assertEqual(
            tuple(sorted(["chr4:12_13,+", "chr5:88_89,-"])),
            tuple(sorted([None if z is None else z.str() for z in res]))
        )

        res = ar.map(300)
        self.assertEqual(0, len(res))

    def test_aligned_reference(self):
        ar = AlignedReference("chr1")
        ar.insert("read1", 0, 3, 24, False, CIGAR.cigarString2TuplePairs("3S10M2D8I9M20H"))
        ar.insert("read2", 50, 20, 45, True, CIGAR.cigarString2TuplePairs("4H5M1I10M1D10M"))

        res = ar.map(2)
        self.assertEqual(0, len(res))

        res = ar.map(4)
        self.assertEqual(1, len(res))
        self.assertEqual(
            tuple(sorted(["read1:4_5,+"])),
            tuple(sorted([None if z is None else z.str() for z in res]))
        )

        res = ar.map(14)  # deletion
        self.assertEqual(
            tuple([None]),
            tuple(sorted([None if z is None else z.str() for z in res]))
        )

        res = ar.map(22)
        self.assertEqual(
            tuple(sorted(["read1:28_29,+", "read2:72_73,-"])),
            tuple(sorted([None if z is None else z.str() for z in res]))
        )

        res = ar.map(29)  # deletion
        self.assertEqual(
            tuple([None]),
            tuple(sorted([None if z is None else z.str() for z in res]))
        )
