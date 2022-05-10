from datetime import datetime, timedelta
from Rotate import *

import time
import numpy as np

class Frame_Data :

    def __init__(self,Time = None, TimeStep = 0,
            Acceleration = np.zeros(3), Angular_Acceleration = np.zeros(3),
            Velocity = np.zeros(3), Angular_Velocity = np.zeros(3),
            Angle = np.zeros(3)):
        self.Time = Time
        self.TimeStep = TimeStep

        self.Acceleration = Acceleration
        self.Angular_Acceleration = Angular_Acceleration

        self.Velocity = Velocity
        self.Angular_Velocity = Angular_Velocity

        self.Angle = Angle

class Main_Data :

    def __init__(self, Name=None, Data = None):
        self.Name = Name

        self.Data = Data

class Read :
    def __init__(self):
        self.Device_List = []
        self.Make_List()
        return None

    def Make_List(self):
        File = open('/home/tot4766/종설/data.txt','r')
        print("----- Start Reading File & Make Device Variables -----")
        while True:
            Line = File.readline()
            if not Line :
                print("----- End Reading File -----","","",sep="\n")
                break
            Line = Line.split()
            if Line[2] != "Device":
                self.File_Divide(Line)
        File.close()
        return 0

    def File_Divide(self,Line):
        # 장치에 대한 변수 여부 확인
        Date_Time = "{} {}".format(Line[0],Line[1])

        if f'{Line[2]}' in globals(): # 변수 있을 시 넘어감
            self.Input_Datetime_Calculation_TimeStep(Line[2],Date_Time)
            self.Input_Acceleration_AngularVelocity_Angle(Line)
            self.Calculation_Velocity(Line[2])
            self.Calculation_Angular_Acceleration(Line[2])
            pass
        else : # 변수 없을 시 생성 
            print("Device Variables Number : ", f"{Line[2]}")
            self.Device_List.append(Line[2])
            # 동적 변수 할당
            globals()[f'{Line[2]}']=Main_Data(Line[2])
            # 장치의 멏 데이터 추가
            globals()[f'{Line[2]}'].Data = [Frame_Data(Date_Time)]
            self.Input_Acceleration_AngularVelocity_Angle(Line)
            #print(globals()[f'{Line[2]}'].Data[0].Time)
        return 0

    def Input_Acceleration_AngularVelocity_Angle(self,Line):
        Acceleration = np.zeros(3)
        Angular_Velocity = np.zeros(3)
        Angle = np.zeros(3)
        
        for i in range(3):
            Acceleration[i] = float(Line[3+i])
            Angular_Velocity[i] = float(Line[6+i])
            Angle[i] = float(Line[9+i])

        globals()[f'{Line[2]}'].Data[-1].Angle = Angle
        self.Change_Coordinate(Line[2],Acceleration,Angular_Velocity,Angle)

    def Input_Datetime_Calculation_TimeStep(self,Name,Date_Time):
        globals()[f'{Name}'].Data.append(Frame_Data(Date_Time))

        Before_Date = globals()[f'{Name}'].Data[-2].Time
        After_Date = globals()[f'{Name}'].Data[-1].Time

        Before_Date = datetime.strptime(Before_Date,"%Y-%m-%d %H:%M:%S.%f")
        After_Date = datetime.strptime(After_Date,"%Y-%m-%d %H:%M:%S.%f")

        Deltatime = After_Date - Before_Date
        TimeStep = Deltatime.seconds + Deltatime.microseconds /(10**6)
        
        globals()[f'{Name}'].Data[-1].TimeStep = TimeStep

        return None

    def Calculation_Velocity(self,Name):
        Before_Velocity = globals()[f'{Name}'].Data[-2].Velocity
        Before_Acceleration = globals()[f'{Name}'].Data[-2].Acceleration
        
        Now_TimeStep = globals()[f'{Name}'].Data[-1].TimeStep
        Now_Acceleration = globals()[f'{Name}'].Data[-1].Acceleration
        Now_Velocity = Before_Velocity + (Before_Acceleration + Now_Acceleration) / Now_TimeStep
        
        globals()[f'{Name}'].Data[-1].Velocity = Now_Velocity

    def Calculation_Angular_Acceleration(self,Name):
        Before_Angular_Velocity = globals()[f'{Name}'].Data[-2].Angular_Velocity
        
        Now_TimeStep = globals()[f'{Name}'].Data[-1].TimeStep
        Now_Angular_Velocity = globals()[f'{Name}'].Data[-1].Angular_Velocity
        Now_Angular_Acceleration = (Now_Angular_Velocity - Before_Angular_Velocity) / Now_TimeStep
        
        globals()[f'{Name}'].Data[-1].Angular_Acceleration = Now_Angular_Acceleration

    def Change_Coordinate(self,Name,Acceleration,Angular_Velocity,Angle):
        Gravity_Accleration = np.array([0,0,9.8], dtype = np.float64)
        Acceleration = Actual_Rotation(Acceleration,Angle)*9.8 - Gravity_Accleration
        Angular_Velocity = Actual_Rotation(Angular_Velocity,Angle)

        globals()[f'{Name}'].Data[-1].Acceleration = Acceleration
        globals()[f'{Name}'].Data[-1].Angular_Velocity = Angular_Velocity
        return None

if __name__=="__main__":
    # 직접 실행시킬 때만 실행되길 원하는 코드
    File = Read()
    print(File.Device_List)
