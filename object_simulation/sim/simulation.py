import ode, time, random
from agent import Agent
from draw import Draw
from OpenGL.GLUT import glutPostRedisplay

class Simulation(object):
    fps = 50
    dt = 1.0 / fps
    agents_to_add=[]

    def __init__(self, agents):
        self.create_world()
        self.create_environment()
        self.contactJoints = ode.JointGroup()

        self.agents = []

        for i in range(agents):
            self.agents.append(Agent(self, i, Agent.SHAPE_SPHERE))

    def create_world(self):
        self.world = ode.World()
        self.world.setGravity((0, -9.81, 0))
        self.world.setERP(0.8)
        self.world.setCFM(1E-5)

    def create_environment(self):
        self.space = ode.Space()
        self.floor = ode.GeomPlane(self.space, (0, 1, 0), 0)
        self.wall1 = ode.GeomPlane(self.space, (1, 0, 0), -6)
        self.wall2 = ode.GeomPlane(self.space, (-1, 0, 0), -6)
        self.wall3 = ode.GeomPlane(self.space, (0, 0, -1), -6)
        self.wall4 = ode.GeomPlane(self.space, (0, 0, 1), -6)

    def get_world(self):
        return self.world

    def get_space(self):
        return self.space

    def get_agents(self):
        return self.agents

    def near_callback(self, args, geom1, geom2):
        body1, body2 = geom1.getBody(), geom2.getBody()

        if (body1 is None):
            body1 = ode.environment
        if (body2 is None):
            body2 = ode.environment

        if (ode.areConnected(body1, body2)):
            return

        contacts = ode.collide(geom1, geom2)

        #try to fight or breed
        if (body1 is not None) and (body2 is not None) and contacts  :
                    rd=random.random()
                    if rd<0.9:
                        print 'fighting'
                        body1.agent.fight(body2.agent)
                    elif rd>=0.9:
                        print 'breeding'
                        if body1.agent.energy>400 and body2.agent.energy>400:
                            self.agents_to_add.append(Agent(self,len(self.agents),body1.agent.shape,False,body1.agent,body2.agent))

#

        for c in contacts:
            c.setBounce(0.2)
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
            if(agent.energy<=0):
                self.agents.remove(agent)
                del agent.body
                del agent.geom
                del agent
            else :
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
