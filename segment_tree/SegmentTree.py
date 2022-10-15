import math
from typing import List, Callable, TypeVar, Union
from segment_tree.TreeNode import TreeNode, Segment

T = TypeVar("T")  # input type
DV = TypeVar("DV")  # type of default value

TDV = Union[T, DV]


class SegmentTree:
    """
    A generic data structure used for storing information about segments/intervals.
    Builds in O(n) and allows for querying for interval and updating a single item in O(logn) each.
    The query supports all binary-associative operations (it doesn't have to be commutative).
    """

    def __init__(
        self, items: List[T], operation: Callable[[TDV, TDV], T], default_val: DV
    ) -> None:
        self.default_val = default_val
        self.operation = operation
        self.num_items = len(items)

        self.num_leaves = 2 ** math.ceil(math.log2(self.num_items))
        self._first_leaf_loc = self.num_leaves - 1

        # empty initialize
        self.arr = [self.default_val] * (2 * self.num_leaves - 1)

        # put values on the leaves
        for i, item in enumerate(items):
            self.arr[self._first_leaf_loc + i] = item

        # update parents
        for i in range(self._first_leaf_loc - 1, -1, -1):
            self._local_parent_update(i)

    def _local_parent_update(self, parent_id: int) -> None:
        left_child_id = 2 * parent_id + 1
        right_child_id = 2 * parent_id + 2
        self.arr[parent_id] = self.operation(
            self.arr[left_child_id], self.arr[right_child_id]
        )

    def _get_split_point(self, desired_segment: Segment) -> TreeNode:
        cur_node = TreeNode(node_id=0, left=0, right=self.num_leaves - 1)

        while not cur_node.is_leaf():  # not leaf
            left_child = cur_node.get_left_child()
            right_child = cur_node.get_right_child()

            if left_child.is_containing_segment(desired_segment):
                cur_node = left_child

            elif right_child.is_containing_segment(desired_segment):
                cur_node = right_child

            else:
                # we've reached to the split point
                break
        return cur_node

    def _query_left_to_split(self, desired_segment: Segment, cur_node: TreeNode) -> T:
        if cur_node.is_segment_contained_by(desired_segment):
            return self.arr[cur_node.node_id]

        else:
            right_val = self._query_left_to_split(
                desired_segment, cur_node.get_right_child()
            )

            left_val = self.default_val
            left_child = cur_node.get_left_child()

            if left_child.is_segment_intersects(desired_segment):
                left_val = self._query_left_to_split(desired_segment, left_child)

            return self.operation(left_val, right_val)

    def query_right_to_split(self, desired_segment: Segment, cur_node: TreeNode) -> T:
        if cur_node.is_segment_contained_by(desired_segment):
            return self.arr[cur_node.node_id]

        else:
            left_val = self.query_right_to_split(
                desired_segment, cur_node.get_left_child()
            )

            right_child = cur_node.get_right_child()
            right_val = self.default_val

            if right_child.is_segment_intersects(desired_segment):
                right_val = self.query_right_to_split(desired_segment, right_child)

            return self.operation(left_val, right_val)

    def query(self, left: int, right: int) -> T:
        """
        Get the Value of the class's operation over the segment [left, right]
        """
        if right > self.num_items or left > right:
            raise ValueError(f"Invalid segment for query [{left}, {right}]")

        desired_segment = Segment(left, right)
        split_node = self._get_split_point(desired_segment)

        if split_node.is_leaf() or split_node.is_segment_exactly(desired_segment):
            return self.arr[split_node.node_id]

        left_val = self._query_left_to_split(
            desired_segment, split_node.get_left_child()
        )
        right_val = self.query_right_to_split(
            desired_segment, split_node.get_right_child()
        )

        return self.operation(left_val, right_val)

    def update(self, item_id: int, new_val: T) -> None:
        """
        Updates the value of specific item with a new value
        """
        prev_id = self._first_leaf_loc + item_id
        self.arr[prev_id] = new_val
        parent_id = (prev_id - 1) // 2

        while parent_id >= 0:
            self._local_parent_update(parent_id)
            parent_id = (parent_id - 1) // 2

    def get_all_items(self) -> List[T]:
        return self.arr[self._first_leaf_loc : self._first_leaf_loc + self.num_items]
