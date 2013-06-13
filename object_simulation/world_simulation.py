#!/usr/bin/python

from sim.simulation import Simulation,Configuration
from sim.agent import Sphere,Agent

class AverageSphere(Sphere):
    def create_new_sizes(self, shape1,shape2):
        self.sizes = {'radius': ( shape1.sizes['radius'] + shape2.sizes['radius'])/2}
        print self.sizes["radius"]

def breed(self, other):
    if self.energy > 400 and other.energy > 400:
        self.energy -= 400
        other.energy -= 400
        newAgent = Agent(self.sim, self.sim.newAgentNumber,self.shape.__class__, self,other)

def fitness(self):
    return self.color[1] - self.color[0] - self.color[2]

board_size = 20


if __name__ == '__main__':
    configuration=Configuration(20,15.0,AverageSphere)
    configuration.function_breed(breed)
    configuration.set_max_iterations(1000)
    sim = Simulation(configuration)
    sim.run(False)
