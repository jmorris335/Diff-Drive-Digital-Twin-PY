# Program: DrawTank.py
# Author: John Morris, jhmrrs@clemson.edu
# Date: 30 Jun 2022
# Purpose: Return a set of patches imitating a robotic, differential drive
#  vehicle that can be plotted to a matplotlib canvas.
# Permissions: All rights reserved. Do not reuse without written permission from the owner.
# Sources: 
#   For more information on patches see 
#   https://matplotlib.org/stable/gallery/shapes_and_collections/artist_reference.html#sphx-glr-gallery-shapes-and-collections-artist-reference-py


import numpy as np
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

from src.objects.Tank import Tank

class SuperPatch:
    def __init__(self):
        pass

    def rotate(self, x, y, theta):
        ''' Rotates a point (x, y) around the origin by theta (radians)'''
        rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        return rotation @ np.array([[x], [y]])

    def translate(self, del_x, del_y, point: list): 
        ''' Translates a point by del_x and del_y'''
        shifted_x = del_x + point[0][0]
        shifted_y = del_y + point[1][0]
        return (shifted_x, shifted_y) 

    def rotateAndTranslate(self, corner_x, corner_y, center_x, center_y, theta):
        return self.translate(center_x, center_y, self.rotate(corner_x, corner_y, theta))

class Chassis:
    def __init__(self, tank: Tank):
        self.util = SuperPatch()
        self.tank = tank
        self.chassis = self.drawPatch()

    def drawPatch(self):
        x, y = self.calculateXY()
        theta = self.tank.theta * 180 / np.pi
        chassis = mpatches.Rectangle(xy=(x, y), width=self.tank.ch_width, height=self.tank.ch_height, 
                                        angle=theta, animated=True, fc='k', ec='k', lw=2)
        return chassis

    def calculateXY(self):
        x = -self.tank.ch_width / 2
        y = -self.tank.ch_height / 2
        return self.util.rotateAndTranslate(x, y, self.tank.x, self.tank.y, self.tank.theta)

    def update(self):
        (x, y) = self.calculateXY()
        theta = self.tank.theta * 180 / np.pi
        self.chassis.set(xy=(x, y), angle=theta)
        return self.chassis

    def get_patch(self):
        return self.chassis

class Tread:
    def __init__(self, tank: Tank, side: str="port"):
        self.util = SuperPatch()
        self.tank = tank
        self.side = side
        if side == "port": self.color = 'r'
        else: self.color = 'b'
        self.tread = self.drawPatch()

    def drawPatch(self):
        x, y = self.calculateXY()
        theta = self.tank.theta * 180 / np.pi
        chassis = mpatches.Rectangle(xy=(x, y), width=self.tank.td_width, height=self.tank.td_height, 
                                        angle=theta, animated=True, fc=self.color, ec='k', lw=2)
        return chassis

    def calculateXY(self):
        if self.side == "port": x = -self.tank.td_width - self.tank.ch_width / 2
        else: x = self.tank.ch_width / 2
        y = -self.tank.td_height / 2
        return self.util.rotateAndTranslate(x, y, self.tank.x, self.tank.y, self.tank.theta)

    def update(self):
        (x, y) = self.calculateXY()
        theta = self.tank.theta * 180 / np.pi
        self.tread.set(xy=(x, y), angle=theta)
        return self.tread

    def get_patch(self):
        return self.tread

class Ridges:
    def __init__(self, tank: Tank,  time: float, side: str="port"):
        self.util = SuperPatch()
        self.tank = tank
        self.time = time
        self.side = side

        self.num_ridge_lines = 4
        self.ridge_steps_per_second = 7

        self.ridges = self.drawPatch(0.)

    def drawPatch(self, time):
        x_c, y_c = self.calculateXYs(time)
        ridges = list()
        for i in range(self.num_ridge_lines):
            ridges.append(mlines.Line2D([x_c[0][i], x_c[1][i]], [y_c[0][i], y_c[1][i]], c='k', lw=2))

        return ridges

    def calculateXYs(self, time):
        x_c, y_c = self.getXYlive(time)

        new_x = list()
        new_y = list()
        for i in range(len(x_c)):
            new_x.append(list())
            new_y.append(list())
            for j in range(len(x_c[i])):
                x, y = self.util.rotateAndTranslate(x_c[i][j], y_c[i][j], self.tank.x, self.tank.y, self.tank.theta)
                new_x[i].append(x)
                new_y[i].append(y)
        
        return new_x, new_y

    def getXYlive(self, time):
        self.computeSpecs(time)

        x_coord = np.zeros((2, self.num_ridge_lines))
        y_coord = np.zeros((2, self.num_ridge_lines))

        for i in range(self.num_ridge_lines):
            x_coord[0][i] = self.btm_lft[0]
            y_coord[0][i] = self.btm_lft[1] + (i * self.spacing + self.dir * self.bump)
            
            overshoot = y_coord[0][i] - self.top_lft[1]
            undershoot = y_coord[0][i] - self.btm_lft[1]
            if overshoot > 0 and self.dir == 1:
                y_coord[0][i] = self.btm_lft[1] + overshoot
            elif undershoot < 0 and self.dir == -1:
                y_coord[0][i] = self.top_lft[1] + undershoot
            
            x_coord[1][i] = x_coord[0][i] + self.tank.td_width
            y_coord[1][i] = y_coord[0][i]

        return x_coord, y_coord

    def computeSpecs(self, time):
        self.theta = self.tank.theta + np.pi/2
        self.spacing = self.tank.td_height / self.num_ridge_lines

        bump_size = self.tank.td_height / self.num_ridge_lines / self.ridge_steps_per_second
        self.bump = bump_size + np.floor((time - np.fix(time)) * self.ridge_steps_per_second)
        if self.side == "port":
            self.dir = np.sign(self.tank.port_rpm)
            self.btm_lft = [-self.tank.td_width - self.tank.ch_width / 2, -self.tank.td_height / 2]
            self.top_lft = [-self.tank.td_width - self.tank.ch_width / 2, self.tank.td_height / 2]
        else:
            self.dir = np.sign(self.tank.strb_rpm)
            self.btm_lft = [self.tank.ch_width / 2, -self.tank.td_height / 2]
            self.top_lft = [self.tank.ch_width / 2, self.tank.td_height / 2]
            
    def update(self, time):
        (x_c, y_c) = self.calculateXYs(time)
        for i in range(self.num_ridge_lines):
            self.ridges[i].set(xdata=[x_c[0][i], x_c[1][i]], ydata=[y_c[0][i], y_c[1][i]])
        return self.ridges

    def get_lines(self):
        return self.ridges

class FrontDot:
    def __init__(self, tank: Tank):
        self.util = SuperPatch()
        self.tank = tank
        self.height_prop = 4/5
        self.radius = .5
        self.front_dot = self.drawPatch()

    def drawPatch(self):
        x, y = self.calculateXY()
        chassis = mpatches.Circle(xy=(x, y), radius=self.radius, animated=True, fc='y', lw=2)
        return chassis

    def calculateXY(self):
        dot_height = (self.tank.ch_height / 2) * 4/5
        x = self.tank.x + dot_height * np.cos(np.pi/2 + self.tank.theta)
        y = self.tank.y + dot_height * np.sin(np.pi/2 + self.tank.theta)
        return (x, y)

    def update(self):
        (x, y) = self.calculateXY()
        self.front_dot.set(center=(x, y))
        return self.front_dot

    def get_patch(self):
        return self.front_dot

    

