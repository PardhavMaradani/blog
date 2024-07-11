# https://pardhav-m.blogspot.com/2020/06/polygon-stacks.html
# Polygon Stacks
# Polygon Stacks
from _polygonal_stack import draw_polygonal_stack

outer_sides = 6
inner_sides = 4
inner_polygons_multiple = 30
inner_length_factor = 0.2
twists = 1
pen_size = 1
checkerboard = False
animate = False
step_angle = 2

draw_polygonal_stack(outer_sides, inner_sides, inner_polygons_multiple, inner_length_factor, twists, pen_size, checkerboard, animate, step_angle)

# cover image
# first
# draw_polygonal_stack(5, 4, 40, 0.2)
# second
# draw_polygonal_stack(5, 4, 40, 0.8, 21)
# third
# draw_polygonal_stack(5, 3, 40, 1, 26, 1, True)

# penrose polygons
# triangle
# draw_polygonal_stack(3, 4, 60, 0.3)
# square
# draw_polygonal_stack(4, 4, 50, 0.22)
# pentagon
# draw_polygonal_stack(5, 4, 40, 0.18)

# rotating pentagon
# draw_polygonal_stack(5, 4, 40, 0.18, 1, 1, False, True, 9)

# polygon stack variants
# triangle
# draw_polygonal_stack(3, 3, 40, 0.5, 36)
# draw_polygonal_stack(3, 3, 40, 1, 19)
# draw_polygonal_stack(3, 3, 60, 1, 31, 1, True)
# square
# draw_polygonal_stack(4, 4, 50, 0.5, 24)
# draw_polygonal_stack(4, 4, 50, 1, 24)
# draw_polygonal_stack(4, 4, 50, 1, 26, 1, True)
# pentagon
# draw_polygonal_stack(5, 3, 40, 0.5, 13)
# draw_polygonal_stack(5, 3, 40, 1, 13)
# draw_polygonal_stack(5, 5, 40, 1, 21, 1, True)
# draw_polygonal_stack(5, 5, 40, 1, 21, 1, True, True, 4)

# rotating pentagon stack
# draw_polygonal_stack(5, 5, 40, 0.8, 21, 1, False, True, 8)

# rotatng checkerboard stack
# draw_polygonal_stack(5, 3, 40, 1, 19, 1, True, True, 3)

# rotating triangle checkerboard
# draw_polygonal_stack(3, 3, 60, 1, 31, 1, True, True, 10)
