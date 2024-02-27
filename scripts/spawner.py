import pygame

class Spwner:
    def __init__(self, game, pos, size, texture, t_mob):
        self.game = game
        self.pos = pos
        self.size = size
        self.texture = texture
        self.t_mob = t_mob

    @property
    def surface(self):
        return pygame.transform.smoothscale(self.game.get_texture(self.texture), size=self.size)
    
    def spawn_mob(self):
        self.game.chunk.position


