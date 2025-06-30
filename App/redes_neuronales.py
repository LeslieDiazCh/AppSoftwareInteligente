import tkinter as tk
from tkinter import font
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import tensorflow as tf
import random
import pathlib
import sys


# Configuración
CLASES = ["Sol", "Casa", "Árbol", "Gato", "Pez"]


BASE_PATH = getattr(sys, '_MEIPASS', pathlib.Path(__file__).resolve().parent.parent)
MODELO_PATH = BASE_PATH / "data" / "quickdraw_mlp.h5"

IMG_CANVAS = 280
RADIUS = 8

# Cargar modelo
modelo = tf.keras.models.load_model(MODELO_PATH)

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    sw = ventana.winfo_screenwidth()
    sh = ventana.winfo_screenheight()
    x = int((sw / 2) - (ancho / 2))
    y = int((sh / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def lanzar_minijuego(ventana_principal=None):
    if ventana_principal:
        ventana_principal.withdraw()

    juego = tk.Tk()
    juego.title("Minijuego · Adivina el Dibujo")
    juego.configure(bg="#f0f4f8")
    juego.resizable(False, False)
    centrar_ventana(juego, 500, 640)

    juego.focus_force()
    juego.grab_set()

    # Fuentes
    titulo_fuente = font.Font(family="Helvetica", size=16, weight="bold")
    marcador_fuente = font.Font(family="Courier", size=18, weight="bold")
    boton_fuente = font.Font(family="Helvetica", size=12)
    resultado_fuente = font.Font(family="Helvetica", size=12, weight="bold")

    estado = {
        "objetivo": random.randrange(len(CLASES)),
        "jugador": 0,
        "ia": 0
    }
    ultimo_objetivo = estado["objetivo"]

    def actualizar_marcador():
        jugador_lbl.config(text=f"{estado['jugador']}")
        ia_lbl.config(text=f"{estado['ia']}")

    def actualizar_resultado(texto, color):
        resultado_lbl.config(text=texto, fg=color)

    def nuevo_objetivo():
        nonlocal ultimo_objetivo
        opciones = list(range(len(CLASES)))
        if ultimo_objetivo in opciones:
            opciones.remove(ultimo_objetivo)
        nuevo = random.choice(opciones)
        estado["objetivo"] = nuevo
        ultimo_objetivo = nuevo
        objetivo_lbl.config(text=f"Dibuja un/una: {CLASES[nuevo]}")

    def limpiar():
        canvas.delete("all")
        draw.rectangle((0, 0, IMG_CANVAS, IMG_CANVAS), fill="white")
        actualizar_resultado("", "black")

    def dibujar(event):
        x, y = event.x, event.y
        canvas.create_oval(x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS, fill="black", outline="")
        draw.ellipse((x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS), fill="black")

    def predecir():
        img_small = image.resize((28, 28))
        img_small = ImageOps.invert(img_small.convert("L"))
        arr = np.asarray(img_small).reshape(1, -1) / 255.0

        pred = np.argmax(modelo.predict(arr, verbose=0)[0])
        if pred == estado["objetivo"]:
            estado["jugador"] += 1
            actualizar_resultado(f"✅ ¡Correcto! Era un {CLASES[pred]}", "green")
        else:
            estado["ia"] += 1
            actualizar_resultado(f"❌ Incorrecto. Eso parecía un {CLASES[pred]}", "red")

        actualizar_marcador()

        # Esperar 2 segundos antes de limpiar y cambiar
        juego.after(2000, lambda: [limpiar(), nuevo_objetivo()])

    def salir_y_regresar():
        if ventana_principal:
            ventana_principal.deiconify()
        juego.grab_release()
        juego.destroy()

    juego.protocol("WM_DELETE_WINDOW", salir_y_regresar)

    # Marcador visual
    marcador_frame = tk.Frame(juego, bg="#dfe6e9", bd=2, relief="groove", padx=20, pady=10)
    marcador_frame.pack(pady=(15, 5))

    tk.Label(marcador_frame, text="Jugador", font=marcador_fuente, bg="#dfe6e9").grid(row=0, column=0, padx=10)
    tk.Label(marcador_frame, text="IA", font=marcador_fuente, bg="#dfe6e9").grid(row=0, column=2, padx=10)

    jugador_lbl = tk.Label(marcador_frame, text="0", font=marcador_fuente, bg="#2ecc71", fg="white", width=3)
    jugador_lbl.grid(row=1, column=0, padx=10)

    tk.Label(marcador_frame, text="vs", font=marcador_fuente, bg="#dfe6e9").grid(row=1, column=1, padx=10)

    ia_lbl = tk.Label(marcador_frame, text="0", font=marcador_fuente, bg="#e74c3c", fg="white", width=3)
    ia_lbl.grid(row=1, column=2, padx=10)

    objetivo_lbl = tk.Label(juego, font=titulo_fuente, bg="#f0f4f8", fg="#0a3d62")
    objetivo_lbl.pack(pady=10)

    canvas = tk.Canvas(juego, width=IMG_CANVAS, height=IMG_CANVAS, bg="white", cursor="cross")
    canvas.pack()
    image = Image.new("RGB", (IMG_CANVAS, IMG_CANVAS), "white")
    draw = ImageDraw.Draw(image)
    canvas.bind("<B1-Motion>", dibujar)

    estilo_boton = {
        "width": 18,
        "height": 2,
        "font": boton_fuente,
        "fg": "white",
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    tk.Button(juego, text="Adivinar", command=predecir,
              bg="#27ae60", activebackground="#1e8449", **estilo_boton).pack(pady=8)

    tk.Button(juego, text="Limpiar", command=limpiar,
              bg="#e67e22", activebackground="#d35400", **estilo_boton).pack()

    resultado_lbl = tk.Label(juego, text="", font=resultado_fuente, bg="#f0f4f8")
    resultado_lbl.pack(pady=15)

    tk.Button(juego, text="Salir", command=salir_y_regresar,
              bg="#d63031", activebackground="#c0392b", **estilo_boton).pack(pady=2)

    actualizar_marcador()
    nuevo_objetivo()
    juego.mainloop()

# Para prueba individual
if __name__ == "__main__":
    lanzar_minijuego()
