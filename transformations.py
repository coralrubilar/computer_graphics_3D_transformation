"""
    Submitted  by:
    Tsibulsky David  309444065
    Coral Rubilar    316392877
    Haham Omri       308428226
"""

import numpy as np
from math import sin, cos
from auxiliary_classes import Polygon,Point


def rotate(list_3D_Polygons:list, theta,clockWise, axis="x"):
    """
    We recieve a list of polygons, theta (the rotation angle), and the axis to rotate the shape.
    We can express the equations of the 3d rotation along the x-axis using the following matrix:
    [x', y', z', 1] = [x, y, z, 1] * |             1             0             0             0|
                                     |             0         cos_theta     sin_theta         0|
                                     |             0         -sin_theta    cos_theta         0|
                                     |             0             0             0             1|

    We can express the equations of the 3d rotation along the y-axis using the following matrix:
    [x', y', z', 1] = [x, y, z, 1] * |         cos_theta         0         -sin_theta        0|
                                     |             0             1             0             0|
                                     |         sin_theta         0         cos_theta         0|
                                     |             0             0             0             1|

    We can express the equations of the 3d rotation along the z-axis using the following matrix:
    [x', y', z', 1] = [x, y, z, 1] * | cos_theta   sin_theta       0         0|
                                     |-sin_theta   cos_theta       0         0|
                                     |     0             0         1         0|
                                     |     0             0         0         1|
    param: list_3D_Polygons : list of Polygon , theta : int ,clockWise : boolean , axis : x, y and z
    return: new_polygons_list : list of Polygon (after the transformation)
    """

    if(clockWise):
        theta = -theta
    rotation_matrix = []
    theta = np.radians(theta)
    rotate_x_axis_matrix = [[1, 0, 0, 0], [0, cos(theta), sin(theta), 0], [0, -sin(theta), cos(theta), 0], [0, 0, 0, 1]]
    rotate_y_axis_matrix = [[cos(theta), 0, -sin(theta), 0], [0, 1, 0, 0], [sin(theta), 0, cos(theta), 0], [0, 0, 0, 1]]
    rotate_z_axis_matrix = [[cos(theta), sin(theta), 0, 0], [-sin(theta), cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    if axis == "x":
        rotation_matrix = rotate_x_axis_matrix
    elif axis == "y":
        rotation_matrix = rotate_y_axis_matrix
    elif axis == "z":
        rotation_matrix = rotate_z_axis_matrix


    new_polygons_list = []

    transitionFix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    for poly in list_3D_Polygons:
        list_p = []
        color = poly.getColor()
        for i in range(len(poly)):
            p = poly.getPoint(i + 1)
            p_matrix = [p.x, p.y, p.z, 1]
            p_matrix = np.dot(np.array(p_matrix), np.array(transitionFix))
            p_matrix = np.dot(np.array(p_matrix), np.array(rotation_matrix))
            new_p = Point(float(p_matrix[0]), float(p_matrix[1]), float(p_matrix[2]))
            list_p.append(new_p)
            if i + 1 == len(poly):
                if i + 1 == 4:
                    new_poly = Polygon(list_p[0], list_p[1], list_p[2], list_p[3])
                elif i + 1 == 3:
                    new_poly = Polygon(list_p[0], list_p[1], list_p[2])
                new_poly.setColor(color)
                new_polygons_list.append(new_poly)

    return new_polygons_list


def scale(list_3D_Polygons,S):
    """
    We can perform scaling using the following matrix:
    [x', y', z', 1] = [x, y, z, 1] * |S  0   0   0|
                                     |0   S  0   0|
                                     |0   0   S  0|
                                     |0   0   0  1|
    So the equations will be:
    x' = x * S
    y' = y * S
    z' = z * S
    param: list_3D_Polygons : list of Polygon ,S - scaling factors : float - positive number.
    return: new_polygons_list : list of Polygon (after the transformation)
    """
    for poly in list_3D_Polygons:
        for i in range(len(poly)):
            p = poly.getPoint(i + 1)
            p.setX(p.getX() * S)
            p.setY(p.getY() * S)
            p.setZ(p.getZ() * S)
