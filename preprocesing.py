"""Archivo con el preprocesamiento de archivos en inglés y español para el proyecto"""
import csv
import re
import nltk
from googletrans import Translator

lista_palabras = [
    "processor", "ram", "storage", "memory", "battery", "screen", "camera", "display"
    ]

def tiene_palabra_importante(oracion, llave):
    tokens = nltk.word_tokenize(oracion.lower())
    si_esta = False
    for token in tokens:
        if token in lista_palabras:
            llave.append(token)
            si_esta = True
    return si_esta

def generar_oraciones(archivo):
    """
    Función que procesa el texto
    """
    translator = Translator()
    contador = 0
    salida = open('Oraciones_'+archivo, "w")
    writer = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    with open(archivo, 'r') as abierto:
        reader = csv.reader(abierto)
        for row in reader:
            oraciones = row[0].split('.')
            contador += 1
            print(contador)
            lenguaje = translator.detect(oraciones[0])
            if lenguaje.lang == "es":
                for oracion in oraciones:
                    if len(oracion) > 1:
                        oracion = re.sub(r'[\W]', ' ', oracion)
                        oracion = oracion.replace('\n', ' ')
                        oracion = oracion.replace('\t', ' ')
                        oracion = oracion.replace('\r', ' ')
                        traducido = translator.translate(oracion)
                        llave = []
                        if tiene_palabra_importante(traducido.text, llave):
                            writer.writerow([traducido.text, llave])
            else:
                for oracion in oraciones:
                    if len(oracion) > 1:
                        oracion = re.sub(r'[\W]', ' ', oracion)
                        oracion = oracion.replace('\n', ' ')
                        oracion = oracion.replace('\t', ' ')
                        oracion = oracion.replace('\r', ' ')
                        llave = []
                        if tiene_palabra_importante(oracion, llave):
                            writer.writerow([oracion, llave])

generar_oraciones('Samsung.csv')
