//
// Created by xiao on 7/11/20.
//

#include <stdexcept>
#include <iostream>
#include "Zeronate.h"
#include"ValueError.h"
const std::regex Zeronate::PATTERN=std::regex("^(\\w+):(\\d+)(?:[-_ ](\\d+))?,([+-])$");

Zeronate::Zeronate(std::string chr, uint32_t start, uint32_t stop, bool strand) :
        chr(std::move(chr)), start(start), stop(stop), strand(strand) {
    if (start > stop) {
        throw std::runtime_error("Zeronate start cannot be larger than stop.");
    }
}

/**
 *
 * @param coordinate the string that represent the 0-based coordinate of a alignment
 */

Zeronate Zeronate::parse(std::string coordinate) {
    std::smatch match;
    if (std::regex_search(coordinate, match, Zeronate::PATTERN)) {
        if (match[3].str()!=""){
            return Zeronate(match[1].str(),
                            std::stoul(match[2].str()),
                            std::stoul(match[3].str()),
                            match[4].str() == "+");
        }else{
            return Zeronate(match[1].str(),
                            std::stoul(match[2].str()),
                            std::stoul(match[2].str()),
                            match[3].str() == "+");
        }

    } else {
        throw std::runtime_error("Cannot parse string " + coordinate + " to 0-based coordinate.");
    }

}
