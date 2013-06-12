import ode, random, math

class Agent:

    SHAPE_BOX = 1
    SHAPE_SPHERE = 2
    SHAPE_CYLINDER = 3

    def __init__(self, sim, number, shape, breeded=False):

        """
        Constructor
        """
        self.sim = sim
        self.number = number
        self.shape = shape
        self.create_agent(breeded)

        if breeded:
            self.sim.agents_to_add.append(self)
            self.sim.newAgentNumber += 1


    def create_agent(self, breeded):

        if not breeded:
            self.generate_sizes()
            self.create_geometry()
            self.energy = random.randint(1000, 1500)
        else:
            self.energy = 400

        self.direction = ((random.random()*2)-1, 0.0, (random.random()*2)-1)

    def move(self):
        self.body.addForce((self.energy * self.direction[0], 0.0, self.energy * self.direction[2]))

    def generate_sizes(self):

        if (self.shape == self.SHAPE_BOX):
            self.sizes = {'lx': random.uniform(0.2, 1), 'ly': random.uniform(0.2, 1), 'lz': random.uniform(0.2, 1)}
        elif (self.shape == self.SHAPE_SPHERE):
            self.sizes = {'radius': random.uniform(0.2, 0.5)}
        elif (self.shape == self.SHAPE_CYLINDER):
            self.sizes = {'radius': random.uniform(0.2, 0.5), 'height': random.uniform(0.2, 0.5)}

        self.color = (random.random(), random.random(), random.random())
        self.density = 1000

    def get_one(self, value1, value2):
        return value1 if random.random() > 0.5 else value2

    def create_parameters(self, agent1, agent2):

        self.sizes = {}

        if (self.shape == self.SHAPE_BOX):
            self.sizes = {'lx': self.get_one(agent1.sizes['lx'], agent2.sizes['lx']), 'ly': self.get_one(agent1.sizes['ly'], agent2.sizes['ly']), 'lz': self.get_one(agent1.sizes['lz'], agent2.sizes['lz'])}
        elif (self.shape == self.SHAPE_SPHERE):
            self.sizes = {'radius': self.get_one(agent1.sizes['radius'], agent2.sizes['radius'])}
        elif (self.shape == self.SHAPE_CYLINDER):
            self.sizes = {'radius': self.get_one(agent1.sizes['radius'], agent2.sizes['radius']), 'height': self.get_one(agent1.sizes['height'], agent2.sizes['height'])}

        self.color = (self.get_one(agent1.color[0], agent2.color[0]), self.get_one(agent1.color[1], agent2.color[1]), self.get_one(agent1.color[2], agent2.color[2]))
        self.density = 1000

    def create_geometry(self):

        self.body = ode.Body(self.sim.world)
        self.body.agent = self

        M = ode.Mass()

        if (self.shape == self.SHAPE_BOX):
            M.setBox(self.density, self.sizes['lx'], self.sizes['ly'], self.sizes['lz'])
        elif (self.shape == self.SHAPE_SPHERE):
            M.setSphere(self.density, self.sizes['radius'])
        elif (self.shape == self.SHAPE_CYLINDER):
            M.setCylinder(self.density, 1, self.sizes['radius'], self.sizes['height'])

        self.body.setMass(M)

        if (self.shape == self.SHAPE_BOX):
            self.geom = ode.GeomBox(self.sim.space, lengths=(self.sizes['lx'], self.sizes['ly'], self.sizes['lz']))
        elif (self.shape == self.SHAPE_SPHERE):
            self.geom = ode.GeomSphere(self.sim.space, self.sizes['radius'])
        elif (self.shape == self.SHAPE_CYLINDER):
            self.geom = ode.GeomCylinder(self.sim.space, self.sizes['radius'], self.sizes['height'])

        self.geom.setBody(self.body)

        self.body.setPosition((random.uniform(-5, 5), random.uniform(4, 5), random.uniform(-5, 5)))

        theta = 0
        ct = math.cos(theta)
        st = math.sin(theta)
        self.body.setRotation([ct, 0.0, -st, 0.0, 1.0, 0.0, st, 0.0, ct])

    def fight(self, other):

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



    def fitness(self):
        
        if (self.shape == self.SHAPE_BOX):
            return self.sizes['lx'] * self.sizes['ly'] * self.sizes['lz']
        elif (self.shape == self.SHAPE_SPHERE):
            return math.pi * self.sizes['radius'] * self.sizes['radius'] * self.sizes['radius'] * 4/3
        elif (self.shape == self.SHAPE_CYLINDER):
            return math.pi * self.sizes['radius'] * self.sizes['radius'] * self.sizes['height']

    def __str__(self):
        return "\tAgent " + str(self.number) + " [shape: " + str(self.shape) + ", fitness: " + str(self.fitness()) + ", energy: " + str(self.energy) + ", size: "+ str(self.sizes) + "]"
