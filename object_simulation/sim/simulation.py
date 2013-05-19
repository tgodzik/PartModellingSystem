import ode, time
from agent import Agent
from draw import Draw
from OpenGL.GLUT import glutPostRedisplay

class Simulation(object):

	fps = 50
	dt = 1.0/fps

	def __init__(self, agents):

		self.createWorld()
		self.createEnvironment()
		self.contactJoints = ode.JointGroup()

		self.agents = []

		for i in range(agents):
			self.agents.append(Agent(self, i))

	def createWorld(self):

		self.world = ode.World()
		self.world.setGravity((0,-9.81, 0))
		self.world.setERP(0.8)
		self.world.setCFM(1E-5)

	def createEnvironment(self):
		
		self.space = ode.Space()

		self.floor = ode.GeomPlane(self.space, (0, 1, 0), 0)
		#todo - create walls

	def getWorld(self):
		return self.world

	def getSpace(self):
		return self.space

	def getAgents(self):
		return self.agents

	def nearCallback(self, args, geom1, geom2):

		body1, body2 = geom1.getBody(), geom2.getBody()
		if (body1 is None):
			body1 = ode.environment
		if (body2 is None):
			body2 = ode.environment

		if (ode.areConnected(body1, body2)):
			return

		contacts = ode.collide(geom1, geom2)

		for c in contacts:
			c.setBounce(0.2)
			c.setMu(100)
			j = ode.ContactJoint(self.world, self.contactJoints, c)
			j.attach(body1, body2)

	def idle(self):

		t = self.dt - (time.time() - self.lasttime)

		if (t > 0):
			time.sleep(t)

		for agent in self.agents:
			agent.getBody().addForce((-400, 0.0, 0.0))

		glutPostRedisplay()

		n = 4

		for i in range(n):
			self.space.collide((), self.nearCallback)
			self.world.step(self.dt/n)
			self.contactJoints.empty()		

		self.lasttime = time.time()

	def run(self):
		self.lasttime = time.time()
		self.draw = Draw(self)
