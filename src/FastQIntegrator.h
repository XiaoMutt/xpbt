//
// Created by Xiao on 2/26/20.
//

#ifndef XPBT_FASTQINTEGRATOR_H
#define XPBT_FASTQINTEGRATOR_H

#include <vector>
#include <array>
#include "FastQ.h"

class FastQIntegrator {
private:
    // ATCG/atcg are set to 0,1,2, and 3, respectively
    // Do not handle N and other degenerated base
    const char BASE2BIN[128] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    const char BIN2BASE[4] = {'A', 'T', 'C', 'G'};
    std::vector<std::array<double, 4>> positiveProbabilities; // position -> [A, T, C, G ]-> positive probabilities
    std::vector<std::array<double, 4>> negativeProbabilities; // position -> [A, T, C, G ]-> negative probabilities
    std::vector<std::array<uint32_t, 4>> baseCounts; // position-> [A, T, C, G]'s base counts
    uint32_t length = 0;
public:
    /**
     * Add a new FastQ record to the integrator
     * @param read
     * @return
     */
    void add(FastQ &fastq);

    static double phred2p(const char &c);

    static char p2phred(double p);

    static char count2ascii(int c);

    static uint32_t ascii2count(char c);

    FastQ integrate(const std::string &newId);

    static FastQ integratePair(FastQ &fastq1, FastQ &fastq2, const std::string &newId);
};


#endif //XPBT_FASTQINTEGRATOR_H
