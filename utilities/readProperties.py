# To read common data from config.ini file, use config parser
import configparser
config=configparser.RawConfigParser() # To access methods of RawConfigParser class, create a method
config.read(".//configurations//config.ini")

# Create a Class and to read Keyword-value create individual method
# Make this method static

class ReadConfig:

    @staticmethod
    def getbaseURL():
        url=config.get('Common Info','baseURL')
        return url

    @staticmethod
    def getuserName():
        usrnm = config.get('Common Info','userName')
        return usrnm

    @staticmethod
    def getpassword():
        pwd = config.get('Common Info','password')
        return pwd
    @staticmethod
    def getFilePath():
        path=config.get('Common Info','testDataPath')
        return path
