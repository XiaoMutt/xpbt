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

    class OPERATION(IntEnum):
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
        S = 4  # soft clipping (clipped sequences present in SEQ)
        H = 5  # hard clipping (clipped sequences NOT present in SEQ)
        P = 6  # padding (silent deletion from padded reference)
        E = 7  # sequence match (this is = in sam format)
        X = 8  # sequence mismatch

        U = 9  # not a CIGAR code; reserved; not used
        _ = -1  # not a CIGAR code; reserved; not used

        # CIGAR string is aligner dependent. For H and S, aligner may do additional things to choose H or S
        # If you use bwa-mem, here is from BWA's github (https://github.com/lh3/bwa):
        # * 2. Why does a read appear multiple times in the output SAM?
        # * BWA-SW and BWA-MEM perform local alignments. If there is a translocation, a gene fusion or a long deletion,
        # a read bridging the break point may have two hits, occupying two lines in the SAM output.
        # With the default setting of BWA-MEM, one and only one line is primary and is soft clipped;
        # other lines are tagged with 0x800 SAM flag (supplementary alignment) and are hard clipped.

        # With these being said, a primary and a supplementary alignment can share overlapping regions on the query.
        # If there are enough overlapping bases, the additional alignment might be labeled as a secondary alignment.

    CONSUMES_QUERY = (True, True, False, False, True, False, False, True, True, False, False)
    CONSUMES_REFER = (True, False, True, True, False, False, False, True, True, False, False)
    CONSUMES_BOTH = (True, False, False, False, False, False, False, True, True, False, False)
    CONSUME_EITHER = (True, True, True, True, True, False, False, True, True, False, False)

    PATTERN = re.compile(r'(\d+)([MIDNSHPEX])')

    @classmethod
    def cigarString2TuplePairs(cls, cigarString: str):
        """
        Convert cigarString to cigar tuple pairs (CIGAR.OPERATION, length).
        ATTENTION: this function does not check whether the cigar string is valid or not. For example, it does not
        raise exceptions when an H is between two M.
        :param cigarString: the cigarString to be converted
        :return: a tuple of cigar tuple pairs
        """
        return tuple((cls.OPERATION[code_char], int(length))
                     for length, code_char in cls.PATTERN.findall(cigarString))


class Cigarette(RedBlackIntervalTreeNode, Immutable):
    def __init__(self, start: int, stop: int, zeronate: Zeronate, cigarOperation: CIGAR.OPERATION):
        """
        A RedBlackIntervalTreeNode representing a single CIGAR OPERATION unit.
        * start and stop are the 0-based positions on the source sequence (start must < stop)
        * zeronate is the the Zeronate on the target sequence where the [start,stop) source sequence aligned.
        * cigarOperation: is the CIGAR operation code.

        NOTE: Cigarette can represent the mapping of read to reference genome and reference genome to read.
        * For read to reference: the read (aka query) is the source. The start and stop are positions on
        the read, and Zeronate is the aligned coordinate on the reference genome. The CIGAR operation should be the
        ones that consumes the query.
        * For reference to read: the reference genome is the source, The start and stop are positions on the genome,
        and Zeronate is the aligned coordinate on the read (aka query). The CIGAR operation should be the ones that
        consumes the reference. Notice since the aligned genome can be on the reverse strand, you can convert this
        alignment to the forward strand and zeronate represent an imaginary reverse strand of the read.

        This class objects are immutable at the python level.
        :param start: the start position of the alignment on the source sequence (0-based)
        :param stop: the stop position of the alignment on the source sequence (0-based)
        :param zeronate: the aligned Zeronate on the target sequence.
        :param cigarOperation: the cigar operation code
        """

        super(Cigarette, self).__init__(start, stop)
        self.zeronate = zeronate
        self.cigarOperation = cigarOperation

    def map(self, zeroBasedPosition: int) -> tp.Optional[Zeronate]:
        """
        Map a base of the source sequence to the aligned target base.
        The query position should be 0-based, indicating the base [position, position+1).
        The returned Zeronate's start and stop always enclose the mapped base between start and stop.
        This is to avoid DNA reverse strand coordinate confusions (the string slicing go backwards).

        For example, in following figure query will return:
        * position 9 of query1: Zeronate("some_chr", 10, 11 ,"+") instead of Zeronate("some_chr", 10, 10, "+")
        * position 0 of query2: Zeronate("some_chr", 10, 11, "-") instead of Zeronate("some_chr", 11, 11, "-")

                         0 =========?>   query1 aligned to some_chr:1_11,+
        forward strand  0 ----------*--------->20
        reverse stand   0<----------*--------- 20
                          <=========? 0  query2 aligned to some_chr:1_11,-

        :param zeroBasedPosition: 0-based query position
        :return: Zeronate of the the aligned reference position or None if not aligned on reference
        """
        if CIGAR.CONSUMES_BOTH[self.cigarOperation]:
            if self.zeronate.reverseStrand:
                mapped = self.zeronate.stop - (zeroBasedPosition - self.start)
                return Zeronate(self.zeronate.chr, mapped - 1, mapped, self.zeronate.reverseStrand)
            else:
                mapped = self.zeronate.start + (zeroBasedPosition - self.start)
                return Zeronate(self.zeronate.chr, mapped, mapped + 1, self.zeronate.reverseStrand)

        return None

    @property
    def start(self):
        return self.low

    @property
    def stop(self):
        return self.high
