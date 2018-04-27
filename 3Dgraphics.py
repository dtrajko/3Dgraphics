import pygame, sys, math, os

from classes.display import Display
from classes.camera import Camera
from classes.mesh import Mesh
from classes.scene import Scene
from classes.renderer import Renderer

pygame.init()
pygame.event.get()
#pygame.event.set_grab(1)
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)

w,h = 1280, 720;
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

display = Display()
camera = Camera((0, 4, -30), (0, 0, 0))
scene = Scene(camera)
renderer = Renderer()

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		camera.events(event)

	renderer.render(screen, clock, scene, display)
