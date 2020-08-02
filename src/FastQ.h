//
// Created by Xiao on 2/26/20.
//

#ifndef XPBT_FASTQ_H
#define XPBT_FASTQ_H

#include<string>

class FastQ {
protected:
    static const char VALID_BASES[128];
public:
    const std::string id;
    const std::string seq;
    const std::string qual;
    const std::string desc;
    const uint32_t length;


    FastQ(std::string recordId, std::string recordSeq, std::string recordDesc, std::string recordQual);

    FastQ reverseComplement(const std::string &newId);

    FastQ reverseComplement();

    FastQ reverse(const std::string &newId);

    FastQ reverse();

    FastQ operator()(const std::string &newId, uint32_t a, uint32_t b);

    FastQ operator()(uint32_t a, uint32_t b);

    uint32_t hammingDistance(const FastQ &compareTo);

    std::string str();

};

#endif //XPBT_FASTQ_H
