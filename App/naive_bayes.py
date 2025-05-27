import pandas as pd
from sklearn.naive_bayes import CategoricalNB
from sklearn.preprocessing import LabelEncoder
import tkinter as tk
from tkinter import messagebox
import os
import random
import subprocess
import sys

# === ENTRENAMIENTO ===
csv_path = os.path.join("..", "data", "sospechosos.csv")
df = pd.read_csv(csv_path)

X = df[['sombrero', 'gafas', 'altura', 'ropa_negra']]
y = df['culpable']

# Codificación segura
encoders = {}
for col in X.columns:
    le = LabelEncoder()
    X.loc[:, col] = le.fit_transform(X[col])
    encoders[col] = le

y_encoder = LabelEncoder()
y_encoded = y_encoder.fit_transform(y)

model = CategoricalNB()
model.fit(X, y_encoded)


def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# === INTERFAZ ===
class JuegoDetectives:

    def __init__(self, root):
        self.root = root
        self.root.title("🕵️ Juego de Detectives")
        centrar_ventana(self.root, 520, 580)
        self.root.configure(bg="#f5f5f5")
        self.reiniciar_juego()


    def volver_al_menu(self):
        self.root.destroy()
        import Main
        Main.lanzar_menu()


    def reiniciar_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.pistas = {
            'sombrero': None,
            'gafas': None,
            'altura': None,
            'ropa_negra': None
        }

        self.pistas_reveladas = 0

        tk.Label(self.root, text="💼 Un crimen ha ocurrido...",
                 font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

        tk.Label(self.root, text="Recoge todas las pistas para resolver el caso.",
                 font=("Arial", 11), bg="#f5f5f5").pack()

        # Marco de pistas
        self.marco_pistas = tk.LabelFrame(self.root, text="Pistas descubiertas", font=("Arial", 12, "bold"),
                                          bg="#ffffff", padx=10, pady=10)
        self.marco_pistas.pack(pady=10)

        self.label_pistas = {
            'sombrero': tk.Label(self.marco_pistas, text="🔍 Testigo aún no interrogado", font=("Arial", 11), bg="#ffffff"),
            'gafas': tk.Label(self.marco_pistas, text="📸 Cámaras sin revisar", font=("Arial", 11), bg="#ffffff"),
            'altura': tk.Label(self.marco_pistas, text="📏 Estatura sin identificar", font=("Arial", 11), bg="#ffffff"),
            'ropa_negra': tk.Label(self.marco_pistas, text="🧥 Ropa aún no analizada", font=("Arial", 11), bg="#ffffff"),
        }

        for lbl in self.label_pistas.values():
            lbl.pack(pady=2, anchor='w')

        # Botones de pistas
        self.boton_sombrero = tk.Button(self.root, text="👂 Interrogar testigo", command=lambda: self.revelar_pista('sombrero', "¿Tenía sombrero?"), width=30, bg="#dff0d8")
        self.boton_gafas = tk.Button(self.root, text="🎥 Revisar cámaras", command=lambda: self.revelar_pista('gafas', "¿Llevaba gafas?"), width=30, bg="#d9edf7")
        self.boton_altura = tk.Button(self.root, text="📏 Observar estatura", command=lambda: self.revelar_pista('altura', "¿Qué altura tenía?"), width=30, bg="#fcf8e3")
        self.boton_ropa_negra = tk.Button(self.root, text="👕 Inspeccionar ropa", command=lambda: self.revelar_pista('ropa_negra', "¿Vestía de negro?"), width=30, bg="#f2dede")

        self.boton_sombrero.pack(pady=4)
        self.boton_gafas.pack(pady=4)
        self.boton_altura.pack(pady=4)
        self.boton_ropa_negra.pack(pady=4)

        # Botón para volver al menú principal directamente (sin función extra)
        tk.Button(
            self.root,
            text="🚪 Volver al menú principal",
            width=30,
            bg="#cccccc",
            fg="black",
            command=self.volver_al_menu
        ).pack(pady=55)



    def revelar_pista(self, tipo, pregunta):
        opciones = encoders[tipo].classes_.tolist()
        eleccion = random.choice(opciones)
        self.pistas[tipo] = eleccion

        emoji = {
            'sí': "✅",
            'no': "❌",
            'alto': "⬆️",
            'medio': "➡️",
            'bajo': "⬇️"
        }.get(eleccion, "❓")

        self.label_pistas[tipo].config(text=f"{pregunta} ➤ {emoji} {eleccion.capitalize()}")

        getattr(self, f'boton_{tipo}').config(state='disabled')
        self.pistas_reveladas += 1

        if self.pistas_reveladas == 4:
            self.predecir_culpable()

    def predecir_culpable(self):
        entrada = [[
            encoders['sombrero'].transform([self.pistas['sombrero']])[0],
            encoders['gafas'].transform([self.pistas['gafas']])[0],
            encoders['altura'].transform([self.pistas['altura']])[0],
            encoders['ropa_negra'].transform([self.pistas['ropa_negra']])[0],
        ]]
        pred = model.predict(entrada)
        culpable = y_encoder.inverse_transform(pred)[0]

        messagebox.showinfo("🔍 Caso resuelto", f"El sistema cree que el culpable es:\n\n🎯 {culpable}")
        self.root.after(500, self.reiniciar_juego)

# Permite usar desde Main.py
def lanzar_minijuego(ventana_anterior=None):
    if ventana_anterior:
        ventana_anterior.destroy()
    root = tk.Tk()
    app = JuegoDetectives(root)
    root.mainloop()

# Permite ejecutar directamente
if __name__ == "__main__":
    lanzar_minijuego()
