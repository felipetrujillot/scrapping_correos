from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from seleniumwire.utils import decode
import json


driver = webdriver.Chrome()
driver.get("https://www.correos.cl")
elem = driver.find_element(By.CLASS_NAME, "codigopost_tab_cont")
elem.click()


inputComuna = driver.find_element(By.ID, 'comuna_domicilio')
inputComuna.send_keys('Puente Alto')
time.sleep(1)
comunaSeleccionada = driver.find_element(By.ID, 'search-comuna-domicilio-0')
comunaSeleccionada.click()


inputCalle = driver.find_element(By.ID, 'calle_domicilio')
inputCalle.send_keys('las')
time.sleep(1)

# Access requests via the `requests` attribute

for request in driver.requests:

    if (request.url.__contains__('obtenerDirecciones')):
        body = decode(request.response.body, request.response.headers.get(
            'Content-Encoding', 'identity'))

        res = json.loads(body.decode('utf-8'))

        for nombre in res['listado']:
            print(nombre['nombre'])
            print('\n')
        # print(res['listado'][0])

time.sleep(10)


driver.close()
