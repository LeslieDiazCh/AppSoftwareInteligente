import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import spacy
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

nlp = spacy.load("es_core_news_md")
modelo = None

def vectorizar(texto):
    return nlp(texto).vector

def entrenar_modelo(path):
    global modelo
    df = pd.read_csv(path)
    if 'frase' not in df.columns or 'emocion' not in df.columns:
        raise ValueError("El CSV debe tener columnas: frase, emocion")

    X = df['frase'].astype(str).apply(lambda x: vectorizar(x.strip().lower()))
    X = list(X)
    y = df['emocion']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return acc

def predecir_emocion(frase):
    global modelo
    if modelo is None:
        raise ValueError("El modelo aún no ha sido entrenado.")

    vec = vectorizar(frase.strip().lower()).reshape(1, -1)
    pred = modelo.predict(vec)[0]
    prob = max(modelo.predict_proba(vec)[0])
    return pred, prob

def lanzar_transfer_learning(ventana_padre):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Transfer Learning - spaCy Embeddings")
    ventana.geometry("600x400")
    ventana.resizable(False, False)

    selected_file = tk.StringVar()
    resultado_var = tk.StringVar()

    def cargar_csv():
        carpeta_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        path = filedialog.askopenfilename(
            initialdir=carpeta_data,
            filetypes=[("CSV Files", "*.csv")]
        )
        if path:
            selected_file.set(path)
            lbl_archivo.config(text=os.path.basename(path))
            resultado_var.set("")

    def entrenar():
        try:
            acc = entrenar_modelo(selected_file.get())
            messagebox.showinfo("Éxito", f"Modelo entrenado con {acc*100:.2f}% de exactitud")
            resultado_var.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def predecir():
        try:
            texto = entrada_texto.get()
            if not texto.strip():
                raise ValueError("Escribe una frase para predecir.")
            pred, prob = predecir_emocion(texto)
            resultado_var.set(f"Emoción: {pred} (confianza: {prob:.2f})")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            resultado_var.set("")

    # GUI
    tk.Label(ventana, text="Transfer Learning: spaCy Embeddings", font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Button(ventana, text="📂 Cargar dataset CSV", command=cargar_csv, bg="dodgerblue", fg="white").pack()
    lbl_archivo = tk.Label(ventana, text="(ningún archivo cargado)")
    lbl_archivo.pack(pady=5)
    tk.Button(ventana, text="⚙️ Entrenar modelo", command=entrenar, bg="mediumseagreen", fg="white").pack(pady=5)
    entrada_texto = tk.Entry(ventana, width=50, font=("Helvetica", 12))
    entrada_texto.pack(pady=10)
    tk.Button(ventana, text="🔍 Predecir emoción", command=predecir, bg="royalblue", fg="white").pack()
    tk.Label(ventana, textvariable=resultado_var, font=("Helvetica", 14), fg="black").pack(pady=20)
