from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class AttributePage:

    def __init__(self,driver):
        self.driver=driver

    def CheckIfAttrIsHidden(self,Attr):
        print("---------- Method: CheckIfAttrIsHidden")
        AttrPath="//label[@class='product-attribute__name']"
        Cnt=self.driver.find_elements_by_xpath(AttrPath)

        if len(Cnt) == 0:
            return True
        else:
            for r in range(len(Cnt)):
                AttrLabel = Cnt[r].text
                if AttrLabel == Attr:
                    print("Attribute " + Attr + " is NOT hidden")
                    return False
                    self.driver.close()
                else:
                    return True
                    print("Attribute " + Attr + " is hidden")

    def AttrPageWaitForPricingToComplete(self):
        print("---------- Method: AttrPageWaitForPricingToComplete")
        time.sleep(4)
        for r in range(300):
            path="//button[contains(@class,'GoToPricing')]"
            pathele=self.driver.find_element_by_xpath(path)
            #print(pathele.is_enabled())
            if pathele.is_enabled() == True:
                break

    def SetQuantity(self,Qty):
        print("---------- Method: SetQuantity")
        path="//label[contains(text(),'Qty')]/..//div//input"
        pathEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,path)))
        pathEle.clear()
        pathEle.send_keys(Qty)
        pathEle.send_keys(Keys.TAB)
        time.sleep(7)

    def IsAttrDisabled(self,AttrType,Attr):
        print("---------- Method: IsAttrDisabled")
        if AttrType == "Text":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//*[@type='text']"
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            if PathEle.get_attribute('disabled') == str("true"):
                return True
            else:
                return False

        if AttrType == "Picklist" or AttrType == "Lookup":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//a/.."
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            if PathEle.get_attribute('disabled') == str("true"):
                return True
            else:
                return False

        if AttrType == "Checkbox":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//*[@type='checkbox']"
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))

            if PathEle.get_attribute('disabled') == str("true"):
                return True
            else:
                return False

        if AttrType == "MultiPickList":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//input"
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            if PathEle.get_attribute('disabled') == str("true"):
                return True
            else:
                return False

    def IsAttrRequired(self,AttrType,Attr):
        print("---------- Method: IsAttrRequired")
        if AttrType == "Text":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//*[@type='text']"
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            print("Req attr is")
            print(PathEle.get_attribute('required'))
            if PathEle.get_attribute('required') == str("true"):
                return True
            else:
                return False

        if AttrType == "Picklist" or AttrType == "Lookup":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//a/.."
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            if PathEle.get_attribute('required') == str("true"):
                return True
            else:
                return False

        if AttrType == "Checkbox":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//*[@type='checkbox']"
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))

            if str("required") in PathEle.get_attribute('class'):
                return True
            else:
                return False

        if AttrType == "MultiPickList":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//input/../../.."
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            if PathEle.get_attribute('required') == str("true"):
                return True
            else:
                return False

    def IsAttrReset(self,AttrType,Attr,Value):
        print("---------- Method: IsAttrReset")
        if AttrType == "Text":
            print("Scroll little more before")
            self.driver.execute_script("window.scrollBy(0, 75);")
            DValue=self.ReadAttr(AttrType,Attr)
            print("Default value for Reset PAR is: "+str(DValue))
            if str(Value) in DValue:
                print("Correct value defaulted for: "+str(Attr))
                Path = "//*[contains(*,'" + Attr + "') and contains(@ng-class,'two')]//*[@type='text']"
                PathEle = WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, Path)))
                # Clear the Attribute and set a new Value
                PathEle.click()
                PathEle.send_keys(Keys.CONTROL+'a')
                PathEle.send_keys(Keys.DELETE)
                time.sleep(3)
                PathEle.send_keys('30')
                PathEle.send_keys(Keys.TAB)
                time.sleep(4)
                # Clear the textbox and see if the correct value is reset
                PathEle.clear()
                DValue = self.ReadAttr(AttrType, Attr)
                if str(Value) in DValue:
                    return True
                else:
                    return False
            else:
                return False

        if AttrType == "MultiPickList":
            DValue = self.ReadAttr(AttrType, Attr)
            print("Dvalue is: " + str(DValue))
            print("Value is: " + str(Value))

            if str(Value) in str(DValue):
                print("Set a new attribute")
                print("Correct value defaulted for: " + str(Attr))
                print("Clear attributes")
                Path = "//a[@class='ui-select-match-close select2-search-choice-close']"
                PathEle = self.driver.find_elements_by_xpath(Path)
                for i in range(len(PathEle)):
                    print("i is : "+str(i))
                    if i == 0:
                        print("Inside if")
                        PathEle[i].click()
                        time.sleep(1)
                    else:
                        print("Inside else")
                        PathEle[i-1].click()
                        time.sleep(1)

                print("Check if the attribute is reset properly")
                DValue = self.ReadAttr(AttrType, Attr)
                if str(Value) in str(DValue):
                    print("Inside True")
                    return True
                else:
                    print("Inside False")
                    return False

        if AttrType == "Picklist":
            print("Inside Picklist")
            DValue = self.ReadAttr(AttrType, Attr)
            print("Dvalue is: " + str(DValue))
            print("Value is: " + str(Value))

            if str(Value) in str(DValue):
                print("Correct value defaulted for: " + str(Attr))
                print("Set a new Attribute")
                path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//a"
                print("Path is : "+str(path))
                PathEle = self.driver.find_element_by_xpath(path)
                PathEle.click()
                path="//div[text()='2025']"
                PathEle = self.driver.find_element_by_xpath(path)
                PathEle.click()
                print("Clear attributes")
                Path = "//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//abbr"
                PathEle = self.driver.find_element_by_xpath(Path)
                PathEle.click()

                print("Check if Picklist attr is reset")
                DValue = self.ReadAttr(AttrType, Attr)
                if str(Value) in str(DValue):
                    return True
                else:
                    return False

    def ClickButton(self,Button):
        print("---------- Method: ClickButton")
        # All Buttons on Attr page works with this path
        if Button=="Remove Item":
            Button=="Remove"
        BtnPath="//button[contains(@class,'"+Button+"')]"
        BtnEle=WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH,BtnPath)))
        BtnEle.click()

    def ReadAttr(self,AttrType,Attr):
        print("---------- Method: ReadAttr")
        if AttrType == "Text":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//*[@type='text']"
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            #PathEle.click()
            Value=PathEle.get_attribute('value')
            print("Value of Attr is: "+str(Value))
            return Value

        if AttrType == "Picklist" or AttrType == "Lookup":
            print("Inside read attr Picklist")
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//a/../a"
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            Value = PathEle.get_attribute('title')
            print("Value of Attr is: " + str(Value))
            return Value

        if AttrType == "MultiPickList":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//li//span"
            PathEles=self.driver.find_elements_by_xpath(Path)
            my_list=[]
            for i in range(len(PathEles)):
                print(PathEles[i].text)
                my_list.append(PathEles[i].text)
                print(my_list)

            return my_list

    def CheckIfCorrectAttrAllowed(self,AttrType,Attr, Expected):
        print("---------- Method: CheckIfCorrectAttrAllowed")
        if AttrType == "Picklist":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]"
            PathEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,Path)))
            actions = ActionChains(self.driver)
            actions.move_to_element(PathEle).perform()
            self.driver.execute_script("window.scrollBy(0, 75);")
            PathEle.click()
            Path="//li[@role='option']//div[@class='select2-result-label ui-select-choices-row-inner']//div"
            Cnt=self.driver.find_elements_by_xpath(Path)
            my_list=[]
            for i in range(len(Cnt)):
                my_list.append(Cnt[i].text)

            print(my_list)
            print(Expected)
            if str(my_list) in str(Expected):
                return True
            else:
                return False

        if AttrType == "MultiPickList":
            Path="//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]//li"
            PathEle=self.driver.find_element_by_xpath(Path)
            actions = ActionChains(self.driver)
            actions.move_to_element(PathEle).perform()
            self.driver.execute_script("window.scrollBy(0, 75);")
            PathEle.click()
            path="//div[contains(@class,'multi')]//ul[@class='select2-result-single']/li[@class='ui-select-choices-row']/div/div"
            PathEle = self.driver.find_elements_by_xpath(path)
            print(len(PathEle))
            my_list = []
            for i in range(len(PathEle)):
                PathEle[i].text
                my_list.append(PathEle[i].text)

            if str(my_list) in str(Expected):
                return True
            else:
                return False

    def AttrPageAbandonCartIcon(self):
        print("---------- Method: AttrPageAbandonCartIcon")
        AbnIconPath = "//*[contains(@ng-class,'Abandon')]"
        AbnIconEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, AbnIconPath)))
        AbnIconEle.click()
        path = "//md-dialog[contains(@aria-label,'Small')]//button[contains(text(),'OK')]"
        print("Path is: " + path)
        ele = self.driver.find_element_by_xpath(path)
        ele.click()

    def SetAttribute(self,AttrType,Attr,Value):
        print("---------- Method: SetAttribute")
        if AttrType == "Picklist":
            Path = "//*[contains(*,'"+Attr+"') and contains(@ng-class,'two')]"
            PathEle = WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, Path)))
            actions = ActionChains(self.driver)
            actions.move_to_element(PathEle).perform()
            self.driver.execute_script("window.scrollBy(0, 75);")
            PathEle.click()
            path1="//li[@role='option']//div[text()='"+Value+"']"
            PathEle1 = WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, path1)))
            PathEle1.click()

