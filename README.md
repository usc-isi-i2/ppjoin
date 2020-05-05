# PPJoin

PPJoin and P4Join Python 3 implementation.

## PPJoin

PPJoin stands for Position Prefix Join which is an efficient set similarity join algorithm using the [Jaccard similarity](https://en.wikipedia.org/wiki/Jaccard_index) with several filtering techniques.


PPJoin is introduced in

> Xiao, Chuan, et al. "Efficient similarity joins for near-duplicate detection." ACM Transactions on Database Systems (TODS) 36.3 (2011): 1-41.

> This implementation is based on https://github.com/teh/ppjoin.

`join` function takes a list of datasets from different parties and a threshold `t` as input. 
Each dataset is a list of records and each record is formed by list of tokens.

```
ppjoin.join(datasets: List[List[List[str]]], t: float) -> Set[Tuple[Tuple]]
```

The return will be a set of tuples and each tuple contains two inner tuples:

```
((dataset1 index, record index), (dataset2 index, record index))
```

Example:

```
from ppjoin import ppjoin

def tokenizer(record):
    return set(ppjoin.whitespace_tokenizer(record.lower()))


ds0 = ['a b d', 'a b c', 'h k']
ds1 = ['a b k', 'a b', 'h k', 'a c h']
ds2 = ['a c h']
ds = [
    [tokenizer(w) for w in ds0],
    [tokenizer(w) for w in ds1],
    [tokenizer(w) for w in ds2]
]


result = ppjoin.join(ds, t=0.5)

for r in result:
    ds1_id, r1id = r[0]
    ds2_id, r2id = r[1]
    print('Found pair: {} from dataset {}, {} from dataset {}'.format(
        ds[ds1_id][r1id], ds1_id, ds[ds2_id][r2id], ds2_id
    ))
```

Output:

```
Found pair: ['a', 'b', 'c'] from dataset 0, ['a', 'b', 'k'] from dataset 1
Found pair: ['h', 'k'] from dataset 0, ['h', 'k'] from dataset 1
Found pair: ['a', 'b', 'c'] from dataset 0, ['a', 'c', 'h'] from dataset 2
Found pair: ['a', 'b', 'd'] from dataset 0, ['a', 'b', 'k'] from dataset 1
Found pair: ['a', 'b', 'd'] from dataset 0, ['a', 'b'] from dataset 1
Found pair: ['a', 'b', 'c'] from dataset 0, ['a', 'c', 'h'] from dataset 1
Found pair: ['a', 'c', 'h'] from dataset 1, ['a', 'c', 'h'] from dataset 2
Found pair: ['a', 'b', 'c'] from dataset 0, ['a', 'b'] from dataset 1
```

## P4Join

P4Join (Privacy-Preserving Prefix Position Join) adapts PPJoin with bit operations to solve privacy-preserving record linkage problem. 
It supports length, prefix and an optimized position filter.


This is introduced in

> Sehili, Ziad, et al. "Privacy preserving record linkage with PPJoin." Datenbanksysteme für Business, Technologie und Web (BTW 2015) (2015).


First step of P4Join is to encode original record into bit vector. 
`encode_record` takes a list of records each contains a list of tokens, a HMAC key, the length of the bit vector and k which indicates applying how many rounds of combined hash functions.
The return of it is a list of encoded record vectors.

```
p4join.encode_record(record: List[List[str]], hmac_key: str, vec_len: int, k: int = 2) -> List[int]
```


P4Join's `join` function is similar to PPJoin's, but it take encoded datasets as input. The return format is also identical to PPJoin.

```
p4join.join(datasets: List[List[[int]]], t: float = 0, vec_len: int = 0) -> Set[Tuple[Tuple]]
```

Example:

```
from ppjoin import ppjoin, p4join


def tokenizer(record):
    return set(ppjoin.whitespace_tokenizer(record.lower()))


hash_key = 'key'
vec_len = 40
k = 2

ds0 = ['a b d', 'a b c', 'h k']
ds1 = ['a b k', 'a b', 'h k', 'a c h']
ds2 = ['a c h']
ds = [
    [tokenizer(w) for w in ds0],
    [tokenizer(w) for w in ds1],
    [tokenizer(w) for w in ds2]
]

ds_encoded = [
    [p4join.encode_record(w, hash_key, vec_len, k) for w in d] for d in ds
]


result = p4join.join(ds_encoded, t=0.5, vec_len=vec_len)

for r in result:
    ds1_id, r1id = r[0]
    ds2_id, r2id = r[1]
    print('Found pair: {} from dataset {}, {} from dataset {}'.format(
        ds[ds1_id][r1id], ds1_id, ds[ds2_id][r2id], ds2_id
    ))
```

## Installation

```
pip install -e .
```

## Test

To run all unit tests:

```
python -m unittest discover ppjoin/tests
```

> Tests on real world dataset Abt-Buy is from [DBGroup of Leipzig](https://dbs.uni-leipzig.de/research/projects/object_matching/benchmark_datasets_for_entity_resolution).