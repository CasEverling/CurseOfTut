from scripts.player import Player
from scripts.enemy import Mummy
from scripts.collisions import is_colliding
from scripts.light_system import LightObject, LightSystem
from scripts.weapons import Spike, Crown
from scripts.menu import *
from scripts.collectasble import Collectable
from scripts.chunk import Chunk, ChunkSystem

import pygame

import time
import random
import screeninfo
import os
import json
import math

class Game:
    transition_duration = 15
    # Game Settings #

    def __init__(self) -> None:
        self.get_screen_size()
        self.tile_size = self.screen_size[1]/10
        self.get_screen_size()
        import pygame
        pygame.init()
        pygame.font.init()

        self.load_textures()

        self.c = pygame.time.Clock()
        pygame.mixer.music.load('menu_music.mp3')
        pygame.mixer.music.set_volume(0.08)
        pygame.mixer.music.play(-1)

    def initilize(self):
        pygame.init()

        self.get_screen_size()
        pygame.init()

        self.load_textures()

        self.s = pygame.display.set_mode(self.screen_size, flags=pygame.FULLSCREEN)
        self.d = pygame.surface.Surface((int(50*self.tile_size), int(50*self.tile_size)))
        self.r = True
        self.p = Player(
            self, 'player_texture', self.tile_size/6, 
            mass = 0, 
            t_collider = 1, 
            pos = [0,0],
            radius = self.tile_size/2,
            )
        
        
        self.joystick_screen()
        self.p.input_mapping()
        self.c = pygame.time.Clock()

    def load_textures(self):
        def change_color_key(surface, color=(255,255,255)):
            surface.set_colorkey(color)
            return surface
        self.textures = {
            'player_texture': pygame.transform.smoothscale(pygame.image.load(os.path.join('Images','explorer.png')), (self.tile_size, self.tile_size)),
            'mummy_texture': pygame.transform.smoothscale(pygame.image.load(os.path.join('Images','mummy.png')), (self.tile_size, self.tile_size)),
            'background_texture': pygame.transform.smoothscale(pygame.image.load(os.path.join('Images','chao.jpeg')), self.screen_size),
            'menu_bg': pygame.transform.smoothscale(pygame.image.load(os.path.join('Images', 'menus', 'bg.png')), self.screen_size),
            'crown_texture': pygame.transform.smoothscale(pygame.image.load(os.path.join('Images', 'crown.png')), (self.tile_size, self.tile_size)),
            'spike_texture': pygame.image.load(os.path.join('Images', 'spike.png')),
            'connect_controller': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'ConnectController.png')))).to_surface(), 2*(self.screen_size[1],)),
            'm1': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'M1.png')))).to_surface(), 2*(self.screen_size[1],)),
            'm2': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'M2.png')))).to_surface(), 2*(self.screen_size[1],)),
            'm3': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'M3.png')))).to_surface(), 2*(self.screen_size[1],)),
            'e1': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'E1.png')))).to_surface(), 2*(self.screen_size[1],)),
            'e2': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'E2.png')))).to_surface(), 2*(self.screen_size[1],)),
            'e3': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'E3.png')))).to_surface(), 2*(self.screen_size[1],)),
            'g1': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'G1.png')))).to_surface(), 2*(self.screen_size[1],)),
            'g2': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'G2.png')))).to_surface(), 2*(self.screen_size[1],)),
            's': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'S.png')))).to_surface(), 2*(self.screen_size[1],)),
            'c': pygame.transform.smoothscale(pygame.mask.from_surface(change_color_key(pygame.image.load(os.path.join('Images', 'menus', 'C.png')))).to_surface(), 2*(self.screen_size[1],)),
        }

    def get_screen_size(self):
        monitor = screeninfo.get_monitors()[0]
        
        self.screen_size = (monitor.width, monitor.height)
        return self.screen_size

    # Gameplay #

    def build_arcade_level(self):      
        # Character Settings #
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
        self.p.pos[0], self.p.pos[1] = [size/2 for size in self.screen_size]
        self.n_mummys = 1

        # Light System #
        self.lights = LightSystem((230,230,230), self.d.get_size())
        self.lights.add_light_object(LightObject(self.p.position, int(5*self.tile_size), int(200), (20,40,50), int(self.tile_size/2)))

        # Backgroun Image #
        self.bg = self.d.copy()
        for i in range(self.bg.get_width()//(x := self.textures['background_texture'].get_width())+1):
            for j in range(self.bg.get_height()//(y := self.textures['background_texture'].get_height()) +1):
                self.bg.blit(self.textures['background_texture'], (i*x,j*y))

        # Collision Settings #
        self.chunksystem = ChunkSystem(4*self.tile_size, self.d.get_size())
        self.chunksystem.add(entity=self.p)
        self.chunksystem.add(entity=self.m)
        self.attacks = set()
        self.del_items = set()

        # Mob Spawn Settings #
        self.last_time = time.time()
        self.spawn_time = 7
        self.n_spawn_mummys = 1
        
        # Music Settings#
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        # Ending Game Settings #
        self.r = True
        self.p.life = 100
        self.crown = None

    def build_explore_level(self):
        self.build_arcade_level()
        self.chunksystem.add(a:=Collectable(
            weapown = Crown(),
            game = self, 
            texture = 'crown_texture',
            speed = 0,
            pos = [self.d.get_width()*(1 + 2*random.random())/3 -self.tile_size, self.d.get_width()*(1 + 2*random.random())/3 - self.tile_size],
            t_collider = 0,
            mass = 0,
            size = 2*(self.tile_size,),
        ))
        self.crown = a


    # Game Loop #

    def run_level(self):
        i = 0
        while self.r:
            # Looking for Joystick #
            if not self.p.joystick:
                self.joystick_screen()
            
            # Level Stuff #
            self.update_game()
            
            # Endings #
            if (self.p.life <= 0) or (type(self.p.weapon)==Crown):
                self.r = False
            
            # camera position #
                
            camera_coord = [-self.p.pos[0] + self.s.get_width()/2, -self.p.pos[1] + self.s.get_height()/2]
            if camera_coord[0] > 0:
                camera_coord[0] = 0
            elif camera_coord[0] < self.s.get_width() - self.d.get_width():
                camera_coord[0] = self.s.get_width() - self.d.get_width()
            if camera_coord[1] > 0:
                camera_coord[1] = 0
            elif camera_coord[1] < self.s.get_height() - self.d.get_height():
                camera_coord[1] = self.s.get_height() - self.d.get_height()

            # Load "Shaders" Effects #
            self.d.blit(self.lights.light_map, (0,0), special_flags=pygame.BLEND_RGB_SUB)

            # Blit Game on Screen #
            self.s.blit(self.d, camera_coord)

            # Blit UI #
            pygame.draw.rect(self.s, (255,0,0), pygame.rect.Rect(0,0,self.p.life*self.screen_size[0]/100, self.tile_size/10))
            pygame.draw.rect(self.s, (100,200,100), pygame.rect.Rect(0,self.tile_size/10,self.p.stamina*self.screen_size[0]/100, self.tile_size/10))
            self.transition_in(i)
            i += 1

            # Updates the game #
            pygame.display.flip()
            self.c.tick(30)
        
        # After Game #

        self.p.joystick.stop_rumble()
        self.transition_out()
        pygame.mixer.music.load('menu_music.mp3')
        pygame.mixer.music.set_volume(0.08)
        pygame.mixer.music.play(-1)

        if type(self.p.weapon) == Crown:
            return -1
        if self.crown:
            return 0
        return self.n_mummys

    def update_game(self):
        self.drawn_entities = set()
        self.chunks_checked = set()
        self.del_items = set()
        self.collisions_checked = set()
        self.p.manage_events(pygame.event.get())

        # Drawing Background #

        w, h = self.textures['background_texture'].get_size()
        for i in [0, 1 if self.p.pos[0]%w > 0.5*w else -1]:
            for j in [0, 1 if self.p.pos[1]%h > 0.5*h else -1]:
                self.d.blit(self.textures['background_texture'], (w* (self.p.pos[0]//w + i), h* (self.p.pos[1]//h + j)))

        self.d.blit(self.textures['background_texture'], (0,0))

        
        # Entity collision Detection #
        
        '''for entity in self.entities:
            self.collisions_checked.add(entity)
            for entity2 in self.entities:
                if entity2 in self.collisions_checked:
                    continue
                if type(entity) == type(entity2): # Colissions between mummys have no relevance
                    continue
                if is_colliding(entity, entity2)['colliding']:
                    if Player in [type(entity), type(entity2)]:
                        self.p.collision_effects([e for e in [entity, entity2] if type(e) != Player][0])
            for attack in self.attacks:
                if type(entity) == Mummy:
                    if attack.is_colliding(entity):
                        entity.receive_damage(attack)'''

 
        for chunk in self.chunksystem.chunk_ids[:-1]:
            for entity in list(self.chunksystem.chunks[chunk].entities):
                if entity in self.drawn_entities:
                    continue
                self.chunksystem.remove(entity)
                entity.update()
                entity.draw(self.d)
                self.chunksystem.add(entity)
                self.drawn_entities.add(entity)
                
                

        '''for chunk1 in self.chunksystem.chunks.keys():
            chunk1 = self.chunksystem.chunks[chunk1]
            self.chunks_checked.add(chunk1.chunk_id)
            for chunk2 in self.chunksystem.get_adjacent_chunks(chunk1.chunk_id):
                if chunk2.chunk_id in self.chunks_checked:
                    continue
                for entity in chunk1.entities.union(chunk2.entities):
                    self.collisions_checked.add(entity)
                    for entity2 in chunk1.entities.union(chunk2.entities):
                        if entity2 in self.collisions_checked:
                            continue
                        if type(entity) == type(entity2): # Colissions between mummys have no relevance
                            continue
                        if is_colliding(entity, entity2)['colliding']:
                            if Player in [type(entity), type(entity2)]:
                                self.p.collision_effects([e for e in [entity, entity2] if type(e) != Player][0])
                    if type(entity) == Mummy:
                        for attack in self.attacks:                   
                            if attack.is_colliding(entity):
                                entity.receive_damage(attack)'''
        
        # Collisions of entitys and enemys has, so far no effect #
        # Calculate collisions between entities and player #
        for chunk in self.chunksystem.get_adjacent_chunks(self.chunksystem.coord_to_chunk(self.p.pos)):
            for entity in list(chunk.entities):
                if is_colliding(self.p, entity)['colliding']:
                    self.p.collision_effects(entity)
        
        # Calculate attacks #
        for attack in self.attacks:
            for chunk in self.chunksystem.get_adjacent_chunks(self.chunksystem.coord_to_chunk(self.p.pos)):
                    for entity in list(chunk.entities):
                        if type(entity) != Player:
                            if attack.is_colliding(entity):
                                entity.receive_damage(attack)


        
        # Deleting dead and collected entities #
        for del_item in self.del_items:
            self.chunksystem.remove(del_item)
            del(del_item)
                    

        if time.time() - self.last_time > self.spawn_time:
            for _ in range(int(self.n_spawn_mummys)):
                mummy_angle = -math.pi + 2*math.pi*random.random()
                if abs(mummy_angle) == math.pi/2:
                    mummy_angle += 0.01
                distance = 6*self.tile_size + self.n_spawn_mummys*self.tile_size*random.random()
                x = self.p.pos[0] + distance*math.cos(mummy_angle)
                y = self.p.pos[1] + distance*math.sin(mummy_angle)
                self.chunksystem.add(Mummy(
                    self, 'mummy_texture', random.random()*self.p.speed*0.6 + self.p.speed*0.2,
                    mass = 0, 
                    t_collider = 1, 
                    pos = [x, y],
                    radius = self.tile_size/2,
                ))
                self.n_mummys += 1
            
            self.last_time = time.time()
            self.spawn_time /= 1.3
            if self.spawn_time < 1.5:
                self.spawn_time = 1.5
                self.n_spawn_mummys += 0.1

    # Transitions #
                
    def transition_out(self):
        t_surface = self.s.copy()
        for _ in range(self.transition_duration):
            pygame.event.get()
            t_surface.fill(3*(255/self.transition_duration,))
            self.s.blit(t_surface, (0,0), special_flags=pygame.BLEND_RGB_SUB)
            pygame.display.flip()
            self.c.tick(30)
    
    def transition_in(self, i):
        if i <= self.transition_duration:
            t_surface = self.s.copy()
            t_surface.fill(3*((self.transition_duration-i)*255/self.transition_duration,))
            self.s.blit(t_surface, (0,0), special_flags=pygame.BLEND_RGB_SUB)

    # Menus #
                
    def joystick_screen(self):
        i = 0
        menu = ConnectController(self, self.s, [self.textures['connect_controller']], 0)
        while not self.p.joystick:
            if pygame.joystick.get_count():
                self.p.set_joystick(0)
            menu.update()
            self.transition_in(i)
            i += 1
            pygame.display.flip()
            self.c.tick(30)
        self.transition_out()  

    def initial_menu(self):
        i = 0
        menu = SelectionMenu(self, self.s, [self.textures['m1'],self.textures['m2'],self.textures['m3']], 0)
        self.main_menu_run = True
        while self.main_menu_run:
            menu.update()
            self.transition_in(i)
            i += 1
            pygame.display.flip()
            self.c.tick(30)
        self.transition_out()  
        return menu.index

    def game_mode_menu(self):
        i = 0
        menu = SelectionMenu(self, self.s, [self.textures['g1'],self.textures['g2']], 0)
        self.main_menu_run = True
        while self.main_menu_run:
            menu.update()
            self.transition_in(i)
            i += 1
            pygame.display.flip()
            self.c.tick(30)
        self.transition_out()  
        return menu.index
    
    def explanation_menu(self):
        i = 0
        menu = InfoTimed(self, self.s, [self.textures['s']], 150)
        self.menu = True
        while self.menu:
            menu.update()
            self.transition_in(i)
            i += 1
            pygame.display.flip()
            self.c.tick(30)
        self.transition_out()  

    def credits_menu(self):
        i = 0
        menu = Info(self, self.s, [self.textures['c']], 0)
        self.credits_menu_running = True
        while self.credits_menu_running:
            menu.update()
            pygame.display.flip()
            self.transition_in(i)
            i += 1
            self.c.tick(30)
        self.transition_out()  
        return menu.index
    
    def lose_menu(self):
        i = 0
        menu = Info(self, self.s, [self.textures['e1']], 0)
        self.credits_menu_running = True
        while self.credits_menu_running:
            menu.update()
            self.transition_in(i)
            i += 1
            pygame.display.flip()
            self.c.tick(30)
        self.transition_out()  
        return menu.index
    
    def win_menu(self):
        i = 0
        menu = Info(self, self.s, [self.textures['e2']], 0)
        self.credits_menu_running = True
        with open('configs.json', 'rb') as file:
            info = json.load(file)
        info['gamemodes']['arcade'] = 1
        with open('configs.json', 'w') as file:
            json.dump(info, file)
        while self.credits_menu_running:
            menu.update()
            self.transition_in(i)
            i += 1
            pygame.display.flip()
            self.c.tick(30)   
        self.transition_out()  
    
    def score_menu(self, score):
        i = 0
        menu = Info(self, self.s, [self.textures['e3']], 2)
        self.credits_menu_running = True
        font = pygame.font.Font(pygame.font.get_default_font(), int(3.5*self.tile_size))
        text_surface = font.render(str(score),True, (0,0,0))
        
        while self.credits_menu_running:
            menu.update()
            self.s.blit(text_surface, ((self.s.get_width()-text_surface.get_width())/2, ((self.s.get_height()-text_surface.get_height())/2)))
            self.transition_in(i)
            i += 1
            pygame.display.flip()
            self.c.tick(30)
        return menu.index

    # Game Manager #

    def run(self):
        self.r1 = True
        while self.r1:
            match (self.initial_menu()):
                case 0:
                    self.initilize()
                    with open('configs.json', 'rb') as file:
                        info = json.load(file)
                    if info['gamemodes']['arcade']:
                        match (self.game_mode_menu()):
                            case 0:
                                self.explanation_menu()
                                self.build_explore_level()
                            case 1:
                                self.build_arcade_level()
                            case _:
                                continue
                    else: 
                        self.explanation_menu()
                        self.build_explore_level()
                    match (score := self.run_level()):
                        case -1:
                            self.win_menu()
                        case 0:
                            self.lose_menu()
                        case _:
                            self.score_menu(score)
                case 1:
                    self.credits_menu()
                case 2:
                    self.r1 = False
                    self.transition_out()
                case _:
                    continue
        pygame.quit()





if __name__ == '__main__':
    game = Game()
    game.initilize()
    game.run()
