from xpbt.algorithms.bloom_filters import DnaKmerBloomFilter
from xpbt.genomes import Sequence
from unittest import TestCase
import math
import os


class TestDnaKmerBloomFilter(TestCase):
    def test_add(self):
        for kmerk in (4, 8, 16, 32, 64):
            for bitwidth in (12, 24):
                tracking = set()
                dkbf = DnaKmerBloomFilter(kmerk, 0.01, bitwidth)
                for _ in range(dkbf.getMaxCapacity()):
                    dna = Sequence.randomDnaKmer(kmerk)
                    if dna in tracking:
                        exist = True
                    else:
                        exist = False
                        tracking.add(dna)

                    added = dkbf.add(dna)
                    if exist:
                        self.assertEqual(False, added, msg="This cannot happen: Bloom Filter has no false negatives.")

                    self.assertEqual(True, dkbf.contains(dna),
                                     msg="This cannot happen: Bloom Filter has no false negatives.")

    def test_false_positive_rate0(self):
        for n in (2, 3, 5,):
            fp = 1 / (10 ** n)
            for kmerk in (64,):  # ATTENTION: 4^kmerk should be way greater than 10^(n+1) for the test to work
                for bitwidth in (10, 24):

                    tracking = set()
                    dkbf = DnaKmerBloomFilter(kmerk, fp, bitwidth)

                    for _ in range(dkbf.getMaxCapacity()):
                        dna = Sequence.randomDnaKmer(kmerk)
                        dkbf.add(dna)
                        tracking.add(dna)

                    false_positive = 0
                    count = 0
                    # ATTENTION: need to have >10^(n+1) rounds to have an accurate estimate
                    while count < 10 ** (n + 2)*2:
                        dna = Sequence.randomDnaKmer(kmerk)
                        if dna not in tracking:
                            false_positive += (dkbf.contains(dna))
                            count += 1
                    false_positive_rate = false_positive / count
                    print(f"expected: {fp}, actual {false_positive_rate}")
                    self.assertAlmostEqual(0, false_positive_rate - fp, n)

    def test_false_positive_rate1(self):
        for max_capacity in (1000000,):
            for kmerk in (64,):  # ATTENTION: 4^kmerk should be way greater than 10^(n+1) for the test to work
                for bitwidth in (24,):
                    tracking = set()
                    dkbf = DnaKmerBloomFilter(kmerk, max_capacity, bitwidth)
                    fp = dkbf.getFalsePositiveRate()
                    n = round(-math.log10(fp)) if fp > 1e-5 else 5
                    for _ in range(dkbf.getMaxCapacity()):
                        dna = Sequence.randomDnaKmer(kmerk)
                        dkbf.add(dna)
                        tracking.add(dna)

                    false_positive = 0
                    count = 0
                    # ATTENTION: need to have >10^(n+1) rounds to have an accurate estimate
                    while count < 10 ** (n + 2) * 2:
                        dna = Sequence.randomDnaKmer(kmerk)
                        if dna not in tracking:
                            false_positive += (dkbf.contains(dna))
                            count += 1

                    false_positive_rate = false_positive / count
                    print(f"expected: {fp}, actual {false_positive_rate}")
                    self.assertAlmostEqual(0, false_positive_rate - fp, n)

    def test_to_string0(self):
        for n in (2, 3, 5,):
            fp = 1 / (10 ** n)
            for kmerk in (64,):  # ATTENTION: 4^kmerk should be way greater than 10^(n+1) for the test to work
                for bitwidth in (10, 24):

                    tracking = set()
                    dkbf1 = DnaKmerBloomFilter(kmerk, fp, bitwidth)

                    for _ in range(dkbf1.getMaxCapacity()):
                        dna = Sequence.randomDnaKmer(kmerk)
                        dkbf1.add(dna)
                        tracking.add(dna)

                    file = './data/test_to_string0.dkbf'
                    dkbf1.saveToFile(file)

                    dkbf2 = DnaKmerBloomFilter(file)

                    self.assertEqual(dkbf1.getKmerK(), dkbf2.getKmerK())
                    self.assertEqual(dkbf1.getNumOfHashers(), dkbf2.getNumOfHashers())
                    self.assertAlmostEqual(dkbf1.getFalsePositiveRate(), dkbf2.getFalsePositiveRate(), n)
                    for dna in tracking:
                        self.assertEqual(dkbf1.contains(dna), dkbf2.contains(dna))

                    for _ in range(1000):
                        dna = Sequence.randomDnaKmer(kmerk)
                        self.assertEqual(dkbf1.contains(dna), dkbf2.contains(dna))
                        self.assertEqual(dkbf1.add(dna), dkbf2.add(dna))

                    os.remove(file)

    def test_to_string1(self):
        for max_capacity in (1000000,):
            for kmerk in (64,):  # ATTENTION: 4^kmerk should be way greater than 10^(n+1) for the test to work
                for bitwidth in (10, 24):
                    tracking = set()
                    dkbf1 = DnaKmerBloomFilter(kmerk, max_capacity, bitwidth)
                    fp = dkbf1.getFalsePositiveRate()
                    n = round(-math.log10(fp)) if fp > 1e-5 else 5
                    for _ in range(dkbf1.getMaxCapacity()):
                        dna = Sequence.randomDnaKmer(kmerk)
                        dkbf1.add(dna)
                        tracking.add(dna)

                    file = './data/test_to_string0.dkbf'
                    dkbf1.saveToFile(file)

                    dkbf2 = DnaKmerBloomFilter(file)

                    self.assertEqual(dkbf1.getKmerK(), dkbf2.getKmerK())
                    self.assertEqual(dkbf1.getNumOfHashers(), dkbf2.getNumOfHashers())
                    self.assertAlmostEqual(dkbf1.getFalsePositiveRate(), dkbf2.getFalsePositiveRate(), n)
                    for dna in tracking:
                        self.assertEqual(dkbf1.contains(dna), dkbf2.contains(dna))

                    for _ in range(1000):
                        dna = Sequence.randomDnaKmer(kmerk)
                        self.assertEqual(dkbf1.contains(dna), dkbf2.contains(dna))
                        self.assertEqual(dkbf1.add(dna), dkbf2.add(dna))

                    os.remove(file)
