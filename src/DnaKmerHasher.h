//
// Created by Xiao on 2/8/20.
//

#ifndef XPBT_DNAKMERHASHER_H
#define XPBT_DNAKMERHASHER_H

#include <cstdint>
#include <vector>
#include <string>

class DnaKmerHasher {
private:
    const unsigned int w = 64;
    // ATCG/atcg are set to 0,1,2, and 3, respectively
    const int BASE2BIN[128] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                               0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

    unsigned int *indexPermutations;
    unsigned int w_M;
    unsigned int k; // normalized k min(KmerK, 31)
    unsigned int K; // kmer K

    uint64_t a;
    uint64_t b;

    DnaKmerHasher(unsigned int K, unsigned int M, uint64_t a, uint64_t b, std::vector<unsigned int> &indexPermutations);

public:
    unsigned int getK() const;

    unsigned int getM() const;

    uint64_t getA() const;

    uint64_t getB() const;

    void getIndexPermutations(std::vector<int> &result);

    DnaKmerHasher(unsigned int K, unsigned int M);

    explicit DnaKmerHasher(const std::string &paramStr);

    ~DnaKmerHasher();

    uint64_t hash(const std::string &kmer);

    std::string str();

};

#endif //XPBT_DNAKMERHASHER_H
