//
// Created by xiao on 7/14/20.
//

#include <stdexcept>
#include "RedBlackIntervalTree.h"

RedBlackIntervalTree::Node::Node(int32_t low, int32_t high) {
    this->low = low;
    this->high = high;
    this->max = high;

    this->left = nullptr;
    this->right = nullptr;
    this->parent = nullptr;
    this->red = true;
}

void RedBlackIntervalTree::Node::updateMax() {
    this->max = std::max(this->left == nullptr ? this->high : this->left->max,
                         this->right == nullptr ? this->high : this->right->max
    );
    this->max = std::max(this->max, this->high);
}

void RedBlackIntervalTree::insert(int32_t low, int32_t high) {
    Node *z = new Node(low, high);
    this->insertNode(z);
}

void RedBlackIntervalTree::insertNode(RedBlackIntervalTree::Node *z) {
    Node *y = nullptr; // track the parent node;
    Node *x = this->root; // transverse to find the insertion spot;
    while (x != nullptr) {
        y = x;
        x = (z->low > x->low ? x->right : x->left);
    }

    z->parent = y;
    if (y == nullptr) {
        this->root = z;
    } else {
        if (z->low > y->low) {
            y->right = z;
        } else {
            y->left = z;
        }
        y->updateMax();
    }

    this->insertFixUp(z);


}

void RedBlackIntervalTree::insertFixUp(RedBlackIntervalTree::Node *z) {
    while (z->parent != nullptr && z->parent->red) {
        if (z->parent == z->parent->parent->left) {
            //z's parent is a left node of it's parent
            Node *y = z->parent->parent->right;
            if (y != nullptr && y->red) {
                z->parent->red = false;
                y->red = false;
                z->parent->parent->red = true;
                z = z->parent->parent;
            } else {
                if (z == z->parent->right) {
                    z = z->parent;
                    this->leftRotate(z);
                }
                z->parent->red = false;
                z->parent->parent->red = true;
                this->rightRotate(z->parent->parent);
                // after this the while loop will exit
            }
        } else {
            //z's parent is a left node of it's parent
            Node *y = z->parent->parent->left;
            if (y != nullptr && y->red) {
                z->parent->red = false;
                y->red = false;
                z->parent->parent->red = true;
                z = z->parent->parent;
            } else {
                if (z == z->parent->left) {
                    z = z->parent;
                    this->rightRotate(z);
                }
                z->parent->red = false;
                z->parent->parent->red = true;
                this->leftRotate(z->parent->parent);
                // after this the while loop will exit
            }
        }
    }
    this->root->red = false;
}

RedBlackIntervalTree::RedBlackIntervalTree() {
    this->root = nullptr;
}

void RedBlackIntervalTree::leftRotate(RedBlackIntervalTree::Node *x) {
    Node *y = x->right;// y must exist. otherwise will not call this function

    x->right = y->left;
    if (y->left != nullptr) {
        y->left->parent = x;
    }

    y->parent = x->parent;
    if (x->parent == nullptr) {
        this->root = y;
    } else if (x == x->parent->left) {
        x->parent->left = y;
    } else {
        x->parent->right = y;
    }

    y->left = x;
    x->parent = y;

    x->updateMax();
    y->updateMax();
}

void RedBlackIntervalTree::rightRotate(RedBlackIntervalTree::Node *x) {
    Node *y = x->left;

    x->left = y->right;
    if (y->right != nullptr) {
        y->right->parent = x;
    }

    y->parent = x->parent;
    if (x->parent == nullptr) {
        this->root = y;
    } else if (x == x->parent->left) {
        x->parent->left = y;
    } else {
        x->parent->right = y;
    }

    y->right = x;
    x->parent = y;

    x->updateMax();
    y->updateMax();
}

RedBlackIntervalTree::~RedBlackIntervalTree() {
    this->destructorHelper(this->root);
}

void RedBlackIntervalTree::destructorHelper(RedBlackIntervalTree::Node *z) {
    if (z != nullptr) {
        this->destructorHelper(z->left);
        this->destructorHelper(z->right);
        delete z;
    }
}

void RedBlackIntervalTree::check() {
    int numBlackNode = -1;
    this->checkHelper(this->root, 0, numBlackNode, false);
}

void RedBlackIntervalTree::checkHelper(RedBlackIntervalTree::Node *z,
        int counter, int &numBlackNode, bool parentIsRed) {
    if (z == nullptr) {
        // at leaf
        if (numBlackNode < 0) {
            numBlackNode = counter;
        } else if (numBlackNode != counter) {
            throw std::runtime_error("unequal black nodes count");
        }
    } else {
        if (parentIsRed && z->red) {
            throw std::runtime_error("double red nodes");
        }
        this->checkHelper(z->left, counter + (z->red ? 0 : 1), numBlackNode, z->red);
        this->checkHelper(z->right, counter + (z->red ? 0 : 1), numBlackNode, z->red);
    }
}

