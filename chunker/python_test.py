from collections import defaultdict

abc = defaultdict(int)

abc['123'] = 1
abc['456'] = 2

items = []

for i in abc:
	items.append(i)

for i in range(0,len(items)):
	print(items[i])
	abc.pop(items[i])

print(abc)
