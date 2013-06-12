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
    return self.color[1] - self.color[0] - self.color[2]

board_size = 20


if __name__ == '__main__':

    sim = Simulation()
    #sim.run()
    sim.run()
