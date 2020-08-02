from xpbt.basis import *
from xpbt.algorithms.trees import RedBlackIntervalTreeNode
from xpbt.genomes.coordinates import Zeronate
from enum import IntEnum
import re


class CIGAR(metaclass=Frozen):
    """
    Contains CIGAR CODE and the properties of CIGAR CODE. Contains methods related to CIGAR CODE.
    """

    class CODE(IntEnum):
        # do not change the number
        M = 0
        I = 1
        D = 2
        N = 3
        S = 4
        H = 5
        P = 6
        E = 7
        X = 8
        _ = 9  # not a CIGAR code; reserved; not used

    CONSUMES_QUERY = (True, True, False, False, True, False, False, True, True, False)
    CONSUMES_REFERENCE = (True, False, True, True, False, False, False, True, True, False)

    PATTERN = re.compile(r'(\d+)([MIDNSHPEX])')

    @classmethod
    def cigarString2Tuple(cls, cigar: str):
        return [(int(num), getattr(cls, code)) for num, code in cls.PATTERN.findall(cigar)]


class Cigarette(RedBlackIntervalTreeNode, Immutable):
    def __init__(self, start: int, stop: int, zeronate: Zeronate, cigarCode: CIGAR.CODE):
        """
        A RedBlackIntervalTreeNode representing a single CIGAR CODE unit. It holds the start, stop on the read and
        the aligned coordinates on the reference genome, as well as the CIGAR CODE.

        It can be used in a RedBlackIntervalTree.

        This class objects are immutable at the python level.
        :param start: the start position of the alignment on the read (0-based)
        :param stop: the stop position of the alignment on the read (0-based)
        :param zeronate: the aligned Zeronate on the reference genome.
        :param cigarCode: the cigarCode
        """
        super(Cigarette, self).__init__(start, stop)
        self.zeronate = zeronate
        self.cigarCode = cigarCode

    @property
    def start(self):
        return self.low

    @property
    def stop(self):
        return self.high
