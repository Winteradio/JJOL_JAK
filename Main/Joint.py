import numpy as np
import File

class Part_Of_Joint :
    # Part of Joint : Right or Left Part
    # WD : World Coordinate System's Dimensions
    WD = 3

    def __init__(self,Device_Name=None,Device_Data=None,mass = 0, moment_of_inertia=np.zeros(WD),
            COP=np.zeros(WD), COG=np.zeros(WD), Length=np.zeros(WD),
            ground_force=np.zeros(WD), ground_moment=np.zeros(WD),
            joint_force=np.zeros(WD),joint_moment=np.zeros(WD)):

        self.Device_Name = Device_Name
        self.Device_Data = Device_Data

        self.mass = mass
        self.moment_of_inertia = moment_of_inertia
        
        self.COP = COP
        self.COG = COG
        self.Length = Length

        self.ground_force = ground_force
        self.ground_moment = ground_moment

        self.joint_force = joint_force
        self.joint_moment = joint_moment

class Joint_Data:
    # Joint Main Data
    def __init__(self, Name = None, 
            Right_Part = None, Left_Part = None,
            next = None):
        self.Name = Name
        self.Right_Part = Right_Part
        self.Left_Part = Left_Part
        
        self.next = next

def Set_Joint(Device_List):
    ## 전체 데이터 구조를 알 수 있는 Tree를 그린다.
    Make_Total_Data_Tree()

    ## Joint Setting 시작~~
    print("----- Joint Setting Start -----")
    print("Joint의 이름들을 입력하시오")
    Joint_Name = list(input(">>> ").split())
    print("")
    
    ## Joint와 Joint Part를 만들고 연결시켜준다.
    for i in range(len(Joint_Name)):
        Make_Joint(Joint_Name[i])
        Make_Part_Of_Joint_And_Connect_to_Joint(Joint_Name[i])
    
    ## 상위 Joint와 하위 Joint를 연결시켜준다.
    for i in range(len(Joint_Name)-1):
        Connect_Joint_to_Joint(Joint_Name[i],Joint_Name[i+1])
    print("----- Joint Setting End -----","","",sep="\n")

    ## Joint와 Device를 연결시켜준다.
    print("----- Check Connection Device to Joint Part -----")
    Print_Device(Device_List) ## Device List 확인
    Check_Connection_Device_with_Joint_Part(Device_List,Joint_Name) ## 연결 Device 설정
    print("----- End Checking Connection -----","","",sep="\n")

    ## Joint 연결부를 확인할 수 있는 Tree를 그린다.
    print("----- Make Joint Tree -----")
    Make_Joint_Tree(Joint_Name)
    print("----- End Joint Tree -----","","",sep="\n")
    return 0

def Make_Joint(Joint_Name):
    globals()[f'{Joint_Name}'] = Joint_Data(Joint_Name)
    print("Joint Name :",Joint_Name)

def Make_Part_Of_Joint_And_Connect_to_Joint(Joint_Name):
    Vec = ["R","L"]
    for i in Vec :
        globals()[f'{i}_{Joint_Name}'] = Part_Of_Joint()
    globals()[f'{Joint_Name}'].Right_Part = globals()[f'R_{Joint_Name}']
    globals()[f'{Joint_Name}'].Left_Part = globals()[f'L_{Joint_Name}']
    for i in Vec:
        print(">>> Name of {0}'s Part : {1}_{2}".format(Joint_Name,i,Joint_Name))

def Make_Joint_Tree(Joint_Name):
    for i in Joint_Name:
        Joint = globals()[f'{i}']
        print("Joint : {0}".format(Joint.Name))
        print("      ↳ Right Part of Joint : R_{0}".format(Joint.Name))
        print("             ↳ Device : {0}".format(Joint.Right_Part.Device_Data.Name))
        print("")
        print("      ↳ Left Part of Joint : L_{0}".format(Joint.Name))
        print("             ↳ Device : {0}".format(Joint.Left_Part.Device_Data.Name))

def Make_Total_Data_Tree():
    print("----- Total Data Structure -----")
    print("Joint_Data")
    print("     ↳ Name")
    print("     ↳ Joint's Part")
    print("            ↳ Device's Name")
    print("            ↳ Device's Data (Main Data - Frame Data)")
    print("                     ↳ (Main Data) Name")
    print("                     ↳ (Main Data) Data")
    print("                            ↳ (Frame Data) Time")
    print("                            ↳ (Frame Data) TimeStep")
    print("                            ↳ (Frame Data) Acceleration")
    print("                            ↳ (Frame Data) Angular Acceleration")
    print("                            ↳ (Frame Data) Velocity")
    print("                            ↳ (Frame Data) Angular Velocity")
    print("                            ↳ (Frame Data) Angle")
    print("            ↳ Mass")
    print("            ↳ Moment of Inertia")
    print("            ↳ Center of Pressure")
    print("            ↳ Center of Gravity")
    print("            ↳ Length")
    print("            ↳ Ground Force")
    print("            ↳ Ground Moment")
    print("            ↳ Joint Force")
    print("            ↳ Joint Moment")
    print("----- End Data Structure -----","","",sep="\n")

def Connect_Joint_to_Joint(Before_Joint,Next_Joint):
    globals()[f'{Before_Joint}'].next = globals()[f'{Next_Joint}']

def Connect_Device_to_Joint_Part(Device,Joint_Part):
    Joint_Part.Device_Name = Device.Name
    Joint_Part.Device_Data = Device

def Check_Connection_Device_with_Joint_Part(Device_List,Joint_Name):
    Vec = ["R","L"]
    for i in range(len(Joint_Name)):
        for j in Vec:
            print("{0}의 {1} 파트와 연결할 장치의 순번을 고르시오. ".format(Joint_Name[i],j))
            Answer = int(input(">>> "))
            Device = getattr(File,Device_List[Answer])
            Joint_Part = globals()[f'{j}_{Joint_Name[i]}']
            Connect_Device_to_Joint_Part(Device,Joint_Part)

def Print_Device(Device_List):
    print("다음 목록에서 연결한 장치를 고르시오.")
    for index, value in enumerate(Device_List):
        print(index,"번째 장치",value)
    print("")

if __name__=="__main__":
    Set_Joint()
