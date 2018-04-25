import math

class Util:

	def rotate2d(pos, rad):
		x, y = pos
		rx = x * math.cos(rad) - y * math.sin(rad)
		ry = y * math.cos(rad) + x * math.sin(rad)
		return rx, ry
