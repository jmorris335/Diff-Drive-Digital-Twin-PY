import numpy as np

from src.objects import *
from src.objects.DC_Motor import DC_Motor
from src.objects.Tank import Tank

from src.gui.TankAnimator import TankAnimator

class Tank_TD:
    def __init__(self):
        end_time = 3

        # Simulation parameters
        self.time = np.arange(0, end_time, 0.03)

        # Motor Parameters
        R_a = 0.5 #Ohms
        L_a = 1.5e-3 #Hertz
        J_M = 2.5e-4 #N-m/(rad/s^2)
        k = 0.05 #N-m/A
        B_M = 1.0e-4 #N-m/(rad/s)
        T_L = .5 #N-m

        port_motor = DC_Motor(R_a, L_a, J_M, k, B_M)
        strb_motor = DC_Motor(R_a, L_a, J_M, k, B_M)

        # Tank Parameters
        chassis_height = 10.
        chassis_width = 5.
        tread_height = 12.
        tread_width = 2.
        driving_radius = 1.

        self.tank = Tank(ch_height=chassis_height, ch_width=chassis_width,
                         td_height=tread_height, td_width=tread_width, 
                         radius=driving_radius, port_motor=port_motor, strb_motor=strb_motor)

        # Voltage parameters
        self.port_voltage = [18 for z in self.time]
        self.strb_voltage = [12 for z in self.time]
        self.port_rpm, self.strb_rpm = self.tank.simulateMotors(self.time, self.port_voltage, self.strb_voltage, 
                                                        np.zeros_like(self.time), np.zeros_like(self.time)) 

    def animate(self):
        self.anim = TankAnimator(tank = self.tank, time=self.time, 
                                 port_rpm=self.port_rpm, strb_rpm=self.strb_rpm)
        self.anim.animate()

if __name__ == '__main__':
    dt = Tank_TD()
    dt.animate()

