from scripts.player import Player
from scripts.enemy import Mummy
from scripts.collisions import is_colliding
from scripts.light_system import LightObject, LightSystem
from scripts.weapons import Spike

import pygame
import sys
import tkinter
import time
import random
import screeninfo

class Game:
    def __init__(self) -> None:
        self.get_screen_size()
        self.tile_size = self.screen_size[1]/10

    def initilize(self):
        pygame.init()

        self.display = pygame.display.set_mode((1000,500))

    def load_textures(self):
        self.textures = {
            'player_texture': pygame.transform.smoothscale(pygame.image.load('explorer.png'), (self.tile_size, self.tile_size)),
            'mummy_texture': pygame.transform.smoothscale(pygame.image.load('mummy.png'), (self.tile_size, self.tile_size)),
            'background_texture': pygame.transform.smoothscale(pygame.image.load('chao.jpeg'), self.screen_size)
        }

    def get_screen_size(self):
        monitor = screeninfo.get_monitors()[0]
        
        self.screen_size = (monitor.width, monitor.height)
        return self.screen_size

    def run_player(self):
        print('Hello World!')
        self.get_screen_size()
        import pygame
        pygame.init()

        self.load_textures()

        self.d = pygame.display.set_mode(self.screen_size, flags=pygame.FULLSCREEN)
        self.r = True
        self.p = Player(
            self, 'player_texture', self.tile_size/6, 
            mass = 0, 
            t_collider = 1, 
            pos = [0,0],
            radius = self.tile_size/2,
            )
        self.p.input_mapping()
        self.p.weapon = Spike(
            self.p,
            range=3*self.tile_size,
        )
        self.m = Mummy(
            self, 'mummy_texture', 5.0,
            mass = 0, 
            t_collider = 1, 
            pos = [300,300],
            radius = self.tile_size/2,
        )
        self.n_mummys = 1
        self.lights = LightSystem((230,230,230), self.screen_size)
        self.lights.add_light_object(LightObject(self.p.position, int(5*self.tile_size), int(200), (20,40,50), int(self.tile_size/2)))

        self.entities = {self.p, self.m}
        self.p.set_joystick(0)
        c = pygame.time.Clock()

        self.last_time = time.time()
        self.spawn_time = 15
        self.attacks = set()

        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)

        self.del_items = set()

        while self.r:
            self.update_game()

            if self.p.life <= 0:
                self.r = False
            
            pygame.display.flip()
            c.tick(30)
        
        self.p.joystick.stop_rumble()
        time.sleep(0.5)
        self.p.joystick.quit()
        pygame.quit()
        print(self.n_mummys) 



    def update_game(self):
        self.del_items = set()
        self.p.manage_events(pygame.event.get())

        self.d.blit(self.textures['background_texture'], (0,0))
        
        for entity in self.entities:
            entity.update()
            entity.draw(self.display)

        self.d.blit(self.lights.light_map, (0,0), special_flags=pygame.BLEND_RGB_SUB)
        pygame.draw.rect(self.d, (255,0,0), pygame.rect.Rect(0,0,self.p.life*self.screen_size[0]/100, self.tile_size/10))
        pygame.draw.rect(self.d, (100,200,100), pygame.rect.Rect(0,self.tile_size/10,self.p.stamina*self.screen_size[0]/100, self.tile_size/10))

        for entity in self.entities:
            for entity2 in self.entities:
                if entity is entity2:
                    continue
                if is_colliding(entity, entity2)['colliding']:
                    if Player in [type(entity), type(entity2)]:
                        self.p.collision_effects([e for e in [entity, entity2] if type(e) != Player][0])
            for attack in self.attacks:
                if type(entity) == Mummy:
                    if attack.is_colliding(entity):
                        entity.receive_damage(attack)
        
        for del_item in self.del_items:
            self.entities.remove(del_item)
            del(del_item)
                    


        if time.time() - self.last_time > self.spawn_time:
            self.entities.add(Mummy(
                self, 'mummy_texture', random.random()*self.p.speed*0.6 + self.p.speed*0.2,
                mass = 0, 
                t_collider = 1, 
                pos = [self.display.get_width()*random.choice([1,0]), self.display.get_height()*random.choice([1,0])],
                radius = self.tile_size/2,
            ))
            self.n_mummys += 1
            
            self.last_time = time.time()
            self.spawn_time -= (max(0.1, self.spawn_time/10) if self.spawn_time > 0.5 else 0)


if __name__ == '__main__':
    game = Game()
    game.initilize()
    game.run_player()