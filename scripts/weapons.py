from scripts.collisions import is_colliding, Colider
import math, pygame

class Weapon:
    def __init__ (self, owner, texture, attack_range, damage, durability, cooldown, attack_duration, stamina_cost):
        self.stamina_cost = stamina_cost
        self.attack_duration = attack_duration
        self.owner = owner
        self.texture = texture
        self.damage = damage
        self.durability = durability
        self.range = attack_range
        self.attacking = 0
        self.colldown = cooldown

    def is_colliding(self):
        ...

class Spike(Weapon):
    def __init__(self, owner, texture = 'spike', range = 60, damage = 20, durability = -1, cooldown = 30, attack_duration = 3, stamina_cost = 20):
        super().__init__(owner, texture, range, damage, durability, cooldown, attack_duration, stamina_cost)
        self.angle = None
        self.pos = None
        self.sound = pygame.mixer.Sound('spike.wav')
        self.sprite = pygame.transform.smoothscale(self.owner.game.textures['spike_texture'], 2*(2*self.range,))
        self.current_sprite = None

    def is_colliding(self, entity) -> bool:
        if not self.attacking:
            return False
        collision = is_colliding(Colider(0, 1, self.owner.pos, radius = self.owner.radius + 700), entity)

        if abs(math.degrees(self.angle)) < 90:
            if entity.pos[0] + entity.radius + 0.3 * self.owner.radius < self.pos[0]:
                return False
        else:
            if entity.pos[0] - entity.radius - 0.3 * self.owner.radius > self.pos[0]:
                return False
        
        distance = lambda x, y: abs(math.tan(self.angle)*(x-self.pos[0]) - y + self.pos[1])*math.cos(self.angle)
        if  -entity.radius -0.3 * self.owner.radius < distance(*entity.pos) < entity.radius + 0.3 * self.owner.radius:  
            entity.damage_sound.play()
            return True
        
        return False


    def attack(self):
        if self.owner.stamina < self.stamina_cost:
            return
        self.pos = tuple(self.owner.position)
        self.angle = math.radians(-self.owner.facing_direction)
        self.owner.game.attacks.add(self)
        self.attacking = 1
        self.owner.stamina -= self.stamina_cost
        self.sound.play()
        self.current_sprite = pygame.transform.rotate(self.sprite, (-math.degrees(self.angle)))

        
    def update(self):
        if self.attacking > self.attack_duration:
            self.owner.game.attacks.remove(self)
            self.attacking = 0
        elif self.attacking:
            self.attacking += 1
            f = lambda x: math.tan(self.angle)*x + self.pos[1] - self.pos[0]*math.tan(self.angle)
            self.owner.game.d.blit(
                self.current_sprite,
                [self.owner.pos[0] - self.current_sprite.get_width()/2, self.owner.pos[1]-self.current_sprite.get_height()/2]
            )

class Crown(Weapon):
    def __init__(self, owner=None, texture='crown_texture', attack_range = 0, damage = 100, durability = 9, cooldown = 0, attack_duration = 1, stamina_cost = 1):
        super().__init__(owner, texture, attack_range, damage, durability, cooldown, attack_duration, stamina_cost)
    
    def update(self):
        pass