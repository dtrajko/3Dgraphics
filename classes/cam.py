import pygame, math

class Cam:
	def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0)):
		self.pos = list(pos)
		self.pos_new = list(pos)
		self.rot = list(rot)

	def events(self, event):
		if event.type == pygame.MOUSEMOTION:
			x, y = event.rel
			x /= 1000 #mouse sensitivity
			y /= 1000
			z = 0
			self.rot[0] += x
			self.rot[1] += y
			self.rot[2] += z

	def update(self, dt, key, shapes):

		speed = dt * 5
		x, y = speed * math.sin(self.rot[1]), speed * math.cos(self.rot[1])
		z = speed

		if key[pygame.K_q]: self.pos_new[1] -= z
		if key[pygame.K_e]: self.pos_new[1] += z

		if key[pygame.K_w]: self.pos_new[0] += x; self.pos_new[2] += y
		if key[pygame.K_s]: self.pos_new[0] -= x; self.pos_new[2] -= y
		if key[pygame.K_a]: self.pos_new[0] -= y; self.pos_new[2] += x
		if key[pygame.K_d]: self.pos_new[0] += y; self.pos_new[2] -= x

		if key[pygame.K_UP]:    self.rot[0] -= 0.2 * speed
		if key[pygame.K_DOWN]:  self.rot[0] += 0.2 * speed
		if key[pygame.K_LEFT]:  self.rot[1] -= 0.2 * speed
		if key[pygame.K_RIGHT]: self.rot[1] += 0.2 * speed

		inCollision = False
		for shape in shapes:
			if shape.isColliding(self.pos_new):
				inCollision = True
				break

		if inCollision == False:
			self.pos = self.pos_new
