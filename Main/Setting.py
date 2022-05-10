import numpy as np
import File
import Joint

class Setting :
    ## 여기 안에 있는 것들은, Setting 파일을 import할 시 자동으로 실행
    #File_Data = File.Read()
    #Device_List = File_Data.Device_List
    #Joint.Set_Joint(Device_List)

    def __init__(self):
        self.File_Data = File.Read()
        self.Device_List = self.File_Data.Device_List
        Joint.Set_Joint(self.Device_List)
        return None
