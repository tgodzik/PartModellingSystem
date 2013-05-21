from agent import Agent
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Draw(object):

	def __init__(self, sim):

		self.sim = sim
		self.init_openGl()

		glutKeyboardFunc(self.key_callback)
		glutDisplayFunc(self.draw)
		glutIdleFunc(self.sim.idle)
		glutMainLoop()

	def init_openGl(self):

		glutInit([])
		glutInitDisplayMode (GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)

		glutInitWindowPosition(0, 0);
		glutInitWindowSize(640, 480);
		glutCreateWindow("Simulation window")

	def key_callback(self, c, x, y):
		sys.exit(0)

	def draw(self):

		self.render()
		agents = self.sim.get_agents()

		for agent in agents:
			self.draw_agent(agent)

		glutSwapBuffers()

	def render(self):
		
		glViewport(0, 0, 640, 480)
		glClearColor(0.8, 0.8, 0.9, 0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glEnable(GL_DEPTH_TEST)
		glDisable(GL_LIGHTING)
		glEnable(GL_LIGHTING)
		glEnable(GL_NORMALIZE)
		glShadeModel(GL_FLAT)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(90,1.3333,0.2,20)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		glLightfv(GL_LIGHT0,GL_POSITION,[0,0,1,0])
		glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
		glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
		glEnable(GL_LIGHT0)

		gluLookAt(2.4, 3.6, 4.8, 0.5, 0.5, 0, 0, 1, 0)

	def draw_agent(self, agent):

		body = agent.get_body()
		sizes = agent.get_sizes()
		color = agent.get_color()
		shape = agent.get_shape()

		x, y, z = body.getPosition()
		R = body.getRotation()
		rot = [R[0], R[3], R[6], 0.,
           R[1], R[4], R[7], 0.,
           R[2], R[5], R[8], 0.,
           x, y, z, 1.0]
		glPushMatrix()
		glMultMatrixd(rot)
		glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, color)

		if (shape == Agent.SHAPE_BOX):
			glScalef(sizes['lx'], sizes['ly'], sizes['lz'])
			glutSolidCube(1)
		elif (shape == Agent.SHAPE_SPHERE):
			d = sizes['radius']*2
			glScalef(d, d, d)
			glutSolidSphere(sizes['radius'], 32, 32)
		elif (shape == Agent.SHAPE_CYLINDER):
			d = sizes['radius']*2
			glScalef(sizes['height'], d, d)
			glutSolidCylinder(sizes['radius'], sizes['height'], 32, 32)

		glPopMatrix()
