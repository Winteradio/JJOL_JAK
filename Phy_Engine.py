import numpy as np
import os
import math
import sys

class Physics():

    def __init__(self):
        self.gravity = [0,-9.81,0]
        self.drag_coefficient = 0.5;
        self.collision_coefficient = 0.2;
        self.spring_coefficient = 0.5;
        self.damper_coefficient = 0.8;

        return None

    def Contact(self):
        return None

    def Collision(self):
        return None

    def Cal_Force(self):
        return None

    def Cal_Position(self):
        return None
