from xpbt.basis import *
from xpbt.algorithms.trees import RedBlackIntervalTreeNode
from xpbt.genomes.coordinates import Zeronate
from enum import IntEnum
import re
import typing as tp


class CIGAR(metaclass=Frozen):
    """
    Contains CIGAR CODE and the properties of CIGAR CODE. Contains methods related to CIGAR CODE.
    """

    class CODE(IntEnum):
        # Do not change the numbers: defined in samtools manual: https://samtools.github.io/hts-specs/SAMv1.pdf:
        # * “Consumes query” and “consumes reference” indicate whether the CIGAR operation causes the alignment to step
        # along the query sequence and the reference sequence respectively.
        # * H can only be present as the first and/or last operation.
        # * S may only have H operations between them and the ends of the CIGAR string.
        # * For mRNA-to-genome alignment, an N operation represents an intron.  For other types of alignments,
        # the interpretation of N is not defined.
        # * Sum of lengths of the M/I/S/=/X operations shall equal the length of SEQ (the query).

        M = 0  # alignment match (can be a sequence match or mismatch)
        I = 1  # insertion to the reference
        D = 2  # deletion from the reference
        N = 3  # skipped region from the reference
        S = 4  # soft clipping (clipped sequences present inSEQ)
        H = 5  # hard clipping (clipped sequences NOT present inSEQ)
        P = 6  # padding (silent deletion from padded reference)
        E = 7  # sequence match (this is = in sam format)
        X = 8  # sequence mismatch

        U = 9  # not a CIGAR code; reserved; not used
        _ = -1  # not a CIGAR code; reserved; not used

    CONSUMES_QUERY = (True, True, False, False, True, False, False, True, True, False, False)
    CONSUMES_REFER = (True, False, True, True, False, False, False, True, True, False, False)
    CONSUMES_BOTH2 = (True, False, False, False, False, False, False, True, True, False, False)
    ALIGN_RELEVANT = (True, True, True, True, True, False, False, True, True, False, False)

    PATTERN = re.compile(r'(\d+)([MIDNSHPEX])')

    @classmethod
    def cigarString2Tuple(cls, cigarString: str):
        """
        Convert cigarString to cigar tuple pairs (CIGAR.CODE:int, length:int)
        :param cigarString: the cigarString to be converted
        :return: a tuple of cigar tuple pairs
        """
        return tuple((getattr(cls, code_char), int(length))
                     for length, code_char in cls.PATTERN.findall(cigarString))


class Cigarette(RedBlackIntervalTreeNode, Immutable):
    def __init__(self, start: int, stop: int, zeronate: Zeronate, cigarCode: CIGAR.CODE):
        """
        A RedBlackIntervalTreeNode representing a single alignment-relevant CIGAR CODE unit
        . It holds the start, stop on the read and
        the aligned coordinates on the reference genome, as well as the CIGAR CODE.

        It can be used in a RedBlackIntervalTree.

        This class objects are immutable at the python level.
        :param start: the start position of the alignment on the query sequence (0-based)
        :param stop: the stop position of the alignment on the query sequence (0-based)
        :param zeronate: the aligned Zeronate on the reference genome.
        :param cigarCode: the cigarCode
        """

        super(Cigarette, self).__init__(start, stop)
        self.zeronate = zeronate
        self.cigarCode = cigarCode

    def map(self, zeroBasedPositionOnQuery: int) -> tp.Optional[Zeronate]:
        """
        Map a base of the query to the aligned reference position.
        The query position should be 0-based. 0-based coordinates perfectly represents the boundaries
        The returned Zeronate's start and stop always enclose the mapped base between start and stop.
        This is to avoid DNA reverse strand coordinate confusions (the string slicing go backwards).

        For example, in following figure query will return:
        * position 9 of query1: Zeronate("some_chr", 10, 11 ,"+") instead of Zeronate("some_chr", 10, 10, "+")
        * position 0 of query2: Zeronate("some_chr", 10, 11, "-") instead of Zeronate("some_chr", 11, 11, "-")

                         0 =========?>   query1 aligned to some_chr:1_11,+
        forward strand  0 ----------*--------->20
        reverse stand   0<----------*--------- 20
                          <=========? 0  query2 aligned to some_chr:1_11,-

        :param zeroBasedPositionOnQuery: 0-based query position
        :return: Zeronate of the the aligned reference position or None if not aligned on reference
        """
        if CIGAR.CONSUMES_BOTH2[self.cigarCode]:
            if self.zeronate.reverseStrand:
                mapped = self.zeronate.stop - (zeroBasedPositionOnQuery - self.start)
                return Zeronate(self.zeronate.chr, mapped - 1, mapped, self.zeronate.reverseStrand)
            else:
                mapped = self.zeronate.start + (zeroBasedPositionOnQuery - self.start)
                return Zeronate(self.zeronate.chr, mapped, mapped + 1, self.zeronate.reverseStrand)

        return None

    @property
    def start(self):
        return self.low

    @property
    def stop(self):
        return self.high
