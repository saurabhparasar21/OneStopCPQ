# This Method will return the driver which will be needed for every test case
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def setup():
    # options = Options()
    # options.headless=True
    # driver=webdriver.Chrome(executable_path="C:/Users/mnayak/AppData/Local/Programs/Driver/chromedriver.exe",chrome_options=options)
    #######################################################################################
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path="./utilities/drivers/chromedriver.exe") #,options=options
    return driver

def pytest_addoption(parser):     # Addoption
    parser.addoption("--browser") # This will get the value from CLI


#@pytest.fixture()
#def browser(request):
    #return request.config.getoption("--browser") # This will return the browser value to the Setup method

############## PyTest HTML Reports ########################
# It is hook for adding Environment info to HTML Report. You can add new values to it
def pytest_configure(config):
    config._metadata['Project Name'] = "CPQ"
    config._metadata['Module Name'] = "Login"
    config._metadata['Tester'] = "Manas"

# It is hook for delete/Modify Environment info into HTML report. You can remove additional values
@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME",None)
    metadata.pop("Plugins",None)