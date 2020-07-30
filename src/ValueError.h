//
// Created by Xiao on 4/4/20.
//

#ifndef XPBT_VALUEERROR_H
#define XPBT_VALUEERROR_H


#include <exception>
#include <string>


class ValueError : public std::exception {
private:
    const std::string &error;
public:
    explicit ValueError(const std::string &error) : error(error) {}

    const char *what() const noexcept override {
        return this->error.c_str();
    }
};

#endif //XPBT_VALUEERROR_H
