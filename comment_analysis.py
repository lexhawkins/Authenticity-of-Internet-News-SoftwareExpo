import tkinter as tk
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import chardet
from textblob import TextBlob

# Función para clasificar comentarios
def clasificar_comentarios(comentarios):
    analyzer = SentimentIntensityAnalyzer()
    categorias = {'In favor': 0, 'Ambiguous': 0, 'Against': 0}

    palabras_clave = ['mentira', 'falso', 'invento', 'fake', 'rumor', 'marketing']
    palabras_buena = ['bendiciones', 'felicidades', 'dios', 'bendiga']
    
    for comentario in comentarios:
        comentario = comentario.strip().lower()  # Eliminar espacios y poner en minúsculas
        
        # Verificar si hay palabras clave
        if any(palabra in comentario for palabra in palabras_clave):
            categoria = 'Against'  # Si contiene palabras clave, lo clasifica como 'Desmintiendo'
        elif any(palabra in comentario for palabra in palabras_buena):
            categoria = 'In favor' 
        else:
            # Analizar sentimiento solo si no contiene palabras clave
            sentiment_score = analyzer.polarity_scores(comentario)
            
            if sentiment_score['compound'] >= 0.05:
                categoria = 'In favor'  # Alegría
            elif sentiment_score['compound'] <= -0.05:
                categoria = 'Against'  # Enojo
            else:
                categoria = 'Ambiguous'  # Sorpresa

        # Incrementar las categorías
        categorias[categoria] += 1

    return categorias

# Función para mostrar el gráfico en un subplot
def mostrar_grafico(ax, categorias, titulo):
    labels = list(categorias.keys())
    sizes = list(categorias.values())

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title(f'{titulo} Post Comments Distribution')
    ax.axis('equal')  # Para que el gráfico sea un círculo

def cargar_txt(nombre):
    comentarios = []
    
    try:
        # Cambia la ruta al archivo .txt
        with open(nombre, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        with open(nombre, encoding=encoding) as file:
            comentarios = file.readlines()

        if not comentarios:
            print(f"El archivo {nombre} no contiene comentarios.")
            return None

        comentarios = [comentario.strip().replace('"', '') for comentario in comentarios]
        return clasificar_comentarios(comentarios)

    except Exception as e:
        print(f"Ocurrió un error al cargar el archivo {nombre}: {e}")
        return None

# Crear la figura con tres subgráficos en una sola ventana
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

archivos = ['twitter.txt', 'facebook.txt', 'tiktok.txt']
titulos = ['Twitter', 'Facebook', 'TikTok']

for i in range(3):
    categorias = cargar_txt(archivos[i])
    if categorias:
        mostrar_grafico(axes[i], categorias, titulos[i])

plt.show()
