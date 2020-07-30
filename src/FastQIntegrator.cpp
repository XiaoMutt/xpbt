//
// Created by Xiao on 2/26/20.
//

#include "FastQIntegrator.h"
#include<cmath>
#include<algorithm>
#include<sstream>


void FastQIntegrator::add(FastQ &read) {
    while (this->length < read.length) {
        std::array<uint32_t, 4> intArr = {0, 0, 0, 0};
        std::array<double, 4> dArr1 = {1.0, 1.0, 1.0, 1.0};
        std::array<double, 4> dArr2 = {1.0, 1.0, 1.0, 1.0};
        this->baseCounts.push_back(intArr);
        this->positiveProbabilities.push_back(dArr1);
        this->negativeProbabilities.push_back(dArr2);//not used yet
        this->length++;
    }


    for (uint32_t i = 0; i < read.length; i++) {
        char bin = this->BASE2BIN[read.seq[i]];
        this->baseCounts[i][bin]++;
        double p = FastQIntegrator::phred2p(read.qual[i]);
        double p_1 = 1 - p;
        double p_13 = (1 - p) / 3;
        double p_3 = p / 3;
        for (char j = 0; j < 4; j++) {
            if (j == bin) {
                this->negativeProbabilities[i][j] *= p;
                this->positiveProbabilities[i][j] *= p_1;
            } else {
                this->negativeProbabilities[i][j] *= p_13;
                this->positiveProbabilities[i][j] *= p_3;
            }
        }
    }

}


double FastQIntegrator::phred2p(const char &c) {
    return std::pow(10, (33 - c) / 10.0);
}

/**
 * Convert error probability to Phred character
 * @param p
 * @return
 */
char FastQIntegrator::p2phred(double p) {
    return std::max(std::min((int) (33.0 - std::log10(p) * 10), 75), 33);
}


FastQ FastQIntegrator::integrate(const std::string &newId) {
    std::ostringstream seq;
    std::ostringstream desc;
    std::ostringstream qual;

    for (uint32_t i = 0; i < this->length; i++) {
        unsigned maxBin = 0;
        double maxP = 0;
        double total = 0;
        for (unsigned j = 0; j < 4; j++) {
            if (maxP < this->positiveProbabilities[i][j]) {
                maxP = this->positiveProbabilities[i][j];
                maxBin = j;
            };
            total += this->positiveProbabilities[i][j];
        }

        char base = this->BIN2BASE[maxBin];
        char count = FastQIntegrator::count2ascii(this->baseCounts[i][maxBin]);
        char phred = FastQIntegrator::p2phred(1 - maxP / total);
        seq << base;
        desc << count;
        qual << phred;
    }
    FastQ res(newId, seq.str(), desc.str(), qual.str());
    return res;
}

/**
 * Convert count to ASCII char. Maximum 126 (Counters above 126 will be 126)
 * @param c
 * @return
 */
char FastQIntegrator::count2ascii(int c) {
    return std::min(32 + c, 126);
}

uint32_t FastQIntegrator::ascii2count(char c) {
    return c-32;
}

FastQ FastQIntegrator::integratePair(const std::string &newId, FastQ &record1, FastQ &record2) {
    FastQIntegrator fi{};
    fi.add(record1);
    fi.add(record2);
    return fi.integrate(newId);
}
