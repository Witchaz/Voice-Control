t = [('foo',), ('bar',)]
print(any('oo' in name[0] for name in t))
print('oo' in (name[0] for name in t))
print('foo' in (name[0] for name in t))