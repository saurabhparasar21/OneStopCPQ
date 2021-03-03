# This is a Page Object Class for Home page. Define all Locators here
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    Icon_SearchApps_Xpath="//div[@class='slds-icon-waffle']"
    Txt_SearchApps_xpath="//input[@placeholder='Search apps and items...']"
    link_SwtchToLightning="//a[@class='switch-to-lightning']"

    # Constructor
    def __init__(self,driver):
        self.driver=driver

    def switchToLightning(self):
        print("---------- Method: HomePage>switchToLightning")
        title=self.driver.title
        print("Title is: "+str(title))
        if str("Salesforce") in str(title):
            linkSwitchToLight=WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,self.link_SwtchToLightning)))
            linkSwitchToLight.click()
    # Click on Search Apps Icon present at the left top corner of the page

    def ClickSearchAppsIcon(self):
        time.sleep(4)
        print("---------- Method: HomePage>ClickSearchAppsIcon")
        path="//div[@class='slds-icon-waffle']"
        IconSearchApp=WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH,path)))
        IconSearchApp.click()
    # Search and click the desired App
    def SearchAndClickApp(self,AppName):
        print("---------- Method: HomePage>SearchAndClickApp")
        TextAppToSearch=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, self.Txt_SearchApps_xpath)))
        TextAppToSearch.send_keys(AppName)
        AppToSelectFromSearchReslts="//b[text()='" + AppName + "']"
        eleAppToSelectFromSearchReslts=WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,AppToSelectFromSearchReslts)))
        eleAppToSelectFromSearchReslts.click()

    def SearchRecord(self,AppName,RecordName):
        print("---------- Method: HomePage>SearchRecord")
        eleAppName="//input[@title='Search "+AppName+" and more']"
        eleRecordToSearch=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, eleAppName)))
        eleRecordToSearch.send_keys(RecordName)
        eleRecordName = "//span[@title='"+RecordName+"']"
        try:
            Record=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, eleRecordName)))
            Record.click()
        except:
            Record=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, eleRecordName)))
            Record.click()

    def SwitchToFrame(self):
        print("---------- Method: SwitchToFrame")
        framePath="//iFrame[contains(@title,'MN')]"
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,framePath)))

    def SwitchToDefault(self):
        print("---------- Method: SwitchToDefault")
        self.driver.switch_to.default_content()