import sys

n = 1
if len(sys.argv) == 2:
    n = int(sys.argv[1])

w = 100/n
lines = n + 1

header = """G1 X-1 Y-1
G0 Z0
G4 P5 S0
G0 X0 Y0"""

print(header)
print(';')

x = 0
y = 0
for r in range(lines):
    if r % 2 == 0:
        x = 100
    else:
        x = 0
    print("G0 X{:.2f} Y{:.2f}".format(x, y))
    if r != lines - 1:
        y += w
        print("G0 X{:.2f} Y{:.2f}".format(x, y))

sign = 1
if x == 100:
    sign = -1

print(';')

for c in range(lines):
    if c % 2 == 0:
        y = 0
    else:
        y = 100
    print("G0 X{:.2f} Y{:.2f}".format(x, y))
    if c != lines - 1:
        x += sign * w
        print("G0 X{:.2f} Y{:.2f}".format(x, y))

print(';')

if abs(x) > 0.01:
    print("G0 X{:.2f} Y{:.2f}".format(0, y))
if abs(y) > 0.01:
    print("G0 X{:.2f} Y{:.2f}".format(0, 0))
