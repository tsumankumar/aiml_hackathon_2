from OpenGL.GL import *
from OpenGL.GLU import *

class Road:
    def __init__(self):
        pass

    def getBasicRoad(self):
        #roadSegment1 = RoadSegment(300, 200, 100, 250, "vertical")
        roadSegment1 = RoadSegment(-10, -50, 20, 100, "vertical")
        roadSegment2 = RoadSegment(-30, -10, 60, 20, "horizontal")
        #roadSegment3 = RoadSegment(300, 550, 100, 250, "vertical")
        #roadSegment4 = RoadSegment(400, 450, 100, 100, "horizontal")
        self.road = [roadSegment1 , roadSegment2] #, roadSegment3, roadSegment4]
        return self.road

    def drawBasicRoad(self):
        self.getBasicRoad()
        glPushMatrix()

        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0xAAA)
        glLineWidth(3)
        glColor3fv((1,1,1))
        glBegin(GL_LINES)
        for segment in self.road:
            lines = segment.getLines()
            glVertex3fv(((lines[0][0] + lines[1][0])/2, (lines[0][1] + lines[1][1])/2, -0.5))
            glVertex3fv(((lines[0][2] + lines[1][2])/2, (lines[0][3] + lines[1][3])/2, -0.5))
        glEnd()

        glBegin(GL_QUADS)
        glColor3fv((0,0,0))
        for segment in self.road:
            lines = segment.getLines()
            glVertex3fv((lines[0][0], lines[0][1], -0.5))
            glVertex3fv((lines[0][2], lines[0][3], -0.5))
            glVertex3fv((lines[1][2], lines[1][3], -0.5))
            glVertex3fv((lines[1][0], lines[1][1], -0.5))
        glEnd()
        glPopMatrix()

class RoadSegment:

    def __init__(self, x, y, width, height, orientation):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation

    def getLines(self):
        if self.orientation == "horizontal":
            return [[self.x, self.y, self.x + self.width, self.y], [self.x, self.y + self.height, self.x + self.width, self.y + self.height]]
        else:
            return [[self.x, self.y, self.x, self.y + self.height], [self.x + self.width, self.y, self.x + self.width, self.y + self.height]]




