import math
from _line_clip import cohensutherland
from _DataType import Point

# check if point c is between points a and b
# Source: https://stackoverflow.com/questions/328107/how-can-you-determine-a-point-is-between-two-other-points-on-a-line-segment
def isBetween(a, b, c):
  eps = 0.01
  crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
  # compare versus epsilon for floating point values, or != 0 if using integers
  if abs(crossproduct) > eps:
      return False
  dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
  if dotproduct < 0:
      return False
  squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
  if dotproduct > squaredlengthba:
      return False
  return True

# simplify polygon by removing multiple vertices on same line
def simplify_polygon(polygon):
  simplified_polygon = []
  end = len(polygon) - 1
  for i, v in enumerate(polygon):
    pi = i - 1 # previous index
    ni = i + 1 # next index
    if pi < 0:
      pi = end
    if ni > end:
      ni = 0
    pv = polygon[pi] # previous vertex
    nv = polygon[ni] # next vertex
    a = Point(pv[0], pv[1])
    b = Point(nv[0], nv[1])
    c = Point(v[0], v[1])
    if not isBetween(a, b, c):
      simplified_polygon.append(v)
  simplified_polygon.append(simplified_polygon[0])
  return simplified_polygon

def get_voronoi_polygons(seeds, edges, bounding_box):
  (minx, miny, maxx, maxy) = bounding_box
  polygons = []
  # 1. clip edges
  # save border vertices after clipping
  border_vertices = [None] * 4
  for i in range(4):
    border_vertices[i] = []
  # clip edges
  clipped_edges = []
  for edge in edges:
    (x1, y1, x2, y2) = edge
    (nx1, ny1, nx2, ny2) = cohensutherland(minx, maxy, maxx, miny, x1, y1, x2, y2)
    if nx1 is None:
      continue
    clipped_edges.append((nx1, ny1, nx2, ny2))
    # save edges on border for next step
    if ny1 == miny or ny1 == maxy:
      border_vertices[0 if ny1 == miny else 2].append(nx1)
    if ny2 == miny or ny2 == maxy:
      border_vertices[0 if ny2 == miny else 2].append(nx2)
    if nx1 == minx or nx1 == maxx:
      border_vertices[3 if nx1 == minx else 1].append(ny1)
    if nx2 == minx or nx2 == maxx:
      border_vertices[3 if nx2 == minx else 1].append(ny2)
  # 2. connect borders
  # bb 0, 2
  for i in range(0, 4, 2):
    y = miny if i == 0 else maxy
    x1 = minx
    for v in sorted(border_vertices[i]):
      clipped_edges.append((x1, y, v, y))
      x1 = v
    clipped_edges.append((x1, y, maxx, y))
  # bb 1, 3
  for i in range(1, 4, 2):
    x = minx if i == 3 else maxx
    y1 = miny
    for v in sorted(border_vertices[i]):
      clipped_edges.append((x, y1, x, v))
      y1 = v
    clipped_edges.append((x, y1, x, maxy))
  # 3. get polygons
  # edges array for each seed
  seed_edges = [None] * len(seeds)
  for i, seed in enumerate(seeds):
    seed_edges[i] = []
  # Find the seed (cell) that the edge belongs to
  for edge in clipped_edges:
    (x1, y1, x2, y2) = edge
    midx = (x1 + x2) / 2
    midy = (y1 + y2) / 2
    distances = []
    i = 0
    # calculate distance from edge to each seed
    for seed in seeds:
      sx, sy = seed
      distance = math.sqrt((sx-midx)*(sx-midx) + (sy-midy)*(sy-midy))
      distances.append((distance, i))    
      i += 1
    # sort the distances to get closest seeds (cells)
    sorted_distances = sorted(distances)
    _, si1 = sorted_distances[0]
    _, si2 = sorted_distances[1]
    # for border edges, we only need one cell, for all others, two
    only_one = False
    if x1 == x2 and (x1 == minx or x1 == maxx):
      only_one = True
    if y1 == y2 and (y1 == miny or y1 == maxy):
      only_one = True
    seed_edges[si1].append(edge)
    if not only_one:
      seed_edges[si2].append(edge)
  # 4. create polygons from edges
  polygons = []
  for i in range(len(seeds)):
    # get vertices
    vertices = []
    for edge in seed_edges[i]:
      (x1, y1, x2, y2) = edge
      v1 = (x1, y1)
      v2 = (x2, y2)
      if v1 not in vertices:
        vertices.append(v1)
      if v2 not in vertices:
        vertices.append(v2)
    # find approx center of polygon from vertices
    midx = 0
    midy = 0
    for v in vertices:
      x, y = v
      midx += x
      midy += y
    midx /= len(vertices)
    midy /= len(vertices)
    # calculate angle to approx center to sort vertices
    sorted_vertices =  []
    for v in vertices:
      x, y = v
      angle = math.atan2((y - midy), (x - midx))
      sorted_vertices.append((angle, v))
    # create polygon from sorted vertices
    polygon = []
    for e in sorted(sorted_vertices):
      _, v = e
      polygon.append(v)
    # 5. simplify polygons (remove multiple vertices on same line)
    polygons.append(simplify_polygon(polygon))
  # return polygons
  return polygons
