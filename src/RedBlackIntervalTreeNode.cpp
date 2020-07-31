//
// Created by xiao on 7/30/20.
//

#include <algorithm>
#include "RedBlackIntervalTreeNode.h"
RedBlackIntervalTreeNode::RedBlackIntervalTreeNode(int32_t low, int32_t high) {
    this->low = low;
    this->high = high;
    this->max = high;

    this->left = nullptr;
    this->right = nullptr;
    this->parent = nullptr;
    this->red = true;
}

void RedBlackIntervalTreeNode::updateMax() {
    this->max = std::max(this->left == nullptr ? this->high : this->left->max,
                         this->right == nullptr ? this->high : this->right->max
    );
    this->max = std::max(this->max, this->high);
}
