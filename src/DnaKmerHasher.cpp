//
// Created by Xiao on 2/8/20.
//

#include "DnaKmerHasher.h"
#include "ValueError.h"
#include <random>
#include <chrono>
#include <algorithm>
#include <sstream>

/**
 * DnaKmerHasher hashes a Dna Kmer to an integer in [0, 2^M-1]
 * @param K the number of nucleotides in the K-mer (the K of the K-mer)
 * @param M M sets the upper bound of the hashed value which is 2^M-1
 */
DnaKmerHasher::DnaKmerHasher(unsigned int K, unsigned int M) {
    if (K < 4 || K > 65535) {
        throw std::runtime_error("K must be in [4, 65535].");
    }

    if (M < 1 || M > 64) {
        throw std::runtime_error("K must be in [1, 64]");
    }

    this->K = K;

    // K = w/2-1, the highest 1 bit will be marked as 1 and used as start marker
    // the lowest 1 bit will be marked as 1 and used as end marker
    this->k = (K > (this->w / 2 - 1) ? (this->w / 2 - 1) : K);
    this->w_M = this->w - M;


    std::default_random_engine generator(std::chrono::system_clock::now().time_since_epoch().count());
    std::uniform_real_distribution<double> distribution(0, 1);

    // a is an odd integer in (0, 2^w)
    this->a = (uint64_t) ((distribution(generator) * ((uint64_t) 1u << (this->w - 1)))) * 2 - 1;
    // b is an integer in [0, 2^(w-M))
    this->b = (uint64_t) (distribution(generator) * ((uint64_t) 1u << this->w_M));

    /* Because the machine word length is w (for 64bit, w is 64), the DNA portion that is longer than
     * w/2 (2bit each nucleotide) has no effect on hashing.
     * To fully randomly hash the Kmer, indexPermutations is used to randomize the input sequence.
     * That is to pick the w/2 length of characters randomly for hashing.
     */
    this->indexPermutations = new unsigned int[this->k];
    unsigned int tmp[K];
    for (unsigned int i = 0; i < K; i++) {
        tmp[i] = i;
    }
    std::shuffle(tmp, tmp + K, generator);
    for (unsigned int i = 0; i < this->k; i++) {
        this->indexPermutations[i] = tmp[i];
    }

}

DnaKmerHasher::DnaKmerHasher(unsigned int K, unsigned int M,
                             uint64_t a, uint64_t b,
                             std::vector<unsigned int> &indexPermutations) {
    this->K = K;
    this->k = (K > (this->w / 2 - 1) ? (this->w / 2 - 1) : K);
    this->w_M = this->w - M;

    this->a = a;
    this->b = b;

    if (indexPermutations.size() != this->k) {
        throw std::runtime_error("The length K does not match the size of the indexPermutations array");
    }

    this->indexPermutations = new unsigned int[this->k];
    for (unsigned int i = 0; i < indexPermutations.size(); i++) {
        this->indexPermutations[i] = indexPermutations[i];
    }

}

DnaKmerHasher::DnaKmerHasher(const std::string &paramStr) {
    int startPos = 0;
    const char sep = ',';
    std::vector<uint64_t> params;
    int endPos;
    while ((endPos = paramStr.find(sep, startPos)) != std::string::npos) {
        std::string s = paramStr.substr(startPos, endPos);
        params.push_back(std::stoull(s));
        startPos = endPos + 1;
    }
    if (startPos != paramStr.length()) {
        params.push_back(std::stoull(paramStr.substr(startPos, paramStr.length())));
    }
    this->K = params[0];
    unsigned int M = params[1];
    this->k = (K > (this->w / 2 - 1) ? (this->w / 2 - 1) : K);
    this->w_M = this->w - M;

    this->a = params[2];
    this->b = params[3];

    if (this->k + 4 != params.size()) {
        throw std::runtime_error("Cannot parse the given string to parameters.");
    }
    this->indexPermutations = new unsigned int[this->k];
    std::copy(params.begin() + 4, params.end(), this->indexPermutations);
}

DnaKmerHasher::~DnaKmerHasher() {
    delete[] this->indexPermutations;
}

/**
 *
 * @param kmer DNA sequence in char array
 * @return a 64bit hash value
 */

uint64_t DnaKmerHasher::hash(const std::string &kmer) {
    if (kmer.length() != this->K) {
        throw std::runtime_error("The length of the given Kmer is different from the preset K.");
    }
    uint64_t tmp = 1;
    for (unsigned int i = 0; i < this->k; i++) {
        tmp = (tmp << 2u) + DnaKmerHasher::BASE2BIN[kmer[this->indexPermutations[i]]];
    }
    tmp = (tmp << 1u) + 1;
    return ((this->a * tmp + this->b) >> (this->w_M));
}


unsigned int DnaKmerHasher::getK() const {
    return this->k;
}

unsigned int DnaKmerHasher::getM() const {
    return this->w - this->w_M;
}

uint64_t DnaKmerHasher::getA() const {
    return this->a;
}

uint64_t DnaKmerHasher::getB() const {
    return this->b;
}

void DnaKmerHasher::getIndexPermutations(std::vector<int> &result) {
    for (unsigned int i = 0; i < this->k; i++) {
        result.push_back(this->indexPermutations[i]);
    }
}

std::string DnaKmerHasher::str() {
    std::ostringstream res;
    char sep = ',';
    res << this->K << sep << (this->w - this->w_M) << sep
        << this->a << sep << this->b;
    for (unsigned int i = 0; i < this->k; i++) {
        res << sep;
        res << this->indexPermutations[i];
    }
    // return value optimization should occur;
    return res.str();
}
