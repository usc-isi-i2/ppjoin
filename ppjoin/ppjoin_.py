"""
PPJoin algorithm

Paper:
Xiao, Chuan, et al.
"Efficient similarity joins for near-duplicate detection."
ACM Transactions on Database Systems (TODS) 36.3 (2011): 1-41.

Updated by GreatYYX https://github.com/greatyyx
Fixed several severe bugs and enhanced usability.

Original copyright info:
Copyright 2012 Thomas Hunger. All rights reserved.
Licenced under the 2-clause BSD license ("Simplified BSD License" or "FreeBSD License")
Code taken from https://github.com/teh/ppjoin
"""
import collections
import math
from itertools import groupby, product
from typing import List, Tuple, Set


def ceil(x):
    return math.ceil(float('%.10f' % x))


def prefix_length(s, threshold):
    return len(s) - ceil(threshold*len(s)) + 1


def overlap_constraint(len_s1, len_s2, threshold):
    return ceil(threshold / (1.0 + threshold) * (len_s1 + len_s2))


def jaccard(a, b):
    if not isinstance(a, set):
        a = set(a)
    if not isinstance(b, set):
        b = set(b)
    return 1.0 * len(a & b) / len(a | b)


def compare(records, t, order_map):
    ii = collections.defaultdict(set)  # inverted index
    cp = set()  # candidate pairs

    if t == 0:
        return set(filter(lambda x: x[0] != x[1], product(range(len(records)), range(len(records)))))

    for xr_index, xr in enumerate(records):
        if not xr:
            continue
        xp = prefix_length(xr, t)
        xp = min(xp, len(xr))
        overlap_by_yr = collections.defaultdict(int)
        for i in range(xp):
            xr_element = xr[i]
            for yr_index, j in ii[xr_element]:
                yr = records[yr_index]
                if len(yr) < t * len(xr):
                    continue
                alpha = overlap_constraint(len(xr), len(yr), t)
                upper_bound = 1 + min(len(xr) - i, len(yr) - j)
                # count how many items of yr overlap xr:
                if overlap_by_yr[yr_index] + upper_bound >= alpha:
                    overlap_by_yr[yr_index] += 1
                else:
                    overlap_by_yr[yr_index] = 0

            ii[xr_element].add((xr_index, i))

        # check overlap in suffixes
        for yr_index, overlap in overlap_by_yr.items():
            yr = records[yr_index]
            yp = prefix_length(yr, t)
            yp = min(yp, len(yr))
            wx = xr[xp - 1]
            wy = yr[yp - 1]
            alpha = overlap_constraint(len(xr), len(yr), t)
            rest = 0

            if order_map[wx] < order_map[wy]:
                ubound = overlap + len(xr) - xp
                if ubound >= alpha:
                    rest = len(set(yr[overlap:]) & set(xr[xp:]))
            else:
                ubound = overlap + len(yr) - yp
                if ubound >= alpha:
                    rest = len(set(xr[overlap:]) & set(yr[yp:]))

            overlap += rest
            if overlap >= alpha:
                cp.add((xr_index, yr_index))

    return cp


def preprocess(records):
    # records = list(map(lambda x: normalize_words(x), records))

    # sort records
    argsort = sorted(range(len(records)), key=lambda x: len(records[x]))
    records.sort(key=len)

    # sort tokens
    elements = list(y for r in records for y in r)
    order_map = dict(
        (el, i)
        for i, (el, count) in enumerate(sorted(collections.Counter(elements).items(), key=lambda x: (x[1], x[0])))
    )

    records_sorted = [sorted(x, key=lambda x: order_map[x]) for x in records]

    return records_sorted, argsort, order_map


# def normalize_words(words):
#     """
#     Normalize same words in document to unique words tokens as described in
#     the paper. Use "@#" to split the word and index of the word.
#     """
#     words.sort()
#     tmp = [list(g) for k, g in groupby(words)]
#
#     wwi = map(lambda ws: [x + "@#" + str(i) for i, x in enumerate(ws)], tmp)
#     return [w for same_words in wwi for w in same_words]


def qgram_tokenizer(x, _q, keep_start_and_end=False):
    if keep_start_and_end:
        x = '_{}_'.format(x.lower())
    if len(x) < _q:
        return [x]
    return [x[i:i+_q] for i in range(len(x)-_q+1)]


def whitespace_tokenizer(x):
    return list(filter(lambda t: t is not None, x.split(' ')))


def join(datasets: List[List[List[str]]], t: float = 0) -> Set[Tuple[Tuple]]:

    ret = set()
    if not datasets:
        return ret

    dataset = []
    dataset_id_offset = [0]
    for d in datasets:
        dataset += d
        dataset_id_offset.append(len(d) + dataset_id_offset[-1])
    if len(dataset_id_offset) > 1:
        dataset_id_offset = dataset_id_offset[:-1]
 
    records_sorted, original_order, order_map = preprocess(dataset)
    result = compare(records_sorted, t, order_map)
    for r in result:
        r1id, r2id = r[0], r[1]
        r1id, r2id = original_order[r1id], original_order[r2id]
        if r1id == r2id:
            continue

        # r1id should <= r2id
        if r1id > r2id:
            r1id, r2id = r2id, r1id
        # find which original datasets the rids belong to
        ds1_offset = next(x for x in reversed(dataset_id_offset) if x <= r1id)
        ds2_offset = next(x for x in reversed(dataset_id_offset) if x <= r2id)
        # both are from one source (except only one dataset is provided)
        if len(dataset_id_offset) > 1 and ds1_offset == ds2_offset:
            continue

        ret.add( (
            (dataset_id_offset.index(ds1_offset), r1id-ds1_offset), 
            (dataset_id_offset.index(ds2_offset), r2id-ds2_offset)) )

    return ret