from tkinter import *
import re
from PIL import Image, ImageTk


# emoji y su imagen correspondiente
emoji_a_imagen = {
    "xD": 'emoji_parser-main\emojicshd\png\005-sonriente.png',
    ":3" : 'emoji_parser-main\emojicshd\png\050-enamorado.png'

}




# expresion regular para identificar emojis
regex_emojis = r":3|xD|:\)|:\(|:D|;\)|:P|:-\)|:-\(|\(y\)|\(n\)|<3|\\m/|:-O|:O|:-/|:/|:\*|>:\(|\^\^|:-\]"


def mostrar_imagen(emoji_seleccionado):
    ruta_imagen = emoji_a_imagen.get(emoji_seleccionado)

    if ruta_imagen:
        ventana = Tk()
        ventana.title("Emoji Viewer")

        imagen = Image.open(ruta_imagen)
        imagen = ImageTk.PhotoImage(imagen)

        etiqueta_imagen = Label(ventana, image=imagen)
        etiqueta_imagen.image = imagen

        etiqueta_imagen.pack()
        ventana.mainloop()
    else:
        print("Emoji no encontrado en el diccionario")
        

def analizador_lexicográfico(entrada):
    lista_emojis_encontrados = identificar_emojis(entrada)
    entrada_con_emojis = reemplazar_emojis(entrada, lista_emojis_encontrados)
    #identificar_palabras_espanol(entrada_con_emojis)Lis
    return entrada_con_emojis


def identificar_emojis(entrada):
    return re.findall(regex_emojis, entrada)


def reemplazar_emojis(entrada, lista_emojis_encontrados):
    for emoji_encontrado in lista_emojis_encontrados:
        entrada = entrada.replace(emoji_encontrado, emoji_a_imagen[emoji_encontrado])
    return entrada

# Esto es para probar el script
entrada = "el perro :3 me mordio xD asfasf asdsa"
analizador_lexicográfico(entrada)
