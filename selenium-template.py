from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
from datetime import datetime
import os
import unicodedata
import pandas as pd
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    #"--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    #"--no-sandbox",
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options = chrome_options)
driver.get('https://associado.appai.org.br/')
#time.sleep(70)

print("Iniciando login...")
wait = WebDriverWait(driver, 70)  
username_field = wait.until(EC.visibility_of_element_located(( By.ID, 'UserName')))
username_field.send_keys(os.environ['LOGIN_SECRET'])  # Replace with your actual username
password_field = wait.until(EC.visibility_of_element_located(( By.ID, 'password-field')))  
password_field.send_keys(os.environ['PASSWORD_SECRET'])
login_button = wait.until(EC.visibility_of_element_located((By.ID, 'btnLogin')))  # Replace with the actual element ID or other selector
login_button.click()

time.sleep(5)
print("Login realizado.")

while driver.current_url != "https://associado.appai.org.br/":
    pass

print("Carregando página de eventos...")
driver.get("https://associado.appai.org.br/bom-espetaculo")
