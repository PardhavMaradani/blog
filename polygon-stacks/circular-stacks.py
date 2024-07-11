# https://pardhav-m.blogspot.com/2020/06/polygon-stacks.html
# Polygon Stacks
# Circular Stacks
from _circular_stack import draw_circular_stack

inner_sides = 4
inner_polygons_multiple = 30
inner_length_factor = 0.2
twists = 6
pen_size = 1
checkerboard = False
animate = False
step_angle = 2

draw_circular_stack(inner_sides, inner_polygons_multiple, inner_length_factor, twists, pen_size, checkerboard, animate, step_angle)

# circular stack variants
# draw_circular_stack(3, 40, 0.5, 30)
# draw_circular_stack(3, 40, 1, 35)
# draw_circular_stack(3, 40, 1, 27, 1, True)

# rotating circular stack
# draw_circular_stack(4, 30, 1, 20, 1, False, True, 2)
# draw_circular_stack(3, 22, 0.9, 15, 1, True, True, 6)
