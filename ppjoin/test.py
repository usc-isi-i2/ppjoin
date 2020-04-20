from ppjoin import ppjoin

ds1 = ['a b d', 'a b c', 'h k']
ds2 = ['a b k', 'a b', 'h k', 'a c h']
ds3 = ['a c h']

print(ppjoin(ds1, ds2, ds3, t=0.5))
# it returns {((1, 3), (2, 0)), ((0, 2), (1, 2))}
# which means two pairs found:
# first is 'a c h' from ds2 and 'a c h' from ds3
# second is 'h k' from ds1 and 'h k' from ds2
