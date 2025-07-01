import tkinter as tk
from tkinter import filedialog, messagebox
import threading, io, sys, os, pandas as pd, numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from textwrap import dedent

# ----------- spaCy ----------------
try:
    import spacy
    try:
        nlp = spacy.load("es_core_news_md")
    except OSError:
        import spacy.cli
        spacy.cli.download("es_core_news_md")
        nlp = spacy.load("es_core_news_md")
except ImportError as e:
    raise SystemExit("Necesitas instalar spaCy:  pip install spacy\n" + str(e))

# ---------------- Logger GUI ----------------
class GuiLogger(io.StringIO):
    def __init__(self, widget): super().__init__(); self.w = widget
    def write(self, s):
        if s.strip(): self.w.after(0, self._append, s)
    def _append(self, s):
        self.w.config(state="normal"); self.w.insert(tk.END, s)
        self.w.see(tk.END); self.w.config(state="disabled")
    def flush(self): pass

# ---------------- Variables globales ----------------
selected = {"file": None}
clf = None
encoder = None

def log(m): print(m)

def vectorize(texts):
    return np.vstack([nlp(t).vector for t in texts])

def lanzar_transfer_learning(parent):
    global clf, encoder, entry, btn_pred

    root = tk.Toplevel(parent)
    root.title("Transfer Learning – spaCy Vectores (Español)")
    root.state("zoomed")

    btn_load = tk.Button(root, text="Cargar CSV/XLSX", bg="#0984e3", fg="white", font=("Helvetica", 12), relief="flat")
    btn_load.pack(pady=8)

    btn_train = tk.Button(root, text="Entrenar modelo", state="disabled", bg="#00b894", fg="white", font=("Helvetica", 12), relief="flat")
    btn_train.pack(pady=6)

    frame_pred = tk.Frame(root)
    entry = tk.Entry(frame_pred, font=("Helvetica", 11), width=70, state="disabled")
    entry.pack(side="left", padx=5)

    def predict_phrase():
        global clf, encoder
        phrase = entry.get().strip()
        if not phrase:
            return
        if clf is None:
            messagebox.showwarning("Aviso", "Entrena primero el modelo.")
            return
        vec = vectorize([phrase])
        proba = clf.predict_proba(vec)[0]
        pred_idx = int(np.argmax(proba))
        pred = encoder.inverse_transform([pred_idx])[0]
        conf = proba[pred_idx]
        log(f"➡️  «{phrase}»  →  {pred}  (confianza {conf:.2f})\n")

    btn_pred = tk.Button(frame_pred, text="Predecir etiqueta", state="disabled", font=("Helvetica", 11), command=predict_phrase)
    btn_pred.pack(side="left")
    frame_pred.pack(pady=8)

    scroll = tk.Scrollbar(root); scroll.pack(side="right", fill="y")
    log_box = tk.Text(root, wrap="word", font=("Courier", 10), bg="#f8f9fa")
    log_box.pack(fill="both", expand=True, padx=10, pady=10)
    scroll.config(command=log_box.yview); log_box.config(yscrollcommand=scroll.set)

    sys.stdout = sys.stderr = GuiLogger(log_box)

    def choose_file():
        path = filedialog.askopenfilename(filetypes=[("CSV/XLSX", "*.csv *.xlsx")])
        if path:
            selected["file"] = path
            log("📂 Archivo seleccionado: " + path + "\n")
            btn_train.config(state="normal")

    def train_model():
        global clf, encoder
        try:
            path = selected["file"]
            if not path:
                messagebox.showwarning("Aviso", "Primero carga un archivo CSV/XLSX")
                return
            log(f"📄 Leyendo {path}\n")
            df = pd.read_csv(path) if path.lower().endswith(".csv") else pd.read_excel(path)
            if df.shape[1] < 2:
                raise ValueError("Se requieren al menos dos columnas: texto y etiqueta.")
            if len(df) < 60:
                messagebox.showwarning("Advertencia", "Se recomiendan al menos 30 ejemplos por etiqueta para resultados fiables.")
            text_col, label_col = df.columns[:2]
            encoder = LabelEncoder().fit(df[label_col])
            y = encoder.transform(df[label_col])
            X_vec = vectorize(df[text_col].astype(str))

            rng = np.random.default_rng(42)
            idx = rng.permutation(len(y))
            split = int(0.8 * len(y))
            train_idx, test_idx = idx[:split], idx[split:]
            X_train, X_test, y_train, y_test = X_vec[train_idx], X_vec[test_idx], y[train_idx], y[test_idx]

            log("🔧 Entrenando LogisticRegression …\n")
            clf = LogisticRegression(max_iter=2000, n_jobs=-1).fit(X_train, y_train)
            acc = accuracy_score(y_test, clf.predict(X_test))
            log(f"✅ Exactitud test = {acc:.2f}\n")
            messagebox.showinfo("Terminó", f"Accuracy test: {acc:.2f}")
            entry.configure(state="normal"); btn_pred.configure(state="normal")
        except Exception as e:
            log(f"❌ Error: {e}\n")

    btn_load.config(command=choose_file)
    btn_train.config(command=lambda: threading.Thread(target=train_model, daemon=True).start())

    log_box.insert("1.0", dedent("""
        1. Pulsa «Cargar CSV/XLSX» y selecciona un archivo con columnas:
           texto, etiqueta (mín. recomendado: 30 ejemplos por clase).
        2. Pulsa «Entrenar modelo» (⚡ rápido gracias a vectores spaCy).
        3. Prueba frases en la caja inferior y observa la etiqueta + confianza.
    """))

# Si se ejecuta directamente
if __name__ == "__main__":
    lanzar_transfer_learning(tk.Tk())
    tk.mainloop()
