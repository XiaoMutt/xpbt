from xpbt import Distance
from xpbt import Sequence
from unittest import TestCase


class TestDistance(TestCase):
    def test_hamming(self):
        self.assertEqual(Distance.hamming('', ''), 0)
        self.assertEqual(Distance.hamming("123456789", "12345678*"), 1)

        with self.assertRaises(RuntimeError):
            Distance.hamming('12', '123')

        for i in range(100):
            s = Sequence.randomDnaKmer(100)
            tmp = list(s)
            for j in range(i):
                tmp[j] = '*'

            t = ''.join(tmp)
            self.assertEqual(Distance.hamming(s, t), i)
