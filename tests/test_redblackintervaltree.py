from xpbt.algorithms.red_black_interval_tree import RedBlackIntervalTree
from xpbt.algorithms.red_black_interval_tree import RedBlackIntervalTreeNode

from unittest import TestCase
from random import randint
from tqdm import tqdm


class TestRedBlackIntervalTree(TestCase):
    def setUp(self) -> None:
        self.tree = RedBlackIntervalTree()
        self.nodes = []
        self.lower_bound = -100000000
        self.upper_bound = 100000000
        self.interval = 1000000
        for _ in range(100000):
            low = randint(-1000000, self.upper_bound - self.interval)
            delta = randint(1, self.interval)
            self.nodes.append((low, low + delta))

        for node in tqdm(self.nodes):
            self.tree.insert(RedBlackIntervalTreeNode(node[0], node[1]))

    def test_insert(self):
        # insertion finished in setUp
        # check tree properties
        self.assertEqual(True, self.tree.check())

    def test_search(self):
        for _ in tqdm(range(1000)):
            value = randint(2 * self.lower_bound, 2 * self.upper_bound)
            natives = sorted([(a, b) for a, b in self.nodes if a <= value < b])
            res = sorted([(node.low, node.high) for node in self.tree.search(value)])
            self.assertEqual(len(natives), len(res))

            for real, test in zip(natives, res):
                self.assertEqual(real, test)
