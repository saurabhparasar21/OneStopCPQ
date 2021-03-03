import string
from utilities import XLUtils
from utilities.readProperties import ReadConfig

class Test_WorkingFile:


    def test_FileWrite(self,setup):
        self.driver=setup
        file = ReadConfig.getFilePath()
        print("File path is: "+str(file))
        Summary="Manas"
        i=2
        XLUtils.writeData(file,'PullReqs',i,4,Summary)
        self.driver.close()

    def test_TextCompare(self):
        Dvalue= "['Value2', 'Value3']"
        Value="['Value2', 'Value3']"

        if str(Value) in str(Dvalue):
            print("passed")
        else:
            print("Failed")

    def test_ConvertString1to2(self):
        OldString="1613377508168-uiGrid-000M-header-text"
        NewString1= str.replace(OldString,'-uiGrid','-0-uiGrid')
        print("New String 1 is: ")
        print(NewString1)
        NewString2 = str.replace(NewString1, '-header-text', '-cell')
        print("New String 1 is: ")
        print(NewString2)


