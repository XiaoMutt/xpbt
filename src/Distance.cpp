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

/**
 * The dynamic programming implementation of calculating Levenshtein distance.
 * Time complexity is O(m*n), and space complexity is O(n) (it uses only one row array of length n),
 * where m=aStop-aStart and n=bStop-bStart.
 * Therefore if there is a large length difference it is better to use the shorter one for string b.
 *
 * @param a string a
 * @param aStart 0-based start position of string a for consideration
 * @param aStop  0-based stop position of string a for consideration
 * @param b string b
 * @param bStart 0-based start position of string b for consideration
 * @param bStop 0-based sop position of string b for consideration
 * @return the levenshtein distance
 */
uint32_t Distance::levenshtein(const std::string &a, uint32_t aStart, uint32_t aStop,
                               const std::string &b, uint32_t bStart, uint32_t bStop) {
    // ATTENTION this function does not check if the params are valid.
    // E.g. it does not check if aStart<aStop and aStop<=a.length();
    uint32_t m = aStop - aStart;
    uint32_t n = bStop - bStart;

    if (m == 0) {
        return n;
    } else if (n == 0) {
        return m;
    }

    // one row array is enough. The leftUpper value in the raw dp array is handled by pre;
    auto *lev = new uint32_t[n];
    uint32_t l, k, pre = 0;

    // use a lambda function to handle dp array query;
    auto getLev = [&](uint32_t i, uint32_t j) {
        if (i == 0) {
            return j;
        } else if (j == 0) {
            return i;
        } else if (i < l && j < k) {
            return pre;
        } else {
            return lev[j - 1];
        }
    };

    for (l = 1; l <= m; l++) {
        for (k = 1; k <= n; k++) {
            uint32_t tmp = lev[k - 1];
            lev[k - 1] = std::min(
                    getLev(l - 1, k - 1) + (a[aStart + l - 1] == b[bStart + k - 1] ? 0 : 1),
                    std::min(getLev(l - 1, k) + 1, getLev(l, k - 1) + 1));
            pre = tmp;
        }
    }

    uint32_t res = lev[n - 1];
    delete[] lev;
    return res;
}

uint32_t Distance::levenshtein(const std::string &a, const std::string &b) {
    return Distance::levenshtein(a, 0, a.length(), b, 0, b.length());
}

