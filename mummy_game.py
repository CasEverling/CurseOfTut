import pygame, time, random, math
from fight_bot import A, FightBot
from scripts.light_system import LightObject, LightSystem


class MummyGame:
    def run():
        pass
    
    def set_game():
        pass

    def gameplay():
        pass

    def menu():
        pass

    def sound_menu():
        pass


if __name__ == '__main__':
    pygame.init()
    screen_width, screen_height = screen_size = (2000,1900)
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
    

    player_sprite = pygame.transform.smoothscale_by(pygame.image.load('explorer.png'), 0.04*screen_height/100)
    enemy_sprite = pygame.transform.smoothscale_by(pygame.image.load('mummy.png'), 0.04*screen_height/100)

    light_map = LightSystem(
        ambient_light=(210,)*3,
        size= (display.get_width(), display.get_height())
    )
    
    player_light = LightObject(
        pos = player.pos,
        radius = 250,
        color = (10,20,25),
        platot_size = 0,
        n_circles= 100,
    )

    light_map.add_light_object(player_light)

    bg_image = pygame.transform.smoothscale_by(x:=pygame.image.load('chao.jpeg'), display.get_width()/x.get_width())
    player_current_sprite = player_sprite
    velocity = [0,0]
    player.pos[0] = display.get_width()/2
    player.pos[1] = display.get_height()/2
    music = pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)
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
            velocity[1] = (abs(y:=joystick.get_axis(1)) > 0.1) * player_speed * y
        
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
        
        display.blit(bg_image, (0,0))


        if velocity[0]:
            player_looking_direction = 180 * math.atan(velocity[1]/velocity[0]) / math.pi
            player_looking_direction += 2*(180 - player_looking_direction)

            if velocity[0] < 0:
                player_looking_direction += 180

            player_current_sprite = pygame.transform.rotate(player_sprite, player_looking_direction)

        elif velocity[1]:
            player_looking_direction = -90 if velocity[1] > 0 else 90

        player_current_sprite_size = player_current_sprite.get_width()
        display.blit(
            player_current_sprite,
            [i - player_current_sprite_size/2 for i in player.pos],
            )

        for enemy in enemys:
            enemy.move()
            
            enemy_current_sprite = pygame.transform.rotate(enemy_sprite, enemy.looking_direction)
            enemy_current_sprite_size = enemy_current_sprite.get_width()
            display.blit(
                enemy_current_sprite,
                [i - enemy_current_sprite_size/2 for i in enemy.pos],
                )
            
            if -0.04*screen_height < ((enemy.pos[0] - player.pos[0])**2 + (enemy.pos[1]- player.pos[1])**2)**(1/2) < 0.04*screen_height:
                running = False

        if time.time() - last_time > spawn_time:
            enemys.append(FightBot(
                initial_position=[(screen_width)*random.choice([1,0]),+ (screen_height)*random.choice([1,0])],
                enemys=[[player]],
                speed = player_speed*0.7,
            ))
            enemys[-1].set_target()
            last_time = time.time()
            spawn_time -= (max(0.1, spawn_time/10) if spawn_time > 0.5 else 0)

        display.blit(light_map.light_map, (0,0), special_flags=pygame.BLEND_RGB_SUB)
        pygame.display.flip()
        clock.tick(30)
    joysticks[0].rumble(3,5,1)
    time.sleep(1)
    joysticks[0].stop_rumble()
    pygame.quit()
    print(len(enemys))