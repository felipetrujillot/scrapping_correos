from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from seleniumwire.utils import decode
import json
import requests
from unidecode import unidecode


def seleniumStart(nombreComuna):
    """
    Inicializa el driver de selenium
    Se conecta a correos, busca una comuna e inserta una combinación aleatoria
    Envía la respuesa a la api
    :param nombreComuna
    :param combinacion
    :return: void
    """
    # Inicializa selenium
    driver = webdriver.Chrome()
    driver.get("https://appswls.entel.cl/ContratacionOnLineHogar/inicioContratacion?origen=cobertura&amp;c2=011&amp;_ga=2.153227583.663995988.1689107334-2036770318.1685128516")

    # Input para comuna
    inputComuna = driver.find_element(By.ID, 'inputSelCom')
    inputComuna.send_keys(nombreFiltrado(nombreComuna))

    time.sleep(4)

    clickComuna = driver.find_element(By.XPATH, '/html/body/ul[1]/li/div')
    clickComuna.click()

    time.sleep(3)

    for request in driver.requests:
        if (request.url.__contains__('obtenerCalles')):
            body = decode(request.response.body, request.response.headers.get(
                'Content-Encoding', 'identity'))

            res = json.loads(body.decode('utf-8', errors='ignore'))
            print(res['result'])
            postInfo(res['result'], nombreComuna)

    time.sleep(5)
    driver.close()


def postInfo(jsonListado, nombreComuna):
    """
    Envia post con el listado con la API
    :param nombreComuna
    :param combinacion
    :param jsonListado
    """
    # URL of the API endpoint
    url = 'https://sdx_laravel.test/api/direccion'
    # Request payload (data to send)
    payload = {
        'data': jsonListado,
        'comuna': nombreComuna
    }
    # Send POST request
    response = requests.post(url, json=payload)
    # Check response status code
    if response.status_code == 200:
        # Request was successful
        print('POST request successful.')
    else:
        # There was an error
        print('POST request failed.')
    # Print response content
    print(response.text)
    return


def getComunasRestantes():
    """
    Envia get a la api para obtener un array de comunas restantes
    """

    url = 'https://sdx_laravel.test/api/direcciones_restantes'

    response = requests.get(url)
    res = json.loads(response.content.decode('utf-8'))

    return res['data']


def nombreFiltrado(nombre):

    name = unidecode(nombre)
    return str.upper(name)


if __name__ == "__main__":
    """
    Inicia sistema
    """
    for com in getComunasRestantes():
        seleniumStart(com)
