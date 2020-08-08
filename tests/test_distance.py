from xpbt.genomes import Distance
from xpbt.genomes import Sequence
from random import random
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

    def test_levenshtein(self):
        self.assertEqual(0, Distance.levenshtein('', ''))
        self.assertEqual(3, Distance.levenshtein('', 'abc'))
        self.assertEqual(2, Distance.levenshtein('abcde', 'acd'))
        self.assertEqual(4, Distance.levenshtein('abcabcabc', 'bcabc'))
        self.assertEqual(5, Distance.levenshtein('abcabcabc', 'bcac'))
        self.assertEqual(5, Distance.levenshtein('bcac', 'abcabcabc'))

        for _ in range(100):
            s = Sequence.randomDnaKmer(100)
            tmp = list(s)
            edited = []
            edits = 0
            i = 0
            while i < len(tmp):
                r = random()
                if r < 10 / 100:
                    # deletion
                    edits += 1
                elif r < 20 / 100:
                    # insertion
                    edited.append('-')
                    i -= 1  # do not move index
                    edits += 1
                elif r < 30 / 100:
                    # substitution
                    edited.append('*')
                    edits += 1
                else:
                    edited.append(tmp[i])
                i += 1
            edited = ''.join(edited)
            self.assertLessEqual(Distance.levenshtein(edited, s), edits)
