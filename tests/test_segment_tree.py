import math
import random
from functools import reduce
from segment_tree.SegmentTree import SegmentTree
import pytest


def unique_chars(x, y):
    return set(x).union(y)


def addition(x, y):
    return x + y


def query_test_arr(test_arr, left, right, operation, default_val):
    if left == right:
        return test_arr[left]
    return reduce(operation, test_arr[left : right + 1], default_val)


@pytest.fixture
def small_int_array():
    return [10 * i + i for i in range(1, 9)]


@pytest.fixture
def small_char_array():
    return list("segmenttree")


@pytest.mark.parametrize("left, right", [[0, 9], [6, 0]])
def test_invalid_query(left, right):
    arr = [10 * i + i for i in range(1, 8)]
    st = SegmentTree(arr, operation=lambda x, y: x + y, default_val=0)
    with pytest.raises(ValueError):
        st.query(left, right)


def test_query_full_tree(small_int_array):
    right = len(small_int_array) - 1
    op, default_val = addition, 0
    st = SegmentTree(small_int_array, op, default_val)
    assert st.query(0, right) == query_test_arr(
        small_int_array, 0, right, op, default_val
    )


def test_single_item_tree_query():
    arr = [5]
    st = SegmentTree(arr, operation=lambda x, y: x + y, default_val=0)
    assert [st.query(0, 0)] == arr


@pytest.mark.parametrize("op, default_val", [[unique_chars, set()], [addition, ""]])
def test_char_tree_update(small_char_array, op, default_val):
    st = SegmentTree(small_char_array, op, default_val)
    for i in range(len(small_char_array)):
        st.update(i, small_char_array[-1 - i])

    assert st.get_all_items() == small_char_array[::-1]


@pytest.mark.parametrize(
    "op, default_val, left, right",
    [
        [unique_chars, set(), 0, 7],
        [unique_chars, set(), 7, 7],
        [unique_chars, set(), 6, 7],
        [unique_chars, set(), 0, 4],
        [unique_chars, set(), 1, 3],
        [unique_chars, set(), 2, 3],
        [addition, "", 0, 7],
        [addition, "", 7, 7],
        [addition, "", 6, 7],
        [addition, "", 0, 4],
        [addition, "", 1, 3],
        [addition, "", 2, 3],
    ],
)
def test_char_tree_query(small_char_array, op, default_val, left, right):
    st = SegmentTree(small_char_array, op, default_val)
    assert st.query(left, right) == query_test_arr(
        small_char_array, left, right, op, default_val
    )


def test_big_random_case():
    ops = [
        lambda x, y: x + y,
        lambda x, y: x * y,
        lambda x, y: min(x, y),
        lambda x, y: max(x, y),
    ]
    default_vals = [0, 1, math.inf, -math.inf]
    arr_len = 500

    arr = [random.randint(-10000, 10000) for _ in range(arr_len)]

    for _ in range(400):
        cur_op_id = random.randint(0, 2)
        cur_op, cur_default_value = ops[cur_op_id], default_vals[cur_op_id]
        st = SegmentTree(arr, cur_op, cur_default_value)
        left = random.randint(0, arr_len - 1)
        right = random.randint(left, arr_len - 1)
        assert st.query(left, right) == query_test_arr(
            arr, left, right, cur_op, cur_default_value
        )
