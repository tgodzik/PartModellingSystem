import ode, time, random
from agent import Agent
from draw import Draw
from OpenGL.GLUT import glutPostRedisplay

class Simulation(object):

    fps = 50
    dt = 1.0 / fps

    def __init__(self, agents, boardSize):

        self.boardSize = boardSize
        self.create_world()
        self.create_environment()
        self.contactJoints = ode.JointGroup()

        self.agents = []
        self.agents_to_add = []

        for i in range(agents):
            self.agents.append(Agent(self, i, Agent.SHAPE_SPHERE))

        self.newAgentNumber = agents

    def create_world(self):

        self.world = ode.World()
        self.world.setGravity((0, -9.81, 0))
        self.world.setERP(0.8)
        self.world.setCFM(1E-5)

    def create_environment(self):

        self.space = ode.Space()
        self.floor = ode.GeomPlane(self.space, (0, 1, 0), 0)
        self.wall1 = ode.GeomPlane(self.space, (1, 0, 0), -self.boardSize/2)
        self.wall2 = ode.GeomPlane(self.space, (-1, 0, 0), -self.boardSize/2)
        self.wall3 = ode.GeomPlane(self.space, (0, 0, -1), -self.boardSize/2)
        self.wall4 = ode.GeomPlane(self.space, (0, 0, 1), -self.boardSize/2)

    def near_callback(self, args, geom1, geom2):

        body1, body2 = geom1.getBody(), geom2.getBody()

        if (body1 is None):
            body1 = ode.environment
        if (body2 is None):
            body2 = ode.environment

        if (ode.areConnected(body1, body2)):
            return

        contacts = ode.collide(geom1, geom2)
        
        if body1 is not None and contacts:
            velocity = body1.getLinearVel()
            body1.agent.direction = (max(min(velocity[0], 1.0), -1.0), 0.0, max(min(velocity[2], 1.0), -1.0))

        if body2 is not None and contacts:
            velocity = body2.getLinearVel()
            body2.agent.direction = (max(min(velocity[0], 1.0), -1.0), 0.0, max(min(velocity[2], 1.0), -1.0))

        if body1 is not None and body2 is not None and contacts:

            if random.random() < 0.9:
                body1.agent.fight(body2.agent)
            else:
                body1.agent.breed(body2.agent)

        for c in contacts:

            c.setBounce(0.3)
            c.setMu(100)
            j = ode.ContactJoint(self.world, self.contactJoints, c)
            j.attach(body1, body2)

    def idle(self):

        t = self.dt - (time.time() - self.lasttime)

        if (t > 0):
            time.sleep(t)

        for agent in self.agents_to_add:
            agent.create_geometry()
            self.agents.append(agent)
            self.agents_to_add.remove(agent)

        for agent in self.agents:
            if (agent.energy <= 0):
                self.agents.remove(agent)
                agent.body.disable()
                del agent.body
                del agent.geom
                del agent
            else:
                agent.move()

        glutPostRedisplay()

        n = 4

        for i in range(n):
            self.space.collide((), self.near_callback)
            self.world.step(self.dt / n)
            self.contactJoints.empty()

        self.lasttime = time.time()

    def run(self):
        self.lasttime = time.time()
        self.draw = Draw(self)
