import ode, random, math

def pick_one(value1, value2):
    return value1 if random.random() > 0.5 else value2


class Shape:
    def generate_random(self):
        raise NotImplementedError()

    def create_mass(self, mass):
        raise NotImplementedError()

    def create_geom(self, space):
        raise NotImplementedError()

    def create_new_size(self, shape1,shape2):
        raise NotImplementedError()

    def get_size(self):
        return 0.0


class Box(Shape):
    def __init__(self):
        pass

    def generate_random(self):
        self.sizes = {'lx': random.uniform(0.2, 1), 'ly': random.uniform(0.2, 1), 'lz': random.uniform(0.2, 1)}
        self.color = (random.random(), random.random(), random.random())
        self.density = 1000


    def create_mass(self, mass):
        mass.setBox(self.density, self.sizes['lx'], self.sizes['ly'], self.sizes['lz'])

    def create_geom(self, space):
        return ode.GeomBox(space, lengths=(self.sizes['lx'], self.sizes['ly'], self.sizes['lz']))

    def create_new_size(self, shape1,shape2):
        self.sizes = {'lx': pick_one(shape1.sizes['lx'], shape2.sizes['lx']),
                      'ly': pick_one(shape1.sizes['ly'], shape2.sizes['ly']),
                      'lz': pick_one(shape1.sizes['lz'], shape2.sizes['lz'])}
        self.color = (pick_one(shape1.color[0], shape2.color[0]),
                      pick_one(shape1.color[1], shape2.color[1]),
                      pick_one(shape1.color[2], shape2.color[2]))
        self.density = 1000

    def get_size(self):
        return self.sizes['lx'] * self.sizes['ly'] * self.sizes['lz']

class Sphere(Shape):
    def __init__(self):
        pass

    def generate_random(self):
        self.sizes = {'radius': random.uniform(0.2, 0.5)}
        self.color = (random.random(), random.random(), random.random())
        self.density = 1000

    def create_mass(self, mass):
        mass.setSphere(self.density, self.sizes['radius'])

    def create_geom(self, space):
        return ode.GeomSphere(space, self.sizes['radius'])

    def create_new_size(self, shape1, shape2):
        self.sizes = {'radius': pick_one(shape1.sizes['radius'], shape2.sizes['radius'])}
        self.color = (pick_one(shape1.color[0], shape2.color[0]),
                      pick_one(shape1.color[1], shape2.color[1]),
                      pick_one(shape1.color[2], shape2.color[2]))
        self.density = 1000

    def get_size(self):
        return math.pi * self.sizes['radius'] * self.sizes['radius'] * self.sizes['radius'] * 4 / 3


class Cylinder(Shape):
    def __init__(self):
        pass

    def generate_random(self):
        self.sizes = {'radius': random.uniform(0.2, 0.5), 'height': random.uniform(0.2, 0.5)}
        self.color = (random.random(), random.random(), random.random())
        self.density = 1000

    def create_mass(self, mass):
        mass.setCylinder(self.density, 1, self.sizes['radius'], self.sizes['height'])

    def create_geom(self, space):
        return ode.GeomCylinder(space, self.sizes['radius'], self.sizes['height'])

    def create_new_size(self,shape1 ,shape2):
        self.sizes = {'radius': pick_one(shape1.sizes['radius'], shape2.sizes['radius']),
                      'height': pick_one(shape1.sizes['height'], shape2.sizes['height'])}
        self.color = (pick_one(shape1.color[0], shape2.color[0]),
                      pick_one(shape1.color[1], shape2.color[1]),
                      pick_one(shape1.color[2], shape2.color[2]))
        self.density = 1000
        
    def get_size(self):
        return math.pi * self.sizes['radius'] * self.sizes['radius'] * self.sizes['height']

class Agent:

    def __init__(self, sim, number, parent1=None,parent2=None):
        """
        Constructor
        """
        self.sim = sim
        self.number = number
        self.shape = Sphere()
        self.direction = ((random.random() * 2) - 1, 0.0, (random.random() * 2) - 1)

        if parent1 is  None and parent2 is  None:
            self.shape.generate_random()
            self.create_geometry()
            self.energy = random.randint(1000, 1500)

        else:
            self.shape.create_new_size(parent1.shape,parent2.shape)
            self.energy = 400
            self.sim.agents_to_add.append(self)
            self.sim.newAgentNumber += 1




    def create_geometry(self):
        self.body = ode.Body(self.sim.world)
        self.body.agent = self
        M=ode.Mass()
        self.shape.create_mass(M)
        self.body.setMass(M)

        self.geom = self.shape.create_geom(self.sim.space)

        self.geom.setBody(self.body)

        self.body.setPosition((random.uniform(-5, 5), random.uniform(4, 5), random.uniform(-5, 5)))

        theta = 0
        ct = math.cos(theta)
        st = math.sin(theta)
        self.body.setRotation([ct, 0.0, -st, 0.0, 1.0, 0.0, st, 0.0, ct])


    def move(self):
        self.body.addForce((self.energy * self.direction[0], 0.0, self.energy * self.direction[2]))

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
            newAgent = Agent(self.sim, self.sim.newAgentNumber, self,other)

    def fitness(self):
        """
        default function for returning the overall fitness of the agent.
        """
        return self.shape.get_size()



    def __str__(self):
        return "\tAgent " + str(self.number) + " [shape: " + str(self.shape) + ", fitness: " + str(
            self.fitness()) + ", energy: " + str(self.energy) + ", size: " + str(self.shape.sizes) + "]"
