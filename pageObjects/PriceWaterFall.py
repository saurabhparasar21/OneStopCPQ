# Price Waterfall Page Object Class
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
from utilities.Logger import Logger
import time

class PriceWaterfallPage:

    # Constructor
    def __init__(self, driver):
        self.driver = driver

    # Verify the Price of a given Price Point
    def VerifyPricePointValueColor(self,PricePoint,ExpectedColor,ExpectedPrice):
        time.sleep(1)
        path="//header[text()='Line Items']"
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH,path)))
        FindPPSeq="//*[name()='g' and @class='highcharts-axis-labels highcharts-xaxis-labels']//*[contains(@transform,'translate(0,0)')]"
        PricePointCnt=self.driver.find_elements_by_xpath(FindPPSeq)
        #print("Total No. of Price Points are: "+str(len(PricePointCnt)))
        for i in range(len(PricePointCnt)):
            #print(PricePointCnt[i].text)
            if PricePointCnt[i].text == str(PricePoint):
                #print("Inside If & matched i is: "+str(i))
                path1 = "//*[@stroke='#333333']"
                ToolTip = self.driver.find_elements_by_xpath(path1)

                for j in range(len(ToolTip)):
                    if j == i:
                        #print("Inside For i is: "+str(i))
                        actions = ActionChains(self.driver)
                        actions.move_to_element(ToolTip[j]).perform()
                        time.sleep(2)
                        PPColor = ToolTip[j].get_attribute("fill")
                        print("Price Point Color is: " + str(PPColor))
                        print("Expected Color is: " + str(ExpectedColor))
                        #print("After move to tool tip, J is: " + str(j))
                        path = "//*[@class='highcharts-label highcharts-tooltip highcharts-color-undefined']/*[5]/*[2]"
                        pathEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
                        print("Price Point Value is: "+(pathEle.text))
                        if ExpectedPrice in pathEle.text:
                            if str(ExpectedColor) in str(PPColor):
                                return True
                            else:
                                return False






