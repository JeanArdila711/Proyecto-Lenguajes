import tkinter as tk
from analizador_lexicografico import analizador_lexicográfico


def presionar_boton():
    entrada_texto = input_entry.get()
    texto_salida = analizador_lexicográfico(entrada_texto)
    etiqueta_salida.config(text=texto_salida)

def mostrar_imagen(emoji_seleccionado):
    ruta_imagen = tk.emoji_a_imagen.get(emoji_seleccionado)

    if ruta_imagen:

        imagen = tk.Image.open(ruta_imagen)
        imagen = tk.ImageTk.PhotoImage(imagen)

        etiqueta_imagen = tk.Label(ventana, image=imagen)
        etiqueta_imagen.image = imagen

        etiqueta_imagen.pack()
        ventana.mainloop()
    else:
        print("Emoji no encontrado en el diccionario")

ventana = tk.Tk()
ventana.title("Emoji Parser")

etiqueta_entrada = tk.Label(ventana, text="Ingrese un texto")
etiqueta_entrada.pack()

input_entry = tk.Entry(ventana)
input_entry.pack()

boton = tk.Button(ventana, text="Procesar cadena de texto", command=presionar_boton)
boton.pack()

etiqueta_salida = tk.Label(ventana, text="")
etiqueta_salida.pack()


ventana.mainloop()
