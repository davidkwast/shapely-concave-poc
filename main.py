from shapely import from_geojson
from shapely import get_parts
from shapely import unary_union
from shapely import concave_hull
from shapely import to_geojson

from utils import group_by_distance

#
import sys

PATH_INPUT_GEOJSON = sys.argv[1]
PATH_OUTPUT_DIR = sys.argv[2]

GROUP_DISTANCE = 0.005
CONCAVE_RATIO = 0.2
CONCAVE_HOLES = False

#

geom = from_geojson(open(PATH_INPUT_GEOJSON).read())


geoms = list(get_parts(geom))
# print(len(geoms))

groups = group_by_distance(geoms, GROUP_DISTANCE)
# print(groups.keys())


for k, polys in groups.items():
    union = unary_union(polys)

    concave = concave_hull(
        union, ratio=CONCAVE_RATIO, allow_holes=CONCAVE_HOLES
    )

    with open(
        f'{PATH_OUTPUT_DIR}/{k}.geojson',
        'wt',
    ) as fd:
        fd.write(to_geojson(concave))
