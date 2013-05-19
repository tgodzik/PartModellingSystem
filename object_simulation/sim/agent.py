import ode, random, math

class Agent(object):

	SHAPE_BOX = 1
	SHAPE_SPHERE = 2
	SHAPE_CYLINDER = 3

	def __init__(self, sim, number):

		self.shape = random.randint(1, 3)
		self.number = number
		self.sim = sim
		
		self.generateSizes()
		self.createGeom()

	def generateSizes(self):

		if (self.shape == self.SHAPE_BOX):
			self.sizes = {'lx': random.uniform(0.2, 1), 'ly': random.uniform(0.2, 1), 'lz': random.uniform(0.2, 1)}
		elif (self.shape == self.SHAPE_SPHERE):
			self.sizes = {'radius': random.uniform(0.2, 0.5)}
		elif (self.shape == self.SHAPE_CYLINDER):
			self.sizes = {'radius': random.uniform(0.2, 0.5), 'height': random.uniform(0.2, 0.5)}

		self.color = (random.random(), random.random(), random.random())
		self.density = 1000

	def createGeom(self):

		self.body = ode.Body(self.sim.getWorld())
		M = ode.Mass()

		if (self.shape == self.SHAPE_BOX):
			M.setBox(self.density, self.sizes['lx'], self.sizes['ly'], self.sizes['lz'])
		elif (self.shape == self.SHAPE_SPHERE):
			M.setSphere(self.density, self.sizes['radius'])
		elif (self.shape == self.SHAPE_CYLINDER):
			M.setCylinder(self.density, 1, self.sizes['radius'], self.sizes['height'])

		self.body.setMass(M)

		if (self.shape == self.SHAPE_BOX):
			self.geom = ode.GeomBox(self.sim.getSpace(), lengths=(self.sizes['lx'], self.sizes['ly'], self.sizes['lz']))
		elif (self.shape == self.SHAPE_SPHERE):
			self.geom = ode.GeomSphere(self.sim.getSpace(), self.sizes['radius'])
		elif (self.shape == self.SHAPE_CYLINDER):
			self.geom = ode.GeomCylinder(self.sim.getSpace(), self.sizes['radius'], self.sizes['height'])

		self.geom.setBody(self.body)

		self.body.setPosition((random.uniform(-10, 10), random.uniform(1, 10), random.uniform(-10, 10)))

		theta = 0
		ct = math.cos(theta)
		st = math.sin(theta)
		self.body.setRotation([ct, 0., -st, 0., 1., 0., st, 0., ct])

	def getShape(self):
		return self.shape

	def getBody(self):
		return self.body

	def getSizes(self):
		return self.sizes

	def getColor(self):
		return self.color
