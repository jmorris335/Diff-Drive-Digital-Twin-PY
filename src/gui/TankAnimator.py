# Class: TankAnimator.py
# Author: John Morris, jhmmrs@clemson.edu
# Date: 30 June 2022
# Purpose: A calling class that animates the motion of a differential drive
#   vehicle given a inputted speed or voltage.
# Permissions: All rights reserved. Do not reuse without written permission from the owner.

import matplotlib.pyplot as plt
from numpy import arange

from src.gui.BlitManager import BlitManager
from src.gui.DrawTank import *
from src.objects.Tank import Tank

class TankAnimator:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "tank": self.tank = value
            if key == "time": self.time = value
            if key == "port_rpm": self.port_rpm = value
            if key == "strb_rpm": self.strb_rpm = value

        if "tank" not in kwargs: self.tank = Tank()
        if "time" not in kwargs: self.time = list(arange(0, 5, 0.1))
        if "port_rpm" not in kwargs: self.port_rpm = [20 for z in self.time]
        if "strb_rpm" not in kwargs: self.strb_rpm = [10 for z in self.time]

        self.fig, self.ax = plt.subplots()
        self.patch_objects = list()
        self.line_objects = list()
        self.patches = list()
        self.lines = list()
        self.x_coords = [self.tank.x]
        self.y_coords = [self.tank.y]
        self.getObjects()
        self.initializePlot()

        for a in self.patches:
            self.ax.add_patch(a)
        for a in self.lines:
            self.ax.add_line(a)
        all_artists = self.patches + self.lines
        self.bm = BlitManager(self.fig.canvas, all_artists)

        plt.show(block=False)
        plt.pause(.1)

    def getObjects(self):
        self.patch_objects.append(Chassis(self.tank))
        self.patch_objects.append(Tread(self.tank, "port"))
        self.patch_objects.append(Tread(self.tank, "strb"))
        self.patch_objects.append(FrontDot(self.tank))

        self.line_objects.append(Ridges(self.tank, 0., side="port"))
        self.line_objects.append(Ridges(self.tank, 0., side="strb"))
        self.getPatches()
        self.getLines()

    def getPatches(self):
        for a in self.patch_objects:
            self.patches.append(a.get_patch())
        
    def getLines(self):
        for a in self.line_objects:
            for b in a.get_lines():
                self.lines.append(b)

    def initializePlot(self):
        plot_width = self.tank.ch_width * 5 #Half the plot width
        self.ax.set_xlim(self.tank.x - plot_width, self.tank.x + plot_width) #Set Screen Limits
        self.ax.set_ylim(self.tank.y - plot_width, self.tank.y + plot_width)
        self.ax.set_aspect('equal', adjustable='box')     
        plt.suptitle('Differential Drive Simulation')
        plt.xlabel('X-Coordinate (cm)')
        plt.ylabel('Y-Coordinate (cm)')

    def moveTank(self, port_rpm, strb_rpm, step_duration):
        ''' Moves the tank and updates the travel route'''
        self.tank.move(port_rpm, strb_rpm, step_duration)
        self.x_coords.append(self.tank.x)
        self.y_coords.append(self.tank.y)

    def plotRoute(self):
        self.ax.plot(self.x_coords, self.y_coords, ls='--', lw=2, color="#F56600")

    def animate(self):
        for j in range(len(self.time)):
            if j == len(self.time) - 1: step_duration = self.time[j] - self.time[j-1]
            else: step_duration = self.time[j+1] - self.time[j]
            self.moveTank(self.port_rpm[j], self.strb_rpm[j], step_duration)
            self.plotRoute()
            for a in self.patch_objects:
                a.update()
            for a in self.line_objects:
                a.update(self.time[j])

            self.bm.update()
            plt.title("Port RPM: {:.2f} Starboard RPM: {:.2f}".format(self.tank.port_rpm, self.tank.strb_rpm))
            plt.pause(0.001)

        plt.show(block=True)
