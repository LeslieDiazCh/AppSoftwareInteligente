import tkinter as tk
from tkinter import font

# Funciones de cada botón (puedes modificar o enlazar con tus módulos)
def abrir_geneticos():
    print("Abrir módulo de Algoritmos Genéticos")

def abrir_naive_bayes():
    print("Abrir módulo de Naive Bayes")

def abrir_redes_neuronales():
    print("Abrir módulo de Redes Neuronales")

def salir_app():
    ventana.quit()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Laboratorios - Software Inteligente - 2025")
ventana.geometry("600x500")
ventana.configure(bg="#f0f4f8")

# Fuente personalizada para títulos
titulo_fuente = font.Font(family="Helvetica", size=18, weight="bold")
subtitulo_fuente = font.Font(family="Helvetica", size=12, weight="normal")
boton_fuente = font.Font(family="Helvetica", size=12)

# Cabecera
titulo_label = tk.Label(ventana, text="Laboratorios - Software Inteligente - 2025",
                        bg="#f0f4f8", fg="#0a3d62", font=titulo_fuente)
titulo_label.pack(pady=(30, 10))

alumnos_label = tk.Label(ventana, text="Alumnos:\n- Germán Callupe Huamán\n- Leslie Diaz Chambi",
                         bg="#f0f4f8", fg="#34495e", font=subtitulo_fuente, justify="left")
alumnos_label.pack(pady=(0, 30))

# Botones
estilo_boton = {
    "width": 25,
    "height": 2,
    "bg": "#74b9ff",
    "fg": "white",
    "activebackground": "#0984e3",
    "activeforeground": "white",
    "font": boton_fuente,
    "bd": 0,
    "relief": "flat",
    "cursor": "hand2"
}

tk.Button(ventana, text="Algoritmos Genéticos", command=abrir_geneticos, **estilo_boton).pack(pady=10)
tk.Button(ventana, text="Naive Bayes", command=abrir_naive_bayes, **estilo_boton).pack(pady=10)
tk.Button(ventana, text="Redes Neuronales", command=abrir_redes_neuronales, **estilo_boton).pack(pady=10)

# Botón de salir
tk.Button(ventana, text="Salir", command=salir_app,
          bg="#d63031", fg="white", activebackground="#c0392b",
          activeforeground="white", font=boton_fuente,
          width=15, height=2, bd=0, relief="flat", cursor="hand2").pack(pady=30)

ventana.mainloop()
