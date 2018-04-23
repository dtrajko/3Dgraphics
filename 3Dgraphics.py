import pygame, sys, math, os

def rotate2d(pos, rad):
	x, y = pos
	rx = x * math.cos(rad) - y * math.sin(rad)
	ry = y * math.cos(rad) + x * math.sin(rad)
	return rx, ry

class Cam:
	def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
		self.pos = list(pos)
		self.rot = list(rot)

	def events(self, event):
		if event.type == pygame.MOUSEMOTION:
			x, y = event.rel
			x /= 1000 #mouse sensitivity
			y /= 1000
			self.rot[0] += y
			self.rot[1] += x

	def update(self, dt, key):

		speed = dt * 2
		x, y = speed * math.sin(self.rot[1]), speed * math.cos(self.rot[1])

		new_pos = list(self.pos)

		if key[pygame.K_q]: new_pos[1] -= speed
		if key[pygame.K_e]: new_pos[1] += speed

		if key[pygame.K_w]: new_pos[0] += x; new_pos[2] += y
		if key[pygame.K_s]: new_pos[0] -= x; new_pos[2] -= y
		if key[pygame.K_a]: new_pos[0] -= y; new_pos[2] += x
		if key[pygame.K_d]: new_pos[0] += y; new_pos[2] -= x

		if key[pygame.K_UP]:    self.rot[0] -= 0.01
		if key[pygame.K_DOWN]:  self.rot[0] += 0.01
		if key[pygame.K_LEFT]:  self.rot[1] -= 0.01
		if key[pygame.K_RIGHT]: self.rot[1] += 0.01

		inCollision = False
		for c in cubes:
			if c.isColliding(new_pos):
				inCollision = True
		if inCollision == False: self.pos = new_pos

class Cube:
	vertices = (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
	edges = (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)
	faces = (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
	colors = (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255), (0, 0, 255), (0, 255, 0)
	pos = (0, 0, 0)
	minX, minY, minZ = 9999, 9999, 9999
	maxX, maxY, maxZ = -9999, -9999, -9999

	def __init__(self, pos=(0, 0, 0), size=1):
		self.pos = list(pos)
		x, y, z = pos
		self.vertices = [((x + X / 2 * size), (y + Y / 2 * size), (z + Z / 2 * size)) for X, Y, Z in self.vertices]
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
		return colliding

pygame.init()

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

w,h = 1280, 720; cx,cy = w//2,h//2; fov = min(w, h)
os.environ['SDL_VIDEO_CENTERED'] = '1'
window_title = '3D Graphics'
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

cam = Cam((-1, 0, -4), (0, 0))
cube_data = [(0, 1, 1, 1), (3, 0.5, 0.5, 2), (7, 0, 0, 3)]
cubes = [Cube((x, y, z), s) for x, y, z, s in cube_data]

while True:
	dt = clock.tick() / 1000
	camPosTitle = "x=" + str(round(cam.pos[0], 2)) + ", y=" + str(round(cam.pos[1], 2)) + ", z="+ str(round(cam.pos[2], 2));
	pygame.display.set_caption(window_title + " | FPS: " + str(round(clock.get_fps())) + " | " + camPosTitle)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		cam.events(event)

	screen.fill((255, 255, 255))

	# need to go through all objects, get all faces
	face_list = []; face_color = []; depth = [] # stores all face data

	for obj in cubes:

		vert_list = []; screen_coords = []

		for x, y, z in obj.vertices:
			x -= cam.pos[0]
			y -= cam.pos[1]
			z -= cam.pos[2]
			x, z = rotate2d((x, z), cam.rot[1])
			y, z = rotate2d((y, z), cam.rot[0])
			vert_list += [(x, y, z)]

			if z < 0.001:
				z = 0.001
			f = fov / z
			x, y = x * f, y * f
			screen_coords += [(cx + int(x), cy + int(y))]

		for f in range(len(obj.faces)):
			face = obj.faces[f]

			on_screen = False
			for i in face:
				x, y = screen_coords[i]
				if vert_list[i][2] > 0 and x > 0 and x < w and y > 0 and y < h:
					on_screen = True
					break

			if on_screen:
				coords = [screen_coords[i] for i in face]
				face_list += [coords]
				face_color += [obj.colors[f]]
				depth += [sum(sum(vert_list[j][i] for j in face)**2 for i in range(3))]

	# final drawing part, all faces from all objects
	order = sorted(range(len(face_list)), key = lambda i: depth[i], reverse = 1)

	for i in order:
		try:
			pygame.draw.polygon(screen, face_color[i], face_list[i])
			#print("i: ", i, " polygon: ", face_list[i])
		except:
			pass

	pygame.display.flip()

	key = pygame.key.get_pressed()
	cam.update(dt, key)
