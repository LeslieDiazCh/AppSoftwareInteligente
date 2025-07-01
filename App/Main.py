import subprocess
import sys
import os
import importlib.util

# Configuración de entorno Tcl/Tk
tcl_path = r"C:\Users\Hermann\AppData\Local\Programs\Python\Python311\tcl"
os.environ['TCL_LIBRARY'] = os.path.join(tcl_path, 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(tcl_path, 'tk8.6')

def esta_instalada(lib):
    return importlib.util.find_spec(lib) is not None

def verificar_e_instalar_dependencias():
    paquetes = {
        "pandas": "pandas",
        "numpy": "numpy",
        "matplotlib": "matplotlib",
        "scikit-learn": "sklearn",
        "tensorflow": "tensorflow",
        "pillow": "PIL",
        "tqdm": "tqdm",
        "spacy": "spacy",
        "openpyxl": "openpyxl"
    }

    faltantes = [paquete for paquete, modulo in paquetes.items() if not esta_instalada(modulo)]

    if faltantes:
        print(f"📦 Instalando {len(faltantes)} paquetes: {', '.join(faltantes)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *faltantes])

    try:
        import spacy
        spacy.load("es_core_news_md")
    except (ImportError, OSError):
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "es_core_news_md"])

    try:
        import tkinter
    except ImportError:
        raise SystemExit("Instala Python con soporte Tcl/Tk desde https://www.python.org/downloads/")

verificar_e_instalar_dependencias()

# ---------------- MENÚ PRINCIPAL ----------------

import tkinter as tk
from tkinter import font, messagebox

def mostrar_ventana_carga(texto="Cargando..."):
    carga = tk.Toplevel()
    carga.title("")
    carga.geometry("300x100")
    carga.configure(bg="white")
    carga.overrideredirect(True)
    centrar_ventana(carga, 300, 100)
    tk.Label(carga, text=texto, font=("Helvetica", 12, "bold"), bg="white", fg="#2d3436").pack(expand=True)
    carga.update()
    return carga

def abrir_modulo(nombre, funcion):
    carga = mostrar_ventana_carga(f"Cargando {nombre}...")
    ventana.after(200, lambda: cargar_modulo(funcion, carga))

def cargar_modulo(funcion, carga):
    try:
        funcion()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el módulo:\n{e}")
    finally:
        carga.destroy()

def abrir_transfer_learning():
    abrir_modulo("Transfer Learning", lambda: __import__("transferlearning").lanzar_transfer_learning(ventana))

def abrir_naive_bayes():
    abrir_modulo("Naive Bayes", lambda: __import__("naive_bayes").lanzar_minijuego(ventana))

def abrir_redes_neuronales():
    abrir_modulo("Redes Neuronales", lambda: __import__("redes_neuronales").lanzar_minijuego(ventana))

def abrir_clustering():
    abrir_modulo("Clustering", lambda: __import__("clustering").lanzar_clustering(ventana))

def abrir_geneticos():
    abrir_modulo("Algoritmo Genético", lambda: __import__("algoritmo_genetico").lanzar_algoritmo_genetico(ventana))

def salir_app():
    ventana.destroy()
    sys.exit(0)

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def lanzar_menu():
    global ventana
    ventana = tk.Tk()
    ventana.title("Laboratorios - Software Inteligente - 2025")
    centrar_ventana(ventana, 600, 600)
    ventana.configure(bg="#f0f4f8")

    titulo_fuente = font.Font(family="Helvetica", size=18, weight="bold")
    subtitulo_fuente = font.Font(family="Helvetica", size=12)
    boton_fuente = font.Font(family="Helvetica", size=12)

    tk.Label(ventana, text="Laboratorios - Software Inteligente - 2025",
             bg="#f0f4f8", fg="#0a3d62", font=titulo_fuente).pack(pady=(30, 10))

    tk.Label(ventana, text="Alumnos:\n- Germán Callupe Huamán\n- Leslie Diaz Chambi",
             bg="#f0f4f8", fg="#34495e", font=subtitulo_fuente, justify="left").pack(pady=(0, 30))

    estilo_boton = {
        "width": 25, "height": 2, "bg": "#74b9ff", "fg": "white",
        "activebackground": "#0984e3", "activeforeground": "white",
        "font": boton_fuente, "bd": 0, "relief": "flat", "cursor": "hand2"
    }

    tk.Button(ventana, text="Algoritmos Genéticos", command=abrir_geneticos, **estilo_boton).pack(pady=10)
    tk.Button(ventana, text="Naive Bayes", command=abrir_naive_bayes, **estilo_boton).pack(pady=10)
    tk.Button(ventana, text="Redes Neuronales", command=abrir_redes_neuronales, **estilo_boton).pack(pady=10)
    tk.Button(ventana, text="Aplicación Clustering", command=abrir_clustering, **estilo_boton).pack(pady=10)
    tk.Button(ventana, text="Transfer Learning", command=abrir_transfer_learning, **estilo_boton).pack(pady=10)

    tk.Button(ventana, text="Salir", command=salir_app,
              bg="#d63031", fg="white", activebackground="#c0392b",
              activeforeground="white", font=boton_fuente,
              width=15, height=2, bd=0, relief="flat", cursor="hand2").pack(pady=30)

    ventana.mainloop()

# Lanza el menú
if __name__ == "__main__":
    lanzar_menu()
