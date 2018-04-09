#coding:utf-8

import sys
import time
import random


# binggui, O(nlogn), O(n)
def msort(seq):
    if len(seq) <= 1:
        return seq
    mid = len(seq) / 2
    left = msort(seq[:mid])
    right = msort(seq[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[i:]
    return result

# dui, O(nlogn), O(1)
# def sift_down(arr, start, end):
#     root = start
#     while True:
#         child = 2 * root + 1
#         if child > end:
#             break
#
#         if child + 1 <= end and arr[child] < arr[child + 1]:
#             child += 1
#
#         if arr[root] < arr[child]:
#             arr[root], arr[child] = arr[child], arr[root]
#             root = child
#         else:
#             break
#
#
# def msort(arr):
#     first = len(arr) // 2 - 1
#     for start in range(first, -1, -1):
#         sift_down(arr, start, len(arr) - 1)
#     for end in range(len(arr) -1, 0, -1):
#         arr[0], arr[end] = arr[end], arr[0]
#         sift_down(arr, 0, end - 1)
#     return arr


# maopao1, O(n^2), O(1)
# def msort(mlist):
#     n = len(mlist)
#     for i in range(n-1):
#         change = False
#         for j in range(n-i-1):
#             if mlist[j] < mlist[j+1]:
#                 mlist[j], mlist[j+1] = mlist[j+1], mlist[j]
#                 change = True
#         if not change:
#             break
#     return mlist

# maopao2, O(n^2), O(1)
# def msort(mlist):
#     n = len(mlist)
#     for i in range(n-1):
#         change = False
#         idx = n-i-1
#         for j in range(idx):
#             if mlist[j] < mlist[j+1]:
#                 mlist[j], mlist[j+1] = mlist[j+1], mlist[j]
#                 change = True
#                 idx = j
#         if not change:
#             break
#     return mlist

# xuanze, O(n^2), O(1)
# def msort(mlist):
#     n = len(mlist)
#     for i in range(n-1):
#         max_idx = 0
#         for j in range(n-i):
#             if mlist[j] > mlist[max_idx]:
#                 max_idx = j
#         mlist[n-i-1], mlist[max_idx] = mlist[max_idx], mlist[n-i-1]
#     return mlist

mlist = random.sample(range(10000),10000)

ts = time.time()
result = msort(mlist)
te = time.time()
print(result)
print(te-ts)
