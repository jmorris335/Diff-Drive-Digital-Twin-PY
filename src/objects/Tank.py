# Class: Tank.m
# Author: John Morris, jhmrrs@clemson.edu
# Date: 29 Jun 2022
# Purpose: Represent a differential drive vehicle with a set of motors
# Permission: All rights reserved. Do not reuse without written permission from the owner.

import numpy as np

from src.objects.DC_Motor import DC_Motor
from src.objects.Tread import Tread

class Tank:
    '''
    Represents a treaded, robotic, differential drive vehicle with geometric, physical, and 
    electronic properties. By default this class represents the T-Rex Robotic platform designed
    by DAGU robotics, shown here: https://web.archive.org/web/20220110180229/http://www.dagurobot.com/RS035
    '''

    def __init__(self, **kwargs):
        '''
        Inputs:  
        ---
            * theta : float=0.
                The angle of the tank from the abscissa (radians)
            * port_rpm : float=0.
                Revolutions Per Minute for port sprocket
            * strb_rpm : float=0
                Revolutions Per Minute for starboard sprocket
            * radius : float=1
                Effective radius for drive sprocket (units of length)
            * ch_height : float=10.
                The height of the chassis (units of length)
            * ch_width : float=5.
                The width of the chassis (units of length)
            * td_height : float=12.
                The height of the treads (units of length)
            * td_width : float=2.
                The width of the treads (units of length)
            * mass : float=5.
                The mass of the load, not including treads and sprockets (units of mass)
            * port_motor : DC_Motor
                DC motor driving the port sprocket
            * strb_motor : DC_Motor
                DC motor driving the starboard sprocket
            * gear_reduction : float=100.
                Reduction of speed from the motor to the sprocket
        '''
        for key, value in kwargs.items():
            if key == "theta": self.theta = value
            if key == "port_rpm": self.port_rpm = value
            if key == "strb_rpm": self.strb_rpm = value
            if key == "port_motor": self.port_motor = value
            if key == "strb_motor": self.strb_motor = value
            if key == "tread": self.tread = value
            if key == "ch_height": self.ch_height = value
            if key == "ch_width": self.ch_width = value
            if key == "td_height": self.td_height = value
            if key == "td_width": self.td_width = value
            if key == "mass": self.mass = value
            if key == "radius": self.radius = value
            if key == "gear_reduction": self.gear_reduction = value
        
        #Default Values
        if "theta" not in kwargs: self.theta = 0.
        if "port_rpm" not in kwargs: self.port_rpm = 0.
        if "strb_rpm" not in kwargs: self.strb_rpm = 0.
        if "ch_height" not in kwargs: self.ch_height = 10.
        if "ch_width" not in kwargs: self.ch_width = 5.
        if "td_height" not in kwargs: self.td_height = 12.
        if "td_width" not in kwargs: self.td_width = 2.
        if "mass" not in kwargs: self.mass = 5.
        if "radius" not in kwargs: self.radius = 1.
        if "port_motor" not in kwargs: self.port_motor = DC_Motor()
        if "strb_motor" not in kwargs: self.strb_motor = DC_Motor()
        if "tread" not in kwargs: self.tread = Tread()
        if "gear_reduction" not in kwargs: self.gear_reduction = 100.

        self.updatePosition(0, 0, self.theta)
        self.updateSpeed(self.port_rpm, self.strb_rpm)

    def updatePosition(self, x=0, y=0, theta=0):
        '''Setter for positional state'''
        self.x = x
        self.y = y
        self.theta = theta

    def updateSpeed(self, port_rpm=0, strb_rpm=0):
        '''Setter for sprocket angular velocity'''
        self.port_rpm = port_rpm
        self.strb_rpm = strb_rpm

    def calcDistance(self, time_step=.033):
        '''Calculate distance traveled from RPM over a time_step (s)'''
        p = (self.port_rpm / 60) * (np.pi * self.radius * 2) * time_step
        s = (self.strb_rpm / 60) * (np.pi * self.radius * 2) * time_step
        return p, s

    def calcPosition(self, time_step):
        '''Calculate position based on speed state expanded constantly over a time step'''
        p, s = self.calcDistance(time_step)
        k = self.ch_width + self.td_width
        
        gamma = -(p - s) / k
        newTheta = self.theta + gamma
        if p == s:
            newX = self.x + p * np.cos(np.pi/2 + self.theta)
            newY = self.y + p * np.sin(np.pi/2 + self.theta)
        else:
            r = k / ((p/s) - 1)
            newX = self.x + (r + k/2) * (np.cos(self.theta) - np.cos(newTheta))
            newY = self.y - (r + k/2) * (np.sin(newTheta) - np.sin(self.theta))

        return newX, newY, newTheta
        
    def move(self, port_rpm, strb_rpm, time_step):
        '''Wrapper function to process speed input and update position'''
        self.updateSpeed(port_rpm, strb_rpm)
        newX, newY, newTheta = self.calcPosition(time_step)
        self.updatePosition(newX, newY, newTheta)

    def calcMomentofInertia(self):
        ''' Adds together the moment of inertia for each object in the tank'''
        #TODO: Make a gearbox object
        J_tread = self.tread.MoI
        J_load = self.mass ( self.tread.driver.radius ** 2)
        J_gearbox = 0
        return (J_tread + J_load + J_gearbox) / self.gear_reduction ** 2 + J_gearbox
        
    def simulateMotors(self, time, port_voltage, strb_voltage, port_load, strb_load) -> tuple:
        ''' Solve Motor Speeds (returns speeds in rpm)'''
        # Find motor rpm versus input voltage and payload
        port_t, port_y, port_x = self.port_motor.simulateMotor(time, port_voltage, port_load)
        strb_t, strb_y, strb_x = self.strb_motor.simulateMotor(time, strb_voltage, strb_load)

        # Get rpm values at specific time samplings
        port_motor_rpm = list()
        strb_motor_rpm = list()
        for i in range(len(time)):
            index = np.nonzero(port_t >= time[i])
            port_motor_rpm.append(port_x[index[0][0]][1] * 60 / 2 / np.pi / self.gear_reduction)
            strb_motor_rpm.append(strb_x[index[0][0]][1] * 60 / 2 / np.pi / self.gear_reduction)
        
        return port_motor_rpm, strb_motor_rpm
