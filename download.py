from selenium import webdriver
import os
import time
import pygetwindow as gw

# Obtener la ventana de Chrome abierta
chrome_window = gw.getWindowsWithTitle("Google Chrome")[0]

# Obtener el ID de la ventana de Chrome
chrome_window_id = chrome_window._hWnd

# Conectar Selenium a la ventana de Chrome existente
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = f"localhost:{chrome_window_id}"
driver = webdriver.Chrome(options=chrome_options)

# Obtener todas las pestañas abiertas
ventanas = driver.window_handles

# Directorio donde se guardarán los archivos PDF
directorio_descargas = "C:/Users/Accor/Documents/OGfiducia_Automatic/Download"

for i, ventana in enumerate(ventanas):
    # Cambiar a la pestaña actual
    driver.switch_to.window(ventana)
    
    # Esperar un tiempo para que se cargue la pestaña
    time.sleep(2)
    
    # Obtener la URL de la pestaña actual
    url_actual = driver.current_url
    
    # Descargar el PDF de la URL actual
    driver.get("chrome://settings/content/pdfDocuments")
    time.sleep(2)
    
    # Ejecutar un script JavaScript para hacer clic en el botón de descarga
    driver.execute_script("document.querySelector('button[data-command=\"download\"]').click()")
    
    # Mover el archivo descargado al directorio especificado
    nombre_archivo = f"{i + 1}.pdf"
    os.rename(os.path.join(os.path.expanduser("~"), "Downloads", "archivo.pdf"), os.path.join(directorio_descargas, nombre_archivo))

# Cerrar el navegador al finalizar
driver.quit()

print("Proceso de descarga completado con éxito.")