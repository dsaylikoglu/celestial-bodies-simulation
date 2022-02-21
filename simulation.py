import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1550, 850
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Celestial Bodies Simulation")

YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (128, 128, 128)
DARK_GREY = (80, 78, 81)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
ORANGE = (252, 186, 3)
MILKY_COFFEE = (218, 184, 122)
AQUA = (196, 234, 237)
BLUE = (67, 115, 252)

FONT = pygame.font.SysFont("roboto", 25)

class CelestialBody:
	AU = 149597870700	# in meters
	G = 6.67428e-11
	SCALING_FACTOR = 3
	SCALE = 250 / SCALING_FACTOR / AU		# 1 AU = 100 pixels
	TIMESTEP = 3600*24	# 1 day of seconds

	def __init__(self, x, y, radius, color, mass):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2

		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))

			# to prevent orbit overlapping
			if (len(self.orbit) > 1000) and (abs(self.orbit[-1][0]) <= (2 * self.AU)):
				self.orbit.pop(0)
			if (len(self.orbit) > 600) and (0 < abs(self.orbit[-1][0]) < (self.AU - 10**4)):
				self.orbit.pop(0)

			pygame.draw.lines(win, self.color, False, updated_points, 2)


		pygame.draw.circle(win, self.color, (x, y), self.radius)

		if not self.sun:
			DISTANCE_FONT = pygame.font.SysFont("helvetica", round(16 / self.SCALING_FACTOR * 3.5) if self.SCALING_FACTOR > 2 else 16)
			distance_text = DISTANCE_FONT.render(f"{round(self.distance_to_sun/1000, 1)} 	km", 1, WHITE)
			win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y

		distance = math.sqrt(distance_x**2 + distance_y**2)

		if other.sun:
			self.distance_to_sun = distance

		# Calculating Forces Applied to the Body
		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)	# arctan(y/x) = θ
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force

		return force_x, force_y

	def update_position(self, planets):
		total_f_x = total_f_y = 0

		for planet in planets:
			if self == planet:
				continue

			f_x, f_y = self.attraction(planet)
			total_f_x += f_x
			total_f_y += f_y

		# Calculating Body's Velocity Components
		self.x_vel += total_f_x / self.mass * self.TIMESTEP
		self.y_vel += total_f_y / self.mass * self.TIMESTEP

		# Calculating Body's New Position
		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y))


def main():
	run = True
	clock = pygame.time.Clock()

	sun = CelestialBody(0, 0, 40 / CelestialBody.SCALING_FACTOR, YELLOW, 1.98892 * 10**30)
	sun.sun = True

	mercury = CelestialBody(0.387 * CelestialBody.AU, 0, 9.5 / CelestialBody.SCALING_FACTOR, DARK_GREY, 3.30 * 10**23)
	mercury.y_vel = -47.4 * 1000 	# for initial velocity

	venus = CelestialBody(0.723 * CelestialBody.AU, 0, 14 / CelestialBody.SCALING_FACTOR, WHITE, 4.8685 * 10**24)
	venus.y_vel = -35.02 * 1000		# in meters

	earth = CelestialBody(-1 * CelestialBody.AU, 0, 16 / CelestialBody.SCALING_FACTOR, BLUE, 5.9722 * 10**24)
	earth.y_vel = 29.783 * 1000

	mars = CelestialBody(-1.524 * CelestialBody.AU, 0, 12 / CelestialBody.SCALING_FACTOR, RED, 6.39 * 10**23)
	mars.y_vel = 24.077 * 1000

	jupiter = CelestialBody(5.2 * CelestialBody.AU, 0, 24.5 / CelestialBody.SCALING_FACTOR, ORANGE, 1.89813 * 10**27)
	jupiter.y_vel = -13.06 * 1000

	saturn = CelestialBody(9.5 * CelestialBody.AU, 0, 22.5 / CelestialBody.SCALING_FACTOR, MILKY_COFFEE, 5.6834 * 10**26)
	saturn.y_vel = -9.68 * 1000

	uranus = CelestialBody(-19.8 * CelestialBody.AU, 0, 19.5 / CelestialBody.SCALING_FACTOR, AQUA, 8.6810 * 10**25)
	uranus.y_vel = 6.8 * 1000

	neptune = CelestialBody(-30 * CelestialBody.AU, 0, 18.5 / CelestialBody.SCALING_FACTOR, BLUE, 1.02413 * 10**26)
	neptune.y_vel = 5.43 * 1000

	celestial_bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		scaling_factor_text = FONT.render(f"Scaling Factor: {CelestialBody.SCALING_FACTOR}", 1, WHITE)
		WIN.blit(scaling_factor_text, (scaling_factor_text.get_width() / 2.25, scaling_factor_text.get_height() * 2))

		for celestial_body in celestial_bodies:
			celestial_body.update_position(celestial_bodies)
			celestial_body.draw(WIN)

		pygame.display.update()

	pygame.quit()

main()
