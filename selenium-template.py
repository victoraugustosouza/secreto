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


def remove_accents(input_str):
    # Normalize the string to NFD (Normalization Form Decomposed)
    nfkd_form = unicodedata.normalize('NFD', input_str)
    
    # Filter out combining characters
    only_ascii = ''.join([char for char in nfkd_form if not unicodedata.combining(char)])
    
    return only_ascii


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
    "--ignore-certificate-errors",
    "--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    "--no-sandbox"
    #"--disable-dev-shm-usage",
    #'--remote-debugging-port=9222'
]
#test
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

time.sleep(15)
print("Login realizado.")

while driver.current_url != "https://associado.appai.org.br/":
    pass

print("Carregando página de eventos...")
driver.get("https://associado.appai.org.br/bom-espetaculo")


# In[228]:


while driver.current_url != "https://associado.appai.org.br/bom-espetaculo":
    pass

print("Páginca carregada...")
dropdown_element =  wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'selectLarge.dropdown-toggle.dropdown-toggle-split')))
dropdown = Select(dropdown_element)
dropdown.select_by_visible_text('Rio de Janeiro')  # Replace with the actual visible text of the option


# In[230]:

print("Clicando em Carregar Mais")
counter = 5
while counter > 0 :
    button_text = 'Carregar Mais'  # Replace with the actual text of the button
    #print(counter)
# Retrieve all buttons containing the specified text
    try:
        buttom = driver.find_element(By.XPATH, f"//button[contains(text(), '{button_text}')]")
        buttom.click()
        time.sleep(5)
        counter = counter -1
        print(counter)
    except:
        counter = counter -1
        print(counter)
        continue

print("Expandindo eventos e capturando agendas...")
time.sleep(5)
eventos = []
box_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.box')))
cards = box_container.find_elements(By.CSS_SELECTOR, ".card")

for i in range(len(cards)):
    element = cards[i].find_elements(By.TAG_NAME, "a")[0]
    driver.execute_script("arguments[0].click();", element)
    title = cards[i].find_elements(By.TAG_NAME, "h6")[0].text
    categoria = cards[i].find_elements(By.TAG_NAME, "h6")[1].text
    print(title+" "+categoria)
    table = cards[i].find_elements(By.CLASS_NAME, "appai-table")[0]
    rows = table.find_elements(By.TAG_NAME, "tr")

    for r in rows:
        local_recorder = [remove_accents(title)]
        values = r.find_elements(By.TAG_NAME, "td")
        for i in range(len(values)-2):
            print(values[i].text)
            local_recorder.append(remove_accents(values[i].text))
        if len(local_recorder) > 1:
            eventos.append(tuple(local_recorder))
        
body_text = driver.find_element(By.TAG_NAME, "body").text

now = datetime.now()
timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")+body_text

print("Salvando em dataframe...")
df = pd.DataFrame(eventos, columns=['nm_evento', 'tipo_km','data', 'horario_evento','nm_local','ds_situacao'])
df = df.loc[df['nm_evento'] == "Circuito Rio Antigo 2024 - Etapa Cinelandia"]
df = df.loc[df['tipo_km'] == "Caminhada - 4,0 KM"]

print(df)

with open('./GitHub_Action_Results.txt', 'w') as f:
    f.write(f"This was written with a GitHub action {timestamp_str}")
