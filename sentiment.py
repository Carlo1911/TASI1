"""Archivo con el que se analizará los sentimientos para el proyecto"""
import re
import csv
import nltk
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
from textblob import TextBlob

lista_palabras = [
    "processor", "ram", "storage", "memory", "battery", "screen", "camera", "display"
    ]
caracteristicas = {}
for palabra in lista_palabras:
    caracteristicas[palabra] = []

def obtener_llaves(oracion):
    llaves = oracion.split('\'')
    del llaves[-1]
    del llaves[0]
    llaves = [x for x in llaves if x != ', ']
    print(set(llaves))
    return llaves

def valor_promedio_vader(lista):
    total_suma_pos = 0
    total_suma_neg = 0
    num_elementos = 0
    for elemento in lista:
        total_suma_neg = total_suma_neg + elemento[0]
        total_suma_pos = total_suma_pos + elemento[2]
        num_elementos += 1
    print(num_elementos)
    return [total_suma_neg/num_elementos, total_suma_pos/num_elementos]

def valor_promedio_blob(lista):
    total_suma = 0
    num_elementos = 0
    for elemento in lista:
        total_suma = total_suma + elemento
        num_elementos += 1
    print(num_elementos)
    return [total_suma/num_elementos]

def varder_anilyzer(archivo):
    salida = open('Sentimientos_vader_'+archivo, "w")
    writer = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    analyzer = SentimentIntensityAnalyzer()
    translator = Translator()
    contador = 0
    with open(archivo, 'r') as entrada:
        reader = csv.reader(entrada)
        for row in reader:
            oraciones = row[0].split('.')
            contador += 1
            print(contador)
            llaves = obtener_llaves(row[1])
            for oracion in oraciones:
                if len(oracion) > 1:
                    oracion = re.sub(r'[\W]', ' ', oracion)
                    oracion = oracion.replace('\n', ' ')
                    oracion = oracion.replace('\t', ' ')
                    oracion = oracion.replace('\r', ' ')
                    sentiment = analyzer.polarity_scores(oracion)
                    for llave in llaves:
                        caracteristicas[llave].append([sentiment["neg"], sentiment["neu"], sentiment["pos"]])
                    #print("{:-<65} {}".format(oracion, str(sentiment)))
    for key, value in caracteristicas.items():
        caracteristicas[key] = valor_promedio_vader(value)
        writer.writerow([key, caracteristicas[key][0], caracteristicas[key][1]])

def blob_analyzer(archivo):
    salida = open('Sentimientos_blob_'+archivo, "w")
    writer = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    contador = 0
    with open(archivo, 'r') as entrada:
        reader = csv.reader(entrada)
        for row in reader:
            oraciones = row[0].split('.')
            contador += 1
            print(contador)
            llaves = obtener_llaves(row[1])
            for oracion in oraciones:
                if len(oracion) > 1:
                    oracion = re.sub(r'[\W]', ' ', oracion)
                    oracion = oracion.replace('\n', ' ')
                    oracion = oracion.replace('\t', ' ')
                    oracion = oracion.replace('\r', ' ')
                    blob = TextBlob(oracion)
                    for llave in llaves:
                        for sentence in blob.sentences:
                        #print(sentence + " => " + str(sentence.sentiment.polarity))
                            caracteristicas[llave].append(sentence.sentiment.polarity)
    for key, value in caracteristicas.items():
        caracteristicas[key] = valor_promedio_blob(value)
        writer.writerow([key, caracteristicas[key][0]])

varder_anilyzer('Oraciones_Samsung.csv')
#blob_analyzer('Oraciones_Samsung.csv')
print(caracteristicas)