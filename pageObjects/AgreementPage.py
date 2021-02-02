import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class AgreementPage:

    def __init__(self,driver):
        self.driver=driver

    def AgrmntRecTypPageButton(self,Button):
        print("---------- Method: AgrmntRecTypPageButton")
        time.sleep(3)
        framePath = "//div[@class='iframe-parent slds-template_iframe slds-card']//iFrame[contains(@title,'title')]"
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, framePath)))
        #print("Inside Agreement")
        path="//input[@value='"+Button+"']"
        eleY = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        eleY.click()

    def getFieldValue(self,FieldType,FieldLabel):
        print("---------- Method: getFieldValue")
        if FieldType == "Text":
            element="//span[@class='test-id__field-label' and text()='"+FieldLabel+"']/ancestor::div[2]//div[2]//slot//slot//lightning-formatted-text"
            eleY=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH,element)))
            eleLabel=eleY.get_attribute("value")

        return eleLabel

    def ClickOnDetailPageTab(self,TabName):
        print("---------- Method: ClickOnDetailPageTab")
        if TabName == "Related":
            path = "//a[text()='"+TabName+"']"
            ele=self.driver.find_elements_by_xpath(path)
            for i in range(len(ele)):
                if i == 1:
                    ele[i].click()
                    break

    def CheckConfigurationStatus(self,ExpectedStatus):
        print("---------- Method: CheckConfigurationStatus")
        for i in range(100):
            Path = "//span[@title='Configurations']/ancestor::lst-common-list//div[@class='slds-scrollable_y']//td[@data-label='Status']//lightning-formatted-text"
            Ele = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Path)))
            #print(Ele.text)
            if Ele.text != ExpectedStatus:
                print("Inside If")
                self.driver.find_element_by_xpath(Path).send_keys(Keys.F5)
                print("Page refreshed")
                time.sleep(4)
        return Ele.text

    def CountNoOfAgrmntLines(self):
        print("---------- Method: CountNoOfAgrmntLines")
        time.sleep(3)
        path="//span[text()='Agreement Line Items']/following-sibling::span"
        Ele = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH,path)))
        #print(Ele.text)
        return Ele.text

    def ClickAgreementPageButton(self,Button):
        time.sleep(4)
        print("---------- Method: ClickAgreementPageButton")
        if Button == "Delete":
            path = "//button[text()='"+Button+"']"
            ele=self.driver.find_elements_by_xpath(path)
            for i in range(len(ele)):
                if i == 1:
                    ele[i].click()
                    break

    def DialogAcceptOrCancel(self,Button):
        time.sleep(4)
        print("---------- Method: DialogClickNextOrCancel")
        if Button == 'Next' or Button == 'Delete':
            btn = "//span[text()='"+Button+"']"
            PopUpBtn = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, btn)))
            PopUpBtn.click()
            #print("Agr dialong clicked")
        time.sleep(10)
        path = "//button[@name='Delete']"
        ele = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        ele.click()
        time.sleep(3)