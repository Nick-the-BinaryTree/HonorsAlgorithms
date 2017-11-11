from datetime import datetime
from random import randint

# Levenshtein Distance and Sample Sort Algorithm Tests
# CSE 3500 Honors Project
# By Nicholas Hartunian

# Introduction:
# I use the term Levenshtein Distance instead of "String Edit
# Distance" because it sounds cooler.
# Levenshtein Distance = # of deletions, insertions, or substitutions
# needed to convert one string into a second

# This is a recursive solution I came up with.
# It's dreadfully slow.
def rec(s1, s2, i = 0, res = 0):
    add = rem = sub = nothing = float("inf")
    if s1 == s2:
        return res
    if i >= len(s2):
        return float("inf")
    if len(s1) < len(s2):
        add = rec(s1[:i]+s2[i]+s1[i:], s2, i+1, res+1)
    elif len(s1) > len(s2):
        rem = rec(s1[:i]+s1[i+1:], s2, i, res+1)
    sub = rec(s1[:i]+s2[i]+s1[i+1:], s2, i+1, res+1)
    nothing = rec(s1, s2, i+1, res)
    return min(add, rem, sub, nothing)

# Wagner-Fischer Dynamic Programming Algorithm (1974)
def wF(s1, s2):
    m = [ [ 0 for _ in range(len(s2)+1) ] for _ in range(len(s1)+1) ]
    for i in range(len(m[0])):
        m[0][i] = i
    for i in range(len(m)):
        m[i][0] = i

    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i+1][j+1] = m[i][j]
            else:
                m[i+1][j+1] = min(
                    m[i][j+1] + 1,  # delete
                    m[i+1][j] + 1,  # insert
                    m[i][j] + 1     # substitute
                )

    return m[len(s1)][len(s2)]

# Also, here is Samplesort by Frazer and McKellar (1970)
# L is the input list to be sorted
# p-1 is the number of splitters to be used for splitting L into buckets
def ss(L, p):
    def bucket_search(bucketKeys, x):
        bot, top = 0, len(bucketKeys)
        while bot < top:
            m = (bot + top)//2
            if m == 0: # bottom-most bucket
                return float("-inf")
            elif bucketKeys[m] > x: # bucket key greater than target
                if bucketKeys[m-1] < x: # target is in bucket index range
                    return m
                top = m # target is below bucket
            elif bucketKeys[m] < x: # target is above bucket
                bot = m+1
            else: # target is bucket index
                return m
        return -1
    if p < 2 or p > len(L) - 1 or len(L) < 2:
        return -1 # Error or poor choice of p
    # Random splitters w/ no dups
    bucketKeys = [float("-inf")] # one of the catch-all buckets, so every element has a place
    bucketKeys.extend(sorted([ L[randint(0, len(L)-1)] for _ in range(p) ])) # extend avoids complexity of creating new list
    bucketKeys.append(float("inf")) # Append unlike add above b/c O(1) vs O(n)
    bucketArrays= [ [] for _ in bucketKeys ]
    # loop over L and place in buckets
    for x in L:
        bucketArrays[bucket_search(bucketKeys, x)].append(x) # 4% runtime
    # sort each bucket
    for A in bucketArrays:
        A.sort()

    res = [ x for A in bucketArrays for x in A ] # neglibible runtime
    return res

# For comparison w/ Python's "Tim Sort"
def normal_sort(L):
    return sorted(L)

# --------------------------------------------------------------
# Tests

def avg1000Lev(args, f):
    for arg in args:
        sum = 0
        print("Argument:", str(arg))
        for _ in range(1000):
            start = datetime.now()
            f(*arg)
            end = datetime.now()
            passed = end - start
            sum += passed.microseconds
        print("Avg runtime:", sum/1000, "microseconds")

def avg10Sort(args, f):
    sum = 0
    for _ in range(10):
        start = datetime.now()
        if type(args) == list:
            f(args)
        else:
            f(*args)
        end = datetime.now()
        passed = end - start
        sum += passed.microseconds
    print("Avg runtime:", sum/10, "microseconds")

def runTests():
    print("**Levenshtein Distance Tests**\n")

    print("*Testing close words*\n")
    pairs = (("ham", "sam"), ("Monday", "Tuesday"), ("North Dakota", "South Dakota"))
    print("-Recursive Function-")
    avg1000Lev(pairs, rec)
    print("-Wagner-Fischer-")
    avg1000Lev(pairs, wF)
    # upper bound known
    print()

    print("*Testing distinct words*\n")
    pairs = (("abc", "efg"), ("a", "aaaaaaaaa"), ("123", "octopus"))
    print("-Recursive Function-")
    avg1000Lev(pairs, rec)
    print("-Wagner-Fischer-")
    avg1000Lev(pairs, wF)

    print("\n**Frazer-McKellar Tests**\n")
    print("*Sorting 1000000 numbers with a small range of values and p=3*\n")
    sequence = [ randint(-20, 20) for _ in range(1000000) ]
    print("-Tim Sort-")
    avg10Sort(sequence, normal_sort)
    print("-Frazer-McKellar-")
    avg10Sort((sequence, 3), ss)
    print()

    print("*Sorting 1000000 numbers with a large range of values and p=3*\n")
    sequence = [ randint(-1000, 1000) for _ in range(1000000) ]
    print("-Tim Sort-")
    avg10Sort(sequence, normal_sort)
    print("-Frazer-McKellar-")
    avg10Sort((sequence, 3), ss)
    print()

    print("*Sorting 1000000 numbers with a small range of values and p=30*\n")
    sequence = [randint(-20, 20) for _ in range(1000000)]
    print("-Tim Sort-")
    avg10Sort(sequence, normal_sort)
    print("-Frazer-McKellar-")
    avg10Sort((sequence, 30), ss)
    print()

    print("*Sorting 1000000 numbers with a large range of values and p=30*\n")
    sequence = [randint(-1000, 1000) for _ in range(1000000)]
    print("-Tim Sort-")
    avg10Sort(sequence, normal_sort)
    print("-Frazer-McKellar-")
    avg10Sort((sequence, 30), ss)
    print()


runTests()


# Sources:
# http://news.mit.edu/2015/algorithm-genome-best-possible-0610