import pygame
from typing import List, Tuple


try:
    if not pygame.get_init():
        pygame.init()
except:
    import pygame
    if not pygame.get_init():
        pygame.init()


class LightObject:
    def __init__ (self, pos: List[int], radius: int, n_circles: int, color: Tuple[int,int,int], platot_size: int):
        self.pos = pos
        self.n_circles = n_circles
        self.color = color
        self.radius = radius
        self.platot_size = platot_size


class LightSystem:
    def __init__ (self, ambient_light, size):
        self.ambient_light = ambient_light
        self.light_objects: List[LightObject] = []
        self._light_map = pygame.surface.Surface(size)
    
    def draw_lights(self):
        for light_source in self.light_objects:
            self._light_map.blit(self.draw_light(light_source.radius, light_source.color, light_source.n_circles, light_source.platot_size), [pos - light_source.radius for pos in light_source.pos])
    
    def draw_light(self, radius, color, n_circles, platot_size):
        r, g, b = color
        er, eg, eb = self.ambient_light
        circular_light = pygame.surface.Surface((2*radius,2*radius))
        circular_light.fill(self.ambient_light)
        for i in range(n_circles):
            percentage = i / n_circles
            pygame.draw.circle(circular_light, (er - percentage*(er - r), eg - percentage*(eg - g), eb - percentage*(eb - b)), (radius,radius), radius = platot_size+(n_circles-i)*(radius-platot_size)/n_circles)
        pygame.draw.circle(circular_light, color, (radius,radius), radius = platot_size)

        return circular_light

    def create_light_object(self, pos, n_circles, color):
        self.light_objects.append(
            LightObject(pos, n_circles, color)
        )

    def add_light_object(self, light_object: LightObject):
        self.light_objects.append(
            light_object
        )

    @property
    def light_map(self) -> pygame.surface.Surface:
        self._light_map.fill(self.ambient_light)
        self.draw_lights()
        return self._light_map
