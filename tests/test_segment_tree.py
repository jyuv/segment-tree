import random
from functools import reduce
from SegmentTree import SegmentTree, func_with_defaults, SpecialVals
import pytest


def unique_chars(x, y):
    return set(x).union(y)


def addition(x, y):
    return x + y


def query_test_arr(test_arr, left, right, func):
    if left == right:
        return test_arr[left]
    f = func_with_defaults(func)
    return reduce(f, test_arr[left : right + 1], SpecialVals.default)


@pytest.fixture
def small_int_array():
    return [10 * i + i for i in range(1, 9)]


@pytest.fixture
def small_char_array():
    return list("segmenttree")


@pytest.mark.parametrize("left, right", [[0, 9], [6, 0]])
def test_invalid_query(left, right):
    arr = [10 * i + i for i in range(1, 8)]
    st = SegmentTree(arr, func=lambda x, y: x + y)
    with pytest.raises(ValueError):
        st.query(left, right)


def test_query_full_tree(small_int_array):
    right = len(small_int_array) - 1
    st = SegmentTree(small_int_array, func=addition)
    assert st.query(0, right) == query_test_arr(
        small_int_array, 0, right, func=addition
    )


def test_single_item_tree_query():
    arr = [5]
    st = SegmentTree(arr, func=lambda x, y: x + y)
    assert [st.query(0, 0)] == arr


@pytest.mark.parametrize("func", [unique_chars, addition])
def test_char_tree_update(small_char_array, func):
    st = SegmentTree(small_char_array, func)
    for i in range(len(small_char_array)):
        st.update(i, small_char_array[-1 - i])

    assert st.get_all_items() == small_char_array[::-1]


@pytest.mark.parametrize(
    "func, left, right",
    [
        [unique_chars, 0, 7],
        [unique_chars, 7, 7],
        [unique_chars, 6, 7],
        [unique_chars, 0, 4],
        [unique_chars, 1, 3],
        [unique_chars, 2, 3],
        [addition, 0, 7],
        [addition, 7, 7],
        [addition, 6, 7],
        [addition, 0, 4],
        [addition, 1, 3],
        [addition, 2, 3],
    ],
)
def test_char_tree_query(small_char_array, func, left, right):
    st = SegmentTree(small_char_array, func)
    assert st.query(left, right) == query_test_arr(small_char_array, left, right, func)


def test_big_random_case():
    funcs = [
        lambda x, y: x + y,
        lambda x, y: x * y,
        lambda x, y: min(x, y),
        lambda x, y: max(x, y),
    ]
    arr_len = 500

    arr = [random.randint(-10000, 10000) for _ in range(arr_len)]

    for _ in range(400):
        f = funcs[random.randint(0, len(funcs) - 1)]
        st = SegmentTree(arr, func=f)
        left = random.randint(0, arr_len - 1)
        right = random.randint(left, arr_len - 1)
        assert st.query(left, right) == query_test_arr(arr, left, right, func=f)
