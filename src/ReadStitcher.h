//
// Created by Xiao on 2/26/20.
//

#ifndef XPBT_READSTITCHER_H
#define XPBT_READSTITCHER_H

#include "FastQ.h"
#include <exception>

class ReadStitcher {
private:


    unsigned minNumOfOverlappingBases;
    unsigned maxHammingDistance;
    bool allow3PrimeOverhang;

public:
    ReadStitcher();

    explicit ReadStitcher(unsigned int minNumOfOverlappingBases);

    ReadStitcher(unsigned int minNumOfOverlappingBases, unsigned maxHammingDistance);

    ReadStitcher(unsigned minNumOfOverlappingBases, unsigned maxHammingDistance, bool allow3PrimeOverhang);

    FastQ lazyStitch(const std::string &newId, FastQ &read1, FastQ &read2) const;
};

class UnableToStitchException : public std::exception {
    const char *what() const noexcept override {
        return "ValueError: unable to stitch";
    }
};

#endif //XPBT_READSTITCHER_H
