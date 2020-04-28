# PPJoin

This repository is based on https://github.com/teh/ppjoin

## Usage

`ppjoin` function takes a list of datasets from different parties and a threshold `t` as input. 
Each dataset is a list of records and each record is formed by list of tokens.

```
ppjoin(datasets: List[List[List[str]]], t: float = 0) -> Set[Tuple[Tuple]]
```

The return will be a set of tuples and each tuple contains two inner tuples:

```
((dataset1 index, record index), (dataset2 index, record index))
```

Example:

```
from ppjoin import ppjoin, whitespace_tokenizer

ds0 = ['a b d', 'a b c', 'h k']
ds1 = ['a b k', 'a b', 'h k', 'a c h']
ds2 = ['a c h']
ds = [
    [whitespace_tokenizer(w) for w in ds0],
    [whitespace_tokenizer(w) for w in ds1],
    [whitespace_tokenizer(w) for w in ds2]
]


result = ppjoin(ds, t=0.5)

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