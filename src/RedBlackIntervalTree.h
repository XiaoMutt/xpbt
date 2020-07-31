//
// Created by xiao on 7/14/20.
//

#ifndef XPBT_REDBLACKINTERVALTREE_H
#define XPBT_REDBLACKINTERVALTREE_H


#include "RedBlackIntervalTreeNode.h"

class RedBlackIntervalTree {

public:

    void insert(RedBlackIntervalTreeNode *z);

    void check();

    RedBlackIntervalTree();

//    ~RedBlackIntervalTree();

protected:


    void insertFixUp(RedBlackIntervalTreeNode *z);

    void leftRotate(RedBlackIntervalTreeNode *x);

    void rightRotate(RedBlackIntervalTreeNode *x);

//    void destructorHelper(RedBlackIntervalTreeNode *z);

    void checkHelper(RedBlackIntervalTreeNode *z, int counter, int &numBlackNode, bool parentIsRed);

    RedBlackIntervalTreeNode *root;
};


#endif //XPBT_REDBLACKINTERVALTREE_H
