from xpbt.frames import *
from xpbt.core import RedBlackIntervalTreeNode
from xpbt.genome.coordinates import Zeronate
from enum import IntEnum
import re


class CIGAR(metaclass=Frozen):
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
        super(Cigarette, self).__init__(start, stop)
        self.zeronate = zeronate
        self.cigarCode = cigarCode

    @property
    def start(self):
        return self.low

    @property
    def stop(self):
        return self.high
