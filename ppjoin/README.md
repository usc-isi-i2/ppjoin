# PPJoin

This repository is based on https://github.com/teh/ppjoin

## Usage

`ppjoin` function takes datasets from different parties and a threshold `t` as input.

```
from ppjoin import ppjoin

ppjoin(dataset1, dataset2, dataset2, t=0.5)
```

Each dataset is a list of string records.

The return will be a set of tuples and each tuple contains two inner tuples:

```
((dataset1 index, record index), (dataset2 index, record index))
```

Example:

```
from ppjoin import ppjoin

ds1 = ['a b d', 'a b c', 'h k']
ds2 = ['a b k', 'a b', 'h k', 'a c h']
ds3 = ['a c h']

print(ppjoin(ds1, ds2, ds3, t=0.5))
# it returns {((1, 3), (2, 0)), ((0, 2), (1, 2))}
# which means two pairs found:
# first is 'a c h' from ds2 and 'a c h' from ds3
# second is 'h k' from ds1 and 'h k' from ds2
```