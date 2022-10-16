# Segment Tree

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![LicenseLink](https://img.shields.io/badge/license-MIT-blue.svg)


## Overview
A generic python3 implementation of segment tree and dual segment tree
data structures. The implementation is not only supporting generic inputs but
also supports non-commutative functions and non-commutative composition
of functions.

A segment tree is a data structure useful for storing items in a way
which makes it easy to update individual elements and query for the cumulative
value of applying a certain function to items' segments/intervals.

A dual segment tree is a data structure useful for applying a series of 
functions on all items in a segment/interval individually, while also allowing
to query for specific items.


## API and Time Complexity
Denote `n` as the total number of elements in the array.

#### Segment Tree

| Function | Description | Time Complexity
| ------ |---------|----------:
| `SegmentTree(array, func)` | Builds a segment tree from an `array` with `func` as cumulative function  | O(n)        
| `update(item_id, value)` | Updates an the content of item in `item_id` to `value`| O(log n)
| `query(left, right)` | Returns the cumulative value of applying function to`[left, right]`| O(log n)


#### Dual Segment Tree

| Function | Description | Time Complexity
| ------ |---------|----------:
| `DualSegmentTree(array)` | Builds a dual segment tree from an `array` | O(n)        
| `update(left, right, func)` | Apply function to each of the items in `[left, right]` individually| O(log n) Amortized
| `query(item_id)` | Get the value of item with id=`item_id`| O(log n)

## How to use?

#### Installation

Install using pip from the command line:
`pip install seg-tree`

#### Segment Tree
As seen below you can use arrays of any type and any binary-associative functions
(even non-commutative like chars concatenation)

```python
from segment_tree import SegmentTree

# ints with multiplication function
arr = [1, 2, 3, 4, 5, 6, 7, 8]
st = SegmentTree(arr, func=lambda x, y: x * y)
st.update(3, 9) # now the items' values are [1, 2, 3, 9, 5, 6, 7, 8]
st.query(0, 2) # 6 (= 1 * 2 * 3)
st.query(2, 5) # 810 (= 3 * 9 * 5 * 6)

# chars with concatenation function
arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
st = SegmentTree(arr, func=lambda x, y: x + y)
st.update(3, 'r')  # now the items' values are ['a', 'b', 'c', 'r', 'e', 'f', 'g']
st.query(0, 2)  # "abc"
st.query(2, 5)  # "cref"
```

#### Dual Segment Tree
As seen below you can compose any associative series of unary functions
and use arrays of any type

```python
from segment_tree import DualSegmentTree

# Examole ints array
arr = [1, 2, 3, 4, 5, 6, 7, 8]
st = DualSegmentTree(arr)
st.update(1, 3, lambda x: x + 5) # now the items' values are [1, 7, 8, 9, 5, 6, 7, 8]
st.update(2, 4, lambda x: -x) # now the items' values are [1, 7, -8, -9, -5, 6, 7, 8]
st.query(0) # 1
st.query(3) # -9

# Method 1 - using logical blocks directly
arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
def concat_r(x): return x + 'r'
st = DualSegmentTree(arr)
st.update(3, concat_r)  # now the items' values are ['a', 'b', 'c', 'r', 'e', 'f', 'g']
st.query(0, 2)  # "abc"
st.query(2, 5)  # "cref"
```

## Further Explanation On The Implementation
The segments tree creates an array that simulate a complete binary tree
which its leaves are the items of the input array. This tree is composed of
roughly `2 * n - 1` nodes (in case where n is not power of 2 additional dummy
leaves are added to maintain the complete binary tree structure).

The tree is taking advantage of the non-leaves nodes to store values there
which will help us to perform actions on segments of the items without going
all the way down to all of the items.

### (Regular) Segment Tree

**build** - Fill the leaves with the values from the input array and fill the
rest of the tree applying the provided function on `(left_child, right_child)`.

**update** - We update the relevant leaf and updating its ancestors all the way
up to the root.

**query** - Here the idea is to start at the root of the tree and going down
looking for the `split_node`. The `split_node` is the lowest node in the tree
that all the requested query segment is contained in its dominating segment of leaves.
An example for a `split_node` is shown below, where the blue node is the split
node for the segment marked in black. 
<br>
<p align=center>
<img src="https://github.com/jyuv/segment_tree/blob/main/assets/split_node.png?raw=true">
</p>
<br>

From the `split_node` we are taking 2 tours - one to each of its children.
Taking the left tour we go the the left child of `split_node`. Looking at the
left child of `split_node` we have 3 options:

1. The dominating segment of `split_node.left` is contained within the requested 
query segment. In this case we end the tour with `split_node.left.val`.
<br>
<p align=center>
<img src="https://github.com/jyuv/segment_tree/blob/main/assets/case_contained.png?raw=true">
</p>
<br>

2. The dominating segment of `split_node.left.left` intersects with the requested
query segment. This means that the whole dominating segment of `split_node.left.right`
is contained within the query segment, so all of its leaves decendents are relevant.
Therefore we can remember `split_node.left.right.val` call continue our trip to 
`split_node.left.left` which will result in a value `left_val` and than return
`func(left_val, split_node.left.right.val)` as the left tour's result.
query segment. In this case we end the tour with `split_node.left.val`.
<br>
<p align=center>
<img src="https://github.com/jyuv/segment_tree/blob/main/assets/case_left_intersects.png?raw=true">
</p>
<br>

3. The dominating segment of `split_node.left.left` intersects with the requested
query segment. This means we can continue our tour to `split_node.left.right`
and return the result of it as the result of the whole left tour.
<br>
<p align=center>
<img src="https://github.com/jyuv/segment_tree/blob/main/assets/case_left_not_intersects.png?raw=true">
</p>
<br>

The right tour is done similarly and we return `func(left_tour_result, right_tour_result)` 

This whole method maintains narrow routs, not spreading to many allies, which helps
keep the time complexity low.

### Dual Segment Tree

**build** - Fill the leaves with the values from the input array and fill the
rest of the tree with the identity function.

**query** - start from the relevant leaf and going up to the root composing the
functions on the way one over the the others.

**update** - Works similarly to the SegmentTree's query. There is an additional
tweak here to allow non-commutative series of functions composition (cases where
`f(g(x)) != g(f(x))`). In order to achieve this it does as follows: during the update,
on the way down from the root the non-identity it functions it meets on the way are pushed
downwards to their children. An illustration of this in a simple case is shown below.

<br>
<p align=center>
<img src="https://github.com/jyuv/segment_tree/blob/main/assets/giffy.gif?raw=true">
</p>
<br>
