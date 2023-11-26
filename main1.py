import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import re


# emojis y sus rutas de imagen correspondientes
EMOJI_A_IMAGEN = {
    ":)": "emojicshd/png/005-sonriente.png",
    ":3": "emojicshd/png/064-perro-4.png",
    "xD": "emojicshd/png/010-risa.png",
    ":\(": "emojicshd/png/009-triste.png",
    ":D": "emojicshd/png/058-riendo.png",
    ";\)": "emojicshd/png/018-guino.png",
    ":-\)": "emojicshd/png/006-feliz-1.png",
    "(y)": "emojicshd/png/031-me-gusta-1.png",
    "(n)": "emojicshd/png/028-pulgares-abajo.png",
    ":-O": "emojicshd/png/055-sorpresa.png",
    ":\(": "emojicshd/png/009-triste.png",
    ":O": "emojicshd/png/004-conmocionado.png",
    ":/": "emojicshd/png/008-confuso.png",
    ":*": "emojicshd/png/068-beso.png",
    "\^\^": "emojicshd/png/016-estrella.png"
}

# expresión regular para identificar emojis
REGEX_EMOJIS =  r":3|xD|:\)|:\(|:D|;\)|:-\)|\(y\)|\(n\)|<3|:-O|:O|:/|·--·"


class VerificadorPalabras:
    def __init__(self, ruta_diccionario):
        self.ruta_diccionario = ruta_diccionario
        self.palabras_espanol = self.cargar_diccionario()

    def cargar_diccionario(self):
        try:
            with open(self.ruta_diccionario, "r", encoding="utf-8") as archivo:
                palabras = archivo.read().splitlines()
                return set(palabras)
        except FileNotFoundError:
            print("El archivo del diccionario no se encontró.")
            return set()

    def contar_palabras_espanol(self, texto, lista_emojis_encontrados):
        # Eliminar emojis
        for emoji_encontrado in lista_emojis_encontrados:
            texto = texto.replace(emoji_encontrado, " ")
        palabras = texto.split(" ")
        palabras_espanol = 0
        for palabra in palabras:
            palabra_limpia = palabra.strip()
            if palabra_limpia.isalpha() and not re.match(REGEX_EMOJIS, palabra_limpia):
                palabras_espanol += 1
        return palabras_espanol


def identificar_emojis(texto):
    lista_emojis = re.findall(REGEX_EMOJIS, texto)
    return lista_emojis, len(lista_emojis)


def reemplazar_emojis_con_imagenes(entrada, lista_emojis_encontrados):
    for emoji_encontrado in lista_emojis_encontrados:
        entrada = entrada.replace(
            emoji_encontrado, f" {EMOJI_A_IMAGEN[emoji_encontrado]} "
        )
    return entrada


def texto_a_imagenes(entrada_con_emojis):
    lista_palabras = entrada_con_emojis.split(" ")
    for indice, palabra in enumerate(lista_palabras):
        if palabra == "":
            lista_palabras.pop(indice)
    print(lista_palabras)
    for indice, palabra in enumerate(lista_palabras):
        if "emojicshd/png" in palabra:
            continue
        else:
            palabra += "   "
            nombre_archivo = f"output/{indice}.png"
            lista_palabras[indice] = nombre_archivo

            # Crear imagen
            tamano = 14
            fuente = ImageFont.truetype("arial.ttf", tamano)
            imagen = Image.new(
                mode="RGB",
                size=(int(tamano / 2) * len(palabra), tamano + 30),
                color="white",
            )
            draw = ImageDraw.Draw(imagen)
            draw.text((14, 14), palabra, font=fuente, fill=(0, 0, 0))
            imagen.save(nombre_archivo)
    return lista_palabras


def concatenar_imagenes(lista_imagenes):
    print(lista_imagenes)
    images = []
    for archivo_imagen in lista_imagenes:
        imagen_abierta = Image.open(archivo_imagen)
        if "emojicshd" in archivo_imagen:
            # Ajusta el tamaño del emoji a 45x45 píxeles
            imagen_abierta = imagen_abierta.resize((45, 45))
        images.append(imagen_abierta)

    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    new_im.save("output/resultado_imagen.png")


def analizador_lexicográfico(entrada):
    lista_emojis_encontrados, total_emojis = identificar_emojis(entrada)

    # Mostrar el resultado en la etiqueta de salida
    palabras_espanol = VerificadorPalabras("diccionario.txt")
    total_palabras = palabras_espanol.contar_palabras_espanol(
        entrada, lista_emojis_encontrados
    )
    etiqueta_salida.config(
        text=f"Se encontraron {total_palabras} palabras y {total_emojis} emojis."
    )

    # Reemplazar emojis con imagenes
    entrada_con_emojis = reemplazar_emojis_con_imagenes(
        entrada, lista_emojis_encontrados
    )
    lista_imagenes = texto_a_imagenes(entrada_con_emojis)
    concatenar_imagenes(lista_imagenes)

    # Mostrar imagen como salida
    imagen = Image.open("output/resultado_imagen.png")
    imagen = ImageTk.PhotoImage(imagen)
    etiqueta_imagen = tk.Label(ventana, image=imagen)
    etiqueta_imagen.image = imagen
    etiqueta_imagen.pack(side=tk.BOTTOM)


def presionar_boton():
    entrada_texto = input_entry.get()
    texto_salida = analizador_lexicográfico(entrada_texto)
    etiqueta_salida.config(text=texto_salida)


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
imagen = Image.open("emojicshd/logo_eafit_completo.png")
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
label_ingrese_texto.grid(
    row=0, column=0, padx=20, pady=20, sticky="w"
)  # Posicionamiento a la izquierda

# Campo de entrada de texto al lado del texto "Ingrese un texto"
fuente_entrada = ("Arial", 14)
input_entry = tk.Entry(frame_top, font=fuente_entrada)
input_entry.grid(
    row=0, column=1, padx=5, pady=20, sticky="w"
)  # Posicionamiento a la izquierda

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
