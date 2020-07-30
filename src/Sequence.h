//
// Created by Xiao on 2/27/20.
//

#ifndef XPBT_SEQUENCE_H
#define XPBT_SEQUENCE_H


#include <string>
#include <functional>

class Sequence {
private:
    static const char DNA_COMPLEMENT_TABLE[128];
    static const char RNA_COMPLEMENT_TABLE[128];
    static const char DNA_BASES[4];
    static const char RNA_BASES[4];
    static const std::function<unsigned()> dnaRnaBaseRandomIndex;

    static std::string complement(const std::string &seq, const char *alphabetComplementTable);

    static std::string reverseComplement(const std::string &seq, const char *alphabetComplementTable);

    static std::string randomKmer(uint32_t k, const char *bases);

public:

    static std::string reverse(const std::string &seq);

    static std::string complementDna(const std::string &dna);

    static std::string complementRna(const std::string &rna);

    static std::string reverseComplementDna(const std::string &dna);

    static std::string reverseComplementRna(const std::string &rna);

    static std::string randomDnaKmer(uint32_t k);

    static std::string randomRnaKmer(uint32_t k);

};


#endif //XPBT_SEQUENCE_H
