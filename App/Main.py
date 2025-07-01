import tkinter as tk
import sys
from tkinter import font, messagebox

def mostrar_ventana_carga(texto="Cargando...", duracion=2500):
    carga = tk.Toplevel()
    carga.title("")
    carga.geometry("300x100")
    carga.configure(bg="white")
    carga.overrideredirect(True)
    centrar_ventana(carga, 300, 100)
    tk.Label(carga, text=texto, font=("Helvetica", 12, "bold"), bg="white", fg="#2d3436").pack(expand=True)
    carga.update()
    return carga

def abrir_geneticos():
    carga = mostrar_ventana_carga("Cargando Algoritmo Genético...")
    ventana.after(200, lambda: cargar_geneticos(carga))

def cargar_geneticos(carga):
    try:
        from algoritmo_genetico import lanzar_algoritmo_genetico
        lanzar_algoritmo_genetico(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir Algoritmos Genéticos:\n{e}")
    finally:
        carga.destroy()

def abrir_naive_bayes():
    carga = mostrar_ventana_carga("Cargando Naive Bayes...")
    ventana.after(200, lambda: cargar_naive_bayes(carga))

def cargar_naive_bayes(carga):
    try:
        import naive_bayes
        naive_bayes.lanzar_minijuego(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir Naive Bayes:\n{e}")
    finally:
        carga.destroy()

def abrir_redes_neuronales():
    carga = mostrar_ventana_carga("Cargando Redes Neuronales...")
    ventana.after(200, lambda: cargar_redes(carga))

def cargar_redes(carga):
    try:
        import redes_neuronales
        redes_neuronales.lanzar_minijuego(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el módulo de Redes Neuronales:\n{e}")
    finally:
        carga.destroy()

def abrir_clustering():
    carga = mostrar_ventana_carga("Cargando Clustering...")
    ventana.after(200, lambda: cargar_clustering(carga))

def cargar_clustering(carga):
    try:
        import clustering
        clustering.lanzar_clustering(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la Aplicación de Clustering:\n{e}")
    finally:
        carga.destroy()


def cargar_clustering(carga):
    try:
        import clustering
        clustering.lanzar_clustering(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la Aplicación de Clustering:\n{e}")
    finally:
        carga.destroy()

def abrir_transfer_learning():
    carga = mostrar_ventana_carga("Cargando Transfer Learning...")
    ventana.after(200, lambda: cargar_transfer_learning(carga))

def cargar_transfer_learning(carga):
    try:
        import transferlearning
        transferlearning.lanzar_transfer_learning(ventana)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el módulo de Transfer Learning:\n{e}")
    finally:
        carga.destroy()

def salir_app():
    ventana.destroy()
    sys.exit(0)  # Mata el proceso sin condiciones


def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
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

if __name__ == "__main__":
    lanzar_menu()
