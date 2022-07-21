class Sprocket:
    def __init__(self, radius, mass):
        self.radius = radius
        self.mass = mass
        self.MoI = self.calcMomentOfInertia(self.mass, self.radius)

    @staticmethod
    def calcMomentOfInertia(mass, radius):
        return 1 / 2 * mass * radius ** 2