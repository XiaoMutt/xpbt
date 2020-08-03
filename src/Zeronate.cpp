//
// Created by xiao on 7/11/20.
//

#include <stdexcept>
#include <iostream>
#include "Zeronate.h"

const std::regex Zeronate::PATTERN = std::regex(R"(^(\w+):(\d+)(?:[_ ](\d+))?(?:,([+-]))?$)");

Zeronate::Zeronate(std::string chr, uint32_t start, uint32_t stop, bool strand) :
        chr(std::move(chr)), start(start), stop(stop), reverseStrand(strand) {
    if (this->chr.empty()) {
        throw std::runtime_error("chr cannot be empty");
    }

    if (this->start > this->stop) {
        throw std::runtime_error("start cannot be larger than stop.");
    }
}

/**
 *
 * @param coordinate the string that represent the 0-based coordinate of a alignment
 */

Zeronate Zeronate::parse(const std::string &coordinate) {
    std::smatch match;
    if (std::regex_search(coordinate, match, Zeronate::PATTERN)) {
        if (!match[3].str().empty()) {
            return Zeronate(match[1].str(),
                            std::stoul(match[2].str()),
                            std::stoul(match[3].str()),
                            match[4].str() == "-");
        } else {
            return Zeronate(match[1].str(),
                            std::stoul(match[2].str()),
                            std::stoul(match[2].str()),
                            match[4].str() == "-");
        }

    }
    throw std::runtime_error("Cannot parse string " + coordinate + " to 0-based coordinate.");


}

std::string Zeronate::str() {
    std::ostringstream stream;
    stream << this->chr << ':' << this->start << '_' << this->stop << ',' << (this->reverseStrand ? '-' : '+');
    // return value optimization should occur;
    std::string res = stream.str();
    return res;
}
