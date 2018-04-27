from classes.cube import Cube
from classes.pyramid import Pyramid

class Scene:

	cube_data = [(0, 0, 0, 15, 0.5, 15), (0, 1, 0, 1, 1, 1), (0, 2, 0, 1, 1, 1), (0, 3, 0, 1, 1, 1), (-1, 1, 0, 1, 1, 1), (1, 1, 0, 1, 1, 1), (0, 1, -1, 1, 1, 1), (0, 1, 1, 1, 1, 1), (0, 1, 2, 1, 1, 1)]
	cube_data += [(0, 1, 4, 7, 1, 1), (-3, 1, 0, 1, 1, 7), (3, 1, 0, 1, 1, 7)]
	pyramid_data = [(0, 4, 0, 1, 1, 1), (-1, 2, 0, 1, 1, 1), (1, 2, 0, 1, 1, 1)]
	entities = list()
	camera = None

	def __init__(self, cam):
		self.cam = cam
		self.entities = [Cube((x, y, z), (sx, sy, sz)) for x, y, z, sx, sy, sz in self.cube_data]
		self.entities += [Pyramid((x, y, z), (sx, sy, sz)) for x, y, z, sx, sy, sz in self.pyramid_data]

	def getEntities(self):
		return self.entities

	def getCamera(self):
		return self.cam
