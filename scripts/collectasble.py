from scripts.entity import Entity

class Collectable(Entity):
    team = -1
    def __init__(self, weapown, game, texture: str, speed: float, invencible: int = 5, **kwargs):
        super().__init__(game, texture, speed, invencible, **kwargs)
        self.weapon = weapown

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(
            self.game.textures[self.texture],
            self.pos,
        )
    