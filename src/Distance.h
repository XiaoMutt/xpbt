//
// Created by Xiao on 3/28/20.
//

#ifndef XPBT_DISTANCE_H
#define XPBT_DISTANCE_H

#include <cstdint>
#include<string>


class Distance {
public:
    static uint32_t hamming(const std::string &a, const std::string &b);
    static uint32_t hamming(const std::string &a, uint32_t aStart,
                            const std::string &b, uint32_t bStart, uint32_t length);

    static uint32_t levenshtein(const std::string &a, const std::string &b);
    static uint32_t levenshtein(const std::string &a, uint32_t aStart, uint32_t aStop,
                                const std::string &b, uint32_t bStart, uint32_t bStop);
};


#endif //XPBT_DISTANCE_H
