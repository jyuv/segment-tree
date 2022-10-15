import pytest
import random
import math
from segment_tree.DualSegmentTree import DualSegmentTree, id_func


def plus_5(x):
    return x + 5


def additive_inverse(x):
    return -x


def ten_times(x):
    return 10 * x


def get_random_interval(arr_len):
    left = random.choice(range(arr_len))
    right = random.choice(range(left, arr_len))
    return left, right


def apply_function_range_array(arr, left, right, func):
    for i in range(left, right + 1):
        arr[i] = func(arr[i])


@pytest.fixture
def small_int_array():
    return [10 * i + i for i in range(1, 9)]


@pytest.mark.parametrize("array_len", [8, 11])
def test_build(array_len):
    arr = [10 * i + i for i in range(1, 1 + array_len)]
    dst = DualSegmentTree(arr)
    num_leaves = 2 ** math.ceil(math.log2(array_len))
    assert dst.arr == [id_func] * (num_leaves - 1) + arr + [id_func] * (
        num_leaves - array_len
    )


def test_query(small_int_array):
    dst = DualSegmentTree(small_int_array)
    dst_array = [dst.query(i) for i in range(len(small_int_array))]
    assert small_int_array == dst_array


def _do_multiple_updates(dst, arr, intervals, ops):
    for i, op in enumerate(ops):
        left, right = intervals[i]
        dst.update(left, right, op)
        apply_function_range_array(arr, left, right, op)


def test_multiple_updates_int(small_int_array):
    ops = [ten_times, plus_5, additive_inverse, additive_inverse, ten_times]
    intervals = [(7, 7), (6, 7), (0, 5), (0, 3), (2, 3)]
    dst = DualSegmentTree(small_int_array)
    _do_multiple_updates(dst, small_int_array, intervals, ops)

    dst_array = [dst.query(i) for i in range(len(small_int_array))]
    assert small_int_array == dst_array


def test_multiple_updates_char():
    def add_a(x):
        return x + "a"

    def add_b(x):
        return x + "b"

    def add_z(x):
        return x + "c"

    ops = [add_a, add_b, add_z, add_a, add_z]
    intervals = [(7, 7), (6, 7), (0, 5), (0, 3), (2, 3)]
    char_arr = ["d", "u", "a", "l", "s", "e", "g", "m"]
    dst = DualSegmentTree(char_arr)
    _do_multiple_updates(dst, char_arr, intervals, ops)

    dst_array = [dst.query(i) for i in range(len(char_arr))]
    assert char_arr == dst_array


@pytest.mark.parametrize("item_id", [7, -1])
def test_invalid_query(item_id):
    arr = [10 * i + i for i in range(1, 6)]
    dst = DualSegmentTree(arr)
    with pytest.raises(ValueError):
        dst.query(item_id)


def test_deal_incummutative_updates(small_int_array):
    dst = DualSegmentTree(small_int_array)

    dst.update(0, 1, plus_5)
    apply_function_range_array(small_int_array, left=0, right=1, func=plus_5)
    dst.update(1, 3, additive_inverse)
    apply_function_range_array(small_int_array, left=1, right=3, func=additive_inverse)

    dst_array = [dst.query(i) for i in range(len(small_int_array))]
    assert small_int_array == dst_array


@pytest.mark.parametrize("left, right", [[1, 7], [0, 6]])
def test_update_split(left, right):
    arr = [10 * i + i for i in range(1, 9)]
    dst = DualSegmentTree(arr)

    dst.update(left, right, plus_5)
    apply_function_range_array(arr, left, right, func=plus_5)

    dst_array = [dst.query(i) for i in range(len(arr))]
    assert arr == dst_array


def test_big_random_case():
    arr_len = 500
    num_intervals = 1000
    ops = [plus_5, ten_times, additive_inverse]
    arr = [random.randint(-10000, 10000) for _ in range(arr_len)]
    dst = DualSegmentTree(arr)
    for _ in range(num_intervals):
        cur_op = ops[random.randint(0, 2)]
        left, right = get_random_interval(arr_len)
        dst.update(left, right, cur_op)
        apply_function_range_array(arr, left, right, cur_op)

    dst_array = [dst.query(i) for i in range(len(arr))]
    assert arr == dst_array
