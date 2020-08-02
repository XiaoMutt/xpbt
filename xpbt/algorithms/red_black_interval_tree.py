"""
RedBlackIntervalTree
"""
import xpbt.core


class RedBlackIntervalTreeNode(xpbt.core.RedBlackIntervalTreeNode):
    pass


class RedBlackIntervalTreeNodeVector(xpbt.core.RedBlackIntervalTreeNodeVector):
    pass


class RedBlackIntervalTree(xpbt.core.RedBlackIntervalTree):
    def __init__(self):
        super(RedBlackIntervalTree, self).__init__()
        # address map serves two purpose:
        # 1. the key holds the physical address of the c++ RedBlackIntervalTreeNode object so after search the
        #    (extended) python node object can be mapped
        # 2. the value holds the reference of the given node in python, so python always take control of the lifetime
        #    of the node object
        # otherwise object pointer passed to c++ will be cleared by python if no python variables hold the object
        self._address_map = dict()

    def insert(self, node: RedBlackIntervalTreeNode):
        self._address_map[node.getAddress()] = node
        super(RedBlackIntervalTree, self).insert(node)

    def search(self, value: int):
        res = RedBlackIntervalTreeNodeVector()
        super(RedBlackIntervalTree, self).search(value, res)
        return [self._address_map[node.getAddress()] for node in res]
