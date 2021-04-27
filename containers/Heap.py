
from containers.BinaryTree import BinaryTree, Node


class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        super().__init__()
        if xs is not None:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string
        that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap
        will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether
        insert/delete functions are actually working.
        '''
        if self.root:
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        '''
        ret_l = True
        ret_r = True
        if node is None:
            return True
        if node.left:
            if node.left.value >= node.value and\
                 Heap._is_heap_satisfied(node.left):
                ret_l = True
            else:
                ret_l = False
        if node.right:
            if node.right.value >= node.value and\
                 Heap._is_heap_satisfied(node.right):
                ret_r = True
            else:
                ret_r = False
        return ret_l and ret_r

    def insert(self, value):
        '''
        Inserts value into the heap.

        FIXME:
        Implement this function.

        HINT:
        Create a @staticmethod helper function,
        following the same pattern used in the
        BST and AVLTree insert functions.
        '''
        if self.root:
            size = self.__len__()
            convert_to_binary = size + 1
            binary = '{0:b}'.format(convert_to_binary)
            self.root = Heap._insert(self.root, value, binary[1:])
        else:
            self.root = Node(value)

    @staticmethod
    def _insert(node, value, next_pos_route):
        if next_pos_route[0] == '0':
            if node.left:
                node.left = Heap._insert(node.left, value, next_pos_route[1:])
            else:
                node.left = Node(value)
            if node.value > node.left.value:
                Heap._swap_left(node)
                return node
            else:
                return node
        if next_pos_route[0] == '1':
            if node.right:
                node.right = Heap._insert(node.right, value,
                                          next_pos_route[1:])
            else:
                node.right = Node(value)
            if node.value > node.right.value:
                Heap._swap_right(node)
                return node
            else:
                return node

    @staticmethod
    def _swap_left(node):
        temp = node.value
        node.value = node.left.value
        node.left.value = temp

    @staticmethod
    def _swap_right(node):
        temp = node.value
        node.value = node.right.value
        node.right.value = temp

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        for x in xs:
            self.insert(x)

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        '''
        if self.root:
            return self.root.value
        else:
            return None

    def remove_min(self):
        '''
        Removes the minimum value from the Heap.
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        I created two @staticmethod helper functions:
        _remove_bottom_right and _trickle.
        It's possible to do it with only a single helper
        (or no helper at all),
        but I personally found dividing up the code
        into two made the most sense.
        '''
        if self.root:
            size = self.__len__()
            binary = '{0:b}'.format(size)
            self.root, removed_node_val = Heap._remove_min(self.root,
                                                           binary[1:])
            if self.root:
                self.root.value = removed_node_val
            self.root = Heap._trickle(self.root)

    @staticmethod
    def _remove_min(node, last_node_path):
        last_node = None
        if len(last_node_path) == 0:
            return None, None
        if last_node_path[0] == '0':
            if len(last_node_path) != 1:
                node.left, last_node = Heap._remove_min(node.left,
                                                        last_node_path[1:])
            else:
                last_node = node.left.value
                node.left = None
        if last_node_path[0] == '1':
            if len(last_node_path) != 1:
                node.right, last_node = Heap._remove_min(node.right,
                                                         last_node_path[1:])
            else:
                last_node = node.right.value
                node.right = None
        return node, last_node

    @staticmethod
    def _trickle(node):
        if Heap._is_heap_satisfied(node):
            return node
        else:
            if node.left and node.right:
                if node.left.value < node.right.value:
                    Heap._swap_left(node)
                    node.left = Heap._trickle(node.left)
                else:
                    Heap._swap_right(node)
                    node.right = Heap._trickle(node.right)
            elif node.left and not node.right:
                Heap._swap_left(node)
                node.left = Heap._trickle(node.left)
            else:
                Heap._swap_right(node)
                node.right = Heap._trickle(node.right)
        return node
