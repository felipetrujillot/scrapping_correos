from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from seleniumwire.utils import decode
import json
import requests


def seleniumStart(nombreComuna, combinacion):
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
    driver.get("https://www.correos.cl")

    # Pestaña de código postal
    elem = driver.find_element(By.CLASS_NAME, "codigopost_tab_cont")
    elem.click()

    # Input para comuna
    inputComuna = driver.find_element(By.ID, 'comuna_domicilio')
    inputComuna.send_keys(nombreComuna)

    # La búsqueda es asíncrona, por lo que no siempre encuentra el primer resultado a tiempo
    time.sleep(1)
    # Validamos que el primer resultado de búsqueda sea el correcto
    # Caso contrario busca los otros hasta encontrar coincidencia
    comunaSeleccionada = driver.find_element(
        By.ID, 'search-comuna-domicilio-0')
    if (comunaSeleccionada.text != nombreComuna):
        comunaSeleccionada = driver.find_element(
            By.ID, 'search-comuna-domicilio-1')
        if (comunaSeleccionada.text != nombreComuna):
            comunaSeleccionada = driver.find_element(
                By.ID, 'search-comuna-domicilio-2')
            if (comunaSeleccionada.text != nombreComuna):
                comunaSeleccionada = driver.find_element(
                    By.ID, 'search-comuna-domicilio-3')
    comunaSeleccionada.click()

    # La búsqueda comienza en los tres carácteres, por lo que el mismo problema que las comunas no ocurre
    inputCalle = driver.find_element(By.ID, 'calle_domicilio')
    inputCalle.send_keys(combinacion)
    time.sleep(1)

    # Buscamos los resultados de la request y buscamos la request de dirección
    for request in driver.requests:
        if (request.url.__contains__('obtenerDirecciones')):
            body = decode(request.response.body, request.response.headers.get(
                'Content-Encoding', 'identity'))
            res = json.loads(body.decode('utf-8'))
            postInfo(nombreComuna, combinacion, res)
            print(res['listado'])
            # for nombre in res['listado']:
            #    print(nombre['nombre'])
    driver.close()


def postInfo(nombreComuna, combinacion, jsonListado):
    """
    Envia post con el listado con la API
    :param nombreComuna
    :param combinacion
    :param jsonListado
    """
    # URL of the API endpoint
    url = 'https://sdx_laravel.test/api/linkcloud/direccion'
    # Request payload (data to send)
    payload = {
        'key1': 'value1',
        'key2': 'value2'
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


def generar_combinaciones():
    """
    Genera todas las combinaciones aleatorias de hasta tres dígitos
    :return: array
    """
    combinaciones = []
    # Recorre todos los números de 0 a 999
    for numero in 'ÁABCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZ0123456789 ':
        # Genera todas las combinaciones de letras y números
        for letra1 in 'ÁABCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZ0123456789 ':
            for letra2 in 'ÁABCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZ0123456789 ':
                combinacion = letra1 + letra2 + numero
                combinaciones.append(combinacion)

    return combinaciones


if __name__ == "__main__":
    """
    Inicia sistema
    """
    res = generar_combinaciones()
    for combinacion in res:
        seleniumStart('PUENTE ALTO', combinacion)
