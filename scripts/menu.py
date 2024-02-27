import time, pygame

class Menu:
    setas = [0,0,0,0]
    sound_effect = pygame.mixer.Sound('menu_effect_1.wav')
    def __init__ (self, game, display, sprites, duration):
        self.sprites = sprites
        self.index = 0
        self.duration = duration
        self.display = display
        self.game = game
    
    def close(self):
        ...

    def update(self):
        self.display.blit(self.game.textures['menu_bg'], (0,0))
        self.display.blit(self.sprites[self.index], ((self.display.get_width()-self.display.get_height())/2,0), special_flags = pygame.BLEND_RGB_SUB)
        

class SelectionMenu(Menu):
    def __init__(self, game, display, sprites, duration):
        super().__init__(game, display, sprites, duration)
        self.p_click = False
        self.click = False

    def update(self):
        self.p_click = self.click
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    self.game.main_menu_run = False
                    self.sound_effect.play()
                if event.button == 1:
                    self.game.main_menu_run = False
                    self.index = -1
                    self.sound_effect.play()

        if abs(x:=self.game.p.joystick.get_axis(1)) > 0.7:
            self.click = True
        else:
            self.click = False

        if self.click and not self.p_click:
            if x < 0:
                if self.index > 0:
                    self.index -= 1 
                    self.sound_effect.play()
            elif x > 0:
                if self.index < len(self.sprites)-1:
                    self.index += 1 
                    self.sound_effect.play()
        

        super().update()

class Info(Menu):
    def __init__(self, game, display, sprites, duration):
        super().__init__(game, display, sprites, duration)
        self.start_time = time.time()
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if time.time() - self.start_time > self.duration:
                    self.game.credits_menu_running = False
                    self.sound_effect.play()
        
        super().update()

class InfoTimed(Menu):
    def update(self):
        pygame.event.get()
        self.duration -= 1
        if self.duration <= 0:
            self.game.menu = False

        super().update()

class ConnectController(Menu):
    def update(self):
        pygame.event.get()
        super().update()
        
