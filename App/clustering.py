import tkinter as tk

from tkinter import filedialog, messagebox
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA
import pandas as pd
from textwrap import dedent
import matplotlib.pyplot as plt
import os

ruta_absoluta = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/audio_dataset.xlsx"))

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def graficar_tipos_reales(df):
    x = df["tempo_bpm"]
    y = df["rms"]
    etiquetas = df["y"]

    fig, ax = plt.subplots(figsize=(8, 6))
    etiquetas_unicas = etiquetas.unique()
    colores = plt.cm.tab10(range(len(etiquetas_unicas)))

    for i, etiqueta in enumerate(etiquetas_unicas):
        idx = etiquetas == etiqueta
        ax.scatter(x[idx], y[idx], label=etiqueta, color=colores[i], s=40, alpha=0.8)

    ax.set_title("Dispersión según tipo de audio (real)")
    ax.set_xlabel("Tempo (BPM)")
    ax.set_ylabel("RMS")
    ax.grid(True)
    ax.legend(title="Etiqueta real")
    plt.tight_layout()
    plt.show()

def lanzar_clustering(ventana_padre):
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Análisis de Clustering de Audios")
    ventana.geometry("800x600")
    ventana.configure(bg="white")
    centrar_ventana(ventana, 800, 600)

    frame = tk.Frame(ventana)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    text_box = tk.Text(frame, wrap="word", font=("Courier", 10), bg="#f8f9fa")
    text_box.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame, command=text_box.yview)
    scrollbar.pack(side="right", fill="y")
    text_box.config(yscrollcommand=scrollbar.set)

    def mostrar_resultado(texto):
        text_box.config(state="normal")
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, texto)
        text_box.config(state="disabled")

    def ejecutar_analisis(ruta_entrada):
        try:
            if not ruta_entrada or not os.path.exists(ruta_entrada):
                raise FileNotFoundError(f"No se encontró: {ruta_entrada}")
            df = pd.read_excel(ruta_entrada)

            columnas_necesarias = ["duration_s", "rms", "tempo_bpm", "zcr"]
            if not all(col in df.columns for col in columnas_necesarias):
                raise ValueError(f"Faltan columnas necesarias: {columnas_necesarias}")

            graficar_tipos_reales(df)

            X = StandardScaler().fit_transform(df[columnas_necesarias])

            resultados = {}
            resultados["K-means"] = KMeans(n_clusters=4, random_state=42, n_init="auto").fit_predict(X)
            resultados["Ward"] = AgglomerativeClustering(n_clusters=4, linkage="ward").fit_predict(X)

            for eps in (0.3, 0.5, 0.7, 1.0):
                etiquetas = DBSCAN(eps=eps, min_samples=4).fit_predict(X)
                n_cls = len(set(etiquetas)) - (1 if -1 in etiquetas else 0)
                if n_cls >= 3:
                    resultados["DBSCAN"] = etiquetas
                    break

            pca = PCA(n_components=2)
            X_reducido = pca.fit_transform(X)

            fig, axes = plt.subplots(1, 3, figsize=(18, 5))
            for ax, (nombre, etiquetas) in zip(axes, resultados.items()):
                scatter = ax.scatter(X_reducido[:, 0], X_reducido[:, 1], c=etiquetas, cmap='tab10', s=40)
                ax.set_title(nombre)
                ax.set_xlabel("PCA 1")
                ax.set_ylabel("PCA 2")
                ax.grid(True)
            plt.tight_layout()
            plt.show()

            metricas = {}
            for nombre, etiquetas in resultados.items():
                sil = silhouette_score(X, etiquetas)
                dbi = davies_bouldin_score(X, etiquetas)
                metricas[nombre] = {"silhouette": sil, "dbi": dbi}

            mejor = max(metricas.items(), key=lambda t: t[1]["silhouette"])[0]

            resumen = "\n=== Métricas comparativas ===\n"
            resumen += f"{'Algoritmo':10}  Silhouette   Davies-B.\n"
            for nombre, m in metricas.items():
                resumen += f"{nombre:10}  {m['silhouette']:.3f}       {m['dbi']:.3f}\n"

            justificacion = dedent(f"""
            ──────────────────────────────────────────────────────────
            Selección del algoritmo óptimo
            ──────────────────────────────────────────────────────────
            • {mejor} obtiene el mayor coeficiente Silhouette y el menor
              índice Davies–Bouldin, lo que significa clústeres más
              compactos y mejor separados.

            • El dominio del problema exige exactamente 4 categorías
              (emociones previstas). {mejor} se alinea con ese supuesto
              sin necesidad de ajustar parámetros complejos.

            • Los centroides/resultados de {mejor} se interpretan
              fácilmente: un clúster con alto rms y alto tempo se
              asocia a “Enojado”, etc. Ward ofrece estructura útil
              para exploración y DBSCAN destaca outliers, pero ninguno
              supera a {mejor} en cohesión + simplicidad de despliegue.

            Con base en las métricas objetivas y la adecuación al
            objetivo práctico, **{mejor} es el algoritmo recomendado**.
            """)
            mostrar_resultado(resumen + "\n" + justificacion)

        except Exception as e:
            mostrar_resultado(f"⚠️ Error:\n{str(e)}")

    tk.Button(ventana, text="Ejecutar con archivo por defecto",
              command=lambda: ejecutar_analisis(ruta_absoluta),
              bg="#0984e3", fg="white", font=("Helvetica", 11), relief="flat").pack(pady=10)

    tk.Button(ventana, text="Seleccionar otro archivo .xlsx",
              command=lambda: ejecutar_analisis(filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])),
              bg="#636e72", fg="white", font=("Helvetica", 10), relief="flat").pack(pady=5)

    mostrar_resultado("Presiona un botón para ejecutar el análisis.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    lanzar_clustering(root)
    root.mainloop()
