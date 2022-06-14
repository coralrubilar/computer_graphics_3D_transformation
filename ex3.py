"""
    Submitted  by:
    Tsibulsky David  309444065
    Coral Rubilar    316392877
    Haham Omri       308428226
"""

"""
imports:
"""
from tkinter import *
import numpy as np
import os
import random
from tkinter import messagebox
from auxiliary_classes import Polygon,Point
from projections import perspective_projection,oblique_projection
from transformations import rotate ,scale
from copy import deepcopy

"""
global variables:
"""
WIDTH = 1000
HEIGHT = 600
fileParams =""  #File Relative Path
list_3D_Polygons = []
obliqueProjection = True
clockWise = True




##########################################################################################################
###################################           Get from file :        #####################################
##########################################################################################################

def getPoligonsLstFromFile():
    """
    read the data from the current file and update the list_3D_Polygons list.
    """
    global list_3D_Polygons
    new_list_3D_Polygons =[]
    try:
        list_polygon_cube = []
        list_point_cube = []
        list_polygon_pyramid = []
        list_point_pyramid = []
        try:
            text_file = open(fileParams, "r")
        except FileNotFoundError:
            display_error("Incorect file name")
            return
        shape = None  # if cube or pyramid
        type_p = None  # polygon or point

        for line in text_file:
            count = 0
            list_number = []  # take all numbers in only line
            for x in line.split(','):
                if x == 'cube' or x == 'pyramid':
                    shape = x
                elif x == 'polygon' or x == 'point':
                    type_p = x
                elif line == 'cube,\n' or line == 'pyramid,\n' or line == 'polygon,\n' or line == 'point,\n':
                    continue
                else:
                    if x != '\n':
                        # take all numbers in line
                        try:
                            list_number.append(float(x))
                        except:
                            display_error("Expected float number")
                    elif shape == 'cube' and type_p == 'polygon':
                        list_polygon_cube.append(list_number)
                    elif shape == 'cube' and type_p == 'point':
                        list_point_cube.append(list_number)
                    elif shape == 'pyramid' and type_p == 'polygon':
                        list_polygon_pyramid.append(list_number)
                    elif shape == 'pyramid' and type_p == 'point':
                        list_point_pyramid.append(list_number)

        # We have listPolygon and list point
        # So we want to create a class of list polygons
        for poligon_cube in list_polygon_cube:
            p1 = list_point_cube[int(poligon_cube[0]) - 1]  # 1, 2, 4, 3
            p2 = list_point_cube[int(poligon_cube[1]) - 1]
            p3 = list_point_cube[int(poligon_cube[2]) - 1]
            p4 = list_point_cube[int(poligon_cube[3]) - 1]
            poly = Polygon(Point(p1[0], p1[1],p1[2]), Point(p2[0],p2[1], p2[2]),Point(p3[0], p3[1], p3[2]),Point(p4[0], p4[1],p4[2]))
            poly.setColor("#{:06x}".format(random.randint(0, 0xFFFFFF)))
            new_list_3D_Polygons.append(poly)
        for poligon_pyramid in list_polygon_pyramid:
            p1 = list_point_pyramid[int(poligon_pyramid[0]) - 1]  # 1, 2, 4, 3
            p2 = list_point_pyramid[int(poligon_pyramid[1])- 1]
            p3 = list_point_pyramid[int(poligon_pyramid[2]) - 1]
            poly = Polygon(Point(p1[0],p1[1],p1[2]), Point(p2[0],p2[1],p2[2]),Point(p3[0],p3[1],p3[2]))
            poly.setColor("#{:06x}".format(random.randint(0, 0xFFFFFF)))
            new_list_3D_Polygons.append(poly)
    except Exception:
        display_error(Exception)
    else:
        list_3D_Polygons = deepcopy(new_list_3D_Polygons)

def change_file_name(my_canvas, text_box):
    """
    change the current file name, read the data from the file, update the list_3D_Polygons list and disply then shapes
    param :  my_canvas:canvas , text_box:Text
    """
    global fileParams
    file_temp=fileParams
    fileParams = text_box.get(1.0, END+"-1c")
    if fileParams == "":
        return

    fileParams = os.path.join("Params/", fileParams)
    if not os.path.isfile(fileParams):
        fileParams = file_temp
        display_error("Incorect file name")
    else:
        text_box.delete("1.0", "end")
        getPoligonsLstFromFile()
        displayShapes(my_canvas)




##########################################################################################################
#############################         Polygon Manipulation Functions :      ##############################
##########################################################################################################

def setVisibility():
    """
    calculate the normal for each polygon and set the visibility of the polygon by the sign of the result.
    param :  my_canvas:canvas , text_box:Text
    """
    global list_3D_Polygons
    for poly in list_3D_Polygons:
        p1: Point = poly.getPoint(1)
        p2: Point = poly.getPoint(2)
        p3: Point = poly.getPoint(3)

        # vector product
        vector_edge1 = np.array(
            [(p2.getX() - p1.getX()), (p2.getY() - p1.getY()), (p2.getZ() - p1.getZ())])  # P2-P1 vector
        vector_edge2 = np.array(
            [(p3.getX() - p2.getX()), (p3.getY() - p2.getY()), (p3.getZ() - p2.getZ())])  # P3 -P2 vector
        normal = np.cross(vector_edge1, vector_edge2)
        normal = np.fix(normal).astype(int)

        # scalar product
        if (obliqueProjection):
            vector_cop_p1 = np.array(
                [0 - p1.getX(), 300 - p1.getY(), -1200 - p1.getZ()])  # COP-P1 vector (COP -froma a bit bottom)
        else:
            vector_cop_p1 = np.array([0 - p1.getX(), 0 - p1.getY(), -1200 - p1.getZ()])  # COP-P1 vector

        visible = np.dot(vector_cop_p1, normal)

        if visible > 0:
            poly.setVisibility(True)
        else:
            poly.setVisibility(False)


def myPolygonSort(poly):
    """
    sort the polygon's point by their z-values
    param :  poly: Polygon
    return : max z value
    """
    z1 = poly.getPoint(1).getZ()
    z2 = poly.getPoint(2).getZ()
    z3 = poly.getPoint(3).getZ()
    p4: Point = poly.getPoint(4)
    if p4 is not None:
        z4 = p4.getZ()
        return max(z1, z2, z3, z4)
    else:
        return max(z1, z2, z3)


def sortPoligons():
    """
    sort the polygon list
    """
    global list_3D_Polygons
    list_3D_Polygons.sort(key=myPolygonSort)



def scale_func(my_canvas, S):
    """
    scale the 3D shapes by the S parameter and disply the result
    param: my_canvas: Canvas , S - scale value : float
    """
    global list_3D_Polygons
    scale(list_3D_Polygons, S)
    displayShapes(my_canvas)


def rotate_func(my_canvas, theta, axis="x"):
    """
    rotate the 3D shapes by the theta degree parameter and disply the result
    param : my_canvas: Canvas , theta - rotate degree value : int , axis : x,y or z
    """
    global list_3D_Polygons ,clockWise
    new_polygons_list = rotate(list_3D_Polygons, theta,clockWise, axis)
    list_3D_Polygons = deepcopy(new_polygons_list)
    displayShapes(my_canvas)




##########################################################################################################
##################################           Display Functions :        ##################################
##########################################################################################################

def display_error(msg: str):
    """
        Display an error message to the user
        param : msg - message : string
    """
    messagebox.showerror(title="Error", message=msg)


def clear(my_canvas):
    """
     clear all the canvas pixels
     """
    my_canvas.delete('all')


def reset_canvas(my_canvas):
    """
    Reopen the current file, read the data, update the polygon list and then redraw the image on canvas
    param :  my_canvas: canvas
    """
    global list_3D_Polygons
    list_3D_Polygons = []
    getPoligonsLstFromFile()
    displayShapes(my_canvas)

def Switch_clock_wise():
    """
    Switch the flag from anti-clockwise to clockwise and reverse
    """
    global clockWise
    if clockWise:
        clock_wise_switch_button.config(image=counter_clock_wise_img)
        clockWise = False
    else:
        clock_wise_switch_button.config(image=clock_wise_img)
        clockWise = True

def Switch_Projection(my_canvas):
    """
    Switch the flag from oblique projection to perspective projection and reverse
    param :  my_canvas: canvas
    """
    global obliqueProjection

    if obliqueProjection:
        switch_button.config(image=P_projection_img)
        switch_label.config(text="Perspective Projection is On",
                            fg="grey")
        obliqueProjection = False
    else:
        switch_button.config(image=O_projection_img)
        switch_label.config(text="Oblique Projection is On", fg="grey")
        obliqueProjection = True

    displayShapes(my_canvas)


def draw_poligons(my_canvas , list_2D_Polygon):
    """
    disply all the polygons in the polygon list on the canvas
    param :  my_canvas: canvas , list_2D_Polygon : Polygon array
    """
    list_2D_Polygon.reverse()
    for poly in list_2D_Polygon:
        if (poly.isVisible()):
            p1: Point = poly.getPoint(1)
            p2: Point = poly.getPoint(2)
            p3: Point = poly.getPoint(3)
            p4: Point = poly.getPoint(4)
            if p4 is not None:
                my_canvas.create_polygon([p1.getX() + 500, p1.getY() + 300,
                                       p2.getX() + 500, p2.getY() + 300,
                                       p3.getX() + 500, p3.getY() + 300,
                                       p4.getX() + 500, p4.getY() + 300],
                                      outline='blue', fill=poly.getColor(), width=1)
            else:
                my_canvas.create_polygon([p1.getX() + 500, p1.getY() + 300,
                                       p2.getX() + 500, p2.getY() + 300,
                                       p3.getX() + 500, p3.getY() + 300],
                                      outline='blue', fill=poly.getColor(), width=1)


def  displayShapes(my_canvas):
    """
    this function responsible fot all the steps from the 3D points until the shapes shown to the screen
    param :  my_canvas: canvas
    """
    global list_3D_Polygons
    setVisibility()
    sortPoligons()
    if(obliqueProjection):
        list_2D_Polygon = oblique_projection(list_3D_Polygons)
    else:
        list_2D_Polygon = perspective_projection(list_3D_Polygons)
    clear(my_canvas)
    draw_poligons(my_canvas,list_2D_Polygon)




##########################################################################################################
######################################           MAIN             ########################################
##########################################################################################################


if __name__ == "__main__":
    # get shapes from file :
    fileName = "data.txt"
    fileParams = os.path.join("Params/",fileName)
    getPoligonsLstFromFile()

    # Windows and canvas definitions  :
    my_window = Tk()
    my_window.maxsize(WIDTH+300,HEIGHT)
    my_window.minsize(WIDTH +300,HEIGHT)
    my_window.title("Targil 3 - 3D Projections")
    my_canvas = Canvas(my_window, width=WIDTH, height=HEIGHT, background='white')
    my_canvas.grid(row=0, column=0, columnspan=4)

    # Display the polygons:
    displayShapes(my_canvas)




##########################################################################################################
########################### User Control : sliders ,buttons , switches .. . ##############################
##########################################################################################################



    # return slider value
    def get_slider_values(slider):
        return slider.get()


    def set_all_sliders(all_sliders):
        """
        Set all sliders  to tho midle of the bar .
        :param all_sliders: list with all sliders
        """
        for slider in all_sliders:
            slider_fefault_value = float((slider["to"] + slider["from"]) / 2)
            slider.set(float(slider_fefault_value))

    # sliders:

    # rotate on point slider
    slider_scale_point = Scale(my_window, from_=1, to=2, tickinterval=1,resolution =0.1, orient=HORIZONTAL, troughcolor='red')
    # slider_scale_point.set(1.1)
    slider_scale_point.place(x=1160, y=290)

    # scale on point slider
    slider_rotate_point = Scale(my_window, from_=0, to=45, tickinterval=45, orient=HORIZONTAL, troughcolor='purple1')
    # slider_rotate_point.set(22.5)
    slider_rotate_point.place(x=1160, y=360)

    all_sliders = [slider_scale_point ,slider_rotate_point]
    set_all_sliders(all_sliders)




    # buttons :
    button1 = Button(my_window, text="Scale-Up on place", width=20, bg="red", fg="white",
                     command=lambda: scale_func(my_canvas ,get_slider_values(slider_scale_point)))
    button2 = Button(my_window, text="Scale-Down on place", width=20, bg="red", fg="white",
                      command=lambda: scale_func(my_canvas, 1/get_slider_values(slider_scale_point)))

    button3 = Button(my_window, text="Rotate X axis ", width=20, bg="purple1", fg="white",
                      command=lambda: rotate_func(my_canvas,get_slider_values(slider_rotate_point),"x" ))
    button4 = Button(my_window, text="Rotate Y axis", width=20, bg="purple1", fg="white",
                      command=lambda: rotate_func( my_canvas, get_slider_values(slider_rotate_point), "y"))
    button5 = Button(my_window, text="Rotate Z axis", width=20, bg="purple1", fg="white",
                      command=lambda: rotate_func( my_canvas, get_slider_values(slider_rotate_point), "z"))

    button_reset = Button(my_window, text="Reset image", width=20, bg="gray", fg="white",command=lambda: reset_canvas(my_canvas))
    button_reset_sliders = Button(my_window, text="Reset sliders", width=10, bg="ivory3", fg="black",
                          command=lambda: set_all_sliders(all_sliders) )


    # Place the buttons :
    button1.place(x=1005, y=290)
    button2.place(x=1005, y=325)
    button3.place(x=1005, y=360)
    button4.place(x=1005, y=395)
    button5.place(x=1005, y=430)

    button_reset.place(x=1005, y=565)
    button_reset_sliders.place(x=1040, y=530)



    # textbox
    input_file_name = Text(my_window, height=1, width=16)
    input_file_name.place(x=1160, y=540)
    button_file_name = Button(my_window, text="Change File", width=15, bg="black", fg="white",
                              command=lambda: change_file_name(my_canvas, input_file_name))
    button_file_name.place(x=1170, y=565)


    # Help button :
    def help_me_file():
        # Method 2: Open with subprocess
        import subprocess
        path = "help.pdf"
        subprocess.Popen([path], shell=True)
        pass

    button_help = Button(my_window, text="Help", width=6, bg="blue4", fg="white", borderwidth=1,command=lambda: help_me_file())
    button_help.place(x=1225, y=10)

    # Projection switch:
    switch_label = Label(my_window,
                  text="Oblique Projection is On",
                  fg="grey",
                  font=("Helvetica", 32))

    switch_label.place(x=200, y=30)
    O_projection_img = PhotoImage(file="images/O_projection.png")
    P_projection_img = PhotoImage(file="images/P_projection.png")

    switch_button = Button(my_window, image=O_projection_img, bd=0,
                    command=lambda: Switch_Projection(my_canvas))
    switch_button.place(x=1080, y=12)




    # clockWize counterClockwise switch:
    clock_wise_img = PhotoImage(file="images/ClockW.png")
    counter_clock_wise_img = PhotoImage(file="images/counterClockW.png")

    clock_wise_switch_button = Button(my_window, image=clock_wise_img, bd=0,
                           command=lambda: Switch_clock_wise())
    clock_wise_switch_button.place(x=1080, y=460)



    # start running the interface window :
    my_window.mainloop()
