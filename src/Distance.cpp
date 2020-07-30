//
// Created by Xiao on 3/28/20.
//

#include "Distance.h"
#include <stdexcept>

uint32_t Distance::hamming(const std::string &a, const std::string &b) {
    if (a.length() != b.length()) {
        throw std::runtime_error("Hamming distance cannot be applied to strings with unequal lengths.");
    }

    return Distance::hamming(a, 0, b, 0, a.length());
}

uint32_t Distance::hamming(const std::string &a, uint32_t aStart,
                           const std::string &b, uint32_t bStart,
                           uint32_t length) {
    if (a.length() < aStart + length) {
        throw std::runtime_error("The given string a does not have enough length");
    }
    if (b.length() < bStart + length) {
        throw std::runtime_error("The given string b does not have enough length");
    }
    uint32_t res = 0;
    for (uint32_t i = 0; i < length; i++) {
        res += a[aStart + i] != b[bStart + i];
    }
    return res;
}

