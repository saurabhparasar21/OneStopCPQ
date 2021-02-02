from utilities import XLUtils
from utilities.readProperties import ReadConfig

class GetPullRequestsInfo:


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
