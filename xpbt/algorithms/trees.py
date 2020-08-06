"""
RedBlackIntervalTree
"""
import xpbt.core


class RedBlackIntervalTreeNode(xpbt.core.RedBlackIntervalTreeNode):
    """
    RedBlackIntervalTreeNode
    """
    pass


class RedBlackIntervalTreeNodeVector(xpbt.core.RedBlackIntervalTreeNodeVector):
    """
    A Helper Class for transfer std::vector results from C++. It is a vector holds RedBlackIntervalTreeNode*
    """
    pass


class RedBlackIntervalTree(xpbt.core.RedBlackIntervalTree):
    def __init__(self):
        """
        A RedBlackIntervalTree.
        The RedBlackTree is a self-balanced binary search tree structure. This implementation consulted the book:
        * Introduction to Algorithms *.

        This tree stores the RedBlackIntervalTreeNode which has 3 values: low, high, and max. They are all integers.
        Low and high forms the interval [low, high), and max is to facilitate the fast binary search for intervals
        containing a target value. The max variable is handled automatically and is not exposed to the end users.

        The RedBlackIntervalTree he has the following rules:
        * Left child's low < parent Node's low.
        * Right child's low>= parent Node's low.
        * Parent's max>=all children's max.
        """
        super(RedBlackIntervalTree, self).__init__()

        # address map serves two purpose:
        # 1. the key holds the physical address of the c++ RedBlackIntervalTreeNode object so after search the
        #    (extended) python node object can be mapped
        # 2. the value holds the reference of the given node in python, so python always take control of the lifetime
        #    of the node object
        # otherwise object pointer passed to c++ will be cleared by python if no python variables hold the object
        self.__address_map = dict()

    def insert(self, node: RedBlackIntervalTreeNode):
        """
        Insert a node to the tree.
        :param node: A RedBlackIntervalTreeNode or its subclass object.
        :return: None
        """
        self.__address_map[node.getAddress()] = node
        super(RedBlackIntervalTree, self).insert(node)

    def search(self, value: int) -> list:
        """
        Search the Nodes that contains the value.
        :param value: the value
        :return: a list of nodes whose intervals containing the value.
        """
        result = RedBlackIntervalTreeNodeVector()
        super(RedBlackIntervalTree, self).search(value, result)
        return [self.__address_map[node.getAddress()] for node in result]
