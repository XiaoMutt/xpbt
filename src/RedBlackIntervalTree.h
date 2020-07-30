//
// Created by xiao on 7/14/20.
//

#ifndef XPBT_REDBLACKINTERVALTREE_H
#define XPBT_REDBLACKINTERVALTREE_H

class RedBlackIntervalTree {
protected:
    class Node{
    public:
        Node* left;
        Node* right;
        Node* parent;

        bool red;

        int32_t low;
        int32_t high;
        int32_t max;
        explicit Node(int32_t low, int32_t high);
        void updateMax();
    };

    void insertNode(Node *z);
    void insertFixUp(Node *z);
    void leftRotate(Node *x);
    void rightRotate(Node *x);

    void destructorHelper(Node *z);
    void checkHelper(Node *z, int counter, int &numBlackNode, bool parentIsRed);
    Node* root;
public:
    void insert(int32_t low, int32_t high);
    void check();

    RedBlackIntervalTree();
    ~RedBlackIntervalTree();
};


#endif //XPBT_REDBLACKINTERVALTREE_H
