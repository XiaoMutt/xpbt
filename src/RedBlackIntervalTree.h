//
// Created by xiao on 7/14/20.
//

#ifndef XPBT_REDBLACKINTERVALTREE_H
#define XPBT_REDBLACKINTERVALTREE_H


#include <vector>
#include "RedBlackIntervalTreeNode.h"

class RedBlackIntervalTree {

public:

    bool check();

    void insert(RedBlackIntervalTreeNode *z);

    void search(int32_t value, std::vector<RedBlackIntervalTreeNode *> &result);

    RedBlackIntervalTree();

//    ~RedBlackIntervalTree();

protected:

    void insertFixUp(RedBlackIntervalTreeNode *z);

    void leftRotate(RedBlackIntervalTreeNode *x);

    void rightRotate(RedBlackIntervalTreeNode *x);

//    void destructorHelper(RedBlackIntervalTreeNode *z);
    void search(RedBlackIntervalTreeNode *node, int32_t value, std::vector<RedBlackIntervalTreeNode *> &result);

    void check(RedBlackIntervalTreeNode *z,
               uint32_t counter, uint32_t &numBlackNode,
               int32_t parentMax,
               bool parentIsRed);

    RedBlackIntervalTreeNode *root;

};


#endif //XPBT_REDBLACKINTERVALTREE_H
