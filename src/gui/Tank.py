# Class:      Tank.m
# Author:     John Morris, jhmrrs@clemson.edu
# Date:       29 Jun 2022
# Permission: All rights reserved. Do not reuse without written permission from the owner

import numpy as np

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
            theta:        The angle of the tank from the abscissa (radians)
            port_rpm:     Revolutions per Minute for port sprocket
            strb_rpm:     Revolutions per Minute for starboard sprocket
            radius:       Effective radius for drive sprocket
            ch_height:    The height of the chassis (cm)
            ch_width:     The width of the chassis (cm)
            td_height:    The height of the treads (cm)
            td_width:     The width of the treads (cm)
        '''
        for arg in kwargs:
            if arg == "ch_height": self.ch_height = arg["ch_height"]
            if arg == "ch_width": self.ch_height = arg["ch_width"]
            if arg == "td_height": self.ch_height = arg["td_height"]
            if arg == "td_width": self.ch_height = arg["td_width"]
            if arg == "radius": self.ch_height = arg["radius"]
            if arg == "port_motor": self.ch_height = arg["port_motor"]
            if arg == "strb_motor": self.ch_height = arg["strb_motor"]
        
        if "ch_height" not in kwargs: self.ch_height = 10
        if "ch_width" not in kwargs: self.ch_width = 5
        if "td_height" not in kwargs: self.td_height = 12
        if "td_width" not in kwargs: self.td_width = 2
        if "radius" not in kwargs: self.radius = 1
        # if "port_motor" not in kwargs: self.port_motor = 10
        # if "strb_motor" not in kwargs: self.strb_motor = 10

    def updatePosition(self, x=0, y=0, theta=0):
        # Setter for positional state
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
        
    def simulateMotors(self, time, port_voltage, strb_voltage, port_load, strb_load):
        ''' Solve Motor Speeds '''
        # Find motor rpm versus input voltage and payload
        port_t, port_y = self.port_motor.simulate(time[len(time)-1], port_voltage, port_load)
        strb_t, strb_y = self.strb_motor.simulate(time[len(time)-1], strb_voltage, strb_load)

        # Get rpm values at specific time samplings
        port_motor_rpm = np.zeros([1, len(time)])
        strb_motor_rpm = np.zeros([1, len(time)])
        for i in range(len(time)):
            port_motor_rpm[i] = port_y(np.where(port_t >= time[i], 1), 2) * 60 / 2 / np.pi
            strb_motor_rpm[i] = strb_y(np.where(strb_t >= time[i], 1), 2) * 60 / 2 / np.pi
