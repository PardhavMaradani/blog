import math

n_pins = 60
radius = 112.5 #378.0
pin_angle = 360 / n_pins
factor = 2
pen_radius = 10 #8 #6 #27

def get_coords(pin, delta = 0):
        angle = -90 + (pin * pin_angle)
        x = (radius + delta) * math.cos(math.radians(angle))
        y = (radius + delta) * math.sin(math.radians(angle))
        return [round(x, 2), round(y, 2)]

header = """G1 X0 Y-200
G0 Z0"""
print(header)

[sx1, sy1] = get_coords(0, pen_radius)
[sx2, sy2] = get_coords(0)
[sx3, sy3] = get_coords(0, -pen_radius)
print("G0 X{:.2f} Y{:.2f}".format(sx1, sy1))
print("G2 X{:.2f} Y{:.2f} I{:.2f} J{:.2f}".format(sx3, sy3, sx2, sy2))

seq = []
prev = -1
def add_to_seq(p):
        global seq
        global prev
        if prev != p:
                seq.append(p)
                prev = p

for i in range(1):
        for p in range(n_pins):
                #if p == 0:
                #    continue
                add_to_seq(p + i*15)
                add_to_seq(((factor*p) % n_pins) + i*15)
                add_to_seq(p + i*15)
        add_to_seq(0 + i*15)

#print(seq)
for p in seq:
        [x, y] = get_coords(p, -pen_radius)
        print("G0 X{:.2f} Y{:.2f}".format(x, y))
        [x2, y2] = get_coords(p)
        [x3, y3] = get_coords(p, pen_radius)
        print("G2 X{:.2f} Y{:.2f} I{:.2f} J{:.2f}".format(x3, y3, x2, y2))
        print("G2 X{:.2f} Y{:.2f} I{:.2f} J{:.2f}".format(x, y, x2, y2))

