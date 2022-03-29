from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import os
import math
import numpy as np

class Drawing:

    def __init__(self):
        return None

    def Baseline(self):
        for i in range(200):
            glLineWidth(2.0)
            glBegin(GL_LINES)
            if i==100:
                glColor3f(1,1,0) # x축
                glVertex3fv([1,0,0])
                glVertex3fv([0,0,0])
                glColor3f(0,1,0) # z축
                glVertex3fv([0,0,1])
                glVertex3fv([0,0,0])
                
                glColor3f(0.5,0.5,0.5)
                glVertex3fv([100,0,0])
                glVertex3fv([1,0,0])
                glVertex3fv([0,0,0])
                glVertex3fv([-100,0,0])
                glVertex3fv([0,0,100])
                glVertex3fv([0,0,1])
                glVertex3fv([0,0,0])
                glVertex3fv([0,0,-100])
            else :
                glColor3f(0.5,0.5,0.5)
                glVertex3fv([-100+i,0,-100])
                glVertex3fv([-100+i,0,100])
                glVertex3fv([100,0,-100+i])
                glVertex3fv([-100,0,-100+i])
            glEnd()

        glLineWidth(2.0)
        glBegin(GL_LINES)    
        glColor3f(0,0,1)
        glVertex3fv([0,1,0])
        glVertex3fv([0,0,0])
        glEnd()


    def Box(self,degree):
        glutSolidCube(1.0)

    def Sphere(self,degree):
        glutSolidSphere(degree,30,30)

    def Draw_Skeleton(self,Pos,Euler,Scale,Name):
        glPushMatrix()
        glTranslatef(Pos[0],Pos[1],Pos[2])
        glMultMatrixf(Euler.T)
        glScalef(Scale[0],Scale[1],Scale[2])

        if Name == "Ground":
            glColor3f(0.1,0.1,0.0)
            self.Box(1.0)

        else :
            glColor3f(0.0,0.5,0.2)
            self.Sphere(1.0)
        glPopMatrix()
        glFlush()
