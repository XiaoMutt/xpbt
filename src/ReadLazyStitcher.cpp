//
// Created by Xiao on 2/26/20.
//

#include <sstream>
#include "ReadLazyStitcher.h"
#include "FastQIntegrator.h"
#include "ValueError.h"
#include "Distance.h"
#include <stdexcept>

ReadLazyStitcher::ReadLazyStitcher(unsigned int minNumOfOverlappingBases, unsigned maxHammingDistance,
                                   bool allow3PrimeOverhang) {
    if (minNumOfOverlappingBases < 8) {
        throw std::runtime_error("minNumOfOverlappingBases must be above 8");
    }

    if (maxHammingDistance > minNumOfOverlappingBases) {
        throw std::runtime_error("minNumOfOverlappingBases is larger than minNumOfOverlappingBases");
    }
    this->minNumOfOverlappingBases = minNumOfOverlappingBases;
    this->maxHammingDistance = maxHammingDistance;
    this->allow3PrimeOverhang = allow3PrimeOverhang;
}

/**
    Stitch Read1 and Read2 based on their sequence.
    It is a lazy stitching, which means as long as read1 and read2 have a common region of length>=minNumOfOverlappingBases
    they are stitched together. Here is how it works:
    - starts from minNumOfOverlappingBases
    - sliding inwards
    - if the hamming distance of the overlapping part <= maxHammingDistance, the overlapping part is stitched
    (highest qual base is used when there is a discrepancy)

                 read1Begin                          read1End
                     |     minNumOfOverlappingBases     |
    read1 ---------------------------------------------->
                     <---------------------------------------------- read2
                     |                                  |
                 read2End                          read2Begin
 * @param r1
 * @param r2
 * @return the stitched FastQ or an empty FastQ if fail to stitch
 */

FastQ ReadLazyStitcher::stitch(FastQ &read1, FastQ &read2, const std::string &newId) const {
    int32_t overlappingRange = (this->allow3PrimeOverhang ?
                                -(read1.length + read2.length - this->minNumOfOverlappingBases) :
                                -(read1.length < read2.length ? read1.length : read2.length));

    int32_t read1Begin, read1End, read2Begin, read2End;
    FastQ read2rc = read2.reverseComplement();
    for (int32_t i = -this->minNumOfOverlappingBases; i > overlappingRange; i--) {
        if (i < -read1.length) {
            read2End = read2.length + read1.length + i;
            read1Begin = 0;
        } else {
            read2End = read2.length;
            read1Begin = read1.length + i;
        }

        if (i < -read2.length) {
            read2Begin = 0;
            read1End = read1.length + read2.length + i;
        } else {
            read2Begin = read2.length + i;
            read1End = read1.length;
        }

        // convert read2 begin and end position to its reverse complement sequence position
        uint32_t read2rcBegin = read2.length - read2End;
        uint32_t read2rcEnd = read2.length - read2Begin;

        if (Distance::hamming(read1.seq, read1Begin,
                              read2rc.seq, read2rcBegin,
                              read1End - read1Begin) <= maxHammingDistance) {
            std::ostringstream seq;
            std::ostringstream qual;

            FastQ leftPart = (read1Begin == 0 ?
                              read2rc(0, read2rcBegin) : read1(0, read1Begin)
            );
            seq << leftPart.seq;
            qual << leftPart.qual;

            // merge read1Overlap and read2Overlap
            FastQ read1Overlap = read1(read1Begin, read1End);
            FastQ read2rcOverlap = read2rc(read2rcBegin, read2rcEnd);
            FastQ overlap = FastQIntegrator::integratePair(read1Overlap, read2rcOverlap, "overlap");
            seq << overlap.seq;
            qual << overlap.qual;

            FastQ rightPart = (read2Begin == 0 ?
                               read1(read1End, read1.length) : read2rc(read2rcEnd, read2.length));
            seq << rightPart.seq;
            qual << rightPart.qual;
            FastQ res(newId, seq.str(), "stitched", qual.str());
            return res;
        }
    }
    throw ValueError("Unable to stitch");
}



