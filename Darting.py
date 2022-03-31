from scipy.spatial.transform import Rotation as R

import os
import math
import dartpy as dart
import numpy as np

import Drawing
import Reading

class Darting :

    def __init__(self):
        self.world=dart.utils.SkelParser.readWorld(os.path.abspath('human32.skel'))
        self.world.setGravity([0,0,0])
        self.Num_Skeleton = self.world.getNumSkeletons()
        self.timestep = self.world.getTimeStep()

        # World.getNumSkeletons() : World 상에 존재하는 SKeleton의 개수들을 추출한다        

        self.Drawing = Drawing.Drawing()
        self.Reading = Reading.Reading()
        self.Frame_VEC = self.Reading.BVH_vec

        self.start = 0
        self.end = 198

        self.frame = self.start

        self.Coefficient()

        return None

    def Skeleton(self):
        for i in range(self.Num_Skeleton):
            Skel = self.world.getSkeleton(i)
            if Skel.getName() == "Ground":
                Body = Skel.getBodyNode(0)
                self.Ground_pos = np.array(Body.getWorldTransform().translation())

        for i in range(self.Num_Skeleton):
            Skel = self.world.getSkeleton(i)
            Num_Body = Skel.getNumBodyNodes()
            Num_Joint = Skel.getNumJoints()

            for j in range(Num_Body):
                Body = Skel.getBodyNode(j)
                Position = np.array(Body.getWorldTransform().translation())
                Rotation = np.array(Body.getWorldTransform().rotation())
                Scale = np.array(Body.getShapeNode(0).getShape().getSize())/2
                Euler = self.Euler(Rotation)

                self.Drawing.Draw_Skeleton(Position-self.Ground_pos,Euler,Scale,Skel.getName())

    def Euler(self,Rot):
        Real_Rot = np.zeros((4,4))

        for i in range(3):
            for j in range(3):
                Real_Rot[i][j] = Rot[i][j]
        Real_Rot[3][3]=1

        return Real_Rot

    def Counter(self):
        self.Skeleton()

        for i in range(30):
            self.world.step()
            self.SPD_Control()
        
        if self.frame >= self.end:
            self.frame = self.start

        elif self.frame < self.end:
            self.frame +=1

    def PD_Control(self):
        return None

    def SPD_Control(self):
        for i in range(self.Num_Skeleton):
            Skel = self.world.getSkeleton(i)
            if Skel.getName() != "Ground":
                position = Skel.getPositions()
                velocity = Skel.getVelocities()
                    
                invM = np.linalg.inv(Skel.getMassMatrix() + self.Kd * self.timestep)
                PP = np.matmul(-self.Kp,position + velocity*self.timestep - self.Frame_VEC[self.frame])
                DD = np.matmul(-self.Kd, velocity)
                QDDOT = np.matmul(invM,-Skel.getCoriolisAndGravityForces() + PP + DD + Skel.getConstraintForces())
                Torque = PP + DD + np.matmul( -self.Kd , QDDOT) * self.timestep 
                
                Skel.setForces(Torque)

        return None

    def Coefficient(self):
        for i in range(self.Num_Skeleton):
            Skel = self.world.getSkeleton(i)
            if Skel.getName() != "Ground":
                self.dofs = Skel.getNumDofs()
                self.Kp = np.eye(self.dofs)
                self.Kd = np.eye(self.dofs)

                for i in range(6):
                    self.Kp[i,i] = 0.0
                    self.Kd[i,i] = 0.0

                for i in range(6,self.dofs):
                    self.Kp[i,i] = 2000
                    self.Kd[i,i] = 40

        return None
