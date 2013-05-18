__author__ = 'tomasz'

import ode, random

# world - ode world, space - ode space   
def create_box(world, space, density, lx, ly, lz):

    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setBox(density, lx, ly, lz)
    body.setMass(M)

    # Set parameters for drawing the body
    body.shape = "box"
    body.color = (random.random(), random.random(), random.random())
    body.box_size = (lx, ly, lz)

    # Create a box geom for collision detection
    geom = ode.GeomBox(space, lengths=body.box_size)
    geom.setBody(body)

    return body, geom

# world - ode world, space - ode space
def create_sphere(world, space, density, radius):

    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setSphere(density,radius)
    body.setMass(M)

    # Set parameters for drawing the body
    body.shape = "sphere"
    body.color = (random.random(), random.random(), random.random())
    body.sphere_size = (radius)

    # Create a box geom for collision detection
    geom = ode.GeomSphere(space,radius)
    geom.setBody(body)

    return body, geom

# world - ode world, space - ode space, axis - 1-x, 2-y, 3-z,
def create_cylinder(world, space, density, radius, height,axis):

    # Create body
    body = ode.Body(world)
    M = ode.Mass()
    M.setCylinder(density,axis,radius,height)
    body.setMass(M)

    # Set parameters for drawing the body
    body.shape = "cylinder"
    body.color = (random.random(), random.random(), random.random())
    body.cylinder_size = (radius,axis,height)

    # Create a box geom for collision detection
    geom = ode.GeomCylinder(space,radius,height)
    geom.setBody(body)

    return body, geom