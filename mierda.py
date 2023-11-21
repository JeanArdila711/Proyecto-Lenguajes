import tkinter as tk
from PIL import Image, ImageTk
import re
import os

# emojis y sus rutas de imagen correspondientes
emoji_a_imagen = {
    ":)": os.path.abspath('emoji_parser-main/emojicshd/png/005-sonriente.png'), 
    ":3": os.path.abspath('emoji_parser-main/emojicshd/png/063-perro-3.png'),
    "xD": os.path.abspath('emoji_parser-main/emojicshd/png/010-risa.png'),
    ":\(": os.path.abspath('emoji_parser-main/emojicshd/png/009-triste.png'),
    ":D": os.path.abspath('emoji_parser-main/emojicshd/png/058-riendo.png'),
    ";\)": os.path.abspath('emoji_parser-main/emojicshd/png/018-guino.png'),
    ":-\)": os.path.abspath('emoji_parser-main/emojicshd/png/006-feliz-1.png'),
    "(y)": os.path.abspath('emoji_parser-main/emojicshd/png/031-me-gusta-1.png'),
    "(n)": os.path.abspath('emoji_parser-main/emojicshd/png/028-pulgares-abajo.png'),
    "<3": os.path.abspath('emoji_parser-main/emojicshd/png/067-corazon.png'),
    ":-O": os.path.abspath('emoji_parser-main/emojicshd/png/055-sorpresa.png'),
    ":\(": os.path.abspath('emoji_parser-main/emojicshd/png/009-triste.png'),
    ":O": os.path.abspath('emoji_parser-main/emojicshd/png/004-conmocionado.png'),
    ":/": os.path.abspath('emoji_parser-main/emojicshd/png/008-confuso.png'),
    ":*": os.path.abspath('emoji_parser-main/emojicshd/png/068-beso.png'),
    "\^\^": os.path.abspath('emoji_parser-main/emojicshd/png/016-estrella.png'),
    "·--·": os.path.abspath('emoji_parser-main/emojicshd/png/069_gato.png')
}
# expresión regular para identificar emojis
regex_emojis = r":3|xD|:\)|:\(|:D|;\)|:P|:-\)|:-\(|\(y\)|\(n\)|<3|:-O|:O|:-/|:/|:*|>:\(|\^\^|:-\]|·--·"

class VerificadorPalabras:
    def __init__(self, ruta_diccionario):
        self.palabras_espanol = self.cargar_diccionario(ruta_diccionario)

    def cargar_diccionario(self, ruta_diccionario):
        diccionario_palabras_espanol = set()
        with open(ruta_diccionario, 'r', encoding='utf-8') as archivo_diccionario:
            for linea in archivo_diccionario:
                palabra = linea.strip()
                diccionario_palabras_espanol.add(palabra.lower())
        return diccionario_palabras_espanol

    def es_palabra_espanol(self, palabra):
        return palabra.lower() in self.palabras_espanol

def identificar_emojis(texto):
    return re.findall(regex_emojis, texto)

def mostrar_resultados(entrada, palabras_encontradas, total_emojis):
    etiqueta_texto.config(text=entrada)
    etiqueta_salida.config(text=f"Se encontraron {palabras_encontradas} palabras en español y {total_emojis} emojis.")

def analizador_lexicografico(entrada):
    lista_emojis_encontrados = identificar_emojis(entrada)
    entrada_con_emojis = reemplazar_palabra_con_emoji(entrada, lista_emojis_encontrados)

    verificador = VerificadorPalabras('emoji_parser-main/diccionario.txt')
    palabras_encontradas = 0
    palabras = re.findall(r'\b[a-zA-ZáéíóúüÁÉÍÓÚÜñÑ]+\b', entrada)
    for palabra in palabras:
        if verificador.es_palabra_espanol(palabra.lower()):
            palabras_encontradas += 1

    total_emojis = len(lista_emojis_encontrados)
    mostrar_resultados(entrada_con_emojis, palabras_encontradas, total_emojis)

def reemplazar_palabra_con_emoji(entrada, lista_emojis_encontrados):
    texto_con_emojis = entrada
    emojis_frame = tk.Frame(ventana)
    emojis_frame.pack()

    for emoji_encontrado in lista_emojis_encontrados:
        ruta_imagen = emoji_a_imagen.get(emoji_encontrado)
        if ruta_imagen:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((40, 40), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(imagen)

            etiqueta_imagen = tk.Label(emojis_frame, image=imagen)
            etiqueta_imagen.image = imagen
            etiqueta_imagen.pack(side=tk.LEFT)

            texto_con_emojis = texto_con_emojis.replace(emoji_encontrado, f" {emoji_encontrado} ")

    return texto_con_emojis

ventana = tk.Tk()
ventana.title("Analizador de Emojis")
ventana.geometry("800x500")

texto_adicional = "UNIVERSIDAD EAFIT PROYECTO FINAL"
texto_adicional1 = "LENGUAJES DE PROGRAMACIÓN"
fuente_negrita = ("Arial", "13", "bold")
label_texto_adicional = tk.Label(ventana, text=texto_adicional, font=fuente_negrita)
label_texto_adicional1 = tk.Label(ventana, text=texto_adicional1, font=fuente_negrita)
label_texto_adicional.pack(anchor="ne")  
label_texto_adicional1.pack(anchor="ne")

imagen = Image.open('./emoji_parser-main/emojicshd/logo_eafit_completo.png')
imagen = imagen.resize((300, 100), Image.LANCZOS)
render = ImageTk.PhotoImage(imagen)
imagen_label = tk.Label(ventana, image=render)
imagen_label.pack(anchor="nw", side="top")

frame_top = tk.Frame(ventana)
frame_top.pack()

fuente_label = ("Arial", 14, "bold")
label_ingrese_texto = tk.Label(frame_top, text="Ingrese un texto:", font=fuente_label)
label_ingrese_texto.grid(row=0, column=0, padx=20, pady=20, sticky="w")  

fuente_entrada = ("Arial", 14)
input_entry = tk.Entry(frame_top, font=fuente_entrada)
input_entry.grid(row=0, column=1, padx=5, pady=20, sticky="w")  

boton = tk.Button(ventana, text="Procesar texto", command=lambda: analizador_lexicografico(input_entry.get()))
boton.pack(pady=10)  

etiqueta_texto = tk.Label(ventana, text="", wraplength=600)
etiqueta_texto.pack()

etiqueta_salida = tk.Label(ventana, text="Salida: ", font=fuente_label)
etiqueta_salida.pack()

ventana.mainloop()
