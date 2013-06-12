import ode, time, random
from agent import Agent
from draw import Draw
from OpenGL.GLUT import glutPostRedisplay

class Configuration:

    def fight_function(self,other):

        fit1 = self.fitness()
        fit2 = other.fitness()

        if fit1 > fit2:
            self.energy += 100
            other.energy -= 100
        elif fit2 > fit1:
            self.energy -= 100
            other.energy += 100

    def breed(self, other):

        if self.energy > 400 and other.energy > 400:

            self.energy -= 200
            other.energy -= 200

            newAgent = Agent(self.sim, self.sim.newAgentNumber, self.shape, True)
            newAgent.create_parameters(self, other)

            self.sim.agents_to_add.append(newAgent)
            self.sim.newAgentNumber += 1

class Simulation:
    """
    Main class responsible for Simulation
    """

    #framerate for the simulation
    fps = 50
    dt = 1.0 / fps


    def __init__(self, agents=20, boardSize=12, parameters=[]):
        """
        :type boardSize: int - size of the board
        :type agents: int - number of initial agents
        :type parameters: dict - all simulation parameters
        """

        self.iter = 0
        self.max_iter = -1
        self.boardSize = boardSize

        if "func_fight" in parameters:
            Agent.fight = parameters["func_fight"]

        if "func_fit" in parameters:
            Agent.fitness = parameters["func_fit"]

        if "func_breed" in parameters:
            Agent.breed = parameters["func_breed"]

        if "maximum_iterations" in parameters:
            self.max_iter = parameters["maximum_iterations"]

        if "func_create" in parameters:
            Agent.create_agent = parameters["func_create"]

        if "vertices" in parameters:
            self.vertices = parameters["vertices"]
        else:
            self.vertices = [(self.boardSize / 2, -1.0, self.boardSize / 2),
                             (0.0, -1.0, self.boardSize / 2),
                             (-self.boardSize / 2, 1.0, self.boardSize / 2),
                             (-self.boardSize / 2, 1.0, 0.0),
                             (-self.boardSize / 2, 0.0, -self.boardSize / 2),
                             (0.0, 0.0, -self.boardSize / 2),
                             (self.boardSize / 2, -1.0, -self.boardSize / 2),
                             (self.boardSize / 2, 0.0, 0.0),
                             (0.0, 1.0, 0.0)]

        if "indices" in parameters:
            self.indices = parameters["indices"]
        else:
            self.indices = [(0, 8, 1), (1, 8, 2), (2, 8, 3), (3, 8, 4), (4, 8, 5), (5, 8, 6), (6, 8, 7), (7, 8, 0)]

        self.create_world()
        self.create_environment()
        self.contactJoints = ode.JointGroup()

        self.agents = []
        self.agents_to_add = []

        for i in range(agents):
            self.agents.append(Agent(self, i, Agent.SHAPE_BOX))

        self.newAgentNumber = agents

    def create_world(self):
        """
        Creating the world, main parameters and setting gravity.
        """
        self.world = ode.World()
        self.world.setGravity((0, -9.81, 0))
        self.world.setERP(0.8)
        self.world.setCFM(1E-5)

    def create_floor(self):
        """
        Creating the floor for the simulation using 3D mesh
        """
        td = ode.TriMeshData()
        td.build(self.vertices, self.indices)
        self.floor = ode.GeomTriMesh(td, self.space)

    def create_environment(self):
        """
        Creating the needed environment - floor, walls and Space for collisions
        """
        self.space = ode.Space()
        self.create_floor()
        self.wall1 = ode.GeomPlane(self.space, (1, 0, 0), -self.boardSize / 2)
        self.wall2 = ode.GeomPlane(self.space, (-1, 0, 0), -self.boardSize / 2)
        self.wall3 = ode.GeomPlane(self.space, (0, 0, -1), -self.boardSize / 2)
        self.wall4 = ode.GeomPlane(self.space, (0, 0, 1), -self.boardSize / 2)

    def near_callback(self, args, geom1, geom2):
        """
        Function invoke when detected collisions
        :type geom2: GeomObject
        :type geom1: GeomObject
        :type args: object
        """

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
            self.encounter(body1,body2)

        for c in contacts:
            c.setBounce(0.3)
            c.setMu(100)
            j = ode.ContactJoint(self.world, self.contactJoints, c)
            j.attach(body1, body2)

    def encounter(self,body1,body2):
        if random.random() < 0.9:
            body1.agent.fight(body2.agent)
        else:
            body1.agent.breed(body2.agent)
    def __str__(self):

        result = ""

        for agent in self.agents:
            result += str(agent) + "\n"

        return result + "Total: " + str(len(self.agents)) + " agents in environment\n"

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

        if not self.no_graphics:
            glutPostRedisplay()

        n = 4

        for i in range(n):
            self.space.collide((), self.near_callback)
            self.world.step(self.dt / n)
            self.contactJoints.empty()

        self.iter += 1

        if self.max_iter != -1:
            if self.iter > self.max_iter:
                print self
                exit(0)

        self.lasttime = time.time()

    def run(self, draw=True):

        self.no_graphics = not draw
        self.lasttime = time.time()

        if not self.no_graphics:
            self.draw = Draw(self)
        else:
            while True:
                self.idle()
