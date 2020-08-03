from xpbt.core import Zeronate
from unittest import TestCase


class TestZeronate(TestCase):
    def test_init(self):
        z = Zeronate("abc", 124, 12938, True)
        self.assertEqual("abc", z.chr)
        self.assertEqual(124, z.start)
        self.assertEqual(12938, z.stop)
        self.assertEqual(True, z.reverseStrand)

        z = Zeronate("abc", 1245, 129138, False)
        self.assertEqual("abc", z.chr)
        self.assertEqual(1245, z.start)
        self.assertEqual(129138, z.stop)
        self.assertEqual(False, z.reverseStrand)

        with self.assertRaises(RuntimeError):
            Zeronate("abc", 123, 120, False)

        with self.assertRaises(RuntimeError):
            Zeronate("", 124, 1254, True)

        with self.assertRaises(OverflowError):
            Zeronate("abc", -1, 124, False)

    def test_parse(self):
        z = Zeronate.parse("chr1:123_134,-")
        self.assertEqual("chr1", z.chr)
        self.assertEqual(123, z.start)
        self.assertEqual(134, z.stop)
        self.assertEqual(True, z.reverseStrand)

        z = Zeronate.parse("chr2:1234567890,+")
        self.assertEqual("chr2", z.chr)
        self.assertEqual(1234567890, z.start)
        self.assertEqual(1234567890, z.stop)
        self.assertEqual(False, z.reverseStrand)

        z = Zeronate.parse("chr:1234567891,-")
        self.assertEqual("chr", z.chr)
        self.assertEqual(1234567891, z.start)
        self.assertEqual(1234567891, z.stop)
        self.assertEqual(True, z.reverseStrand)

        z = Zeronate.parse("chr2:1234567890 1234567899,-")
        self.assertEqual("chr2", z.chr)
        self.assertEqual(1234567890, z.start)
        self.assertEqual(1234567899, z.stop)
        self.assertEqual(True, z.reverseStrand)

        z = Zeronate.parse("chr2:1234567891")
        self.assertEqual("chr2", z.chr)
        self.assertEqual(1234567891, z.start)
        self.assertEqual(1234567891, z.stop)
        self.assertEqual(False, z.reverseStrand)

        with self.assertRaises(RuntimeError):
            Zeronate.parse("chr1:124-13,+")

    def test_str(self):
        self.assertEqual("chr2:1234567891_1234567899,-", Zeronate.parse("chr2:1234567891 1234567899,-").str())

        self.assertEqual("chr2:1234567891_1234567891,-", Zeronate.parse("chr2:1234567891,-").str())

        self.assertEqual("chr2:1234567891_1234567899,+", Zeronate.parse("chr2:1234567891 1234567899,+").str())

        self.assertEqual("chr2:1234567891_1234567891,+", Zeronate.parse("chr2:1234567891,+").str())

        self.assertEqual("chr2:1234567891_1234567891,+", Zeronate.parse("chr2:1234567891").str())
