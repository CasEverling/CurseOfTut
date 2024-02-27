import math

class Follower:
    def follow(self):

        if not self.target:
            return
        
        angle = math.atan2(self.pos[1] - self.target.pos[1], self.pos[0] - self.target.pos[0])
        acceleration_module: float = self.velocity[0]**2 + self.velocity[1]**2

        self.acceleration[0] = 0 #acceleration_module*math.cos(angle) - self.velocity[0]
        self.acceleration[1] = 0 #acceleration_module*math.sin(angle) - self.velocity[1]

        self.velocity[0] = -self.speed*math.cos(angle)
        self.velocity[1] = -self.speed*math.sin(angle)