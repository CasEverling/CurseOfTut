conslisions_checked_on_frame: set = set()
chunks: dict = {}


class Entity:
	
	def __init__ (self):
		self.foces = [0,0] # forces i^ and j^
		self.acceleration = [0,0] # acceleration i^ and j^
		self.velocity = [0,0] # velocity i^ and j^
		self.position = [0,0] # position i^ and j^
		self.mass = 10 #mass in Kg
	
	def follow_target(self):
		...
		
	def spread(entity1, entity2):
		...
	

		
class Chunk:
	chunks = {}
	
	def __init__ (self, id):
		chunks[id] = self
		
	def __get_item__ (self, id):
		chunks[id]
	
    def __gettat
		
    



def getTeamMateColisionDetection(entity, team):
	chunk = entity.get_chunk(int)
	for i in range(i-1,i+2):
		for j in range(i-1, 1+2):
			for entity2 in chunk[f'{min(i,j)}x{max(i,j)}'].get_team(team):
				distance = entity.distance_from(entity2.pos)
				min_distance = (entity.radius + entity2.radius)
				if distance < 2*(entity.radius + entity2.radius):
				    Entity.spread(entity, entity2)
					
					
			
			
	
