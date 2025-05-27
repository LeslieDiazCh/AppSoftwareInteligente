import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import pandas as pd
from random import sample, randint, random, choice
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import threading
import time



def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    sw = ventana.winfo_screenwidth()
    sh = ventana.winfo_screenheight()
    x = int((sw / 2) - (ancho / 2))
    y = int((sh / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")



class AlgoritmoGenetico:
    def __init__(self):
        self.mapa_puntos = []
        self.x_coords = []
        self.y_coords = []
        self.ejecutando = False
        self.ventana = None
        self.progreso = None
        
    def crear_ventana(self, ventana_padre):
        """Crear la ventana del algoritmo genético"""
        self.ventana = tk.Toplevel(ventana_padre)
        centrar_ventana(self.ventana, 1200, 800)
        self.ventana.title("Algoritmo Genético - Problema del Viajero")
        self.ventana.geometry("1200x800")
        self.ventana.configure(bg="#f0f4f8")
        
        # Hacer que la ventana sea modal
        self.ventana.transient(ventana_padre)
        self.ventana.grab_set()
        
        self._crear_interfaz()
        
    def _crear_interfaz(self):
        """Crear la interfaz de usuario"""
        # Frame principal dividido en dos
        main_frame = tk.Frame(self.ventana, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel de control (izquierda)
        control_frame = tk.LabelFrame(main_frame, text="Panel de Control", 
                                    bg="#f0f4f8", fg="#0a3d62", font=("Helvetica", 12, "bold"))
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Panel de visualización (derecha)
        viz_frame = tk.LabelFrame(main_frame, text="Visualización", 
                                bg="#f0f4f8", fg="#0a3d62", font=("Helvetica", 12, "bold"))
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self._crear_panel_control(control_frame)
        self._crear_panel_visualizacion(viz_frame)
        
    def _crear_panel_control(self, parent):
        """Crear el panel de control"""
        # Sección de datos
        data_frame = tk.LabelFrame(parent, text="Datos", bg="#f0f4f8", fg="#34495e")
        data_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(data_frame, text="📁 Cargar desde archivo CSV", 
                 command=self.cargar_desde_csv,
                 bg="#74b9ff", fg="white", font=("Helvetica", 10),
                 cursor="hand2", relief="flat").pack(fill=tk.X, pady=2)
        
        tk.Button(data_frame, text="🎲 Usar datos de prueba", 
                 command=self.cargar_puntos_predefinidos,
                 bg="#00b894", fg="white", font=("Helvetica", 10),
                 cursor="hand2", relief="flat").pack(fill=tk.X, pady=2)
        
        tk.Button(data_frame, text="➕ Generar datos aleatorios", 
                 command=self.generar_datos_aleatorios,
                 bg="#fdcb6e", fg="white", font=("Helvetica", 10),
                 cursor="hand2", relief="flat").pack(fill=tk.X, pady=2)
        
        # Estado de los datos
        self.estado_datos = tk.StringVar()
        self.estado_datos.set("Sin datos cargados")
        tk.Label(data_frame, textvariable=self.estado_datos, 
                bg="#f0f4f8", fg="#636e72", font=("Helvetica", 9)).pack(pady=5)
        
        # Parámetros del algoritmo
        params_frame = tk.LabelFrame(parent, text="Parámetros del Algoritmo", 
                                   bg="#f0f4f8", fg="#34495e")
        params_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Tamaño de población
        tk.Label(params_frame, text="Tamaño de población:", bg="#f0f4f8").pack(anchor=tk.W)
        self.entry_cromosomas = tk.Scale(params_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                                       bg="#f0f4f8", highlightthickness=0)
        self.entry_cromosomas.set(50)
        self.entry_cromosomas.pack(fill=tk.X, padx=5)
        
        # Número de generaciones
        tk.Label(params_frame, text="Número de generaciones:", bg="#f0f4f8").pack(anchor=tk.W)
        self.entry_generaciones = tk.Scale(params_frame, from_=50, to=500, orient=tk.HORIZONTAL,
                                         bg="#f0f4f8", highlightthickness=0)
        self.entry_generaciones.set(100)
        self.entry_generaciones.pack(fill=tk.X, padx=5)
        
        # Tasa de mutación
        tk.Label(params_frame, text="Tasa de mutación (%):", bg="#f0f4f8").pack(anchor=tk.W)
        self.entry_mutacion = tk.Scale(params_frame, from_=1, to=50, orient=tk.HORIZONTAL,
                                     bg="#f0f4f8", highlightthickness=0)
        self.entry_mutacion.set(20)
        self.entry_mutacion.pack(fill=tk.X, padx=5)
        
        # Controles de ejecución
        control_exec_frame = tk.Frame(parent, bg="#f0f4f8")
        control_exec_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.btn_ejecutar = tk.Button(control_exec_frame, text="🚀 Ejecutar Algoritmo", 
                                    command=self.ejecutar_algoritmo,
                                    bg="#00b894", fg="white", font=("Helvetica", 11, "bold"),
                                    cursor="hand2", relief="flat", height=2)
        self.btn_ejecutar.pack(fill=tk.X, pady=2)
        
        self.btn_detener = tk.Button(control_exec_frame, text="⏹ Detener", 
                                   command=self.detener_algoritmo,
                                   bg="#d63031", fg="white", font=("Helvetica", 10),
                                   cursor="hand2", relief="flat", state=tk.DISABLED)
        self.btn_detener.pack(fill=tk.X, pady=2)
        
        # Barra de progreso
        self.progreso = ttk.Progressbar(control_exec_frame, mode='determinate')
        self.progreso.pack(fill=tk.X, pady=5)
        
        # Información del resultado
        resultado_frame = tk.LabelFrame(parent, text="Resultados", bg="#f0f4f8", fg="#34495e")
        resultado_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.label_resultado = tk.Label(resultado_frame, text="Ejecuta el algoritmo para ver resultados",
                                      bg="#f0f4f8", fg="#636e72", font=("Helvetica", 9), 
                                      wraplength=200, justify=tk.LEFT)
        self.label_resultado.pack(pady=5)
        
        # Botón volver
        tk.Button(parent, text="← Volver al Menú Principal", 
                 command=self.cerrar_ventana,
                 bg="#74b9ff", fg="white", font=("Helvetica", 10),
                 cursor="hand2", relief="flat").pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=10)
        
    def _crear_panel_visualizacion(self, parent):
        """Crear el panel de visualización"""
        # Crear figura de matplotlib
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 10))
        self.fig.suptitle("Algoritmo Genético - Problema del Viajero", fontsize=14, fontweight='bold')
        
        # Configurar subplot superior (mapa)
        self.ax1.set_title("Mejor Ruta Encontrada")
        self.ax1.set_xlabel("Coordenada X")
        self.ax1.set_ylabel("Coordenada Y")
        self.ax1.grid(True, alpha=0.3)
        
        # Configurar subplot inferior (evolución)
        self.ax2.set_title("Evolución de la Distancia")
        self.ax2.set_xlabel("Generación")
        self.ax2.set_ylabel("Distancia Total")
        self.ax2.grid(True, alpha=0.3)
        
        # Integrar matplotlib con tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def cargar_desde_csv(self):
        """Cargar puntos desde un archivo CSV"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                df = pd.read_csv(archivo)
                # Asumir que las columnas son 'x' e 'y' o las dos primeras columnas
                if 'x' in df.columns and 'y' in df.columns:
                    self.mapa_puntos = list(zip(df['x'], df['y']))
                else:
                    # Usar las dos primeras columnas numéricas
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) >= 2:
                        self.mapa_puntos = list(zip(df[numeric_cols[0]], df[numeric_cols[1]]))
                    else:
                        raise ValueError("No se encontraron suficientes columnas numéricas")
                
                self.x_coords, self.y_coords = zip(*self.mapa_puntos)
                self.estado_datos.set(f"✓ {len(self.mapa_puntos)} puntos cargados desde CSV")
                self._actualizar_mapa_inicial()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo:\n{str(e)}")
                
    def cargar_puntos_predefinidos(self):
        """Cargar puntos predefinidos para prueba"""
        puntos_fijos = [
            (12, 34), (20, 45), (40, 12), (32, 60), (50, 30),
            (10, 80), (70, 25), (15, 15), (65, 50), (25, 70),
            (80, 40), (35, 85), (90, 20), (5, 5), (75, 75)
        ]
        self.mapa_puntos = puntos_fijos
        self.x_coords, self.y_coords = zip(*self.mapa_puntos)
        self.estado_datos.set(f"✓ {len(self.mapa_puntos)} puntos de prueba cargados")
        self._actualizar_mapa_inicial()
        
    def generar_datos_aleatorios(self):
        """Generar datos aleatorios"""
        dialog = tk.Toplevel(self.ventana)
        dialog.title("Generar Datos Aleatorios")
        dialog.geometry("300x150")
        dialog.configure(bg="#f0f4f8")
        dialog.transient(self.ventana)
        dialog.grab_set()
        
        tk.Label(dialog, text="Número de ciudades:", bg="#f0f4f8").pack(pady=10)
        entry_num = tk.Entry(dialog)
        entry_num.insert(0, "20")
        entry_num.pack()
        
        def generar():
            try:
                num_ciudades = int(entry_num.get())
                if num_ciudades < 3:
                    messagebox.showerror("Error", "Mínimo 3 ciudades")
                    return
                    
                # Generar puntos aleatorios
                self.mapa_puntos = [(randint(0, 100), randint(0, 100)) for _ in range(num_ciudades)]
                self.x_coords, self.y_coords = zip(*self.mapa_puntos)
                self.estado_datos.set(f"✓ {len(self.mapa_puntos)} ciudades generadas aleatoriamente")
                self._actualizar_mapa_inicial()
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Ingresa un número válido")
                
        tk.Button(dialog, text="Generar", command=generar,
                 bg="#00b894", fg="white", cursor="hand2").pack(pady=10)
        
    def _actualizar_mapa_inicial(self):
        """Actualizar el mapa con los puntos cargados"""
        self.ax1.clear()
        self.ax1.scatter(self.x_coords, self.y_coords, c='red', s=50, alpha=0.7)
        self.ax1.set_title(f"Ciudades Cargadas ({len(self.mapa_puntos)} puntos)")
        self.ax1.set_xlabel("Coordenada X")
        self.ax1.set_ylabel("Coordenada Y")
        self.ax1.grid(True, alpha=0.3)
        
        # Numerar los puntos
        for i, (x, y) in enumerate(self.mapa_puntos):
            self.ax1.annotate(str(i), (x, y), xytext=(5, 5), textcoords='offset points')
            
        self.canvas.draw()
        
    def calcular_distancia_total(self, ruta):
        """Calcular la distancia total de una ruta"""
        if not ruta:
            return float('inf')
            
        distancia = 0
        for i in range(len(ruta)):
            ciudad_actual = ruta[i]
            ciudad_siguiente = ruta[(i + 1) % len(ruta)]  # Volver al inicio
            
            x1, y1 = self.mapa_puntos[ciudad_actual]
            x2, y2 = self.mapa_puntos[ciudad_siguiente]
            distancia += ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            
        return distancia
        
    def crear_individuo(self):
        """Crear un individuo (ruta) aleatoria"""
        ruta = list(range(len(self.mapa_puntos)))
        np.random.shuffle(ruta)
        return ruta
        
    def seleccion_torneo(self, poblacion, k=3):
        """Selección por torneo"""
        torneo = sample(poblacion, min(k, len(poblacion)))
        return min(torneo, key=lambda x: x[1])[0]
        
    def cruzamiento_ox(self, padre1, padre2):
        """Cruzamiento de orden (OX)"""
        start, end = sorted([randint(0, len(padre1) - 1) for _ in range(2)])
        
        hijo = [-1] * len(padre1)
        hijo[start:end + 1] = padre1[start:end + 1]
        
        # Completar con genes del padre2
        padre2_filtrado = [gen for gen in padre2 if gen not in hijo]
        j = 0
        for i in range(len(hijo)):
            if hijo[i] == -1:
                hijo[i] = padre2_filtrado[j]
                j += 1
                
        return hijo
        
    def mutacion_swap(self, individuo, tasa_mutacion):
        """Mutación por intercambio"""
        if random() < tasa_mutacion / 100:
            i, j = randint(0, len(individuo) - 1), randint(0, len(individuo) - 1)
            individuo[i], individuo[j] = individuo[j], individuo[i]
        return individuo
        
    def ejecutar_algoritmo(self):
        """Ejecutar el algoritmo genético en un hilo separado"""
        if not self.mapa_puntos:
            messagebox.showerror("Error", "Primero debes cargar los puntos.")
            return
            
        if self.ejecutando:
            return
            
        # Iniciar en un hilo separado para no bloquear la UI
        self.hilo_algoritmo = threading.Thread(target=self._algoritmo_genetico)
        self.hilo_algoritmo.daemon = True
        self.hilo_algoritmo.start()
        
    def _algoritmo_genetico(self):
        """Algoritmo genético principal"""
        self.ejecutando = True
        self.btn_ejecutar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        
        try:
            # Parámetros
            tam_poblacion = self.entry_cromosomas.get()
            generaciones = self.entry_generaciones.get()
            tasa_mutacion = self.entry_mutacion.get()
            
            # Inicializar población
            poblacion = []
            for _ in range(tam_poblacion):
                individuo = self.crear_individuo()
                fitness = self.calcular_distancia_total(individuo)
                poblacion.append((individuo, fitness))
                
            mejores_distancias = []
            mejor_global = min(poblacion, key=lambda x: x[1])
            
            # Configurar progreso
            self.progreso.config(maximum=generaciones)
            
            # Evolución
            for gen in range(generaciones):
                if not self.ejecutando:  # Verificar si se detuvo
                    break
                    
                nueva_poblacion = []
                
                # Elitismo: mantener los 2 mejores
                poblacion.sort(key=lambda x: x[1])
                nueva_poblacion.extend(poblacion[:2])
                
                # Generar nueva población
                while len(nueva_poblacion) < tam_poblacion and self.ejecutando:
                    # Selección
                    padre1 = self.seleccion_torneo(poblacion)
                    padre2 = self.seleccion_torneo(poblacion)
                    
                    # Cruzamiento
                    hijo = self.cruzamiento_ox(padre1, padre2)
                    
                    # Mutación
                    hijo = self.mutacion_swap(hijo, tasa_mutacion)
                    
                    # Evaluar fitness
                    fitness = self.calcular_distancia_total(hijo)
                    nueva_poblacion.append((hijo, fitness))
                    
                poblacion = nueva_poblacion
                
                # Actualizar mejor global
                mejor_actual = min(poblacion, key=lambda x: x[1])
                if mejor_actual[1] < mejor_global[1]:
                    mejor_global = mejor_actual
                    
                mejores_distancias.append(mejor_global[1])
                
                # Actualizar visualización cada 5 generaciones
                if gen % 5 == 0:
                    self.ventana.after(0, self._actualizar_visualizacion, 
                                     mejor_global, mejores_distancias, gen)
                    
                # Actualizar progreso
                self.ventana.after(0, lambda: self.progreso.config(value=gen + 1))
                
                time.sleep(0.01)  # Pequeña pausa para no saturar la CPU
                
            # Actualización final
            if self.ejecutando:
                self.ventana.after(0, self._algoritmo_terminado, mejor_global, mejores_distancias)
                
        except Exception as e:
            self.ventana.after(0, lambda: messagebox.showerror("Error", f"Error en el algoritmo:\n{str(e)}"))
        finally:
            self.ejecutando = False
            self.ventana.after(0, self._resetear_controles)
            
    def _actualizar_visualizacion(self, mejor_solucion, historial_distancias, generacion):
        """Actualizar la visualización durante la ejecución"""
        # Actualizar mapa con mejor ruta
        self.ax1.clear()
        
        mejor_ruta = mejor_solucion[0]
        ruta_coordenadas = [self.mapa_puntos[i] for i in mejor_ruta]
        ruta_coordenadas.append(self.mapa_puntos[mejor_ruta[0]])  # Cerrar el ciclo
        
        x_ruta, y_ruta = zip(*ruta_coordenadas)
        
        # Dibujar ruta
        self.ax1.plot(x_ruta, y_ruta, 'b-', linewidth=2, alpha=0.7)
        self.ax1.scatter(self.x_coords, self.y_coords, c='red', s=60, zorder=5)
        
        # Marcar ciudad inicial
        self.ax1.scatter(self.x_coords[mejor_ruta[0]], self.y_coords[mejor_ruta[0]], 
                        c='green', s=100, marker='s', zorder=6, label='Inicio')
        
        self.ax1.set_title(f"Gen {generacion}: Distancia = {mejor_solucion[1]:.2f}")
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # Actualizar gráfico de evolución
        self.ax2.clear()
        self.ax2.plot(historial_distancias, 'g-', linewidth=2)
        self.ax2.set_title("Evolución de la Mejor Distancia")
        self.ax2.set_xlabel("Generación")
        self.ax2.set_ylabel("Distancia")
        self.ax2.grid(True, alpha=0.3)
        
        self.canvas.draw()
        
    def _algoritmo_terminado(self, mejor_solucion, historial_distancias):
        """Acciones al terminar el algoritmo"""
        self._actualizar_visualizacion(mejor_solucion, historial_distancias, len(historial_distancias))
        
        # Mostrar resultados
        distancia_final = mejor_solucion[1]
        mejora = ((historial_distancias[0] - distancia_final) / historial_distancias[0]) * 100
        
        resultado_texto = f"""✅ Algoritmo completado exitosamente!

🎯 Mejor distancia: {distancia_final:.2f} unidades
📈 Mejora obtenida: {mejora:.1f}%
🔄 Generaciones: {len(historial_distancias)}
🏙️ Ciudades: {len(self.mapa_puntos)}"""
        
        self.label_resultado.config(text=resultado_texto)
        messagebox.showinfo("Algoritmo Completado", 
                          f"Mejor distancia encontrada: {distancia_final:.2f} unidades\n"
                          f"Mejora del {mejora:.1f}% respecto a la distancia inicial")
        
    def detener_algoritmo(self):
        """Detener la ejecución del algoritmo"""
        self.ejecutando = False
        
    def _resetear_controles(self):
        """Resetear el estado de los controles"""
        self.btn_ejecutar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
        self.progreso.config(value=0)
        
    def cerrar_ventana(self):
        """Cerrar la ventana del algoritmo genético"""
        if self.ejecutando:
            self.detener_algoritmo()
        self.ventana.destroy()


def lanzar_algoritmo_genetico(ventana_padre):
    """Función principal para lanzar el módulo del algoritmo genético"""
    ag = AlgoritmoGenetico()
    ag.crear_ventana(ventana_padre)