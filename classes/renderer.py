import pygame

class Renderer:

	def render(self, screen, clock, scene, display):

		dt = clock.tick() / 1000
		camera = scene.getCamera()

		if dt % 1000 == 0:

			display.setTitle(camera, clock)

			# need to get all faces for all objects	
			face_list = []; face_color = []; depth = [] # stores all face data

			screen.fill((255, 255, 255))

			for entity in scene.getEntities():
				entity.render(camera, face_list, face_color, depth)

			# final drawing part, all faces from all objects
			order = sorted(range(len(face_list)), key = lambda i: depth[i], reverse = 1)

			for i in order:
				try:
					pygame.draw.polygon(screen, face_color[i], face_list[i])
				except:
					pass

			pygame.display.flip()

		key = pygame.key.get_pressed()
		camera.update(dt, key, scene.getEntities())
