import matplotlib.pyplot as plt
from numpy import arange

from src.gui.BlitManager import BlitManager
from src.gui.DrawTank import *
from src.objects.Tank import Tank

class TankAnimator:
    def __init__(self, **kwargs):
        for arg in kwargs:
            if arg == "tank": self.tank = arg["tank"]
            if arg == "time": self.time = arg["time"]
            if arg == "port_rpm": self.port_rpm = arg["port_rpm"]
            if arg == "strb_rpm": self.strb_rpm = arg["strb_rpm"]

        if "tank" not in kwargs: 
            self.tank = Tank()
            self.tank.updatePosition()
            self.tank.updateSpeed()
        if "time" not in kwargs: self.time = list(arange(0, 5, 0.1))
        if "port_rpm" not in kwargs: self.port_rpm = [20 for z in self.time]
        if "strb_rpm" not in kwargs: self.strb_rpm = [10 for z in self.time]

        self.fig, self.ax = plt.subplots()
        self.patch_objects = list()
        self.line_objects = list()
        self.patches = list()
        self.lines = list()
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
        plt.title('Differential Drive Simulation')
        # plt.subtitle(str('Port RPM: %f Starboard RPM: %f',tank.port_rpm, tank.strb_rpm))
        plt.xlabel('X-Coordinate (cm)')
        plt.ylabel('Y-Coordinate (cm)')

    def animate(self):
        for j in range(len(self.time)):
            if j == len(self.time) - 1: step_duration = self.time[j] - self.time[j-1]
            else: step_duration = self.time[j+1] - self.time[j]
            self.tank.move(self.port_rpm[j], self.strb_rpm[j], step_duration)
            for a in self.patch_objects:
                a.update()
            for a in self.line_objects:
                a.update(self.time[j])

            self.bm.update()
            plt.pause(0.1)

        plt.show(block=True)

if __name__ == "__main__":
    ta = TankAnimator()
    ta.animate()
