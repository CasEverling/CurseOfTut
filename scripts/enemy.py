import math, pygame, time, random

from scripts.entity import Entity
from scripts.follower import Follower

class Bot(Entity):
    def behavior_manager(self):
        pass

    def change_behavior(self):
        pass

    def set_target(self):
        ...

class Mummy (Bot, Follower):
    team = 0
    

    def __init__(self, game, texture: str, speed: float, **kwargs):
        super().__init__(game, texture, speed, **kwargs)
        self.sounds = [pygame.mixer.Sound(f'm{i+1}.wav') for i in range(3)]
        self.target = None
        self.life = 10
        self.last_step = time.time()
        self.damage_sound = pygame.mixer.Sound('damage0.wav')
    
    def update(self):
        if self.t_invencible:
            self.t_invencible -= 1

        if self.life <= 0:
            self.game.del_items.add(self)

        if not self.target:
            self.set_target()
        else:
            self.follow()
        self.update_knematics()

        if time.time()-self.last_step >= self.speed/2*self.game.tile_size:
            self.step_sound.play()
            self.last_step = time.time()

        match x:=random.randint(0,300):
            case 0|1|2:
                self.sounds[x].play()

    def set_target(self):
        closest = None
        distance = None

        for chunk in self.game.chunksystem.chunks.values():
            for entity in chunk.entities:
                if entity.team != self.team:
                    if distance:
                        if distance*distance > (self.position[0]-entity.position[0])**2 + (self.position[1]-entity.position[1])**2:
                            closest = entity
                            distance = ((self.position[0]-entity.position[0])**2 + (self.position[1]-entity.position[1])**2)**(1/2)
                    else:
                        closest = entity
                        distance = ((self.position[0]-entity.position[0])**2 + (self.position[1]-entity.position[1])**2)**(1/2)

        self.target = closest


    def draw(self, surface):
        current_sprite = pygame.transform.rotate(self.game.textures[self.texture], self.facing_direction)
        current_sprite_size = current_sprite.get_width()
        surface.blit(
            current_sprite,
            [i - current_sprite_size/2 for i in self.pos],
            )
    
    def receive_damage(self, weapon):
        if self.t_invencible:
            return
        self.life -= weapon.damage
        self.t_invencible = self.invencible
