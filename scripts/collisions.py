from typing import Dict, List, Tuple
import math

class Colider:
    def __init__ (self, mass: int = 0, t_collider: int = 1, pos: List[int] = [0,0], radius = 0, size = [0,0]):
        self.pos = pos
        self.t_collider = t_collider
        self.mass = mass

        if t_collider:
            self.radius = radius

        else:
            self.size = size
    
def is_colliding(object1: Colider, object2: Colider) -> Dict[str,int]:
    collide: bool = False
    angle_of_collision: int = None

    #caso os dois objetos sejam circulares
    if object1.t_collider and object2.t_collider:

        #confere a se a distancia entre os centros dos
        x, y = object1.pos[0] - object2.pos[0], object1.pos[1] - object2.pos[1]
        if (x*x + y*y) < (object1.radius + object2.radius)**2:
            collide = True
            angle_of_collision = -math.atan2(y,x)
        
    #caso um objeto seja circular e um seja retancular
    elif object1.t_collider or object2.t_collider:
        
        #caso o objeto cirsular seja object2, inverte as variaveis
        if object2.t_collider:
            object2, object1 = object1, object2
        
        #confere se o circulo colide com uma circunderencia circunscrita no quadrado
        if (object1.pos[0] - (object2.pos[0] + object2.size[0]/2))**2 + (object1.pos[1] - (object2.pos[1] + object2.size[1]/2))**2 < (object1.radius + ((object2.size[0]/2)**2 + (object2.size[1]/2)**2)**(1/2))**2:

            #confere se um quadrado circusscrito no circulo colide com o retanculo
            return is_colliding(Colider(object1.mass, 0, [pos-object1.radius for pos in object1.pos], size=2*[object1.radius*2]), object2)

    #caso os dois objetos sejam retangulares
    else:
        # cria uma lista com os verices superior esquerdo e inferiordireito
        vertexes1: List[Tuple[int, int]] = [object1.pos, tuple([object1.pos[i] + object1.size[i] for i in range(2)])]
        vertexes2: List[Tuple[int, int]] = [object2.pos, tuple([object2.pos[i] + object2.size[i] for i in range(2)])]
        collide = True

        #se estiver muito para a direita ou esquerda, nao colide
        if vertexes1[1][0] < vertexes2[0][0] or vertexes2[1][0] < vertexes1[0][0]:
            collide = False
        
        #se estiver muito para cima ou para baixo, nao colide
        elif vertexes1[1][1] < vertexes2[0][1] or vertexes2[1][1] < vertexes1[0][1]:
            collide = False
            
    # O angulo de colisao apenas e relevante para colisao de circulos
    return {
        'colliding': collide,
        'type': object1.t_collider + object2.t_collider,
        'angle': angle_of_collision,
        }

if __name__ == '__main__':
    print('Hello world!')

    a = Colider(0, 1, [0,0], radius = 10)
    b = Colider(0, 0, [1,0], size = [4,4])

    print(is_colliding(a,b))

