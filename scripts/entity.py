#from abc import abstractmethod
from typing import List, Tuple
from scripts.collisions import Colider, is_colliding

import math, random, pygame

class Entity(Colider):
    
    def __init__ (self, game, texture: str, speed:float, invencible: int = 5,  **kwargs):
        self.step_sound = pygame.mixer.Sound('step.wav')
        super().__init__(**kwargs)
        self.texture = texture
        self.speed = speed
        self.game = game
        self.position: List[int] = self.pos
        self.velocity: List[int] = [0,0]
        self.acceleration: List[int] = [0,0]
        self.last_looking_direction = random.randint(-180, 181)
        self.invencible = invencible
        self.t_invencible = 0

    def update_knematics(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def check_colision(self):
        chunk: str = self.game.chunks.coord_to_chunk(self.pos)
        chunk_objects: List[Entity] = self.game.chunks[chunk].get_entities()

        for object in chunk_objects:
            if is_colliding(self, object):
                self.collision_effects(object)

    @property
    def facing_direction(self):
        if self.velocity[0] or self.velocity[1]:
            self.last_looking_direction = -180 * math.atan2(self.velocity[1],self.velocity[0]) / math.pi
        return self.last_looking_direction

    def collision_effects(self, collider):
        ...
    
    def update(self):
        ...

    def draw(self):
        ...

    def receive_damage(self, weapon):
        ...

    


    
