#coding: utf-8

import time


# 简单选择法, O(n^2), O(1), 稳定
def sort_number0(number):
    n = len(number)
    for i in range(n-1):
        max_num = 0
        for j in range(n-i):
            if number[j] > number[max_num]:
                max_num = j
        number[n-i-1], number[max_num] = number[max_num], number[n-i-1]
    return number


# 有问题 -> 简单选择法（改进）, O(n^2), O(1), 稳定
# [1,2,0]结果是[2, 0, 1]
def sort_number0_1(number):
    n = len(number)
    for i in range(n/2):
        max_num, min_num = i, i
        for j in range(i, n-i):
            if number[j] > number[max_num]:
                max_num = j
            if number[j] < number[min_num]:
                min_num = j
        number[n-i-1], number[max_num] = number[max_num], number[n-i-1]
        number[i], number[min_num] = number[min_num], number[i]
    return number


# 冒泡法, O(n^2), O(1), 稳定
def sort_number1(number):
    n = len(number)
    for i in range(n):
        for j in range(n-i-1):
            if number[j] > number[j+1]:
                number[j], number[j+1] = number[j+1], number[j]
    return number


# 冒泡法（改进）, O(n^2), O(1), 稳定
def sort_number1_1(number):
    n = len(number)
    for i in range(n):
        change = False
        for j in range(n-i-1):
            if number[j] > number[j+1]:
                number[j], number[j+1] = number[j+1], number[j]
                change = True
        if not change:
            break
    return number


time_s = time.time()
for i in range(100000):
    result = sort_number0_1([1,2,0])
print(result)
time_e = time.time()
print("%s" % (time_e - time_s))
