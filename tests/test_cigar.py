from xpbt.genomes.cigar import CIGAR, Cigarette
from unittest import TestCase


class TestCigar(TestCase):
    def test_cigar_code(self):
        cigar_codes = tuple("MIDNSHPEX")
        for idx, op in enumerate(cigar_codes):
            self.assertEqual(idx, CIGAR.OPERATION[op])

        with self.assertRaises(AttributeError):
            CIGAR.OPERATION.M = 2

    def test_cigar(self):
        with self.assertRaises(Exception):
            CIGAR.CONSUMES_REFER = False

        self.assertEqual(CIGAR.ALIGN_RELEVANT,
                         tuple([a or b for a, b in zip(CIGAR.CONSUMES_QUERY, CIGAR.CONSUMES_REFER)]))

        self.assertEqual(CIGAR.CONSUMES_BOTH2,
                         tuple([a and b for a, b in zip(CIGAR.CONSUMES_QUERY, CIGAR.CONSUMES_REFER)]))

    def test_cigar_string2tuple(self):
        self.assertEqual(((5, 76), (0, 130)),
                         CIGAR.cigarString2TuplePairs("76H130M"))
        self.assertEqual(((0, 85), (3, 88), (0, 16)),
                         CIGAR.cigarString2TuplePairs("85M88N16M"))
        self.assertEqual(((4, 6), (0, 5), (2, 8), (1, 7), (0, 16), (5, 32)),
                         CIGAR.cigarString2TuplePairs("6S5M8D7I16M32H"))
        self.assertEqual((), CIGAR.cigarString2TuplePairs(""))
