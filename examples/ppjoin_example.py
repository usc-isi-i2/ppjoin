import ppjoin


def tokenizer(record):
    return ppjoin.whitespace_tokenizer(record.lower())


ds0 = ['a b d', 'a b c', 'h k']
ds1 = ['a b k', 'a b', 'h k', 'a c h']
ds2 = ['a c h']
ds = [
    [tokenizer(w) for w in ds0],
    [tokenizer(w) for w in ds1],
    [tokenizer(w) for w in ds2]
]


result = ppjoin.ppjoin(ds, t=0.5)

for r in result:
    ds1_id, r1id = r[0]
    ds2_id, r2id = r[1]
    print('Found pair: {} from dataset {}, {} from dataset {}'.format(
        ds[ds1_id][r1id], ds1_id, ds[ds2_id][r2id], ds2_id
    ))
