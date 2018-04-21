from OpenGL.GL import *
from OpenGL.GLU import *
class Cuboid:
    def __init__(self,scalex, scaley, scalez, color):
        self.vertices = ((1*scalex, -1*scaley, -1*scalez), (1*scalex, 1*scaley, -1*scalez), (-1*scalex, 1*scaley, -1*scalez), (-1*scalex, -1*scaley, -1*scalez),
                        (1*scalex, -1*scaley, 1*scalez), (1*scalex, 1*scaley, 1*scalez), (-1*scalex, -1*scaley, 1*scalez), (-1*scalex, 1*scaley, 1*scalez))
        self.edges    = ( (0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))
        self.surfaces = ((0,1,2,3), (3,2,7,6), (6,7,5,4), (4,5,1,0), (1,5,7,2), (4,0,3,6)) 
        #self.drawCuboid()
        self.color = color

    def drawCuboid(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def drawSolidCuboid(self):
        glBegin(GL_QUADS)
        glColor3f(self.color[0], self.color[1], self.color[2])
        for surface in self.surfaces:
            for vertex in surface:
                glVertex3f(self.vertices[vertex][0], self.vertices[vertex][1], self.vertices[vertex][2])
        glEnd()
