import json

js = json.loads(open('english.json').read())

s = set()
def f(d, r):
    global s
    if type(d) == dict:
        for k, v in d.items():
            s.add(k)
            f(v, r)
    elif type(d) == list:
        for v in d:
            f(v, r)
    else:
        return

for d in js:
    f(d, d)

print(*sorted(s), sep = '\n')

