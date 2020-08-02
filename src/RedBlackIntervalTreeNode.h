//
// Created by xiao on 7/30/20.
//

#ifndef XPBT_REDBLACKINTERVALTREENODE_H
#define XPBT_REDBLACKINTERVALTREENODE_H

#include <cstdint>

class RedBlackIntervalTreeNode {
public:
    RedBlackIntervalTreeNode *left;
    RedBlackIntervalTreeNode *right;
    RedBlackIntervalTreeNode *parent;

    bool red;

    int32_t low;
    int32_t high;
    int32_t max;

    explicit RedBlackIntervalTreeNode(int32_t low, int32_t high);

    void updateMax();

    void updateMax(RedBlackIntervalTreeNode *x);

    uint64_t getAddress();
};


#endif //XPBT_REDBLACKINTERVALTREENODE_H
