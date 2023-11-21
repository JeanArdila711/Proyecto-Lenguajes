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
emoji_a_palabra = {
    ":)": "sonriente",
    ":D": "riendo",
    "xD": "risa",
    ":-\)": "feliz",
    ":-O": "sorpresa",
    ":O": "conmocionado",
    ":/": "confuso",
    ":*": "beso",
    "(y)": "me gusta",
    "(n)": "pulgares abajo",
    "<3": "corazón",
}



# expresión regular para identificar emojis
regex_emojis = r":3|xD|:\)|:\(|:D|;\)|:P|:-\)|:-\(|\(y\)|\(n\)|<3|:-O|:O|:-/|:/|:*|>:\(|\^\^|:-\]|·--·"

class VerificadorPalabras:
    def __init__(self, ruta_diccionario):
        self.ruta_diccionario = ruta_diccionario
        self.palabras_espanol = self.cargar_diccionario()

    def cargar_diccionario(self):
        try:
            with open(self.ruta_diccionario, 'r', encoding='utf-8') as archivo:
                palabras = archivo.read().splitlines()
                return set(palabras)
        except FileNotFoundError:
            print("El archivo del diccionario no se encontró.")
            return set()

    def contar_palabras_espanol(self, texto):
        palabras = texto.split()
        palabras_espanol = 0
        emojis = 0

        for palabra in palabras:
            palabra_limpia = palabra.strip().lower()

            if palabra_limpia.isalpha() and not re.match(regex_emojis, palabra_limpia):
                palabras_espanol += 1

        return palabras_espanol, emojis
    
def identificar_emojis(texto):
    return re.findall(regex_emojis, texto)

def presionar_boton():
    entrada_texto = input_entry.get()
    verificador = VerificadorPalabras('emoji_parser-main\diccionario.txt')
    palabras_espanol = verificador.contar_palabras_espanol(entrada_texto)
    lista_emojis_encontrados = identificar_emojis(entrada_texto)

    total_emojis = len(lista_emojis_encontrados)
    
    # Mostrar resultado en la etiqueta de salida
    etiqueta_salida.config(text=f"Se encontraron {palabras_espanol} palabras y {total_emojis} emojis.")

    entrada_con_palabras, emojis = reemplazar_emojis_con_palabras(entrada_texto, lista_emojis_encontrados)

    # Mostrar texto con emojis reemplazados por palabras
    etiqueta_texto.config(text=entrada_con_palabras)

def reemplazar_emojis_con_palabras(entrada, lista_emojis_encontrados):
    texto_con_palabras = entrada
    emojis = 0

    for emoji_encontrado in lista_emojis_encontrados:
        ruta_imagen = emoji_a_imagen.get(emoji_encontrado)
        if ruta_imagen:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((40, 40), Image.LANCZOS)  # Ajusta el tamaño del emoji a 40x40 píxeles con filtro LANCZOS
            imagen = ImageTk.PhotoImage(imagen)

            etiqueta_imagen = tk.Label(ventana, image=imagen)
            etiqueta_imagen.image = imagen
            etiqueta_imagen.pack(side=tk.LEFT)

            palabra_encontrada = emoji_a_palabra.get(emoji_encontrado)
            palabra_encontrada = palabra_encontrada or "emoji"
            texto_con_palabras = texto_con_palabras.replace(emoji_encontrado, palabra_encontrada)
            emojis += 1

    return texto_con_palabras, emojis

def analizador_lexicográfico(entrada):
    lista_emojis_encontrados = identificar_emojis(entrada)
    entrada_con_emojis, emojis = reemplazar_emojis_con_palabras(entrada, lista_emojis_encontrados)

    # Actualiza la etiqueta de texto con el texto procesado
    etiqueta_texto.config(text=entrada_con_emojis)

    # Muestra el resultado en la etiqueta de salida
    palabras_espanol, emojis_contados = VerificadorPalabras('emoji_parser-main\diccionario.txt').contar_palabras_espanol(entrada)
    total_emojis = len(lista_emojis_encontrados)
    etiqueta_salida.config(text=f"Se encontraron {palabras_espanol} palabras y {total_emojis[1]} emojis.")

# Crear la ventana principal
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

# Imagen
imagen = Image.open('./emoji_parser-main/emojicshd/logo_eafit_completo.png')
imagen = imagen.resize((300, 100), Image.LANCZOS)
render = ImageTk.PhotoImage(imagen)
imagen_label = tk.Label(ventana, image=render)
imagen_label.pack(anchor="nw", side="top")

# Frame para organizar elementos superiores
frame_top = tk.Frame(ventana)
frame_top.pack()

# Label "Ingrese un texto" en negrita debajo de la imagen
fuente_label = ("Arial", 14, "bold")
label_ingrese_texto = tk.Label(frame_top, text="Ingrese un texto:", font=fuente_label)
label_ingrese_texto.grid(row=0, column=0, padx=20, pady=20, sticky="w")  # Posicionamiento a la izquierda

# Campo de entrada de texto al lado del texto "Ingrese un texto"
fuente_entrada = ("Arial", 14)
input_entry = tk.Entry(frame_top, font=fuente_entrada)
input_entry.grid(row=0, column=1, padx=5, pady=20, sticky="w")  # Posicionamiento a la izquierda

# Botón "Procesar texto" debajo del campo de entrada
boton = tk.Button(ventana, text="Procesar texto", command=presionar_boton)
boton.pack(pady=10)  # Ajuste de espaciado

# Etiqueta para mostrar el texto analizado
etiqueta_texto = tk.Label(ventana, text="", wraplength=600)
etiqueta_texto.pack()

# Etiqueta de salida para mostrar el resultado después de procesar la cadena
etiqueta_salida = tk.Label(ventana, text="Salida: ", font=fuente_label)
etiqueta_salida.pack()

ventana.mainloop()
