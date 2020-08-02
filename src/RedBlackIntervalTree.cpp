//
// Created by xiao on 7/14/20.
//

#include <stdexcept>
#include "RedBlackIntervalTree.h"


void RedBlackIntervalTree::insert(RedBlackIntervalTreeNode *z) {
    RedBlackIntervalTreeNode *y = nullptr; // track the parent node;
    RedBlackIntervalTreeNode *x = this->root; // transverse to find the leaf insertion spot;
    while (x != nullptr) {
        y = x;
        y->updateMax(z);
        x = (z->low < x->low ? x->left : x->right);
    }

    z->parent = y;
    if (y == nullptr) {
        this->root = z;
    } else {
        // < put on left; >= put on right; this way it matchs the [low, high) interval search
        if (z->low < y->low) {
            y->left = z;
        } else {
            y->right = z;
        }
    }

    this->insertFixUp(z);


}

void RedBlackIntervalTree::insertFixUp(RedBlackIntervalTreeNode *z) {
    while (z->parent != nullptr && z->parent->red) {
        if (z->parent == z->parent->parent->left) {
            //z's parent is a left node of it's parent
            RedBlackIntervalTreeNode *y = z->parent->parent->right;
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
            RedBlackIntervalTreeNode *y = z->parent->parent->left;
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

void RedBlackIntervalTree::leftRotate(RedBlackIntervalTreeNode *x) {
    RedBlackIntervalTreeNode *y = x->right;// y must exist. otherwise will not call this function

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

    x->updateMax(); //must update x's first because x is the child
    y->updateMax();
}

void RedBlackIntervalTree::rightRotate(RedBlackIntervalTreeNode *x) {
    RedBlackIntervalTreeNode *y = x->left;

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

/**
 * For debugging and testing purpose. Check whether the tree violates the RedBlackTree properties
 * @return true if all good; throw runtime errors if errors found.
 */
bool RedBlackIntervalTree::check() {
    uint32_t numBlackNode = 0;
    if (this->root != nullptr && this->root->red) {
        throw std::runtime_error("root node is red");
    }
    this->check(this->root, 0, numBlackNode, this->root->max, false);
    return true;
}

void RedBlackIntervalTree::check(RedBlackIntervalTreeNode *z,
                                 uint32_t counter, uint32_t &numBlackNode,
                                 int32_t parentMax,
                                 bool parentIsRed) {
    if (z == nullptr) {
        // at leaf
        if (numBlackNode == 0) {
            numBlackNode = counter;
        } else if (numBlackNode != counter) {
            throw std::runtime_error("unequal black nodes count");
        }
    } else {
        if (parentIsRed && z->red) {
            throw std::runtime_error("double red nodes");
        }
        if (parentMax < z->max) {
            throw std::runtime_error("parent max < currentmax");
        }
        this->check(z->left, counter + (z->red ? 0 : 1), numBlackNode, z->max, z->red);
        this->check(z->right, counter + (z->red ? 0 : 1), numBlackNode, z->max, z->red);
    }
}

void RedBlackIntervalTree::search(RedBlackIntervalTreeNode *node, int32_t value,
                                  std::vector<RedBlackIntervalTreeNode *> &result) {
    if (node != nullptr) {
        if (value < node->low) {
            // value < node->max; no need to check
            this->search(node->left, value, result);
        } else {
            if (value < node->max) {
                if (value < node->high) {
                    result.push_back(node);
                }
                this->search(node->left, value, result);
                this->search(node->right, value, result);
            }

        }
    }
}

void RedBlackIntervalTree::search(int32_t value, std::vector<RedBlackIntervalTreeNode *> &result) {
    this->search(this->root, value, result);
}

//RedBlackIntervalTree::~RedBlackIntervalTree() {
//    this->destructorHelper(this->root);
//}
//
//void RedBlackIntervalTree::destructorHelper(RedBlackIntervalTreeNode *z) {
//    if (z != nullptr) {
//        this->destructorHelper(z->left);
//        this->destructorHelper(z->right);
//        delete z;
//    }
//}