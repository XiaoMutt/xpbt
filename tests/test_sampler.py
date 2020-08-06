from xpbt.algorithms.sampler import ReservoirSampler
from unittest import TestCase
from collections import Counter
from tqdm import tqdm


class TestUniformSamplingReservoir(TestCase):
    def test_uniform(self):
        counter = Counter()
        n = 20000
        for _ in tqdm(range(n)):
            usr = ReservoirSampler(10)
            usr.sample(range(1000))
            counter += Counter(usr)

        # all numbers should be there
        self.assertEqual(1000, len(counter))

        # uniform distribution
        for i in counter:
            self.assertAlmostEqual(0.01, counter[i] / n, 2)
