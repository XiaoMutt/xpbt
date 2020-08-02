//
// Created by Xiao on 2/26/20.
//

#ifndef XPBT_READLAZYSTITCHER_H
#define XPBT_READLAZYSTITCHER_H

#include "FastQ.h"
#include <exception>

class ReadLazyStitcher {
private:


    unsigned minNumOfOverlappingBases;
    unsigned maxHammingDistance;
    bool allow3PrimeOverhang;

public:

    ReadLazyStitcher(unsigned minNumOfOverlappingBases, unsigned maxHammingDistance, bool allow3PrimeOverhang);

    FastQ stitch(FastQ &read1, FastQ &read2, const std::string &newId) const;
};

#endif //XPBT_READLAZYSTITCHER_H
