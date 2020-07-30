//
// Created by Xiao on 2/11/20.
//

#include "DnaKmerBloomFilter.h"
#include <cmath>
#include <iostream>
#include <fstream>

unsigned int DnaKmerBloomFilter::getKmerK() const {
    return this->kmerK;
}

double DnaKmerBloomFilter::getFalsePositiveRate() const {
    return this->epsilon;
}

uint64_t DnaKmerBloomFilter::getMaxCapacity() const {
    return this->n;
}

uint64_t DnaKmerBloomFilter::getStorageBitSize() const {
    return this->m;
}

unsigned int DnaKmerBloomFilter::getNumOfHashers() const {
    return this->k;
}

DnaKmerBloomFilter::DnaKmerBloomFilter(unsigned int kmerK, double falsePositiveRate,
                                       unsigned int storageBitWidth) {
    if (storageBitWidth < 10 || storageBitWidth > 36) {
        throw std::runtime_error("StorageBitWidth must be in [10, 36] corresponding to [1KB, 8GB] memory.");
    }
    this->kmerK = kmerK; // kmer length i.e. K
    this->epsilon = falsePositiveRate;
    this->m = ((uint64_t) 1u) << storageBitWidth;
    //ATTENTION: add - to an unsigned int number will result in a very large unsigned int
    this->n = (uint64_t) round(this->m * -log(2) * log(2) / log(this->epsilon));
    this->k = (unsigned int) round(-log2(this->epsilon));

    this->bitArray = new unsigned char[this->m >> 3u]();
    this->dnaKmerHashers = new DnaKmerHasher *[this->k];
    for (unsigned int i = 0; i < this->k; i++) {
        this->dnaKmerHashers[i] = new DnaKmerHasher(this->kmerK, storageBitWidth);
    }
}

DnaKmerBloomFilter::DnaKmerBloomFilter(unsigned int kmerK, uint64_t numOfKmers, unsigned int storageBitWidth) {
    if (storageBitWidth < 10 || storageBitWidth > 32) {
        throw std::runtime_error("StorageBitWidth must be in [10, 32]");
    }
    this->kmerK = kmerK;
    this->m = ((uint64_t) 1u) << storageBitWidth;
    this->n = numOfKmers;
//    this->epsilon = pow(2, this->m * -log(2) / this->n);
    this->epsilon = exp(this->m * -log(2) * log(2) / this->n);
    this->k = (unsigned int) round(-log2(this->epsilon));

    this->bitArray = new unsigned char[this->m >> 3u]();
    this->dnaKmerHashers = new DnaKmerHasher *[this->k];
    for (unsigned int i = 0; i < this->k; i++) {
        this->dnaKmerHashers[i] = new DnaKmerHasher(this->kmerK, storageBitWidth);
    }
}

DnaKmerBloomFilter::~DnaKmerBloomFilter() {
    delete[] this->bitArray;
    for (unsigned int i = 0; i < this->k; i++) {
        delete this->dnaKmerHashers[i];
    }
    delete[] this->dnaKmerHashers;
}

/**
 * Strike the bit at the bitPosition of the bitArray to 1
 * @param bitPosition
 * @return true if it already been struck before, false if not.
 */
bool DnaKmerBloomFilter::strike(uint64_t bitPosition) {
    uint64_t bytePosition = bitPosition >> 3u;
    unsigned char mask = 1u << (bitPosition & 0b111u); //& 111u is mod 8
    bool struck = this->bitArray[bytePosition] & mask;
    this->bitArray[bytePosition] |= mask; // strike

    return struck;
}

/**
 * Peek at bitPosition in the bitArray
 * @param bitPosition
 * @return true if 1 at this position, false is 0 at this position
 */
bool DnaKmerBloomFilter::peek(uint64_t bitPosition) {
    uint64_t bytePosition = bitPosition >> 3u;
    unsigned char mask = 1u << (bitPosition & 0b111u); //& 111u is mod 8
    return this->bitArray[bytePosition] & mask;
}

/**
 * Add DNA to the bloom filter
 * @param dna the DNA sequence
 * @return false if this DNA sequence already exists, i.e. not need to add, else false i.e. added
 */
bool DnaKmerBloomFilter::add(const std::string &dna) {
    bool exist = true;
    for (unsigned int i = 0; i < this->k; i++) {
        uint64_t bitPosition = this->dnaKmerHashers[i]->hash(dna);
        exist &= this->strike(bitPosition);
    }
    return !exist;
}

/**
 * Check if the Bloom Filter contains the DNA array
 * @param dna the DNA sequence
 * @return true if the Bloom Filter contains the DNA sequence, else false
 */
bool DnaKmerBloomFilter::contains(const std::string &dna) {
    for (unsigned int i = 0; i < this->k; i++) {
        uint64_t bitPosition = this->dnaKmerHashers[i]->hash(dna);
        if (!this->peek(bitPosition)) {
            return false;
        };
    }
    return true;
}

/**
 * Save the current Bloom Filter to file
 * @param fileName the file name to be saved in
 */
void DnaKmerBloomFilter::saveToFile(const std::string &fileName) {
    std::ofstream ofs;
    char sep = ',';
    char div = '\n';
    ofs.open(fileName, std::ios::out | std::ios::trunc);
    if (!ofs.is_open()) {
        throw std::runtime_error("Cannot create file " + fileName);
    }
    ofs << this->kmerK << sep << this->m << sep << this->n << sep << this->k << div;
    for (unsigned int i = 0; i < this->k; i++) {
        ofs << this->dnaKmerHashers[i]->toString() << div;
    }
    uint64_t bytesNum = this->m >> 3u;
    for (uint64_t i = 0; i < bytesNum; i++) {
        ofs << this->bitArray[i];
    }
    ofs.close();
}

/**
 * Create Bloom filter from a saved file.
 * @param fileName
 */
DnaKmerBloomFilter::DnaKmerBloomFilter(const std::string &fileName) {
    std::ifstream ifs;
    char sep = ',';
    std::string line;
    ifs.open(fileName, std::ios::in);
    if (!ifs.is_open()) {
        throw std::runtime_error("Cannot open file " + fileName);
    }
    if (!std::getline(ifs, line)) {
        throw std::runtime_error("Cannot load from " + fileName);
    }
    int startPos = 0;
    std::vector<uint64_t> params;
    int endPos;
    while ((endPos = line.find(sep, startPos)) != std::string::npos) {
        std::string s = line.substr(startPos, endPos);
        params.push_back(std::stoull(s));
        startPos = endPos + 1;
    }
    if (startPos != line.length()) {
        params.push_back(std::stoull(line.substr(startPos, line.length())));
    }

    if (params.size() != 4) {
        throw std::runtime_error("Cannot load from " + fileName);
    }

    this->kmerK = params[0];
    this->m = params[1];
    this->n = params[2];
    this->k = params[3];
    this->epsilon = exp(this->m * -log(2) * log(2) / this->n);

    this->dnaKmerHashers = new DnaKmerHasher *[this->k];
    for (unsigned int i = 0; i < this->k; i++) {
        if (!std::getline(ifs, line)) {
            throw std::runtime_error("Cannot load from " + fileName);
        }
        this->dnaKmerHashers[i] = new DnaKmerHasher(line);
    }

    uint64_t bytesNum = this->m >> 3u;
    this->bitArray = new unsigned char[bytesNum];
    for (uint64_t i = 0; i < bytesNum; i++) {
        if (ifs.eof()) {
            throw std::runtime_error("Cannot load from " + fileName);
        }
        this->bitArray[i] = ifs.get();

    }
    ifs.close();
}

