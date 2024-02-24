from typing import Tuple, List
import math
from scripts.light_system import LightObject, LightSystem

class A:
    def __init__ (self):
        self.pos = [0,0]

class FightBot:
    def __init__ (self, initial_position: List[A], enemys: List[List[A]], speed = 6, *args, **kwargs):
        self.pos: List[int,int] = initial_position
        self.enemys: List[List[int]] = enemys
        self.target: List[int,int] = None
        self.speed = speed
        self.looking_direction = 0

    def set_target (self):
        closest: List[int,int] = None
        closest_distance: float = None

        for list_enemys in self.enemys:
            for enemy in list_enemys:
                distance = ((enemy.pos[0] - self.pos[0])**2 + (enemy.pos[1]- self.pos[1])**2)**(1/2)
                if (not closest_distance) or (distance < closest_distance):
                    closest_distance = distance
                    closest = enemy
        
        self.target = closest
    
    def move(self):
        if self.target:
            tan = (self.pos[1] - self.target.pos[1])/(self.pos[0] - self.target.pos[0]) if self.pos[0] != self.target.pos[0] else None
            cos = abs((1/(1 + tan**2))**(1/2)) if tan else 0
            sin = abs(tan*cos) if tan else 1 if self.pos[1] != self.target.pos[1] else 0

            self.pos[0] += (self.speed*cos) * (-1 if (self.pos[0] - self.target.pos[0]) > 0 else 1)
            self.pos[1] += self.speed*sin  * (-1 if (self.pos[1] - self.target.pos[1]) > 0 else 1)

            self.looking_direction = 180*math.atan(tan)/math.pi

            
            self.looking_direction += 2*(180 - self.looking_direction)

            if self.pos[0] > self.target.pos[0]:
                self.looking_direction += 180



    def behaviors (self):
        pass

if __name__ == '__main__':
    import pygame, time, random
    pygame.init()
    screen_width, screen_height = screen_size = (1000,500)
    display = pygame.display.set_mode(screen_size, flags=pygame.FULLSCREEN)
    running = True
    player = A()
    player.pos = [screen_width/2, screen_height/2]
    clock = pygame.time.Clock()
    last_time = time.time()
    spawn_time = 10
    enemys = []
    player_speed = 8
    joysticks = [pygame.joystick.Joystick(n) for n in range(pygame.joystick.get_count())]

    light_map = LightSystem(
        ambient_light=(100, 100, 100),
        size= (display.get_width(), display.get_height())
    )
    
    player_light = LightObject(
        pos = player.pos,
        radius = 300,
        color = (0,50,50),
        platot_size = 0,
        n_circles= 200,
    )

    light_map.add_light_object(player_light)

    

    velocity = [0,0]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w:
                        velocity[1] -= player_speed
                    case pygame.K_s:
                        velocity[1] += player_speed
                    case pygame.K_a:
                        velocity[0] -= player_speed
                    case pygame.K_d:
                        velocity[0] += player_speed
            elif event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_w:
                        velocity[1] += player_speed
                    case pygame.K_s:
                        velocity[1] -= player_speed
                    case pygame.K_a:
                        velocity[0] += player_speed
                    case pygame.K_d:
                        velocity[0] -= player_speed
        
        #if abs(velocity[0]) == abs(velocity[1]):
        #    velocity[0] *= 1/(2)**(1/2)
        #    velocity[1] *= 1/(2)**(1/2)


        for joystick in joysticks:
            velocity[0] = (abs(x:=joystick.get_axis(0)) > 0.1) * player_speed * x
            velocity[1] += (abs(y:=joystick.get_axis(1)) > 0.1) * player_speed * y
        
        player.pos[0] += velocity[0]
        player.pos[1] += velocity[1]

        if player.pos[0] < 20:
            player.pos[0] = 20
        elif player.pos[0] > display.get_width() -20:
            player.pos[0] = display.get_width() - 20
        if player.pos[1] < 20:
            player.pos[1] = 20
        elif player.pos[1] > display.get_height() - 20:
            player.pos[1] = display.get_height() - 20
        
        display.fill((100,100,100))
        pygame.draw.circle(display, (100,50,50), [int(pos) for pos in player.pos], 20)        

        for enemy in enemys:
            enemy.move()
            pygame.draw.circle(display, (50,50,100), [int(pos) for pos in enemy.pos], 20)
            if -40 < ((enemy.pos[0] - player.pos[0])**2 + (enemy.pos[1]- player.pos[1])**2)**(1/2) < 40:
                running = False

        if time.time() - last_time > spawn_time:
            enemys.append(FightBot(
                initial_position=[(screen_width)*random.choice([1,0]),+ (screen_height)*random.choice([1,0])],
                enemys=[[player]],
                speed = player_speed*0.7,
            ))
            enemys[-1].set_target()
            last_time = time.time()
            spawn_time -= (max(0.1, spawn_time/10) if spawn_time > 0.1 else 0)

        display.blit(light_map.light_map, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    print(len(enemys))