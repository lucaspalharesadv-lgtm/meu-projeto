import sys, csv; sys.path.insert(0, '.')
import pros2
rows = list(csv.reader(open(pros2.P, encoding='utf-8-sig'))); h, b = rows[0], rows[1:]
bad = [r for r in b if not r[15].startswith('MX ok')]
b = [r for r in b if r[15].startswith('MX ok')]
for i, r in enumerate(b, 1): r[0] = f'{i:03d}'
with open(pros2.P + '.tmp', 'w', newline='', encoding='utf-8-sig') as fh:
    csv.writer(fh).writerows([h] + b)
import os; os.replace(pros2.P + '.tmp', pros2.P)
o = list(csv.reader(open(pros2.OUT, encoding='utf-8-sig')))
for r in bad: o.append([r[3], r[1], '', r[9], r[10], r[13], 'DOMINIO SEM SERVIDOR DE E-MAIL: ' + r[15]])
with open(pros2.OUT + '.tmp', 'w', newline='', encoding='utf-8-sig') as fh:
    csv.writer(fh).writerows(o)
os.replace(pros2.OUT + '.tmp', pros2.OUT)
print('removidos', [r[3] for r in bad], '| total agora', len(b))
