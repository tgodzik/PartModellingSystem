import ode, random, math

class Agent(object):

	SHAPE_BOX = 1
	SHAPE_SPHERE = 2
	SHAPE_CYLINDER = 3

	def __init__(self, sim, number):

		self.shape = random.randint(1, 3)
		self.number = number
		self.sim = sim
		
		self.generate_sizes()
		self.create_geometry()

	def generate_sizes(self):

		if (self.shape == self.SHAPE_BOX):
			self.sizes = {'lx': random.uniform(0.2, 1), 'ly': random.uniform(0.2, 1), 'lz': random.uniform(0.2, 1)}
		elif (self.shape == self.SHAPE_SPHERE):
			self.sizes = {'radius': random.uniform(0.2, 0.5)}
		elif (self.shape == self.SHAPE_CYLINDER):
			self.sizes = {'radius': random.uniform(0.2, 0.5), 'height': random.uniform(0.2, 0.5)}

		self.color = (random.random(), random.random(), random.random())
		self.density = 1000

	def create_geometry(self):

		self.body = ode.Body(self.sim.get_world())
		M = ode.Mass()

		if (self.shape == self.SHAPE_BOX):
			M.setBox(self.density, self.sizes['lx'], self.sizes['ly'], self.sizes['lz'])
		elif (self.shape == self.SHAPE_SPHERE):
			M.setSphere(self.density, self.sizes['radius'])
		elif (self.shape == self.SHAPE_CYLINDER):
			M.setCylinder(self.density, 1, self.sizes['radius'], self.sizes['height'])

		self.body.setMass(M)

		if (self.shape == self.SHAPE_BOX):
			self.geom = ode.GeomBox(self.sim.get_space(), lengths=(self.sizes['lx'], self.sizes['ly'], self.sizes['lz']))
		elif (self.shape == self.SHAPE_SPHERE):
			self.geom = ode.GeomSphere(self.sim.get_space(), self.sizes['radius'])
		elif (self.shape == self.SHAPE_CYLINDER):
			self.geom = ode.GeomCylinder(self.sim.get_space(), self.sizes['radius'], self.sizes['height'])

		self.geom.setBody(self.body)

		self.body.setPosition((random.uniform(-5, 5), random.uniform(1, 3), random.uniform(-5, 5)))

		theta = 0
		ct = math.cos(theta)
		st = math.sin(theta)
		self.body.setRotation([ct, 0., -st, 0., 1., 0., st, 0., ct])

	def get_shape(self):
		return self.shape

	def get_body(self):
		return self.body

	def get_sizes(self):
		return self.sizes

	def get_color(self):
		return self.color
