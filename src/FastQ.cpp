//
// Created by Xiao on 2/26/20.
//

#include "FastQ.h"
#include "Sequence.h"
#include "Distance.h"
#include <stdexcept>
#include <utility>
#include <sstream>

const char FastQ::VALID_BASES[128] =
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'A', 0, 'C', 0, 0, 0,
         'G', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T', 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 'a', 0, 'c', 0, 0, 0, 'g', 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 't', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

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
        length(seq.length()) {
    // ATTENTION: use std::move and do not use reference when constructing FastQ.
    // If use reference the string returned from a local variable will be lost.
    if (this->seq.length() != this->qual.length()) {
        throw std::runtime_error("Sequence and qual have different length");
    }

    for (auto &c:this->seq) {
        if (c > 127 || FastQ::VALID_BASES[c] == 0) {
            throw std::runtime_error("Sequence contains invalid bases. Only ATCGatcg are allowed");
        }
    }

    for (auto &c:this->qual) {
        if (c < 33 || c > 75) {
            throw std::runtime_error("Quality contains invalid Phred score. Only ! to K (inclusive) are allowed");
        }
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

std::string FastQ::str() {
    std::ostringstream stream;
    stream << this->id << '\n' << this->seq << '\n' << this->desc << '\n' << this->qual;
    // return value optimization should occur;
    std::string res = stream.str();
    return res;
}


