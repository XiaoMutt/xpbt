//
// Created by Xiao on 2/27/20.
//

#include "Sequence.h"
#include<algorithm>
#include <stdexcept>
#include <random>
#include <chrono>

#include <sstream>

const char Sequence::DNA_COMPLEMENT_TABLE[128] =
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '-', '.', 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'T', 'V', 'G', 'H', 0, 0,
         'C', 'D', 0, 0, 'M', 0, 'K', 'N', 0, 0, 0, 'Y', 'W', 'A', 0, 'B', 'S', 0,
         'R', 0, 0, 0, 0, 0, 0, 0, 't', 'v', 'g', 'h', 0, 0, 'c', 'd', 0, 0, 'm', 0,
         'k', 'n', 0, 0, 0, 'y', 'w', 'a', 0, 'b', 's', 0, 'r', 0, 0, 0, 0, 0, 0};

const char Sequence::RNA_COMPLEMENT_TABLE[128] =
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '-', '.', 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'U', 'V', 'G', 'H', 0, 0,
         'C', 'D', 0, 0, 'M', 0, 'K', 'N', 0, 0, 0, 'Y', 'W', 0, 'A', 'B', 'S', 0,
         'R', 0, 0, 0, 0, 0, 0, 0, 'u', 'v', 'g', 'h', 0, 0, 'c', 'd', 0, 0, 'm', 0,
         'k', 'n', 0, 0, 0, 'y', 'w', 0, 'a', 'b', 's', 0, 'r', 0, 0, 0, 0, 0, 0};

const char Sequence::DNA_BASES[4] = {'A', 'T', 'C', 'G'};
const char Sequence::RNA_BASES[4] = {'A', 'U', 'C', 'G'};

const std::function<unsigned()> Sequence::dnaRnaBaseRandomIndex = std::bind(
        std::uniform_int_distribution<unsigned>(0, 3),
        std::default_random_engine(std::chrono::system_clock::now().time_since_epoch().count()));

std::string Sequence::reverse(const std::string &seq) {
    std::string res(seq);
    std::reverse(res.begin(), res.end());
    return res;
}

std::string Sequence::complement(const std::string &seq, const char *alphabetComplementTable) {
    std::string res(seq);
    for (char &re : res) {
        re = alphabetComplementTable[re];
        if (re==0){
            throw std::runtime_error("The given sequence contains invalid base");
        }
    }
    return res;
}

std::string Sequence::complementDna(const std::string &dna) {
    return Sequence::complement(dna, Sequence::DNA_COMPLEMENT_TABLE);
}

std::string Sequence::complementRna(const std::string &rna) {
    return Sequence::complement(rna, Sequence::RNA_COMPLEMENT_TABLE);
}

std::string Sequence::reverseComplement(const std::string &seq, const char *alphabetComplementTable) {
    std::string res = Sequence::reverse(seq);
    for (char &re : res) {
        re = alphabetComplementTable[re];
    }
    return res;
}


std::string Sequence::reverseComplementDna(const std::string &dna) {
    return Sequence::reverseComplement(dna, Sequence::DNA_COMPLEMENT_TABLE);
}

std::string Sequence::reverseComplementRna(const std::string &rna) {
    return Sequence::reverseComplement(rna, Sequence::RNA_COMPLEMENT_TABLE);
}


std::string Sequence::randomKmer(uint32_t k, const char *alphabet) {
    std::ostringstream oss;
    for (unsigned i = 0; i < k; i++) {
        oss << alphabet[Sequence::dnaRnaBaseRandomIndex()];
    }
    return oss.str();
}

std::string Sequence::randomDnaKmer(uint32_t k) {
    return Sequence::randomKmer(k, Sequence::DNA_BASES);
}

std::string Sequence::randomRnaKmer(uint32_t k) {
    return Sequence::randomKmer(k, Sequence::RNA_BASES);
}

