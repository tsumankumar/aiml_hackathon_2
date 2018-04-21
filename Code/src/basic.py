from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from cuboid import Cuboid
from road import Road, RoadSegment
print("imported Road and Road segment")

## Road at (200, 200) to (500, 1000)
cuboid = Cuboid(1,1,1,(1,0,0))

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glVertex2f(x, y)                                   # bottom left point
    glVertex2f(x + width, y)                           # bottom right point
    glVertex2f(x + width, y + height)                  # top right point
    glVertex2f(x, y + height)                          # top left point
    glEnd()  

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw():
    print("Entered draw")
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    glTranslatef(0.0,0.0,-20.0)
    #refresh2d(600, 1200)
    cuboid.drawSolidCuboid()
    #glColor3f(0.0, 0.0, 1.0)
    #draw_rect(10, 10, 200, 100)
    glutSwapBuffers()

def main_1():
    ## Draw Roadbase
    print("Entered")
    width = 600
    height = 1200
    glutInit()                                             # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    #  Enable Z-buffer depth test
    #glEnable(GL_DEPTH_TEST)
    glutInitWindowSize(width, height)                      # set window size
    glutInitWindowPosition(0, 0)                           # set window position
    window = glutCreateWindow("Turn Right and Win")              # create window with title
    glutDisplayFunc(draw)                                  # set draw function callback
    glutIdleFunc(draw)                                     # draw all the time
    glutMainLoop() 
main_1()
