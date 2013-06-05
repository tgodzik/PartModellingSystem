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
VERTICES = [(board_size / 2, -1.0, board_size / 2),
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

INDICES = [(0, 8, 1),
           (1, 8, 12),
           (1,9,2),
           (1,12,9),
           (2,9,3),
           (9,12,3),
           (3,12,10),
           (3,10,4),
           (4,10,5),
           (12,5,10),
           (6,5,11),
           (11,5,12),
           (6,11,7),
           (7,11,12),
           (0,7,8),
           (8,7,12)]

if __name__ == '__main__':
    parameters = {
        "func_fight": fight,
        "maximum_iterations": 1000,
        "indices": INDICES,
        "vertices": VERTICES
    }

    sim = Simulation(20, board_size, parameters)
    sim.run()
    #sim.run_without_graphics()
