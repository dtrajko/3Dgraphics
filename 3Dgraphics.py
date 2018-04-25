import pygame, sys, math, os

from classes.cam import Cam
from classes.mesh import Mesh


class Cube(Mesh):
	pass

class Pyramid(Mesh):
	vertices = (-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1), (0, -1, 0)
	edges = (0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 4), (2, 4), (3, 4)
	faces = (0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4), (0, 1, 2), (2, 3, 0)
	colors = (255, 0, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255), (255, 0, 255)

	def __init__(self, pos=(0, 0, 0), scale=(1, 1, 1)):
		super().__init__(pos, scale)


pygame.init()

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

w,h = 1280, 720;
os.environ['SDL_VIDEO_CENTERED'] = '1'
window_title = '3D Graphics'
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

cam = Cam((14, -6, -16), (0.3, -0.75, 0))

cube_data = [(-3, -1, 0, 1, 1, 1), (0, -1, 0, 1, 1, 1), (3, -1, 0, 1, 1, 1), (0, 0, 0, 15, 0.5, 15)]
shapes = [Cube((x, y, z), (sx, sy, sz)) for x, y, z, sx, sy, sz in cube_data]

pyramid_data = [(-3, -2, 0, 1, 1, 1), (0, -2, 0, 1, 1, 1), (3, -2, 0, 1, 1, 1)]
shapes += [Pyramid((x, y, z), (sx, sy, sz)) for x, y, z, sx, sy, sz in pyramid_data]

while True:
	dt = clock.tick() / 1000
	camPosTitle = "x=" + str(round(cam.pos[0], 2)) + ", y=" + str(round(cam.pos[1], 2)) + ", z="+ str(round(cam.pos[2], 2));
	camRotTitle = "rx=" + str(round(cam.rot[0], 2)) + ", ry=" + str(round(cam.rot[1], 2)) + ", rz="+ str(round(cam.rot[2], 2));
	pygame.display.set_caption(window_title + " | FPS: " + str(round(clock.get_fps())) + " | " + camPosTitle + " | " + camRotTitle)

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

	# need to get all faces for all objects
	face_list = []; face_color = []; depth = [] # stores all face data

	for shape in shapes:
		shape.render(cam, face_list, face_color, depth)


	# final drawing part, all faces from all objects
	order = sorted(range(len(face_list)), key = lambda i: depth[i], reverse = 1)

	for i in order:
		try:
			pygame.draw.polygon(screen, face_color[i], face_list[i])
		except:
			pass

	pygame.display.flip()

	key = pygame.key.get_pressed()
	cam.update(dt, key, shapes)
