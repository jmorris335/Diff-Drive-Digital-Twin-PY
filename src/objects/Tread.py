from src.objects.Sprocket import Sprocket

class Tread:
    def __init__(self, driver: Sprocket, follower: Sprocket, num_followers: int=4):
        self.driver = driver
        self.follower = follower
        self.num_followers = num_followers 

    