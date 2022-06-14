"""
    Submitted  by:
    Tsibulsky David  309444065
    Coral Rubilar    316392877
    Haham Omri       308428226
"""
import numpy as np
import math
from auxiliary_classes import Polygon,Point



def perspective_projection(list_3D_Polygons:list):
    """
    The function makes perspective projection from 3D polygons and returns list of 2D polygons
    param: list_3D_Polygons: list with 3D polygons
    return: new_list_2D_poly:  list of 2D polygons
    """
    new_list_2D_poly = []
    for poly in list_3D_Polygons:
        list_p = []
        visible = poly.isVisible()
        color = poly.getColor()
        for i in range(len(poly)):
            p: Point = poly.getPoint(i + 1)
            d = 200
            Sz = d / (p.getZ() + d)    # ???minus /plus
            const_matrix = [[Sz, 0, 0, 0], [0, Sz, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]
            p_matrix = [p.getX(), p.getY(), p.getZ(), 1]
            result = np.dot(np.array(p_matrix), np.array(const_matrix))

            new_p = Point(result[0] , result[1], result[2] )
            list_p.append(new_p)
            if i + 1 == len(poly):
                if i + 1 == 4:
                    new_poly = Polygon(list_p[0], list_p[1], list_p[2], list_p[3])
                elif i + 1 == 3:
                    new_poly = Polygon(list_p[0], list_p[1], list_p[2])
                new_poly.setVisibility(visible)
                new_poly.setColor(color)
                new_list_2D_poly.append(new_poly)
    return new_list_2D_poly  # return list of  2D polygons for parallel_projection




def oblique_projection(list_3D_Polygons:list , angle=45):
    """
    The function makes oblique projection from 3D polygons and returns list of 2D polygons
    param:  list_3D_Polygons: list with 3D polygons , angle of projection in degrees
    return: new_list_2D_poly -  list with 2D polygons
    """
    new_list_2D_poly = []
    cos_number: float = math.cos(math.radians(angle)) / 2
    sin_number: float = math.sin(math.radians(angle)) / 2

    const_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [cos_number, sin_number, 0, 0], [0, 0, 0, 1]]

    for poly in list_3D_Polygons:
        list_p = []
        color = poly.getColor()
        visible = poly.isVisible()
        for i in range(len(poly)):
            p: Point = poly.getPoint(i + 1)
            p_matrix = [p.getX(), p.getY(), p.getZ(), 1]
            result = np.dot(np.array(p_matrix), np.array(const_matrix))
            new_p = Point(result[0], result[1], result[2])
            list_p.append(new_p)
            if i + 1 == len(poly):
                if i + 1 == 4:
                    new_poly = Polygon(list_p[0], list_p[1], list_p[2], list_p[3])
                elif i + 1 == 3:
                    new_poly = Polygon(list_p[0], list_p[1], list_p[2])
                new_poly.setVisibility(visible)
                new_poly.setColor(color)
                new_list_2D_poly.append(new_poly)
    return new_list_2D_poly  # return list of  2D polygons for parallel_projection
