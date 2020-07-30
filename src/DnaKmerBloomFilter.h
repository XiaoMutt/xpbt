//
// Created by Xiao on 2/11/20.
//

#ifndef XPBT_DNAKMERBLOOMFILTER_H
#define XPBT_DNAKMERBLOOMFILTER_H

#include <cstdint>
#include "DnaKmerHasher.h"

class DnaKmerBloomFilter {
private:
    unsigned int k; // the number of hash functions
    unsigned int kmerK; // the length of the DNA k-mers
    double epsilon; // the false positive rate
    uint64_t n; // the expected total number of k-mers
    uint64_t m; // the number of storage bits
    unsigned char *bitArray; // bloom filter bitArray
    DnaKmerHasher **dnaKmerHashers; //hashers for bloom filter

    bool peek(uint64_t bitPosition);

    bool strike(uint64_t pos);

public:
    DnaKmerBloomFilter(unsigned int kmerLength, double falsePositiveRate, unsigned int storageBitWidth);

    DnaKmerBloomFilter(unsigned int kmerLength, uint64_t numOfKmers, unsigned int storageBitWidth);

    explicit DnaKmerBloomFilter(const std::string &fileName);

    ~DnaKmerBloomFilter();

    bool add(const std::string &dna);

    bool contains(const std::string &dna);

    unsigned int getKmerK() const;

    double getFalsePositiveRate() const;

    unsigned int getNumOfHashers() const;

    uint64_t getMaxCapacity() const;

    uint64_t getStorageBitSize() const;

    void saveToFile(const std::string &fileName);


};

#endif //XPBT_DNAKMERBLOOMFILTER_H
