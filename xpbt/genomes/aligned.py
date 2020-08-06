from xpbt.algorithms.trees import RedBlackIntervalTree
from xpbt.genomes.cigar import Cigarette, CIGAR
from xpbt.genomes.coordinates import Zeronate
from xpbt.basis import Immutable


class AlignedSequenceRedBlackIntervalTree(RedBlackIntervalTree):
    """
    Storing all the aligned segments (down to the single CIGAR unit).
    This is backed up by a RedBlackIntervalTree for fast interval search.
    """

    def map(self, zeroBasedPosition: int):
        return [cigarette.map(zeroBasedPosition) for cigarette in self.search(zeroBasedPosition)]


class AlignedRead(AlignedSequenceRedBlackIntervalTree, Immutable):
    def __init__(self, readId: str):
        super(AlignedRead, self).__init__()
        self.readId = readId

    def insert(self,
               readStart: int,
               referenceId: str,
               referenceStart: int,
               referenceStop: int,
               referenceReverseStrand: bool,
               cigarTuplePairs: tuple) -> None:
        """
        Insert an aligned segment into the AlignedSequenceRedBlackIntervalTree.
        :param readStart: 0-based position of the start position on the read (query) of the aligned segment
        :param referenceId: the id of the aligned reference, e.g. chr1.
        :param referenceStart: the 0-based start position of the aligned segment on the reference
        :param referenceStop: the 0-based stop position of the aligned segment on the reference
        :param cigarTuplePairs: the cigar tuple pairs (cigarCode, length)
        :return: None
        """
        current_query_pos = readStart
        current_refer_pos = referenceStop if referenceReverseStrand else referenceStart
        flag = -1 if referenceReverseStrand else 1

        for code, length in cigarTuplePairs[::flag]:
            next_query_pos = current_query_pos + length * CIGAR.CONSUMES_QUERY[code]
            next_refer_pos = current_refer_pos + length * CIGAR.CONSUMES_REFER[code] * flag
            if CIGAR.CONSUMES_QUERY[code]:
                if referenceReverseStrand:
                    zeronate = Zeronate(referenceId,
                                        next_refer_pos, current_refer_pos,
                                        True)
                else:
                    zeronate = Zeronate(referenceId,
                                        current_refer_pos, next_refer_pos,
                                        False)
                super(AlignedRead, self).insert(Cigarette(current_query_pos, next_query_pos,
                                                          zeronate,
                                                          code))
            current_query_pos = next_query_pos
            current_refer_pos = next_refer_pos


class AlignedReference(AlignedSequenceRedBlackIntervalTree, Immutable):
    def __init__(self, referenceId: str):
        super(AlignedReference, self).__init__()
        self.referenceId = referenceId

    def insert(self,
               readId: str,
               readStart: int,
               referenceStart: int,
               referenceStop: int,
               referenceReverseStrand: bool,
               cigarTuplePairs: tuple) -> None:
        """
        Insert an aligned segment into the AlignedSequenceRedBlackIntervalTree.
        :param readId: the id of the read
        :param readStart: 0-based position of the start position on the read (query) of the aligned segment
        :param referenceStart: the 0-based start position of the aligned segment on the reference
        :param referenceStop: the 0-based stop position of the aligned segment on the reference
        :param cigarTuplePairs: the cigar tuple pairs (cigarCode, length)
        :return: None
        """
        current_query_pos = readStart
        current_refer_pos = referenceStop if referenceReverseStrand else referenceStart
        flag = -1 if referenceReverseStrand else 1

        for code, length in cigarTuplePairs:
            next_query_pos = current_query_pos + length * CIGAR.CONSUMES_QUERY[code]
            next_refer_pos = current_refer_pos + length * CIGAR.CONSUMES_REFER[code] * flag

            zeronate = Zeronate(readId, current_query_pos, next_query_pos, referenceReverseStrand)
            if CIGAR.CONSUMES_REFER[code]:
                if referenceReverseStrand:
                    super(AlignedReference, self).insert(
                        Cigarette(next_refer_pos, current_refer_pos, zeronate, code))
                else:
                    super(AlignedReference, self).insert(
                        Cigarette(current_refer_pos, next_refer_pos, zeronate, code))
            current_query_pos = next_query_pos
            current_refer_pos = next_refer_pos
