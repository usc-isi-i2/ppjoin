"""
P4Join algorithm

Paper:
Sehili, Ziad, et al.
"Privacy preserving record linkage with PPJoin."
Datenbanksysteme für Business, Technologie und Web (BTW 2015) (2015).


Implemented by GreatYYX https://github.com/greatyyx
"""
import collections
from itertools import product
from functools import reduce
from typing import List, Tuple, Set
import hashlib
import hmac
from ppjoin.ppjoin_ import ceil


def list_to_vec(l):
    vec = 0
    for idx, e in enumerate(reversed(l)):
        vec |= (e << idx)
    return vec


def vec_to_list(vec, l_len):
    l = [0] * l_len
    idx = l_len - 1
    while vec != 0 and l_len >= 0:
        l[idx] = vec & 1
        vec >>= 1; idx -= 1
    return l


def str_to_byte(s):
    return s.encode('utf-8')


def byte_to_str(b):
    return b.decode('utf-8')


def all_sb_idx(b, vec_len):
    """
    Get set-bit indices
    """
    l = []
    for idx in reversed(range(vec_len)):
        if b & 1:
            l.append(idx)
        b >>= 1
    return list(reversed(l))


def set_bit(b, vec_len, idx):
    return b | 1 << (vec_len - 1 - idx)


def base_hash(key, msg, method):
    return int(hmac.new(key=key, msg=msg, digestmod=method).hexdigest(), 16)


def encode_record(record: List[List[str]], hmac_key: str, vec_len: int, k: int = 2) -> List[int]:
    hmac_key = str_to_byte(hmac_key)
    vec = 0
    for t in record:
        t = str_to_byte(t)
        for i in range(1, k+1):
            set_bit_idx = (
                base_hash(key=hmac_key, msg=t, method=hashlib.sha1) +
                base_hash(key=hmac_key, msg=t, method=hashlib.md5) * i
            ) % vec_len
            vec = set_bit(vec, vec_len, set_bit_idx)
    return vec


def prefix(vec, vec_len, t):
    sb_idx = all_sb_idx(vec, vec_len)
    # prefix_length = ceil((1 - t) * len(sb_idx)) + 1
    prefix_length = len(sb_idx) - ceil(t * len(sb_idx)) + 1
    prefix_length = min(prefix_length, len(sb_idx))
    prefix_sb_idx = sb_idx[:prefix_length]
    prefix_vec = map(lambda x: set_bit(0, vec_len, x), prefix_sb_idx[:])
    return reduce(lambda x, y: x | y, prefix_vec)


def compare(records, vec_len, t, order_map):
    cp = set()
    lmap = collections.defaultdict(set)

    if t == 0:
        return set(filter(lambda x: x[0] != x[1], product(range(len(records)), range(len(records)))))

    for xr_idx, xr in enumerate(records):
        xl = len(all_sb_idx(xr, vec_len))
        for el in list(lmap.keys()):

            if el < xl * t:  # length filter
                del lmap[el]
                continue

            for (yr_idx, yr) in lmap[el]:
                xp = prefix(xr, vec_len, t)
                yp = prefix(yr, vec_len, t)
                if xp & yp == 0:  # prefix filter
                    continue

                yl = len(all_sb_idx(yr, vec_len))
                if positional_filter(xp, yp, xl, yl, t, vec_len):
                    continue

                score = jaccard(xr, yr, vec_len)
                if score >= t:
                    cp.add((xr_idx, yr_idx))

        lmap[xl].add((xr_idx, xr))

    return cp


def positional_filter(xp, yp, xl, yl, t, vec_len):
    overlap = len(all_sb_idx(xp & yp, vec_len))
    sb_idx1 = all_sb_idx(xp, vec_len)
    sb_idx2 = all_sb_idx(yp, vec_len)
    p1, p2 = sb_idx1[-1], sb_idx2[-1]
    diff1, diff2 = 0, 0

    if p1 > p2:
        diff1 = len([sb for sb in sb_idx1 if sb > p2])
    else:
        diff2 = len([sb for sb in sb_idx2 if sb > p1])

    rest = min(xl - len(sb_idx1) + diff1, yl - len(sb_idx2) + diff2)

    return overlap + rest < ceil((xl + yl) * t / (t + 1))


def preprocess(records, vec_len):
    # get all set bits index of records
    records_sb_idx = []
    for vec in records:
        records_sb_idx.append(all_sb_idx(vec, vec_len))

    # get frequency order of index of all set bits
    elements = [e for r in records_sb_idx for e in r]
    order_map = dict(
        (el, i)
        for i, (el, count) in enumerate(sorted(collections.Counter(elements).items(), key=lambda x: (x[1], x[0])))
    )  # (element, order)

    # reorder set bit of all records
    reordered_records = []
    for vec_sb_idx in records_sb_idx:
        vec = 0
        for set_bit_idx in sorted(vec_sb_idx, key=lambda x: order_map[x]):
            vec = set_bit(vec, vec_len, set_bit_idx)
        reordered_records.append(vec)

    # sort reordered records based on cardinality
    argsort = sorted(range(len(reordered_records)), key=lambda i: len(all_sb_idx(reordered_records[i], vec_len)))
    reordered_records.sort(key=lambda r: len(all_sb_idx(r, vec_len)))

    return reordered_records, argsort, order_map


def jaccard(n1, n2, vec_len):
    return 1.0 * len(all_sb_idx(n1 & n2, vec_len)) / len(all_sb_idx(n1 | n2, vec_len))


def join(datasets: List[List[int]], t: float = 0, vec_len: int = 0) -> Set[Tuple[Tuple]]:
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

    records_sorted, original_order, order_map = preprocess(dataset, vec_len)
    result = compare(records_sorted, vec_len, t, order_map)

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

        ret.add((
            (dataset_id_offset.index(ds1_offset), r1id - ds1_offset),
            (dataset_id_offset.index(ds2_offset), r2id - ds2_offset)
        ))

    return ret
