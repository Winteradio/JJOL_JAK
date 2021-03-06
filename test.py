import sys
import OpenGL

from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *

def draw():
      glClear(GL_COLOR_BUFFER_BIT)
      glutWireTeapot(0.5)
      glFlush()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(250, 250)
glutInitWindowPosition(100, 100)
glutCreateWindow("Python OGL Program")
glutDisplayFunc(draw)
glutMainLoop()

draw()
