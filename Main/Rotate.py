import numpy as np

def Degree_to_Radian(Angle):
    for i in range(3):
        Angle[i] = -1*np.pi*Angle[i]/180
    return Angle

def Euler_Rotation(Vector,Angle):
    Angle = Degree_to_Radian(Angle)
    Matrix_X = np.array([
        [1,0,0],
        [0,np.cos(Angle[0]),-np.sin(Angle[0])],
        [0,np.sin(Angle[0]),np.cos(Angle[0])]
        ], dtype = np.float64)

    Matrix_Y = np.array([
        [np.cos(Angle[1]),0,np.sin(Angle[1])],
        [0,1,0],
        [-np.sin(Angle[1]),0,np.cos(Angle[1])]
        ], dtype = np.float64)

    Matrix_Z = np.array([
        [np.cos(Angle[2]),-np.sin(Angle[2]),0],
        [np.sin(Angle[2]),np.cos(Angle[2]),0],
        [0,0,1]
        ], dtype = np.float64)
    
    Matrix = Matrix_Z @ Matrix_Y @ Matrix_X
    Vector = Matrix_Z @ Matrix_Y @ Matrix_X @ Vector
    return Vector

def Euler_to_Quaternion(Angle):
    X = Angle[0]/2
    Y = Angle[1]/2
    Z = Angle[2]/2
    Quaternion = np.array([
        np.cos(Z) * np.cos(Y) * np.cos(X) + np.sin(Z) * np.sin(Y) * np.sin(X),
        np.cos(Z) * np.cos(Y) * np.sin(X) - np.sin(Z) * np.sin(Y) * np.cos(X),
        np.cos(Z) * np.sin(Y) * np.cos(X) + np.sin(Z) * np.cos(Y) * np.sin(X),
        np.sin(Z) * np.cos(Y) * np.cos(X) - np.cos(Z) * np.sin(Y) * np.sin(X)
        ], dtype = np.float64)
    return Quaternion

def Quaternion_Rotation(Vector,Quaternion):
    N = Quaternion[0]
    X = Quaternion[1]
    Y = Quaternion[2]
    Z = Quaternion[3]
    Matrix = np.array([
        [np.power(N,2)+np.power(X,2)-np.power(Y,2)-np.power(Z,2), 2*(X*Y - N*Z), 2*(X*Z + N*Y)],
        [2*(X*Y + N*Z), np.power(N,2)-np.power(X,2)+np.power(Y,2)-np.power(Z,2), 2*(Y*Z - N*X)],
        [2*(X*Z - N*Y), 2*(Y*Z + N*X), np.power(N,2)-np.power(X,2)-np.power(Y,2)+np.power(Z,2)]
        ],dtype = np.float64) 
    Vector = Matrix @ Vector
    return Vector

def Actual_Rotation(Vector, Angle):
    Angle = Degree_to_Radian(Angle)
    Quaternion = Euler_to_Quaternion(Angle)
    Vector = Quaternion_Rotation(Vector,Quaternion)
    return Vector
