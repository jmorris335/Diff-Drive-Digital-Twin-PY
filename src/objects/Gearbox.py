class Gearbox:
    '''Represents a gearbox used in a treaded vehicle.
    By default this class represents the gearbox designed by x company,
    shown here: include website
    '''

    def __init__(self, **kwargs ):
        '''
        Keyword Arguments:
        ---
        * mass : float = 0.282
            The total mass of the gearbox, including the electrical wires connected to the motor (units of mass in kg)
        * gear reduction : float = 4.50
            Electric motor drives a 10-tooth gear that meshes with a 45-tooth gear, a reduction of 4.50:1 is achieved (45/10)
        * rolling friction: 0.6
            Found on internet about steel on steel contact is around 0.09 - 0.6
            Link: https://hypertextbook.com/facts/2005/steel.shtml
        * MOI : 
            MOI of the whole gearbox   
        
        # Masses and number of teeth for each gear
        # HY A = outer radius: 45 teeth, 14.05 mm; inner radius: 15 teeth, 5.05 mm; mass: 22 grams
        # HY B = outer radius: 53 teeth, 16.5 mm; inner radius: 15 teeth, 5.05 mm; mass: 29 grams
        # HY C = outer radius: 53 teeth, 16.5; inner radius: 40 teeth, 12.625 mm; mass: 42 grams
        # HY D = outer radius: 28 teeth, 9 mm; inner radius: None; mass: 20 grams
        # Motor and Spindle: outer radius: 10 teeth, 3.575 mm; inner radius: None; mass: 105 grams '''


        for key, value in kwargs.items():
            if key == "mass_a" : self.mass_a = value
            if key == "mass_b" : self.mass_b = value
            if key == "mass_c" : self.mass_c = value
            if key == "mass_d" : self.mass_d = value
            if key == "mass_motor" : self.mass_motor = value
            if key == "radius_a" : self.radius_a = value
            if key == "radius_b" : self.radius_b = value
            if key == "radius_c" : self.radius_c = value
            if key == "radius_d" : self.radius_d = value
            if key == "radius_motor" : self.radius_motor = value            
            if key == "inner_radius_a" : self.inner_radius_a = value
            if key == "inner_radius_b" : self.inner_radius_b = value
            if key == "inner_radius_c" : self.inner_radius_c = value
            if key == "inner_radius_d" : self.inner_radius_d = value
            if key == "inner_radius_motor" : self.inner_radius_motor = value
            if key == "rolling_friction_a" : self.rolling_friction_a = value
            if key == "rolling_friction_b" : self.rolling_friction_b = value
            if key == "rolling_friction_c" : self.rolling_friction_c = value
            if key == "rolling_friction_d" : self.rolling_friction_d = value
            if key == "rolling_friction_motor" : self.rolling_friction_motor = value
            
                
        # Default values
        # HY A gear
        if "mass_a" not in kwargs: self.mass_a = 0.022
        if "radius_a" not in kwargs: self.radius_a = 14.05
        if "inner_radius_a" not in kwargs:self.inner_radius_a = 5.05 
        if "rolling_friction_a" not in kwargs: self.rolling_friction_a = 0.6
            
         # HY B gear
        if "mass_b" not in kwargs: self.mass_b = 0.029
        if "radius_b"not in kwargs: self.radius_b = 16.5
        if "inner_radius_b" not in kwargs:self.inner_radius_b = 5.05
        if "rolling_friction_b" not in kwargs: self.rolling_friction_b = 0.6
            
         # HY C gear
        if "mass_c" not in kwargs: self.mass_c = 0.042
        if "radius_c" not in kwargs: self.radius_c = 16.5
        if "inner_radius_c" not in kwargs:self.inner_radius_c = 12.625 
        if "rolling_friction_c" not in kwargs: self.rolling_friction_c = 0.6
            
         # HY D gear
        if "mass_d" not in kwargs: self.mass_d = 0.020
        if "radius_d" not in kwargs: self.radius_d = 9
        if "inner_radius_d" not in kwargs:self.inner_radius_d = 3.575
        if "rolling_friction_d" not in kwargs: self.rolling_friction_d = 0.6
            
         # Motor
        if "mass_motor" not in kwargs: self.mass_motor = 0.105
        if "radius_motor"not in kwargs: self.radius_motor = 14.05
        if "inner_radius_motor" not in kwargs:self.inner_radius_motor = 5.05 
        if "rolling_friction_motor" not in kwargs: self.rolling_friction_motor = 0.6
            

        
    
    

