from selenium.webdriver import ActionChains

from utilities import XLUtils
from utilities.readProperties import ReadConfig
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Test_GetPullRequestsInfo:
    file = ReadConfig.getFilePath()

    def GetPullRequestsInfo(self,setup):
        print("Inside method")
        self.driver=setup
        self.driver.get("https://github.com/")
        self.driver.maximize_window()
        time.sleep(2)
        ele="/html/body/div[1]/header/div/div[2]/div[2]/a[1]"
        self.driver.find_element_by_xpath(ele).click()
        time.sleep(3)
        unm="//input[@name='login']"
        self.driver.find_element_by_xpath(unm).click()
        self.driver.find_element_by_xpath(unm).send_keys("mnayak@conga.com")
        pwd="//input[@name='password']"
        self.driver.find_element_by_xpath(pwd).send_keys("Onetime123$")
        lgnbtn="//input[@name='commit']"
        self.driver.find_element_by_xpath(lgnbtn).click()
        time.sleep(5)
        totPullReqs=XLUtils.getRowCount(self.file,'PullReqs')
        print("Total Pull Requsts: "+str(totPullReqs))

        for i in range(2,totPullReqs+1):
            PullReq=XLUtils.readData(self.file,'PullReqs',i,1)
            print(PullReq)
            #ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
            self.driver.get(PullReq)
            if i==2:
                CntBtnPath="//button[@type='submit']"
                CntBtn=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, CntBtnPath)))
                CntBtn.click()
                UserNamePath="//input[@name='username']"
                UserName=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, UserNamePath)))
                UserName.send_keys('mnayak@conga.com')
                NxtBtnPath="//*[@id='usernameForm']/div[4]/button"
                NextBtn=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, NxtBtnPath)))
                NextBtn.click()
                time.sleep(5)
                passwordpath="//*[@id='passwordAndMechanismForm']/div[3]/div/input[1]"
                passwordbox=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, passwordpath)))
                passwordbox.send_keys('Omshai123$')
                AuthPath="//*[@id='passwordAndMechanismForm']/div[3]/div/div[1]/input[1]"
                self.driver.find_element_by_xpath(AuthPath).click()
                time.sleep(4)
                OptionPath="//*[@id='passwordAndMechanismForm']/div[4]/span[2]"
                self.driver.find_element_by_xpath(OptionPath).click()
                NextBtn="//*[@id='passwordAndMechanismForm']/div[5]/button"
                self.driver.find_element_by_xpath(NextBtn).click()
                time.sleep(30)
            PullReqSmryPath="//span[@class='js-issue-title']"
            Summary=self.driver.find_element_by_xpath(PullReqSmryPath).text
            print(Summary)
            ColCnt=XLUtils.getColumnCount(self.file,'PullReqs')
            print(ColCnt)
            XLUtils.writeData(self.file,'PullReqs',i,2,Summary)
            #XLUtils.writeData(self.file,'PullReqs',i,2,self.Summary)
        self.driver.close()




