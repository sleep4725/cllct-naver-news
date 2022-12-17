from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from webdriver_manager.chrome import ChromeDriverManager

import chromedriver_autoinstaller
import os 
PROJ_ROOT_DIR :str= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

'''
@author JunHyeon.Kim
@date 20221216금
'''
class ChromeDriver:
    
    def __init__(self) -> None:
        global PROJ_ROOT_DIR
        self._chrome_ver :str= chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        self._driver_path :str= f"{self._chrome_ver}/chromedriver.exe"
        self._chrome_engine_dir :str= os.path.join(PROJ_ROOT_DIR, "selenium_engine")
        self._chrome_driver_file_path :str= self._chrome_engine_dir + "/" + self._driver_path
    
    def get_chrome_driver(self)\
            -> WebDriver:
        '''
        :param:
        :return:
        '''
        chrome_options :Options= webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("disable-gpu")
         
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            )
            , options=chrome_options
        )
        
    """  Function old-version  
    def get_chrome_client(self)\
            -> selenium_webdriver.WebDriver:
        '''
        :param:
        :return:
        '''
        is_file_exists :bool= os.path.exists(self._chrome_driver_file_path)
        
        if is_file_exists: return webdriver.Chrome(self._chrome_driver_file_path) 
        else:
            os.chdir(self._chrome_engine_dir)
            path :str= chromedriver_autoinstaller.install(True)
            return webdriver.Chrome(path)
    """