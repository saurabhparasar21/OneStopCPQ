from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pytest
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from pageObjects.loginPage import loginPage
from utilities import XLUtils
from utilities.readProperties import ReadConfig


class Test_InstallPackages:
    file = ReadConfig.getFilePath()

    def test_InstallPackages(self,setup):
        self.driver = setup
        baseUrl=XLUtils.readData(self.file, 'InstallPackagesSpring21', 1, 2)
        UserName=XLUtils.readData(self.file, 'InstallPackagesSpring21', 2, 2)
        Password=XLUtils.readData(self.file, 'InstallPackagesSpring21', 3, 2)
        Branch = XLUtils.readData(self.file, 'InstallPackagesSpring21', 4, 2)
        self.driver.get(baseUrl)
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(UserName)
        self.lgnObj.setPassword(Password)
        self.lgnObj.clickLoginButton()
        time.sleep(4)
        RwCnt=XLUtils.getRowCount(self.file,'InstallPackagesSpring21')
        print("No of Rows are: "+str(RwCnt))

        if Branch == "Spring21":
            startrow=6
            endrow=18
        elif Branch == "Winter20":
            startrow = 19
            endrow = 31
        for i in range(startrow,endrow):
            print(i)
            PackageName=XLUtils.readData(self.file, 'InstallPackagesSpring21', i, 1)
            NeedtoInstall=XLUtils.readData(self.file, 'InstallPackagesSpring21', i, 2)
            Version=XLUtils.readData(self.file, 'InstallPackagesSpring21', i, 3)
            print("Version is: "+str(Version))
            InstallationUrl=XLUtils.readData(self.file, 'InstallPackagesSpring21', i, 4)
            print("Package Name is: "+str(PackageName))
            print("Need to Install: "+str(NeedtoInstall))
            if str(NeedtoInstall) == str("Yes"):
                print(InstallationUrl)
                self.driver.execute_script('''window.open(self.InstallationUrl,"_blank");''')
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.get(InstallationUrl)

                time.sleep(6)
                path="//input[@id='username']"
                Cnt=self.driver.find_elements_by_xpath(path)
                print(len(Cnt))
                if len(Cnt) >= 1:
                    self.lgnObj.setUsername(UserName)
                    self.lgnObj.setPassword(Password)
                    self.lgnObj.clickLoginButton()
                    time.sleep(4)

                passwordPath="//input[@class='passwordBox input']"
                password=WebDriverWait(self.driver,360).until(EC.presence_of_element_located((By.XPATH, passwordPath)))
                password.send_keys("installapttus")
                ChecboxPath="//div[@class='mappingOption all']//input"
                CheckboxEle=WebDriverWait(self.driver, 180).until(EC.element_to_be_clickable((By.XPATH, ChecboxPath)))
                CheckboxEle.click()

                try:
                    UpgradeBtnPath="//span[text()='Upgrade']"
                    UpgradeBtn=WebDriverWait(self.driver,30).until(EC.element_to_be_clickable((By.XPATH, UpgradeBtnPath)))
                    UpgradeBtn.click()
                except:
                    UpgradeBtnPath="//span[text()='Install']"
                    UpgradeBtn = WebDriverWait(self.driver,30).until(EC.element_to_be_clickable((By.XPATH, UpgradeBtnPath)))
                    UpgradeBtn.click()
                time.sleep(3)
                path="//h2[text()='Approve Third-Party Access']"
                cnt=self.driver.find_elements_by_xpath(path)
                if len(cnt) >=1:
                    path1="//input[contains(@class,'uiInput uiInputCheckbox uiInput--default uiInput--checkbox')]"
                    path1Ele=WebDriverWait(self.driver, 360).until(EC.element_to_be_clickable((By.XPATH,path1)))
                    path1Ele.click()
                    path2="//span[text()='Continue']"
                    path2Ele = WebDriverWait(self.driver, 360).until(EC.element_to_be_clickable((By.XPATH, path2)))
                    path2Ele.click()

                TextPath="//span[contains(text(),'This app is taking a long time to')]"
                WebDriverWait(self.driver,360).until(EC.element_to_be_clickable((By.XPATH,TextPath)))
                DonePath="//span[text()='Done']"
                DonePathEle=WebDriverWait(self.driver, 180).until(EC.element_to_be_clickable((By.XPATH, DonePath)))
                DonePathEle.click()
                time.sleep(8)
                #InstallPckPagePath="//h1[text()='Installed Packages']"
                #WebDriverWait(self.driver,180).until(EC.presence_of_element_located((By.XPATH,InstallPckPagePath)))

                for j in range(1000):
                    elePath = "//div//tr//td[text()='"+Version+"']"
                    print("Inside For")
                    time.sleep(20)
                    MatchingCnt=self.driver.find_elements_by_xpath(elePath)
                    print("Matching version: "+str(len(MatchingCnt)))
                    if len(MatchingCnt) >= 1:
                        print("Package "+str(PackageName)+" "+str(Version)+" is installed successfully")
                        XLUtils.writeData(self.file,'InstallPackagesSpring21',i,2,'No')
                        break
                    self.driver.refresh()

        self.driver.close()