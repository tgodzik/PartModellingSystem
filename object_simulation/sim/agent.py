import ode, random, math

class Agent(object):
    SHAPE_BOX = 1
    SHAPE_SPHERE = 2
    SHAPE_CYLINDER = 3
    direction=(0.0,0.0,1.0)

    def __init__(self, sim, number, shape,new=True,agent1=None,agent2=None):
        self.shape = shape
        self.number = number
        self.sim = sim
        if new:
            self.generate_sizes()
            self.create_geometry()
            self.energy=random.randint(1000,1500)
        else:
            self.energy=400
            self.inherit_sizes(agent1,agent2)
            agent1.energy=agent1.energy-200
            agent2.energy=agent2.energy-200
            #self.create_geometry()



    #moves in one direction or changes it randomly
    def move(self):
        self.body.addForce((self.energy*self.direction[0],0.0,self.energy*self.direction[2]))
        if random.random > 0.9:
            choice=random.randint(1,4)
            if choice==1:
                self.direction=(1.0,0.0,0.0)
            elif choice==2:
                self.direction=(-1.0,0.0,0.0)
            elif choice==3:
                self.direction=(0.0,0.0,1.0)
            else:
                self.direction=(0.0,0.0,-1.0)

    #randomize size and colors initialy
    def generate_sizes(self):
        if (self.shape == self.SHAPE_BOX):
            self.sizes = {'lx': random.uniform(0.2, 1), 'ly': random.uniform(0.2, 1), 'lz': random.uniform(0.2, 1)}
        elif (self.shape == self.SHAPE_SPHERE):
            self.sizes = {'radius': random.uniform(0.2, 0.5)}
        elif (self.shape == self.SHAPE_CYLINDER):
            self.sizes = {'radius': random.uniform(0.2, 0.5), 'height': random.uniform(0.2, 0.5)}

        self.color = (random.random(), random.random(), random.random())
        self.density = 1000

    #    inheritance model
    def inherit_sizes(self,agent1,agent2):
        self.sizes={}

        if (self.shape == self.SHAPE_BOX):

            if random.random()>0.5:
                self.sizes['lx']=agent1.sizes['lx']
            else:
                self.sizes['lx']=agent2.sizes['lx']
            if random.random()>0.5:
                self.sizes['ly']=agent1.sizes['ly']
            else:
                self.sizes['ly']=agent2.sizes['ly']
            if random.random()>0.5:
                self.sizes['lz']=agent1.sizes['lz']
            else:
                self.sizes['lz']=agent2.sizes['lz']

        elif (self.shape == self.SHAPE_SPHERE):
            if random.random()>0.5:
                self.sizes['radius']=agent1.sizes['radius']
            else:
                self.sizes['radius']=agent2.sizes['radius']
        elif (self.shape == self.SHAPE_CYLINDER):
            if random.random()>0.5:
                self.sizes['radius']=agent1.sizes['radius']
            else:
                self.sizes['radius']=agent2.sizes['radius']
            if random.random()>0.5:
                self.sizes['height']=agent1.sizes['height']
            else:
                self.sizes['height']=agent2.sizes['height']
        #chossing color scheme
        r=0
        g=0
        b=0
        if random.random()>0.5:
            r=agent1.color[0]
        else:
            r=agent2.color[0]
        if random.random()>0.5:
            g=agent1.color[1]
        else:
            g=agent2.color[1]
        if random.random()>0.5:
            b=agent1.color[2]
        else:
            b=agent2.color[2]
        self.color = (r,g,b)
        self.density = 1000

    def create_geometry(self):
        self.body = ode.Body(self.sim.get_world())
        self.body.agent=self
        M = ode.Mass()

        if (self.shape == self.SHAPE_BOX):
            M.setBox(self.density, self.sizes['lx'], self.sizes['ly'], self.sizes['lz'])
        elif (self.shape == self.SHAPE_SPHERE):
            M.setSphere(self.density, self.sizes['radius'])
        elif (self.shape == self.SHAPE_CYLINDER):
            M.setCylinder(self.density, 1, self.sizes['radius'], self.sizes['height'])

        self.body.setMass(M)

        if (self.shape == self.SHAPE_BOX):
            self.geom = ode.GeomBox(self.sim.get_space(),
                lengths=(self.sizes['lx'], self.sizes['ly'], self.sizes['lz']))
        elif (self.shape == self.SHAPE_SPHERE):
            self.geom = ode.GeomSphere(self.sim.get_space(), self.sizes['radius'])
        elif (self.shape == self.SHAPE_CYLINDER):
            self.geom = ode.GeomCylinder(self.sim.get_space(), self.sizes['radius'], self.sizes['height'])

        self.geom.setBody(self.body)
        self.body.name="agent"

        self.body.setPosition((random.uniform(-5, 5), random.uniform(2, 5), random.uniform(-5, 5)))

        theta = 0
        ct = math.cos(theta)
        st = math.sin(theta)
        self.body.setRotation([ct, 0., -st, 0., 1., 0., st, 0., ct])

    def fight(self,other):
        size1=self.get_size()
        size2=other.get_size()
        if size1>size2:
            self.energy=self.energy+100
            other.energy=other.energy-100
        elif size2>size1:
            self.energy=self.energy+100
            other.energy=other.energy-100



    def get_shape(self):
        return self.shape

    def get_body(self):
        return self.body

    def get_sizes(self):
        return self.sizes

    def get_size(self):
        if (self.shape == self.SHAPE_BOX):
            return self.sizes['lx']*self.sizes['ly']*self.sizes['lz']
        elif (self.shape == self.SHAPE_SPHERE):
            return math.pi*self.sizes['radius']*self.sizes['radius']*self.sizes['radius']*4/3
        elif (self.shape == self.SHAPE_CYLINDER):
            return math.pi*self.sizes['radius']*self.sizes['radius']*self.sizes['height']

    def get_color(self):
        return self.color
