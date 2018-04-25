import pygame

from classes.util import Util

class Mesh:

	vertices = (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
	edges = (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)
	faces = (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
	colors = (0, 255, 255), (255, 255, 0), (200, 200, 200), (255, 0, 255), (0, 0, 255), (0, 255, 0)
	pos = (0, 0, 0)
	minX, minY, minZ = 9999, 9999, 9999
	maxX, maxY, maxZ = -9999, -9999, -9999
	w, h, cx, cy, fov = 0, 0, 0, 0, 0

	def __init__(self, pos=(0, 0, 0), scale=(1, 1, 1)):
		self.pos = list(pos)
		x, y, z = pos
		self.vertices = [((x + X / 2 * scale[0]), (y + Y / 2 * scale[1]), (z + Z / 2 * scale[2])) for X, Y, Z in self.vertices]
		self.w, self.h = pygame.display.get_surface().get_size()
		self.cx, self.cy = self.w//2, self.h//2;
		self.fov = min(self.w, self.h)

		#bounding box:
		for v in self.vertices:
			self.minX = min(self.minX, v[0])
			self.maxX = max(self.maxX, v[0])
			self.minY = min(self.minY, v[1])
			self.maxY = max(self.maxY, v[1])
			self.minZ = min(self.minZ, v[2])
			self.maxZ = max(self.maxZ, v[2])

	def isColliding(self, camPos=(0, 0, 0)):
		colliding = False
		if (camPos[0] > self.minX and camPos[0] < self.maxX and 
			camPos[1] > self.minY and camPos[1] < self.maxY and 
			camPos[2] > self.minZ and camPos[2] < self.maxZ): colliding = True
		colliding = False # colliding temporary disabled
		return colliding

	def render(self, cam, face_list, face_color, depth):

		vert_list = []; screen_coords = []

		for x, y, z in self.vertices:
			x -= cam.pos[0]
			y -= cam.pos[1]
			z -= cam.pos[2]
			x, z = Util.rotate2d((x, z), cam.rot[1])
			y, z = Util.rotate2d((y, z), cam.rot[0])
			vert_list += [(x, y, z)]

			if z < 0.001:
				z = 0.001

			f = self.fov / z
			x, y = x * f, y * f
			screen_coords += [(self.cx + int(x), self.cy + int(y))]

		for f in range(len(self.faces)):
			face = self.faces[f]

			on_screen = False
			polyCoef = 6
			for i in face:
				x, y = screen_coords[i]
				if vert_list[i][2] > 0 and x > -(polyCoef - 1) * self.w and x < polyCoef * self.w and y > -(polyCoef - 1) * self.h and y < polyCoef * self.h:
					on_screen = True
					break

			if on_screen:
				coords = [screen_coords[i] for i in face]
				face_list += [coords]
				face_color += [self.colors[f]]
				depth += [sum(sum(vert_list[j][i] for j in face)**2 for i in range(3))]
