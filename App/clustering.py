import tkinter as tk
import os, io
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score

# Evita conflictos con Tkinter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from PIL import Image, ImageTk
from textwrap import dedent

# Ruta al archivo CSV
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "customers.csv"))

# Colores y etiquetas
COLORS = {0: "#ff5252", 1: "#2979ff", 2: "#ffd54f", -1: "#7f8c8d"}
LABELS = {
    0: "Ahorradores",
    1: "Grandes consumidores",
    2: "Premium prudentes",
    -1: "Ruido"
}

def _ordenar_por_ingreso(x_raw, y_lab):
    clusters = [k for k in np.unique(y_lab) if k != -1]
    medios = {k: x_raw[y_lab == k, 0].mean() for k in clusters}
    mapping = {k: rank for rank, k in enumerate(sorted(medios, key=medios.get))}
    return np.array([mapping.get(lbl, -1) for lbl in y_lab])

def lanzar_clustering(parent):
    if not os.path.exists(CSV_PATH):
        tk.messagebox.showerror("Error", f"No se encontró el archivo:\n{CSV_PATH}")
        return

    win = tk.Toplevel(parent)
    win.title("Segmentación de clientes – Ingreso vs Gasto")
    win.state("zoomed")

    # Widgets
    btn = tk.Button(win, text="Comparar algoritmos",
                    bg="#00b894", fg="white", font=("Helvetica", 12),
                    relief="flat")
    btn.pack(pady=12)

    lbl_fig = tk.Label(win, bg="white")
    lbl_fig.pack(pady=10)

    txt = tk.Text(win, wrap="word", font=("Courier", 10),
                  bg="#f8f9fa", height=8)
    txt.pack(fill="both", expand=True, padx=10, pady=10)
    txt.insert("1.0", "Pulsa el botón para generar la comparación.")
    txt.configure(state="disabled")

    def ejecutar():
        df = pd.read_csv(CSV_PATH)
        X_raw = df.iloc[:, :2].values
        X_scaled = StandardScaler().fit_transform(X_raw)

        modelos = {
            "K-Means": KMeans(n_clusters=3, random_state=0),
            "Ward": AgglomerativeClustering(n_clusters=3, linkage="ward"),
            "DBSCAN": DBSCAN(eps=0.3, min_samples=20)
        }

        resultados = {}
        for nombre, modelo in modelos.items():
            lab = modelo.fit_predict(X_scaled)
            lab = _ordenar_por_ingreso(X_raw, lab)
            resultados[nombre] = lab

        if len(set(resultados["DBSCAN"])) < 3:
            for eps in (0.35, 0.4, 0.45):
                lab = DBSCAN(eps=eps, min_samples=20).fit_predict(X_scaled)
                lab = _ordenar_por_ingreso(X_raw, lab)
                if len(set(lab)) >= 2:
                    resultados["DBSCAN"] = lab
                    break

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        for ax, (alg, lab) in zip(axes, resultados.items()):
            for k in np.unique(lab):
                idx = lab == k
                ax.scatter(X_raw[idx, 0], X_raw[idx, 1],
                           c=COLORS[k], s=22, edgecolors="k",
                           linewidths=0.25, label=LABELS[k])
            if len(set(lab)) > 1:
                sil = silhouette_score(X_scaled, lab)
                ax.set_title(f"{alg}  (Sil = {sil:.2f})", fontsize=10)
            else:
                ax.set_title(f"{alg}  (un solo clúster)", fontsize=10)
            ax.set_xlabel("Ingreso anual (USD)")
            ax.set_ylabel("Puntaje de gasto")
            ax.legend(fontsize=7, frameon=False)
            ax.grid(alpha=0.25)

        plt.suptitle("Clientes por ingreso vs gasto – comparación de algoritmos", fontsize=13)
        plt.tight_layout(rect=[0, 0.03, 1, 0.93])

        # Mostrar imagen
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img = Image.open(buf)
        max_w = int(win.winfo_screenwidth() * 0.9)
        if img.width > max_w:
            ratio = max_w / img.width
            img = img.resize((max_w, int(img.height * ratio)), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(img, master=win)

        def mostrar_imagen():
            lbl_fig.configure(image=photo)
            lbl_fig.image = photo  # 🔒 mantiene viva la imagen

        win.after(10, mostrar_imagen)  # ⏱ evita error pyimage

        explicacion = dedent("""
            Leyenda de colores:
                🔴 Ahorradores | 🔵 Grandes consumidores
                🟡 Premium prudentes | ❌ Ruido/atípicos

            • K-Means: parte los grupos por líneas rectas equidistantes.
            • Ward: curva los límites pero aún mezcla algo de ruido.
            • DBSCAN: detecta los núcleos densos completos y marca fuera
              de clúster a los compradores aislados.

            Para campañas segmentadas donde interesa mantener limpio cada
            grupo y detectar outliers, DBSCAN es la mejor opción.
        """)
        txt.configure(state="normal")
        txt.delete("1.0", tk.END)
        txt.insert(tk.END, explicacion)
        txt.configure(state="disabled")

    btn.configure(command=ejecutar)

    # Centrado dentro del padre
    parent.update_idletasks()
    w, h = parent.winfo_width(), parent.winfo_height()
    x = parent.winfo_rootx() + (w - win.winfo_reqwidth()) // 2
    y = parent.winfo_rooty() + (h - win.winfo_reqheight()) // 2
    win.geometry(f"+{x}+{y}")
