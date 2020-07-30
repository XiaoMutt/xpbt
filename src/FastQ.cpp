//
// Created by Xiao on 2/26/20.
//

#include "FastQ.h"
#include "Sequence.h"
#include "Distance.h"
#include <stdexcept>
#include <utility>

FastQ FastQ::reverseComplement(const std::string &newId) {
    FastQ res(newId, Sequence::reverseComplementDna(this->seq), this->desc, Sequence::reverse(this->qual));
    return res;
}

FastQ FastQ::reverseComplement() {
    return this->reverseComplement(this->id);
}

FastQ::FastQ(std::string recordId, std::string recordSeq, std::string recordDesc, std::string recordQual) :
        id(std::move(recordId)), seq(std::move(recordSeq)),
        desc(std::move(recordDesc)), qual(std::move(recordQual)),
        length(seq.length())
        {
    // ATTENTION: use std::move and do not use reference when constructing FastQ.
    // If use reference the string returned from a local variable will be lost.
    if (this->seq.length() != this->qual.length()) {
        throw std::runtime_error("Sequence and qual have different length");
    }
}

FastQ FastQ::reverse(const std::string &newId) {
    FastQ res(newId, Sequence::reverse(this->seq), this->desc, Sequence::reverse(this->qual));
    return res;
}

FastQ FastQ::reverse() {
    return this->reverse(this->id);
}

/**
 * Get a slice (whose id will be the newId) of the FastQ: from a to b-1 (b-1 is included). The original FastQ is unchanged.
 * @param newId the new ID of the sliced
 * @param a
 * @param b
 * @return
 */
FastQ FastQ::operator()(const std::string &newId, uint32_t a, uint32_t b) {
    FastQ res(newId, this->seq.substr(a, b - a), this->desc, this->qual.substr(a, b - a));
    return res;
}

/**
 * Get a slice (whose id will be the newId) of the FastQ: from a to b-1 (b-1 is included). The original FastQ is unchanged.
 * @param newId the new ID of the sliced
 * @param a
 * @param b
 * @return
 */
FastQ FastQ::operator()(uint32_t a, uint32_t b) {
    FastQ res(this->id, this->seq.substr(a, b - a),
            this->desc, this->qual.substr(a, b - a));
    return res;
}

uint32_t FastQ::hammingDistance(const FastQ &compareTo) {
    return Distance::hamming(this->seq, compareTo.seq);
}


