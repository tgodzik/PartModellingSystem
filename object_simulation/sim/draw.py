from agent import Agent
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Draw(object):

    def __init__(self, sim):

        self.sim = sim
        self.init_openGl()
        self.init_camera()
        self.drawWalls = True

        glutKeyboardFunc(self.key_callback)
        glutSpecialFunc(self.special_key_callback);
        glutDisplayFunc(self.draw)
        glutReshapeFunc(self.reshape)
        glutIdleFunc(self.sim.idle)
        glutMainLoop()

    def init_openGl(self):

        glutInit([])
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)

        glutInitWindowPosition(0, 0);
        glutInitWindowSize(640, 480);
        glutCreateWindow("Simulation window")

    def init_camera(self):

        self.xpos = 0
        self.ypos = 0
        self.zpos = 0
        self.xrot = 0
        self.yrot = 90
        self.angle = 0.0

    def key_callback(self, c, x, y):

        if (c == '\x1b'):
            sys.exit(0)
        elif (c == 'i'):
            for agent in self.sim.agents:
                print agent
            print "Total: " + str(len(self.sim.agents)) + " agents in environment"
        elif (c == 'd'):
            self.drawWalls = not self.drawWalls

    def special_key_callback(self, c, x, y):

        if (c == GLUT_KEY_RIGHT):

            self.yrot += 10;
            if (self.yrot > 360):
                self.yrot -= 360

        elif (c == GLUT_KEY_LEFT):

            self.yrot -= 10;
            if (self.yrot < -360):
                self.yrot += 360

        elif (c == GLUT_KEY_UP):

            yrotrad = (self.yrot / 180 * pi)
            xrotrad = (self.xrot / 180 * pi)

            self.xpos += sin(yrotrad)/10
            self.zpos -= cos(yrotrad)/10
            self.ypos -= sin(xrotrad)/10

        elif (c == GLUT_KEY_DOWN):

            yrotrad = (self.yrot / 180 * pi)
            xrotrad = (self.xrot / 180 * pi)

            self.xpos -= sin(yrotrad)/10
            self.zpos += cos(yrotrad)/10
            self.ypos += sin(xrotrad)/10

    def draw(self):

        self.render()

        self.draw_floor(self.sim.floor)

        if self.drawWalls:
            self.draw_wall(self.sim.wall1)
            self.draw_wall(self.sim.wall2)
            self.draw_wall(self.sim.wall3)
            self.draw_wall(self.sim.wall4)

        for agent in self.sim.agents:
            self.draw_agent(agent)

        glutSwapBuffers()

    def reshape(self, w, h):
        glViewport(0, 0, w, h)

    def render(self):
        
        glClearColor(0.8, 0.8, 0.9, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_FLAT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 1.3333, 0.2, 20)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glLightfv(GL_LIGHT0, GL_POSITION, [0,0,1,0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])
        glEnable(GL_LIGHT0)

        gluLookAt(2.4, 3.6, 4.8, 0.5, 0.5, 0, 0, 1, 0)

        glRotatef(self.xrot, 1.0, 0.0, 0.0)
        glRotatef(self.yrot, 0.0, 1.0, 0.0)
        glTranslated(-self.xpos, -self.ypos, -self.zpos)

    def draw_floor(self, floor, color=(0.7, 1.0, 0.7)):

        normal, d = floor.getParams()
        glPushMatrix()

        glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, color)

        glBegin(GL_QUADS)

        glNormal3f(*normal)
        d = (normal[0]*self.sim.boardSize/2+normal[2]*self.sim.boardSize/2)/normal[1]
        glVertex3f(-self.sim.boardSize/2, d, -self.sim.boardSize/2)

        glNormal3f(*normal)
        d = (-normal[0]*self.sim.boardSize/2+normal[2]*self.sim.boardSize/2)/normal[1]
        glVertex3f(self.sim.boardSize/2, d, -self.sim.boardSize/2)

        glNormal3f(*normal)
        d = (-normal[0]*self.sim.boardSize/2-normal[2]*self.sim.boardSize/2)/normal[1]
        glVertex3f(self.sim.boardSize/2, d, self.sim.boardSize/2)

        glNormal3f(*normal)
        d = (normal[0]*self.sim.boardSize/2-normal[2]*self.sim.boardSize/2)/normal[1]
        glVertex3f(-self.sim.boardSize/2, d, self.sim.boardSize/2)

        glEnd()

        glPopMatrix()

    def draw_wall(self, wall, color=(0.7, 1.0, 0.7)):

        normal, d = wall.getParams()
        glPushMatrix()

        glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, color)

        if normal[0]:

            glBegin(GL_QUADS)

            glNormal3f(*normal)
            glVertex3f(d*normal[0], -5.0, -self.sim.boardSize/2)

            glNormal3f(*normal)
            glVertex3f(d*normal[0], -5.0, self.sim.boardSize/2)

            glNormal3f(*normal)
            glVertex3f(d*normal[0], 5.0, self.sim.boardSize/2)

            glNormal3f(*normal)
            glVertex3f(d*normal[0], 5.0, -self.sim.boardSize/2)

            glEnd()

        if normal[2]:

            glBegin(GL_QUADS)

            glNormal3f(*normal)
            glVertex3f(-self.sim.boardSize/2, -5.0,d*normal[2] )

            glNormal3f(*normal)
            glVertex3f(self.sim.boardSize/2, -5.0,d*normal[2] )

            glNormal3f(*normal)
            glVertex3f(self.sim.boardSize/2 , 5.0,d*normal[2] )

            glNormal3f(*normal)
            glVertex3f( -self.sim.boardSize/2, 5.0,d*normal[2])

            glEnd()

        glPopMatrix()

    def draw_agent(self, agent):

        x, y, z = agent.body.getPosition()
        R = agent.body.getRotation()
        rot = [R[0], R[3], R[6], 0.,
            R[1], R[4], R[7], 0.,
            R[2], R[5], R[8], 0.,
            x, y, z, 1.0]
        glPushMatrix()
        glMultMatrixd(rot)
        glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, agent.color)

        if (agent.shape == Agent.SHAPE_BOX):
            glScalef(agent.sizes['lx'], agent.sizes['ly'], agent.sizes['lz'])
            glutSolidCube(1)
        elif (agent.shape == Agent.SHAPE_SPHERE):
            d = agent.sizes['radius']*2
            glScalef(d, d, d)
            glutSolidSphere(agent.sizes['radius'], 32, 32)
        elif (agent.shape == Agent.SHAPE_CYLINDER):
            d = agent.sizes['radius']*2
            glScalef(agent.sizes['height'], d, d)
            glutSolidCylinder(agent.sizes['radius'], agent.sizes['height'], 32, 32)

        glPopMatrix()
