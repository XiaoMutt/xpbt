from xpbt.xpbt import DnaKmerHasher
from xpbt.xpbt import Sequence
from unittest import TestCase
from scipy.stats import chisquare
import numpy as np
import matplotlib.pyplot as plt


class TestDnaKmerHasher(TestCase):
    def test_hash_uniform0(self):
        for M in (8, 16, 32, 64):
            upper_bound = 2 ** M - 1

            for K in range(8, 257, 8):
                hashes = []
                dkh = DnaKmerHasher(K, M)
                for _ in range(10000):
                    dna = Sequence.randomDnaKmer(K)
                    hashes.append(dkh.hash(dna) / upper_bound)

                # for the random hash values to reach the boundary (0 and 1), k should be bigger than M/2
                self.assertAlmostEqual(0, min(hashes), 2)
                self.assertAlmostEqual(1, max(hashes), 2)

                hist, edges = np.histogram(hashes, bins=50, density=True)
                self.assertGreater(chisquare(hist)[1], 0.05)

    def test_hash_uniform1(self):
        for M in (8, 16, 32, 64):
            upper_bound = 2 ** M - 1
            for K in range(8, 257, 8):
                dna = Sequence.randomDnaKmer(K)
                hashes = []
                for _ in range(10000):
                    dkh = DnaKmerHasher(K, M)
                    hashes.append(dkh.hash(dna) / upper_bound)

                self.assertAlmostEqual(min(hashes), 0, 2)
                self.assertAlmostEqual(max(hashes), 1, 2)
                hist, edges = np.histogram(hashes, bins=50, density=True)
                self.assertGreater(chisquare(hist)[1], 0.05)

    def test_hash_uniform2(self):
        for M in (8, 16, 32, 64):
            upper_bound = 2 ** M - 1
            for K in range(8, 257, 8):
                for base in ('a', 'T', 'G', 'c'):
                    dna = base * K
                    hashes = []
                    for _ in range(10000):
                        dkh = DnaKmerHasher(K, M)
                        hashes.append(dkh.hash(dna) / upper_bound)
                    self.assertAlmostEqual(min(hashes), 0, 2)
                    self.assertAlmostEqual(max(hashes), 1, 2)
                    hist, edges = np.histogram(hashes, bins=50, density=True)
                    self.assertGreater(chisquare(hist)[1], 0.05)

    def test_hash_uniform3(self):
        # small M
        for M in (1, 2, 4):
            upper_bound = 2 ** M - 1
            for K in range(4, 8, 16):
                for base in ('a', 'T', 'G', 'c'):
                    dna = base * K
                    hashes = []
                    for _ in range(10000):
                        dkh = DnaKmerHasher(K, M)
                        hashes.append(dkh.hash(dna))
                    hist, edges = np.histogram(hashes, bins=upper_bound + 1, density=True)
                    self.assertGreater(chisquare(hist)[1], 0.05)

    def test_hash_certainty(self):
        for M in (8, 16, 32, 64):
            for K in range(8, 257, 8):
                dkh = DnaKmerHasher(K, M)
                dna = Sequence.randomDnaKmer(K)
                h = dkh.hash(dna)
                for _ in range(100):
                    self.assertEqual(h, dkh.hash(dna))

    def test_exception(self):
        with self.assertRaises(RuntimeError):
            dkh = DnaKmerHasher(3, 16)
        with self.assertRaises(RuntimeError):
            dkh = DnaKmerHasher(65536, 16)
        with self.assertRaises(RuntimeError):
            dkh = DnaKmerHasher(4, 0)
        with self.assertRaises(RuntimeError):
            dkh = DnaKmerHasher(4, 65)

        dkh = DnaKmerHasher(4, 64)
        with self.assertRaises(RuntimeError):
            dkh.hash('ATAAA')
        with self.assertRaises(RuntimeError):
            dkh.hash('ATA')

    def test_to_string(self):
        for M in (1, 2, 4, 8, 11, 16, 17, 32, 64):
            for K in range(4, 257, 4):
                for _ in range(100):
                    dkh = DnaKmerHasher(K, M)
                    dna = Sequence.randomDnaKmer(K)
                    hash = dkh.hash(dna)

                    dkh = DnaKmerHasher(dkh.toString())
                    self.assertEqual(hash, dkh.hash(dna))
