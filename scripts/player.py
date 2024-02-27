from scripts.entity import Entity
from scripts.enemy import Mummy
from scripts.collectasble import Collectable

import pygame, time, random

class Player(Entity):

    def __init__(self, game, texture: str, speed: float, invencible: int = 5, **kwargs):
        super().__init__(game, texture, speed, invencible, **kwargs)
        self.last_step = time.time()
        self.team = 1
        self.life = 100
        self.weapon = None
        self.stamina = 100
        self.running = False
        self.rumbling = 0
        self.joystick = None
        self.damage_sounds = [pygame.mixer.Sound(f'damage{i+1}.wav') for i in range(3)]

    def set_joystick(self, id: int):
        self.joystick = pygame.joystick.Joystick(id)

    def update(self) -> None:
        if self.invencible > 0:
            self.invencible -= 1

        speed = self.speed
        if self.running:
            speed = 1.5 * self.speed
            self.stamina -= 2
            if self.stamina <= 0:
                self.running = False
        else:
            self.stamina = min(100, self.stamina+1)

        self.rumbling = max(0, self.rumbling-1)
            
        if self.life < 100:
            self.life += 0.01

        self.acceleration[0] = 0
        self.acceleration[1] = 0

        self.velocity[0] = (abs(x:=self.joystick.get_axis(0)) > 0.1) * x * speed
        self.velocity[1] = (abs(y:=self.joystick.get_axis(1)) > 0.1) * y * speed

        #update the position
        self.update_knematics()

        if self.weapon:
            self.weapon.update()
        
        if time.time()-self.last_step >= 2*self.speed/(self.game.tile_size):
            self.step_sound.play()
            self.last_step = time.time()
        
        

    def manage_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.r = False
                self.joystick.stop_rumble()
            elif event.type == pygame.KEYDOWN:
                try:
                    self.keys[event.key]()
                except:
                    pass
            elif event.type == pygame.JOYBUTTONDOWN:
                try:
                    self.buttons_down[event.button]()
                except:
                    pass
            elif event.type == pygame.JOYBUTTONUP:
                try:
                    self.buttons_up[event.button]()
                except:
                    pass

    def draw(self, surface):
        current_sprite = pygame.transform.rotate(self.game.textures[self.texture], self.facing_direction)
        current_sprite_size = current_sprite.get_width()
        surface.blit(
            current_sprite,
            [i - current_sprite_size/2 for i in self.pos],
            )

    def collision_effects(self, entity):
        if type(entity) is Mummy:
            if not self.invencible:
                self.life -= 10
                self.invencible = 30
                self.damage_sounds[2].play()
            self.life -= .51
            self.damage_sounds[random.randint(0,2)].play()
            if not self.rumbling:
                self.joystick.rumble(1,1,500)
                self.rumbling = 15
        elif type(entity) == Collectable:
            self.game.del_items.add(entity)
            a, self.weapon = self.weapon, entity.weapon
            del(a)
        

    def attack(self):
        if not self.weapon:
            return
    
    def input_mapping(self):
        self.keys = {
            pygame.K_ESCAPE: lambda: (setattr(self.game, 'r', False)),
        }
        self.buttons_down = {
            2: lambda: self.weapon.attack() if self.weapon else self.skip(),
            9: lambda: setattr(self, 'running', True),
        }
        self.buttons_up = {
            9: lambda: setattr(self, 'running', False),
        }

    def skip(self, *args, **kwargs):
        pass
        




        
