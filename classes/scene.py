from classes.cube import Cube
from classes.pyramid import Pyramid

class Scene:

	cube_data = [(0, 1, 0, 1, 1, 1), (0, 2, 0, 1, 1, 1), (0, 3, 0, 1, 1, 1), (-1, 1, 0, 1, 1, 1), (1, 1, 0, 1, 1, 1), (0, 1, -1, 1, 1, 1), (0, 1, 1, 1, 1, 1), (0, 1, 2, 1, 1, 1)]
	cube_data += [(0, 1, 4, 9, 1, 1), (-4, 1, 0, 1, 1, 9), (4, 1, 0, 1, 1, 9)]
	cube_data += [(0, 0, 0, 11, 1, 11), (0, -1, 0, 13, 1, 13), (0, -2, 0, 15, 1, 15)]
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
