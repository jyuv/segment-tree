import pytest
from segment_tree.TreeNode import Segment, TreeNode

LEFT_BASIC = 3
RIGHT_BASIC = 8


@pytest.fixture
def basic_segment():
    return Segment(left=3, right=8)


@pytest.mark.parametrize(
    "left, right",
    [[2, 1], [-1, 5]],
)
def test_invalid_segments(left, right):
    with pytest.raises(ValueError):
        Segment(left, right)


def test_segment_str_repr(basic_segment):
    assert str(basic_segment) == f"[{LEFT_BASIC}, {RIGHT_BASIC}]"
    assert str(basic_segment) == basic_segment.__repr__()


@pytest.mark.parametrize("num", [LEFT_BASIC, LEFT_BASIC + 1, RIGHT_BASIC])
def test_segment_contains_inner_int(basic_segment, num):
    assert num in basic_segment


@pytest.mark.parametrize("num", [LEFT_BASIC - 1, RIGHT_BASIC + 1])
def test_segment_contains_outer_int(basic_segment, num):
    assert num not in basic_segment


def test_tree_node_leaf_chidren():
    cur_node = TreeNode(node_id=8, left=0, right=0)
    assert cur_node.get_left_child() is None
    assert cur_node.get_right_child() is None
