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

board_size=20
VERTICES = [(board_size / 2, -1.0, board_size / 2),
                 (0.0, -1.0, board_size / 2),
                 (-board_size / 2, 1.0,board_size/ 2),
                 (-board_size / 2, 1.0, 0.0),
                 (-board_size / 2, 0.0, -board_size / 2),
                 (0.0, 0.0, -board_size / 2),
                 (board_size / 2, -1.0, -board_size / 2),
                 (board_size / 2, 0.0, 0.0),
                 (0.0, 1.0, 0.0)]

INDICES = [(0, 8, 1), (1, 8, 2), (2, 8, 3), (3, 8, 4),
                (4, 8, 5),
                (5, 8, 6),
                (6, 8, 7),
                (7, 8, 0)]

if __name__ == '__main__':

    parameters = {
        "func_fight": fight,
        "maximum_iterations": 1000,
        "indices":INDICES,
        "vertices":VERTICES,
        "func_fit":fitness
    }

    sim = Simulation(20, board_size, parameters)
    sim.run()
    #sim.run_without_graphics()
