//
// Created by xiao on 7/11/20.
//

#ifndef XPBT_ZERONATE_H
#define XPBT_ZERONATE_H


#include <string>
#include<regex>
class Zeronate {
protected:
    static const std::regex PATTERN;
public:
    const std::string chr;
    const uint32_t start;
    const uint32_t stop;
    const bool reverseStrand;

    Zeronate(std::string chr, uint32_t start, uint32_t stop, bool strand);
    std::string str();
    static Zeronate parse(const std::string& coordinate);


};


#endif //XPBT_ZERONATE_H
