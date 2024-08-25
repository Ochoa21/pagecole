import requests
from bs4 import BeautifulSoup
import time
import hashlib
import logging
from pushbullet import Pushbullet

# Configuración del logging
logging.basicConfig(filename='monitor.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# URL de la página a monitorear
url = "https://coordinaciongeneral.jimdofree.com/"

# Tu API Key de Pushbullet
api_key = "o.dXNNCtYBgWwkhfjsgf5gUdexR0OtoeXp"
pb = Pushbullet(api_key)

# Función para obtener el hash del contenido de la página
def get_page_hash(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verificar que la solicitud fue exitosa
        soup = BeautifulSoup(response.text, 'html.parser')
        return hashlib.md5(soup.encode('utf-8')).hexdigest()
    except Exception as e:
        logging.error(f"Error obteniendo el hash de la página: {e}")
        return None

# Leer el hash inicial desde un archivo (persistencia)
def read_initial_hash():
    try:
        with open('page_hash.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Guardar el hash actual en un archivo
def save_current_hash(hash_value):
    with open('page_hash.txt', 'w') as file:
        file.write(hash_value)

# Hash inicial de la página
initial_hash = read_initial_hash() or get_page_hash(url)
if initial_hash:
    save_current_hash(initial_hash)

# Intervalo de tiempo en segundos (cada hora)
interval = 3600

while True:
    time.sleep(interval)
    current_hash = get_page_hash(url)
    
    if current_hash and current_hash != initial_hash:
        try:
            pb.push_note("¡Actualización en la página!", f"La página {url} ha sido actualizada.")
            logging.info("Notificación enviada: La página ha sido actualizada.")
            
            # Actualiza el hash inicial y lo guarda
            initial_hash = current_hash
            save_current_hash(current_hash)
        except Exception as e:
            logging.error(f"Error enviando notificación: {e}")
