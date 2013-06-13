import ode, time, random
from agent import *
from draw import Draw
from OpenGL.GLUT import glutPostRedisplay
from collections import defaultdict

class Configuration:
    def __init__(self, agents=20, board_size=12.0,object_type=Sphere,(vertices,indices)=(None,None)):

        #setting simple parameters
        self.agents = agents
        self.board_size = board_size
        self.object_type=object_type
        self.max_iter = -1
        #floor parameters
        if not vertices or not indices:

            self.vertices = [(board_size / 2, -1.0, board_size / 2),
                         (0.0, -1.0, board_size / 2),
                         (-board_size / 2, 1.0, board_size / 2),
                         (-board_size / 2, 1.0, 0.0),
                         (-board_size / 2, 0.0, -board_size / 2),
                         (0.0, -1.0, -board_size / 2),
                         (board_size / 2, -1.0, -board_size / 2),
                         (board_size / 2, 0.0, 0.0),
                         (board_size / 4, 1.0, board_size / 4),
                         (-board_size / 4, 2.0, board_size / 4),
                         (-board_size / 4, 0.0, -board_size / 4),
                         (board_size / 4, -2.0, -board_size / 4),
                         (0.0, 2.0, 0.0)]
            self.indices = [(0, 8, 1),(1, 8, 12), (1, 9, 2), (1, 12, 9), (2, 9, 3), (9, 12, 3), (3, 12, 10), (3, 10, 4), (4, 10, 5), (12, 5, 10), (6, 5, 11), (11, 5, 12), (6, 11, 7), (7, 11, 12), (0, 7, 8), (8, 7, 12)]


        #setting function parameters
        self.functions={}


    def set_max_iterations(self, iter):
        """
                Setting up the max number of iteration.
                """
        self.max_iter = iter

    def setup_simulation(self):
        """
        change all needed functions that were specified in configuration
        """
        if "function_fitness" in self.functions:
            Agent.fitness=self.functions["function_fitness"]
        if "function_breed" in self.functions:
            Agent.breed=self.functions["function_breed"]
        if "function_fight" in self.functions:
            Agent.fight=self.functions["function_fight"]
        if "function_live" in self.functions:
            Agent.live=self.functions["function_live"]
        if "function_encounter" in self.functions:
            Simulation.encounter=self.functions["function_encounter"]
        if "function_touch" in self.functions:
            Simulation.touch=self.functions["function_touch"]


    def function_live(self, function):
        """
                Change function in agent responsible for life cycle.
                """
        self.functions["function_live"] = function

    def function_fight(self, function):
        """
                Change function in agent responsible for fighting other agents.
                """
        self.functions["function_fight"] = function

    def function_breed(self, function):
        """
                Change function in agent responsible for creating new agent.
                """
        self.functions["function_breed"] = function

    def function_fitness(self, function):
        """
                Change function in agent responsible for checking agent fitness.
                """
        self.functions["function_fitness"] = function

    def function_touch(self, function):
        """
                Change function in simulation responsible for contact points in agent.
                """
        self.functions["function_touch"] = function

    def function_encounter(self, function):
        """
                Change function in simulation responsible for an encounter between agents.
                """
        self.functions["function_encounter"] = function

class Simulation:
    """
    Main class responsible for Simulation
    """

    #framerate for the simulation
    fps = 50
    dt = 1.0 / fps


    def __init__(self, configuration=Configuration()):
        """
        :type configuration: Configuration - simulation configuration
        """

        #current iteration number
        self.iter = 0
        self.board_size = configuration.board_size

        configuration.setup_simulation()

        self.max_iter = configuration.max_iter

        self.vertices = configuration.vertices

        self.indices = configuration.indices

        self.create_world()
        self.create_environment()
        self.contactJoints = ode.JointGroup()

        self.agents = []
        self.agents_to_add = []

        for i in range(configuration.agents):
            self.agents.append(Agent(self, i,configuration.object_type))

        self.newAgentNumber = configuration.agents

    def set_fps(self,new_fps):
        """
        Setting frames per second
        """
        self.fps=new_fps
        self.dt=1.0/self.fps

    def set_dt(self,new_dt):
        """
        Setting the duration of one iteration
        """
        self.dt=new_dt
        self.fps=1/self.dt

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
        self.wall1 = ode.GeomPlane(self.space, (1, 0, 0), -self.board_size / 2.0)
        self.wall2 = ode.GeomPlane(self.space, (-1, 0, 0), -self.board_size / 2.0)
        self.wall3 = ode.GeomPlane(self.space, (0, 0, -1), -self.board_size / 2.0)
        self.wall4 = ode.GeomPlane(self.space, (0, 0, 1), -self.board_size / 2.0)

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
            self.encounter(body1, body2)

        for c in contacts:
            self.touch(c,body1,body2)
            j = ode.ContactJoint(self.world, self.contactJoints, c)
            j.attach(body1, body2)

    def encounter(self, body1, body2):
        """
        What to do when to bodies encounter each other
        """
        if random.random() < 0.9:
            body1.agent.fight(body2.agent)
        else:
            body1.agent.breed(body2.agent)


    def touch(self,contact,body1,body2):
        """
        What to do on touching surfaces
        """
        contact.setBounce(0.3)
        contact.setMu(100)

    def __str__(self):
        result = ""

        for agent in self.agents:
            result += str(agent) + "\n"

        return result + "Total: " + str(len(self.agents)) + " agents in environment\n"

    def main_loop(self):
        """
        Function responsible for main simulation loop
        """
        t = self.dt - (time.time() - self.lasttime)
        # check if we need to do anything, dt
        if t > 0 and self.real_time:
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
                agent.live()

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

    def run(self, draw=True, real_time=True):
        """
        Running the simulation
        """
        self.no_graphics = not draw
        self.real_time = real_time
        self.lasttime = time.time()

        if not self.no_graphics:
            self.draw = Draw(self)
        else:
            while True:
                self.main_loop()
