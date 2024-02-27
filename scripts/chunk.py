from typing import Dict, Set, Tuple, List
from dataclasses import dataclass

from scripts.entity import Entity
from scripts.objects import Object
from scripts.light_system import LightObject

@dataclass
class Chunk:
    chunk_id: str
    attacks: Set[Object]
    entities: Set[Entity]

class ChunkSystem:
    chunks = {}
    chunk_ids = []
    def __init__(self, chunk_size: int, map_size: Tuple[int,int]):
        self.chunk_size: int = chunk_size
        for i in range(int(map_size[0]//chunk_size)+1):
            for j in range(int(map_size[1]//chunk_size+1)):
                self.chunks[f'{i},{j}'] = Chunk(f'{i},{j}', set(), set())
                self.chunk_ids.append(f'{i},{j}')

    
    def coord_to_chunk(self, coord: List[int]):
        return f'{int(coord[0]//self.chunk_size)},{int(coord[1]//self.chunk_size)}'
    
    def get_adjacent_chunks(self, chunk_id:str):
        x, y = [int(i) for i in chunk_id.split(',')]
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                try:
                    yield self.chunks[f'{i},{j}']
                except:
                    pass
    
    def add(self, entity = None, attack = None):
        chunk_id = self.coord_to_chunk(entity.pos)
        try:
            if entity:
                self.chunks[chunk_id].entities.add(entity)
            else:
                self.chunks[chunk_id].attacks.add(attack)
        except:
            if entity:
                self.chunks[chunk_id] = Chunk(chunk_id, set(), {entity,})
            else:
                self.chunks[chunk_id] = Chunk(chunk_id, {attack,}, set())
            self.chunk_ids.append(chunk_id)

    def remove(self, entity = None, attack = None):
        chunk_id = self.coord_to_chunk(entity.pos)
        if entity:
            self.chunks[chunk_id].entities.remove(entity)
        else:
            self.chunks[chunk_id].attacks.remove(attack)

    

        
