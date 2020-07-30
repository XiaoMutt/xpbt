from xpbt.xpbt import Sequence

from unittest import TestCase
from collections import Counter
from scipy.stats import chisquare
import matplotlib.pyplot as plt


class TestSequence(TestCase):
    def test_randomDnaKmer(self):
        c = Counter()
        for k in range(0, 101):
            seq = Sequence.randomDnaKmer(k)
            self.assertEqual(k, len(seq))
            c += Counter(seq)

        self.assertEqual(tuple(sorted(c.keys())), tuple('ACGT'))

        self.assertGreaterEqual(chisquare(list(c.values()))[1], 0.05)

    def test_randomRnaKmer(self):
        c = Counter()
        for k in range(0, 101):
            seq = Sequence.randomRnaKmer(k)
            self.assertEqual(k, len(seq))
            c += Counter(seq)

        self.assertEqual(tuple(sorted(c.keys())), tuple('ACGU'))

        self.assertGreaterEqual(chisquare(list(c.values()))[1], 0.05)

    def test_reverse(self):
        for k in range(0, 101):
            dna = Sequence.randomDnaKmer(k)
            self.assertEqual(Sequence.reverse(dna), dna[::-1])

    def test_reverseComplementDna(self):
        self.assertEqual('atatataaatcttgtttCTAGa', Sequence.reverseComplementDna('tCTAGaaacaagatttatatat'))
        for k in range(0, 101):
            dna = Sequence.randomDnaKmer(k)
            self.assertEqual(Sequence.complementDna(Sequence.reverse(dna)), Sequence.reverseComplementDna(dna))
            self.assertEqual(Sequence.reverse(Sequence.complementDna(dna)), Sequence.reverseComplementDna(dna))

    def test_reverseComplementRna(self):
        self.assertEqual('auauauaaaucuuguuuCUAGa', Sequence.reverseComplementRna('uCUAGaaacaagauuuauauau'))
        for k in range(0, 101):
            rna = Sequence.randomRnaKmer(k)
            self.assertEqual(Sequence.complementRna(Sequence.reverse(rna)), Sequence.reverseComplementRna(rna))
            self.assertEqual(Sequence.reverse(Sequence.complementRna(rna)), Sequence.reverseComplementRna(rna))