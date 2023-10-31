import numpy as np

from src.objects import *
from src.objects.DC_Motor import DC_Motor
from src.objects.Sprocket import Sprocket
from src.objects.Tread import Tread
from src.objects.Tank import Tank

from src.gui.TankAnimator import TankAnimator

class Tank_TD:
    def __init__(self):
        end_time = 10

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

        # Sprockets Parameters
        spkt_mass = 0.2 #kg
        spkt_radius = 0.02 #m
        spkt_axle_radius = 0.005 #m
        spkt_rolling_friction = 0.6 #kinetic coeff of friction

        self.driver = Sprocket(mass=spkt_mass, radius=spkt_radius, axle_radius=spkt_axle_radius,
                                rolling_friciton=spkt_rolling_friction)
        self.follower = Sprocket(mass=spkt_mass, radius=spkt_radius, axle_radius=spkt_axle_radius,
                                rolling_friciton=spkt_rolling_friction)

        # Tread Parameters
        tread_mass_links = 0.907
        tread_num_followers = 6
        tread_num_links = 200
        tread_link_friction = 0.60
        tread_ground_lift_force = 0.0

        self.tread = Tread(driver=self.driver, follower=self.follower, mass_links=tread_mass_links,
                           num_followers=tread_num_followers, num_links=tread_num_links, link_friction=tread_link_friction,
                           ground_lift_force=tread_ground_lift_force)

        # Tank Parameters
        chassis_height = 10.
        chassis_width = 5.
        tread_height = 12.
        tread_width = 2.
        driving_radius = 1.

        self.tank = Tank(ch_height=chassis_height, ch_width=chassis_width,
                    td_height=tread_height, td_width=tread_width, 
                    radius=driving_radius, port_motor=port_motor, strb_motor=strb_motor, tread=self.tread)

        # Voltage parameters
        self.port_voltage = list()
        self.strb_voltage = list()
        for z in self.time:
            if z < end_time * 1/3:
                self.port_voltage.append(18)
                self.strb_voltage.append(12)
            elif z < end_time * 1/2:
                self.port_voltage.append(18)
                self.strb_voltage.append(-18)
            elif z < end_time * 2/3:
                self.port_voltage.append(-12)
                self.strb_voltage.append(-18)
            else:
                self.port_voltage.append(12)
                self.strb_voltage.append(24)

        # Load parameters
        self.port_load = [self.tread.torque_friction for z in self.time]
        self.strb_load = [self.tread.torque_friction for z in self.time]

        self.port_rpm, self.strb_rpm = self.tank.simulateMotors(self.time, self.port_voltage, self.strb_voltage, 
                                                        self.port_load, self.strb_load, True) 
        #TODO: Figure out how the Moment of Inertia changes with both motors arbitrarily engaged

    def animate(self):
        self.anim = TankAnimator(tank = self.tank, time=self.time, 
                                 port_rpm=self.port_rpm, strb_rpm=self.strb_rpm)
        self.anim.animate()

def main():
    dt = Tank_TD()
    dt.animate()    

if __name__ == '__main__':
    main()
