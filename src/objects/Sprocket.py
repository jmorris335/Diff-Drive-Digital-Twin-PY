class Sprocket:
    ''' Represents a sprocket used in a treaded vehicle.
    By default this class represents the T-Rex Robotic platform designed by DAGU robotics, 
    shown here: https://web.archive.org/web/20220110180229/http://www.dagurobot.com/RS035
    '''

    def __init__(self, **kwargs):
        '''
        Keyword Arguments:  
        ---
            * mass : float=0.2
                The total mass of the sprocket, including axles and pins (units of mass)
            * radius : float=2.
                Distance from the center of the sprocket to the pitch point, AKA pitch radius (units of length)
            * axle_radius : float=0.5
                Distance from the center of the sprocket to the inner rotational surface (units of length)
            * rolling_friction : float=0.6
                The kinetic coefficient of friction for sprocket based on the Normal force
                #TODO: There is a lot of work to agglomerate the total effects of friction in the treads. 
        '''

        for key, value in kwargs.items():
            if key == "mass": self.mass = value
            if key == "radius": self.radius = value
            if key == "axle_radius": self.axle_radius = value
            if key == "rolling_friction": self.link_friciton = value
        
        #Default Values
        if "mass" not in kwargs: self.mass = 0.2
        if "radius" not in kwargs: self.radius = 2.
        if "axle_radius" not in kwargs: self.axle_radius = 0.5
        if "rolling_friction" not in kwargs: self.rolling_friction = 0.60

        self.MoI = self.calcMomentOfInertia(self.mass, self.radius, self.axle_radius)
        self.torque_friction_kinetic = self.calcTorqueFriction(self.rolling_friction, self.mass, self.axle_radius)

    @staticmethod
    def calcMomentOfInertia(mass, radius, axle_radius):
        ''' Returns the moment of inertia for the sprocket (assuming the sprocket is a hollow cylinder)'''
        return 1 / 2 * mass * (radius ** 2 + axle_radius ** 2)

    @staticmethod
    def calcTorqueFriction(mu, mass, axle_radius):
        ''' Calculates the torque friction producted by the rotating sprocket, **UNITS MUST BE MKGS**'''
        g = 9.81 #m/s^2
        return mu * mass * g * axle_radius
