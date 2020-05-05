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
