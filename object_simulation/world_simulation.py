import ode
import sys, os, random, time
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ode_shapes.shapes import *
from opengl_drawing.draw import *

# drop_object
def set_box(x,y,z):
    """Drop an object into the scene."""

    global bodies, geom, counter, objcount

    body, geom = create_box(world, space, 1000, 0.5,0.4,0.3)
    body.setPosition( (x,y,z) )

    theta = 0
    ct = cos (theta)
    st = sin (theta)
    body.setRotation([ct, 0., -st, 0., 1., 0., st, 0., ct])


    bodies.append(body)
    geoms.append(geom)
    counter=0
    objcount+=1


# drop_object
def set_sphere(x,y,z):
    """Drop an object into the scene."""

    global bodies, geom, counter, objcount

    body, geom = create_sphere(world, space, 1000, 0.2)
    body.setPosition( (x,y,z) )

    theta = 0
    ct = cos (theta)
    st = sin (theta)
    body.setRotation([ct, 0., -st, 0., 1., 0., st, 0., ct])
    bodies.append(body)
    geoms.append(geom)
    objcount+=1

# drop_object
def set_cylinder(x,y,z):
    """Drop an object into the scene."""

    global bodies, geom, counter, objcount

    body, geom = create_cylinder(world, space, 1000, 0.2,0.5,1)
    body.setPosition( (x,y,z) )

    theta = 0
    ct = cos (theta)
    st = sin (theta)
    body.setRotation([ct, 0., -st, 0., 1., 0., st, 0., ct])
    bodies.append(body)
    geoms.append(geom)
    objcount+=1

# Collision callback
def near_callback(args, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.
    """

    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    world,contactgroup = args
    for c in contacts:
        c.setBounce(0.2)
        c.setMu(100)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

######################################################################

# Initialize Glut
glutInit ([])

# Open a window
glutInitDisplayMode (GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)

x = 0
y = 0
width = 640
height = 480
glutInitWindowPosition (x, y);
glutInitWindowSize (width, height);
glutCreateWindow ("Simulation window")

# Create a world object
world = ode.World()
world.setGravity( (0,-9.81,0) )
world.setERP(0.8)
world.setCFM(1E-5)

# Create a space object
space = ode.Space()

# plane for the objects
floor = ode.GeomPlane(space, (0.1,1,0), 0)


# A list with ODE bodies
bodies = []

# The geoms for each of the bodies
geoms = []

# A joint group for the contact joints that are generated whenever
# two bodies collide
contactgroup = ode.JointGroup()

# Some variables used inside the simulation loop
fps = 50
dt = 1.0/fps
running = True
state = 0
counter = 0
objcount = 0
lasttime = time.time()


# keyboard callback
def _keyfunc (c, x, y):
    sys.exit (0)


glutKeyboardFunc (_keyfunc)

# draw callback
def _drawfunc ():
    # Draw the scene
    prepare_GL()
    for b in bodies:
        draw_body(b)


    glutSwapBuffers ()

glutDisplayFunc (_drawfunc)

set_sphere(0.05,0.4,0.35)
set_box(0.4,0.4,1.35)
set_cylinder(0.4,2.0,1.35)
# idle callback
def _idlefunc ():
    global counter, state, lasttime

    t = dt - (time.time() - lasttime)
    if (t > 0):
        time.sleep(t)

    counter += 1
    for b in bodies:
        b.addForce((-400,0.0,0.0))
    glutPostRedisplay ()

    # Simulate
    n = 4

    for i in range(n):
        # Detect collisions and create contact joints
        space.collide((world,contactgroup), near_callback)

        # Simulation step
        world.step(dt/n)

        # Remove all contact joints
        contactgroup.empty()

    lasttime = time.time()

glutIdleFunc (_idlefunc)

glutMainLoop ()

