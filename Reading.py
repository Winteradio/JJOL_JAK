from bvh import Bvh
from scipy.spatial.transform import Rotation as R

import numpy as np
import math

class Reading():

    def __init__(self):
        self.BVH_pose = np.zeros(48)
        self.BVH_vec = np.zeros((199,48))
        self.BVH = np.zeros((199,16,3,3))
        self.Num = 0

        self.BVH_Read()
        return None

    def BVH_Read(self):
        f = open("sample-walk.bvh","r")
        while self.Num < 99:
            lines = f.readline()
            self.Num +=1

        if self.Num >= 99:
            while self.Num < 298:
                lines = f.readline()
                lines = lines.split()
                lines = np.array(list(map(float,lines))).T

                self.BVH_pose = np.vstack([self.BVH_pose,lines])
                self.Num+=1

            self.BVH_pose = np.delete(self.BVH_pose,(0),axis=0)

            for i in range(199):
                for j in range(3):
                    self.BVH_pose[i][j] = 0
        f.close()

        for i in range(199):
            for j in range(16):
                Z_angle=self.BVH_pose[i][3*j]*math.pi/180
                X_angle=self.BVH_pose[i][3*j+1]*math.pi/180
                Y_angle=self.BVH_pose[i][3*j+2]*math.pi/180
            
                Z_ROT=np.array([[np.cos(Z_angle),-np.sin(Z_angle),0],
                                [np.sin(Z_angle),np.cos(Z_angle),0],
                                [0,0,1]])
                X_ROT=np.array([[1,0,0],
                                [0,np.cos(X_angle),-np.sin(X_angle)],
                                [0,np.sin(X_angle),np.cos(X_angle)]])
                Y_ROT=np.array([[np.cos(Y_angle),0,np.sin(Y_angle)],
                                [0,1,0],
                                [-np.sin(Y_angle),0,np.cos(Y_angle)]])
                ROT = Z_ROT@ X_ROT @ Y_ROT
                for k in range(3):
                    self.BVH_vec[i][k+3*j] = R.from_matrix(ROT).as_rotvec()[k]
                self.BVH[i][j] = ROT
        return None

    def TXT_Read(self):
        return None

    def C3D_Read(self):
        return None

