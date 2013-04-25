#!/usr/bin/env python
from SimPy.Simulation import *

## Model components -----------------------------

class Customer(Process):
    """ Customer arrives, looks around and leaves """

    def visit(self, timeInBank):
        print("%2.1f %s  Here I am" % (now(), self.name))
        yield hold, self, timeInBank
        print("%2.1f %s  I must leave" % (now(), self.name))

## Experiment data ------------------------------

maxTime = 100.0     # minutes #8
timeInBank = 10.0   # minutes

## Model/Experiment ------------------------------

initialize()                              #9
c = Customer(name="Klaus")                #10
activate(c, c.visit(timeInBank), at=5.0)  #11
simulate(until=maxTime)                   #12
