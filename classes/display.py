import pygame

class Display:

	window_title = 'Python / pygame / 3D graphics'

	def setTitle(self, camera, clock):
		cameraPosTitle = "x=" + str(round(camera.pos[0], 2)) + ", y=" + str(round(camera.pos[1], 2)) + ", z="+ str(round(camera.pos[2], 2));
		cameraRotTitle = "rx=" + str(round(camera.rot[0], 2)) + ", ry=" + str(round(camera.rot[1], 2)) + ", rz="+ str(round(camera.rot[2], 2));
		pygame.display.set_caption(self.window_title + " | FPS: " + str(round(clock.get_fps())) + " | " + cameraPosTitle + " | " + cameraRotTitle)
