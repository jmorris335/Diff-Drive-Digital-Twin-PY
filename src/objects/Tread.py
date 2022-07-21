from src.objects.Sprocket import Sprocket

class Tread:
    ''' Represents a tread containing an arbitrary number of follower sprockets and one driving sprocket.
    By default this class represents the T-Rex Robotic platform designed by DAGU robotics, 
    shown here: https://web.archive.org/web/20220110180229/http://www.dagurobot.com/RS035
    '''

    def __init__(self, **kwargs):
        '''
        Keyword Arguments:  
        ---
            * driver : Sprocket
                The sprocket that is connected to the DC motor on the tread
            * follower : Sprocket
                Any sprocket that is not connected to the DC motor on the tread
            * mass_links : float=.907
                The total mass of the tread, not including sprockets (units of mass)
            * num_followers : int=6
                The number of sprockets not connected to the DC motor on the tread
            * num_links : int=200
                The number of significant friction producing parts (typically pins or axles)
                that make up the tread
            * link_friction : float=0.6
                The kinetic coefficient of friction for tread based on the Normal force
                #TODO: There is a lot of work to agglomerate the total effects of friction in the treads. 
            * ground_lift_force : float=0.0
                The force necessary to lift the treads off the ground, a function of the ground's
                adhesive properties
        '''

        for key, value in kwargs.items():
            if key == "driver": self.driver = value
            if key == "follower": self.follower = value
            if key == "mass_links": self.mass_links = value
            if key == "num_followers": self.num_followers = value
            if key == "num_links": self.num_links = value
            if key == "link_friction": self.link_friciton = value
            if key == "ground_lift_force": self.ground_lift_force = value
        
        #Default Values
        if "driver" not in kwargs: self.driver = Sprocket()
        if "follower" not in kwargs: self.follower = Sprocket()
        if "mass_links" not in kwargs: self.mass_links = 0.907
        if "num_followers" not in kwargs: self.num_followers = 6
        if "num_links" not in kwargs: self.num_links = 200
        if "link_friction" not in kwargs: self.link_friction = 0.60
        if "ground_lift_force" not in kwargs: self.ground_lift_force = 0.0

        self.mass = self.driver.mass + self.num_followers*self.follower.mass + self.mass_links
        self.resistance_force = self.calcRollingFriction(self.link_friciton, self.mass_links, self.num_links) + self.ground_lift_force
        self.MoI = self.calcMomentOfInertia()

    def calcTorqueFriction(self):
        ''' Calculates the torque friction generated during motion (kinetic, not static), **UNITS ARE MKGS**. 
        Reference: https://www.linearmotiontips.com/how-to-calculate-motor-drive-torque-for-belt-and-pulley-systems/
        '''
        g = 9.81 #m/s^2
        link_torque_friction = self.mu * self.mass_links * g * self.driver.radius
        driver_torque_friction = self.driver.calcTorqueFriction()
        flwr_torque_friction = self.follower.calcTorqueFriction()
        return link_torque_friction + driver_torque_friction + self.num_followers * flwr_torque_friction

    def calcMomentOfInertia(self):
        ''' Calculates the total moment of inertia for the tread system. Reference: 
        https://www.linearmotiontips.com/how-to-account-for-belt-and-pulley-inertia-during-system-design/
        '''
        J_driver = self.driver.MoI
        J_follower = self.follower.MoI
        J_links = self.mass_links * self.driver.radius ** 2
        return J_driver + J_follower + J_links
