import json
import math
from functools import reduce
from typing import Tuple, List
import numpy as np


class GeoBlock:
    def __init__(self, x1, x2, y1, y2, sa_code, sa_name):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.sa_code = sa_code
        self.sa_name = sa_name

    def __hash__(self):
        return hash((self.x1, self.x2, self.y1, self.y2))

    def __contains__(self, item):
        x, y = item[0], item[1]
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2


class Polygon:

    def __init__(self, boundary, sa_code, sa_name) -> None:
        self.boundary = boundary
        self.sa_code = sa_code
        self.sa_name = sa_name
    
    def __contains(self, item):
        x, y = item[0], item[1]
        return Polygon.in_poly(x, y, self.boundary)

    @staticmethod
    def in_poly(x: float, y: float, poly: List[Tuple[float]]) -> bool: 
        angle = 0
        if len(poly) <= 1:
            return False
        for p1, p2 in zip(poly[:-1], poly[1:]):
            p1x, p1y = p1[0], p1[1]
            p2x, p2y = p2[0], p2[1]
            angle += Polygon.get_angle(p1x-x, p1y-y, p2x-x, p2y-y)
        p1, p2 = poly[-1], poly[0]
        p1x, p1y = p1[0], p1[1]
        p2x, p2y = p2[0], p2[1]
        angle += Polygon.get_angle(p1x-x, p1y-y, p2x-x, p2y-y)
        return abs(angle) > math.pi

    @staticmethod
    def get_angle(x1: float, y1: float, x2: float, y2: float) -> float:
        ang1 = math.atan2(y1, x1)
        ang2 = math.atan2(y2, x2)
        diff = ang1 - ang2
        if diff > math.pi:
            return 2 * math.pi - diff
        if diff < -math.pi:
            return diff + 2 * math.pi
        return diff


def flat_polygons(poly):
    """
    return list of polygon
    """
    if not poly:
        return []
    target = poly[0]
    # test if target is point
    if len(target) == 2 and (not isinstance(target[0], list)):
        return [poly]
    return reduce(lambda x, y: x + y, [flat_polygons(p) for p in poly])


def read_poly_as_box():
    rst = []
    with open("./polygon.json", 'r') as poly:
        poly_data = json.load(poly)
    for zone in poly_data:
        for poly in flat_polygons(zone["geometry"]["coordinates"]):
            poly_arr = np.array(poly)
            x1, x2 = np.min(poly_arr[:, 0]), np.max(poly_arr[:, 0])
            y1, y2 = np.min(poly_arr[:, 1]), np.max(poly_arr[:, 1])
            rst.append(GeoBlock(x1, x2, y1, y2, zone["sa_code"], zone["sa2_name"]))
    return rst


def read_exact_poly():
    rst = []
    with open("./polygon.json", 'r') as poly:
        poly_data = json.load(poly)
    for zone in poly_data:
        for poly in flat_polygons(zone["geometry"]["coordinates"]):
            rst.append(Polygon(poly, zone["sa_code"], zone["sa2_name"]))
    return rst


BOX_POLY = read_poly_as_box()
EXACT_POLY = read_exact_poly()


def get_sa_code(coords: Tuple[float], polygons=None, *, method="box"):
    if method not in ("box", "exact"):
        raise ValueError("method only support box and exact")
    if polygons is None:
        polygons = BOX_POLY if method.lower() == "box" else EXACT_POLY
    for poly in polygons:
        if coords in poly:
            return poly.sa_code
    return "NaZ"  # not a zone


if __name__ == "__main__":
    codes = [p.sa_code for p in BOX_POLY]
    codes = {c: [] for c in codes}
    for p in EXACT_POLY:
        c = codes[p.sa_code]
        codes[p.sa_code] = codes[p.sa_code] + p.boundary
    rst = {}
    for k, v in codes.items():
        vector = np.array(v)
        rst[k] = [np.mean(vector[:, 0]), np.mean(vector[:, 1])]
    print(rst)
    with open("./poly_center.json", 'w+') as fd:
        json.dump(rst, fd)
    pass
