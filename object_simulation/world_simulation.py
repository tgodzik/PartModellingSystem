#!/usr/bin/python

from sim.simulation import Simulation


def fight(object, other):

    fit1 = object.fitness()
    fit2 = other.fitness()

    if fit1 > fit2:
        object.energy += 100
        other.energy -= 100
    elif fit2 > fit1:
        object.energy -= 100
        other.energy += 100

def fitness(self):
    return self.color[1]-self.color[0]-self.color[2]

if __name__ == '__main__':

    parameters = {
        "func_fight": fight,
        "maximum_iterations": 1000,
        "floor": (0.2, 0.979796, 0)
    }

    sim = Simulation(20, 12, parameters)
    sim.run()
    #sim.run_without_graphics()
