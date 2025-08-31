import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import math
import json
import os
from datetime import datetime

class RuletaTorneo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ruleta de Torneos - Dani666")
        self.root.geometry("800x650")
        self.root.configure(bg='#1a1a1a')
        
        # Variables
        self.participantes = []
        self.enfrentamientos = []
        self.nombre_torneo = ""
        self.fecha_creacion_torneo = None  # Fecha de creación del torneo
        self.max_participantes = 50
        self.rondas = []  # Lista de todas las rondas del torneo
        self.nombres_rondas = []  # Lista de nombres fijos para cada ronda
        self.ronda_actual = 0
        self.ganadores_ronda = []
        self.participante_libre = None
        

        
        # Variables para ventanas
        self.ventana_tabla = None
        self.ventana_vs = None
        self.ventana_historial = None
        
        # Variables para sistema de guardado
        self.carpeta_guardado = "torneos_guardados"
        self.archivo_historial = "historial_torneos.json"
        self.crear_carpeta_guardado()
        self.auto_guardado_activo = True
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz principal
        self.crear_interfaz_principal()
        
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores profesionales (Negro, Amarillo, Rojo, Verde)
        style.configure('Title.TLabel', 
                       background='#1a1a1a', 
                       foreground='#FFD700', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Custom.TButton',
                       background='#FFD700',
                       foreground='#1a1a1a',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Danger.TButton',
                       background='#DC143C',
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background='#228B22',
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Edit.TButton',
                       background='#FF8C00',
                       foreground='white',
                       font=('Arial', 8, 'bold'))

    def crear_interfaz_principal(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Banner Dani666
        banner_frame = tk.Frame(main_frame, bg='#1a1a1a', relief='solid', bd=2)
        banner_frame.pack(fill='x', pady=(0, 10))
        
        # Banner con gradiente simulado
        banner_top = tk.Frame(banner_frame, bg='#FFD700', height=5)
        banner_top.pack(fill='x')
        
        banner_content = tk.Frame(banner_frame, bg='#2a2a2a')
        banner_content.pack(fill='x', padx=2, pady=2)
        
        # Texto del banner
        banner_label = tk.Label(banner_content,
                              text="⚡ DANI666 - Dani Store ⚡",
                              bg='#2a2a2a',
                              fg='#FFD700',
                              font=('Arial', 16, 'bold'))
        banner_label.pack(pady=8)
        
        banner_subtitle = tk.Label(banner_content,
                                 text="¡El desafío está en marcha! Prepárate para enfrentarte a los mejores. Solo uno llegará a la cima.",
                                 bg='#2a2a2a',
                                 fg='#CCCCCC',
                                 font=('Arial', 10, 'italic'))
        banner_subtitle.pack(pady=(0, 8))
        
        banner_bottom = tk.Frame(banner_frame, bg='#DC143C', height=3)
        banner_bottom.pack(fill='x')
        
        # Título principal
        self.titulo_label = tk.Label(main_frame, 
                                   text="🎯 Ruleta de Torneos", 
                                   bg='#1a1a1a', 
                                   fg='#FFD700', 
                                   font=('Arial', 20, 'bold'))
        self.titulo_label.pack(pady=(10, 20))
        
        # Frame para configuración del torneo
        config_frame = tk.LabelFrame(main_frame, 
                                   text="⚙️ Configuración del Torneo", 
                                   bg='#2a2a2a', 
                                   fg='#FFD700',
                                   font=('Arial', 12, 'bold'))
        config_frame.pack(fill='x', pady=(0, 20))
        
        # Botón para configurar nombre del torneo
        ttk.Button(config_frame, 
                  text="📝 Configurar Nombre del Torneo",
                  command=self.configurar_nombre_torneo,
                  style='Custom.TButton').pack(pady=10)
        
        # Label para mostrar el nombre del torneo
        self.nombre_torneo_label = tk.Label(config_frame,
                                          text="Torneo sin nombre",
                                          bg='#2a2a2a',
                                          fg='#FFD700',
                                          font=('Arial', 12, 'bold'))
        self.nombre_torneo_label.pack(pady=(0, 10))
        
        # Frame para participantes
        participantes_frame = tk.LabelFrame(main_frame, 
                                          text="👥 Participantes", 
                                          bg='#2a2a2a', 
                                          fg='#FFD700',
                                          font=('Arial', 12, 'bold'))
        participantes_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Frame para entrada de participantes
        entrada_frame = tk.Frame(participantes_frame, bg='#2a2a2a')
        entrada_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(entrada_frame, 
                text="Nombre del participante:", 
                bg='#2a2a2a', 
                fg='#FFFFFF',
                font=('Arial', 10)).pack(side='left')
        
        self.entrada_participante = tk.Entry(entrada_frame, 
                                           font=('Arial', 10),
                                           width=30)
        self.entrada_participante.pack(side='left', padx=(10, 0))
        self.entrada_participante.bind('<Return>', lambda e: self.agregar_participante())
        
        ttk.Button(entrada_frame, 
                  text="➕ Agregar",
                  command=self.agregar_participante,
                  style='Success.TButton').pack(side='left', padx=(10, 0))
        
        # Lista de participantes
        lista_frame = tk.Frame(participantes_frame, bg='#2a2a2a')
        lista_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar para la lista
        scrollbar = tk.Scrollbar(lista_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.lista_participantes = tk.Listbox(lista_frame,
                                            yscrollcommand=scrollbar.set,
                                            font=('Arial', 10),
                                            bg='#1a1a1a',
                                            fg='#FFFFFF',
                                            selectbackground='#FFD700',
                                            selectforeground='#1a1a1a')
        self.lista_participantes.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.lista_participantes.yview)
        
        # Botones de control
        botones_frame = tk.Frame(participantes_frame, bg='#2a2a2a')
        botones_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(botones_frame, 
                  text="🗑️ Eliminar Seleccionado",
                  command=self.eliminar_participante,
                  style='Danger.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(botones_frame, 
                  text="🧹 Limpiar Todo",
                  command=self.limpiar_participantes,
                  style='Danger.TButton').pack(side='left', padx=(0, 10))
        
        # Contador de participantes
        self.contador_label = tk.Label(botones_frame,
                                     text="Participantes: 0/50",
                                     bg='#2a2a2a',
                                     fg='#FFD700',
                                     font=('Arial', 10, 'bold'))
        self.contador_label.pack(side='right')
        
        # Frame para acciones principales
        acciones_frame = tk.Frame(main_frame, bg='#2a2a2a', relief='solid', bd=1)
        acciones_frame.pack(fill='x', pady=10, padx=20)
        
        ttk.Button(acciones_frame, 
                  text="🎲 Generar Enfrentamientos",
                  command=self.generar_enfrentamientos,
                  style='Custom.TButton').pack(side='left', padx=10, pady=10)
        
        ttk.Button(acciones_frame, 
                  text="📋 Ver Lista de VS",
                  command=self.mostrar_lista_vs,
                  style='Custom.TButton').pack(side='left', padx=(0, 10), pady=10)
        
        ttk.Button(acciones_frame, 
                  text="🏆 Ir a Tabla del Torneo",
                  command=self.mostrar_tabla_torneo,
                  style='Success.TButton').pack(side='left', pady=10)
        
        # Botón de historial de torneos
        ttk.Button(acciones_frame, 
                  text="🕒 Historial",
                  command=self.mostrar_historial_torneos,
                  style='Custom.TButton').pack(side='right', padx=10, pady=10)

    def configurar_nombre_torneo(self):
        nombre = simpledialog.askstring("Nombre del Torneo", 
                                      "Ingresa el nombre del torneo:",
                                      initialvalue=self.nombre_torneo)
        if nombre:
            # Si es la primera vez que se configura el nombre, establecer fecha de creación
            if not self.nombre_torneo or self.fecha_creacion_torneo is None:
                self.fecha_creacion_torneo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.nombre_torneo = nombre
            self.nombre_torneo_label.config(text=f"🏆 {self.nombre_torneo}")
            self.titulo_label.config(text=f"🎯 Ruleta {self.nombre_torneo}")
            # Guardar automáticamente cuando se cambie el nombre
            self.guardar_torneo_automatico()

    def crear_carpeta_guardado(self):
        """Crear la carpeta para guardar torneos si no existe"""
        if not os.path.exists(self.carpeta_guardado):
            os.makedirs(self.carpeta_guardado)
        
        # Migrar torneos existentes al historial centralizado
        self.migrar_torneos_existentes()

    def migrar_torneos_existentes(self):
        """Migrar torneos existentes al sistema de historial centralizado"""
        try:
            ruta_historial = os.path.join(self.carpeta_guardado, self.archivo_historial)
            
            # Si ya existe el historial, no migrar
            if os.path.exists(ruta_historial):
                return
            
            historial = {}
            
            # Buscar archivos JSON existentes
            if os.path.exists(self.carpeta_guardado):
                for archivo in os.listdir(self.carpeta_guardado):
                    if archivo.endswith('.json') and archivo != self.archivo_historial:
                        ruta_completa = os.path.join(self.carpeta_guardado, archivo)
                        try:
                            with open(ruta_completa, 'r', encoding='utf-8') as f:
                                datos = json.load(f)
                            
                            # Crear ID único para el torneo
                            nombre_torneo = datos.get('nombre_torneo', 'Torneo Sin Nombre')
                            fecha_creacion = datos.get('fecha_creacion', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            torneo_id = f"{nombre_torneo}_{fecha_creacion}"
                            
                            # Agregar al historial
                            historial[torneo_id] = {
                                'nombre_torneo': nombre_torneo,
                                'fecha_creacion': fecha_creacion,
                                'fecha_ultima_actualizacion': datos.get('fecha_guardado', fecha_creacion),
                                'participantes': datos.get('participantes', []),
                                'rondas': datos.get('rondas', []),
                                'nombres_rondas': datos.get('nombres_rondas', []),
                                'participante_libre': datos.get('participante_libre', None),
                                'ronda_actual': datos.get('ronda_actual', 0),
                                'estado': 'En progreso' if datos.get('ronda_actual', 0) < len(datos.get('nombres_rondas', [])) else 'Finalizado',
                                'total_participantes': len(datos.get('participantes', [])),
                                'version': datos.get('version', '1.0')
                            }
                            
                            print(f"DEBUG: Migrado torneo: {nombre_torneo}")
                            
                        except Exception as e:
                            print(f"DEBUG: Error migrando archivo {archivo}: {e}")
                            continue
            
            # Guardar historial centralizado
            if historial:
                with open(ruta_historial, 'w', encoding='utf-8') as f:
                    json.dump(historial, f, ensure_ascii=False, indent=2)
                print(f"DEBUG: Migración completada. {len(historial)} torneos migrados al historial centralizado")
            
        except Exception as e:
            print(f"DEBUG: Error durante migración: {e}")

    def guardar_torneo_automatico(self):
        """Guardar automáticamente el estado actual del torneo"""
        if not self.auto_guardado_activo or not self.nombre_torneo:
            return
        
        try:
            # Mostrar indicador visual de guardado
            self.mostrar_indicador_guardado()
            
            # Establecer fecha de creación si no existe
            if self.fecha_creacion_torneo is None:
                self.fecha_creacion_torneo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Crear datos del torneo
            datos_torneo = {
                'nombre_torneo': self.nombre_torneo,
                'fecha_creacion': self.fecha_creacion_torneo,
                'participantes': self.participantes,
                'rondas': self.rondas,
                'nombres_rondas': self.nombres_rondas,
                'participante_libre': self.participante_libre,
                'ronda_actual': self.ronda_actual,
                'fecha_guardado': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'version': '1.0'
            }
            
            # Actualizar historial centralizado
            self.actualizar_historial_centralizado(datos_torneo)
            
            print(f"DEBUG: Torneo guardado automáticamente: {self.nombre_torneo}")
            
        except Exception as e:
            print(f"DEBUG: Error guardando torneo: {e}")

    def mostrar_indicador_guardado(self):
        """Mostrar un indicador visual temporal de que se está guardando"""
        try:
            # Crear un label temporal en la ventana principal
            if hasattr(self, 'root') and self.root.winfo_exists():
                indicador = tk.Label(self.root,
                                   text="💾 Guardado automático...",
                                   bg='#228B22',
                                   fg='white',
                                   font=('Arial', 9, 'bold'),
                                   relief='raised',
                                   bd=1)
                indicador.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
                
                # Remover el indicador después de 1.5 segundos
                self.root.after(1500, lambda: indicador.destroy() if indicador.winfo_exists() else None)
        except:
            # Si hay algún error con el indicador visual, no interrumpir el guardado
            pass

    def actualizar_historial_centralizado(self, datos_torneo):
        """Actualizar el historial centralizado de torneos"""
        try:
            ruta_historial = os.path.join(self.carpeta_guardado, self.archivo_historial)
            
            # Cargar historial existente o crear uno nuevo
            historial = self.cargar_historial_centralizado()
            
            # Crear ID único para el torneo basado en nombre y fecha de creación
            torneo_id = f"{datos_torneo['nombre_torneo']}_{datos_torneo['fecha_creacion']}"
            
            # Actualizar o agregar el torneo al historial
            historial[torneo_id] = {
                'nombre_torneo': datos_torneo['nombre_torneo'],
                'fecha_creacion': datos_torneo['fecha_creacion'],
                'fecha_ultima_actualizacion': datos_torneo['fecha_guardado'],
                'participantes': datos_torneo['participantes'],
                'rondas': datos_torneo['rondas'],
                'nombres_rondas': datos_torneo['nombres_rondas'],
                'participante_libre': datos_torneo['participante_libre'],
                'ronda_actual': datos_torneo['ronda_actual'],
                'estado': 'En progreso' if datos_torneo['ronda_actual'] < len(datos_torneo['nombres_rondas']) else 'Finalizado',
                'total_participantes': len(datos_torneo['participantes']),
                'version': datos_torneo['version']
            }
            
            # Guardar historial actualizado
            with open(ruta_historial, 'w', encoding='utf-8') as f:
                json.dump(historial, f, ensure_ascii=False, indent=2)
            
            print(f"DEBUG: Historial actualizado con torneo: {datos_torneo['nombre_torneo']}")
            
        except Exception as e:
            print(f"DEBUG: Error actualizando historial centralizado: {e}")

    def cargar_historial_centralizado(self):
        """Cargar el historial centralizado de torneos"""
        try:
            ruta_historial = os.path.join(self.carpeta_guardado, self.archivo_historial)
            
            if os.path.exists(ruta_historial):
                with open(ruta_historial, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
                
        except Exception as e:
            print(f"DEBUG: Error cargando historial centralizado: {e}")
            return {}

    def limpiar_nombre_archivo(self, nombre):
        """Limpiar nombre para usar como archivo"""
        caracteres_invalidos = '<>:"/\\|?*'
        nombre_limpio = nombre
        for char in caracteres_invalidos:
            nombre_limpio = nombre_limpio.replace(char, '_')
        return nombre_limpio[:30]  # Limitar longitud para dejar espacio a la fecha

    def crear_nombre_archivo_unico(self, nombre_torneo, fecha_creacion):
        """Crear nombre de archivo único combinando nombre y fecha de creación"""
        # Limpiar nombre del torneo
        nombre_limpio = self.limpiar_nombre_archivo(nombre_torneo)
        
        # Extraer solo fecha (sin hora) de la fecha de creación para el nombre del archivo
        try:
            fecha_obj = datetime.strptime(fecha_creacion, "%Y-%m-%d %H:%M:%S")
            fecha_corta = fecha_obj.strftime("%Y%m%d_%H%M")  # Formato: 20241215_1430
        except:
            # Si hay error, usar timestamp actual
            fecha_corta = datetime.now().strftime("%Y%m%d_%H%M")
        
        # Combinar nombre y fecha
        nombre_archivo = f"{nombre_limpio}_{fecha_corta}"
        return nombre_archivo

    def cargar_torneo_desde_historial(self, torneo_id):
        """Cargar un torneo desde el historial centralizado"""
        try:
            historial = self.cargar_historial_centralizado()
            
            if torneo_id not in historial:
                messagebox.showerror("Error", "Torneo no encontrado en el historial")
                return False
            
            datos = historial[torneo_id]
            
            # Restaurar datos
            self.nombre_torneo = datos.get('nombre_torneo', '')
            self.fecha_creacion_torneo = datos.get('fecha_creacion', None)
            self.participantes = datos.get('participantes', [])
            self.rondas = datos.get('rondas', [])
            self.nombres_rondas = datos.get('nombres_rondas', [])
            self.participante_libre = datos.get('participante_libre', None)
            self.ronda_actual = datos.get('ronda_actual', 0)
            
            # Actualizar interfaz
            self.actualizar_lista_participantes()
            self.nombre_torneo_label.config(text=f"🏆 {self.nombre_torneo}")
            self.titulo_label.config(text=f"🎯 Ruleta {self.nombre_torneo}")
            
            # Cerrar ventana de historial si está abierta
            if self.ventana_historial and self.ventana_historial.winfo_exists():
                self.ventana_historial.destroy()
                self.ventana_historial = None
            
            messagebox.showinfo("Éxito", f"Torneo '{self.nombre_torneo}' cargado exitosamente")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando torneo: {e}")
            return False

    def cargar_torneo(self, ruta_archivo):
        """Cargar un torneo desde archivo (mantenido para compatibilidad)"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Restaurar datos
            self.nombre_torneo = datos.get('nombre_torneo', '')
            self.participantes = datos.get('participantes', [])
            self.rondas = datos.get('rondas', [])
            self.nombres_rondas = datos.get('nombres_rondas', [])
            self.participante_libre = datos.get('participante_libre', None)
            self.ronda_actual = datos.get('ronda_actual', 0)
            
            # Actualizar interfaz
            self.actualizar_lista_participantes()
            self.nombre_torneo_label.config(text=f"🏆 {self.nombre_torneo}")
            self.titulo_label.config(text=f"🎯 Ruleta {self.nombre_torneo}")
            
            # Cerrar ventana de historial si está abierta
            if self.ventana_historial and self.ventana_historial.winfo_exists():
                self.ventana_historial.destroy()
                self.ventana_historial = None
            
            messagebox.showinfo("Éxito", f"Torneo '{self.nombre_torneo}' cargado exitosamente")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando torneo: {e}")
            return False

    def obtener_torneos_guardados(self):
        """Obtener lista de torneos guardados desde el historial centralizado"""
        torneos = []
        try:
            historial = self.cargar_historial_centralizado()
            
            for torneo_id, datos in historial.items():
                torneo_info = {
                    'id': torneo_id,
                    'nombre': datos.get('nombre_torneo', 'Sin nombre'),
                    'fecha_creacion': datos.get('fecha_creacion', 'Fecha desconocida'),
                    'fecha_actualizacion': datos.get('fecha_ultima_actualizacion', 'Fecha desconocida'),
                    'participantes': datos.get('total_participantes', 0),
                    'estado': datos.get('estado', 'Desconocido'),
                    'ronda_actual': datos.get('ronda_actual', 0),
                    'total_rondas': len(datos.get('nombres_rondas', [])),
                    'datos_completos': datos
                }
                torneos.append(torneo_info)
            
            # Ordenar por fecha de creación (más reciente primero)
            torneos.sort(key=lambda x: x['fecha_creacion'], reverse=True)
            return torneos
            
        except Exception as e:
            print(f"DEBUG: Error obteniendo torneos del historial: {e}")
            return []

    def mostrar_historial_torneos(self):
        """Mostrar ventana con historial de torneos guardados"""
        # Verificar si ya existe la ventana
        if self.ventana_historial and self.ventana_historial.winfo_exists():
            self.ventana_historial.lift()
            self.ventana_historial.focus()
            return
        
        # Crear ventana de historial
        self.ventana_historial = tk.Toplevel(self.root)
        self.ventana_historial.title("🕒 Historial de Torneos - Dani666")
        self.ventana_historial.geometry("700x500")
        self.ventana_historial.configure(bg='#1a1a1a')
        self.ventana_historial.transient(self.root)
        
        # Configurar evento de cierre
        self.ventana_historial.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_historial)
        
        # Banner superior
        banner_frame = tk.Frame(self.ventana_historial, bg='#FFD700', height=30)
        banner_frame.pack(fill='x')
        banner_frame.pack_propagate(False)
        
        tk.Label(banner_frame,
                text="🕒 HISTORIAL DE TORNEOS - DANI666",
                bg='#FFD700',
                fg='#1a1a1a',
                font=('Arial', 12, 'bold')).pack(expand=True)
        
        # Título principal
        titulo_frame = tk.Frame(self.ventana_historial, bg='#1a1a1a')
        titulo_frame.pack(fill='x', pady=20)
        
        tk.Label(titulo_frame,
                text="📋 Torneos Guardados",
                bg='#1a1a1a',
                fg='#FFD700',
                font=('Arial', 16, 'bold')).pack()
        
        # Frame para la lista con scroll
        lista_frame = tk.Frame(self.ventana_historial, bg='#2a2a2a', relief='solid', bd=2)
        lista_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Canvas y scrollbar para la lista
        canvas_historial = tk.Canvas(lista_frame, bg='#2a2a2a')
        scrollbar_historial = tk.Scrollbar(lista_frame, orient="vertical", command=canvas_historial.yview)
        scrollable_frame_historial = tk.Frame(canvas_historial, bg='#2a2a2a')
        
        scrollable_frame_historial.bind(
            "<Configure>",
            lambda e: canvas_historial.configure(scrollregion=canvas_historial.bbox("all"))
        )
        
        canvas_historial.create_window((0, 0), window=scrollable_frame_historial, anchor="nw")
        canvas_historial.configure(yscrollcommand=scrollbar_historial.set)
        
        # Obtener y mostrar torneos
        torneos = self.obtener_torneos_guardados()
        
        if not torneos:
            # No hay torneos guardados
            no_torneos_label = tk.Label(scrollable_frame_historial,
                                      text="📭 No hay torneos guardados\n\nCrea un torneo y se guardará automáticamente",
                                      bg='#2a2a2a',
                                      fg='#CCCCCC',
                                      font=('Arial', 12),
                                      justify='center')
            no_torneos_label.pack(expand=True, pady=50)
        else:
            # Mostrar cada torneo
            for i, torneo in enumerate(torneos):
                self.crear_widget_torneo(scrollable_frame_historial, torneo, i)
        
        # Empaquetar canvas y scrollbar
        canvas_historial.pack(side="left", fill="both", expand=True)
        scrollbar_historial.pack(side="right", fill="y")
        
        # Botones inferiores
        botones_frame = tk.Frame(self.ventana_historial, bg='#1a1a1a')
        botones_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        ttk.Button(botones_frame,
                  text="🔄 Actualizar Lista",
                  command=lambda: self.actualizar_lista_historial(),
                  style='Custom.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(botones_frame,
                  text="❌ Cerrar",
                  command=self.cerrar_ventana_historial,
                  style='Danger.TButton').pack(side='right')

    def crear_widget_torneo(self, parent, torneo, indice):
        """Crear widget para mostrar información de un torneo guardado"""
        # Frame principal del torneo
        torneo_frame = tk.Frame(parent, bg='#1a1a1a', relief='solid', bd=2)
        torneo_frame.pack(fill='x', padx=10, pady=5)
        
        # Frame interno con padding
        inner_frame = tk.Frame(torneo_frame, bg='#1a1a1a')
        inner_frame.pack(fill='x', padx=15, pady=10)
        
        # Información del torneo (lado izquierdo)
        info_frame = tk.Frame(inner_frame, bg='#1a1a1a')
        info_frame.pack(side='left', fill='x', expand=True)
        
        # Nombre del torneo
        nombre_label = tk.Label(info_frame,
                              text=f"🏆 {torneo['nombre']}",
                              bg='#1a1a1a',
                              fg='#FFD700',
                              font=('Arial', 14, 'bold'))
        nombre_label.pack(anchor='w')
        
        # Formatear fechas para mostrar
        try:
            fecha_creacion_obj = datetime.strptime(torneo['fecha_creacion'], "%Y-%m-%d %H:%M:%S")
            fecha_creacion_str = fecha_creacion_obj.strftime("%d/%m/%Y %H:%M")
        except:
            fecha_creacion_str = torneo['fecha_creacion']
        
        try:
            fecha_actualizacion_obj = datetime.strptime(torneo['fecha_actualizacion'], "%Y-%m-%d %H:%M:%S")
            fecha_actualizacion_str = fecha_actualizacion_obj.strftime("%d/%m/%Y %H:%M")
        except:
            fecha_actualizacion_str = torneo['fecha_actualizacion']
        
        # Información de fechas
        fecha_info = f"📅 Creado: {fecha_creacion_str}"
        if torneo['fecha_creacion'] != torneo['fecha_actualizacion']:
            fecha_info += f" | 🔄 Actualizado: {fecha_actualizacion_str}"
        
        fecha_label = tk.Label(info_frame,
                             text=fecha_info,
                             bg='#1a1a1a',
                             fg='#CCCCCC',
                             font=('Arial', 9))
        fecha_label.pack(anchor='w', pady=(2, 0))
        
        # Información del progreso
        progreso_info = f"👥 {torneo['participantes']} participantes | 🎯 Ronda {torneo['ronda_actual']}/{torneo['total_rondas']} | {torneo['estado']}"
        progreso_label = tk.Label(info_frame,
                                text=progreso_info,
                                bg='#1a1a1a',
                                fg='#90EE90' if torneo['estado'] == 'Finalizado' else '#FFA500',
                                font=('Arial', 10))
        progreso_label.pack(anchor='w', pady=(2, 0))
        
        # Botones (lado derecho)
        botones_frame = tk.Frame(inner_frame, bg='#1a1a1a')
        botones_frame.pack(side='right', padx=10)
        
        # Botón Abrir
        abrir_btn = tk.Button(botones_frame,
                            text="📂 Abrir",
                            bg='#228B22',
                            fg='white',
                            font=('Arial', 10, 'bold'),
                            relief='raised',
                            bd=2,
                            padx=15,
                            pady=5,
                            command=lambda: self.cargar_torneo_desde_historial(torneo['id']))
        abrir_btn.pack(side='top', pady=(0, 5))
        
        # Botón Eliminar
        eliminar_btn = tk.Button(botones_frame,
                               text="🗑️ Eliminar",
                               bg='#DC143C',
                               fg='white',
                               font=('Arial', 9),
                               relief='raised',
                               bd=2,
                               padx=10,
                               pady=3,
                               command=lambda: self.eliminar_torneo_del_historial(torneo['id'], torneo['nombre']))
        eliminar_btn.pack(side='top')

    def eliminar_torneo_del_historial(self, torneo_id, nombre_torneo):
        """Eliminar un torneo del historial centralizado"""
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar el torneo:\n\n'{nombre_torneo}'?\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                historial = self.cargar_historial_centralizado()
                
                if torneo_id in historial:
                    del historial[torneo_id]
                    
                    # Guardar historial actualizado
                    ruta_historial = os.path.join(self.carpeta_guardado, self.archivo_historial)
                    with open(ruta_historial, 'w', encoding='utf-8') as f:
                        json.dump(historial, f, ensure_ascii=False, indent=2)
                    
                    messagebox.showinfo("Éxito", f"Torneo '{nombre_torneo}' eliminado exitosamente del historial")
                    self.actualizar_lista_historial()
                else:
                    messagebox.showerror("Error", "Torneo no encontrado en el historial")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando torneo del historial: {e}")

    def eliminar_torneo(self, ruta_archivo, nombre_torneo):
        """Eliminar un torneo guardado (mantenido para compatibilidad)"""
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar el torneo:\n\n'{nombre_torneo}'?\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                os.remove(ruta_archivo)
                messagebox.showinfo("Éxito", f"Torneo '{nombre_torneo}' eliminado exitosamente")
                self.actualizar_lista_historial()
            except Exception as e:
                messagebox.showerror("Error", f"Error eliminando torneo: {e}")

    def actualizar_lista_historial(self):
        """Actualizar la lista de torneos en la ventana de historial"""
        if self.ventana_historial and self.ventana_historial.winfo_exists():
            self.ventana_historial.destroy()
            self.mostrar_historial_torneos()

    def cerrar_ventana_historial(self):
        """Cerrar la ventana de historial"""
        if self.ventana_historial:
            self.ventana_historial.destroy()
            self.ventana_historial = None

    def agregar_participante(self):
        nombre = self.entrada_participante.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Por favor ingresa un nombre")
            return
        
        if len(self.participantes) >= self.max_participantes:
            messagebox.showwarning("Límite alcanzado", 
                                 f"Máximo {self.max_participantes} participantes permitidos")
            return
        
        if nombre in self.participantes:
            messagebox.showwarning("Duplicado", "Este participante ya está en la lista")
            return
        
        self.participantes.append(nombre)
        self.actualizar_lista_participantes()
        self.entrada_participante.delete(0, tk.END)
        self.entrada_participante.focus()
        
        # Guardar automáticamente después de agregar participante
        self.guardar_torneo_automatico()

    def eliminar_participante(self):
        seleccion = self.lista_participantes.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un participante para eliminar")
            return
        
        indice = seleccion[0]
        del self.participantes[indice]
        self.actualizar_lista_participantes()

    def limpiar_participantes(self):
        if self.participantes:
            if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar todos los participantes?"):
                self.participantes.clear()
                self.enfrentamientos.clear()
                self.actualizar_lista_participantes()

    def actualizar_lista_participantes(self):
        self.lista_participantes.delete(0, tk.END)
        for i, participante in enumerate(self.participantes, 1):
            self.lista_participantes.insert(tk.END, f"{i}. {participante}")
        
        self.contador_label.config(text=f"Participantes: {len(self.participantes)}/{self.max_participantes}")

    def generar_enfrentamientos(self):
        if len(self.participantes) < 2:
            messagebox.showwarning("Advertencia", "Se necesitan al menos 2 participantes")
            return
        
        # Reiniciar torneo
        self.rondas.clear()
        self.nombres_rondas.clear()  # Limpiar nombres fijos de rondas
        self.ronda_actual = 0
        self.ganadores_ronda.clear()
        self.participante_libre = None
        
        # Mezclar participantes aleatoriamente
        participantes_mezclados = self.participantes.copy()
        random.shuffle(participantes_mezclados)
        
        # Si hay número impar, uno queda libre
        if len(participantes_mezclados) % 2 == 1:
            self.participante_libre = participantes_mezclados.pop()
            messagebox.showinfo("Participante Libre", f"🎯 {self.participante_libre} pasa automáticamente a la siguiente ronda")
        
        # Crear enfrentamientos de la primera ronda
        primera_ronda = []
        for i in range(0, len(participantes_mezclados), 2):
            enfrentamiento = {
                'participante1': participantes_mezclados[i],
                'participante2': participantes_mezclados[i + 1],
                'ganador': None,
                'completado': False,
                'victorias_p1': 0,
                'victorias_p2': 0
            }
            primera_ronda.append(enfrentamiento)
        
        self.rondas.append(primera_ronda)
        self.enfrentamientos = primera_ronda  # Para compatibilidad
        
        messagebox.showinfo("¡Éxito!", 
                          f"Se generó la primera ronda con {len(primera_ronda)} enfrentamientos")
        
        # Guardar automáticamente después de generar enfrentamientos
        self.guardar_torneo_automatico()

    def mostrar_lista_vs(self):
        if not self.rondas:
            messagebox.showwarning("Advertencia", "Primero genera los enfrentamientos")
            return
        
        # Verificar si ya existe la ventana y está abierta
        if self.ventana_vs and self.ventana_vs.winfo_exists():
            self.ventana_vs.lift()  # Traer al frente
            self.ventana_vs.focus()
            return
        
        # Crear ventana para mostrar VS
        self.ventana_vs = tk.Toplevel(self.root)
        self.ventana_vs.title(f"Lista de VS - {self.nombre_torneo or 'Torneo'}")
        self.ventana_vs.geometry("700x600")
        self.ventana_vs.configure(bg='#2c3e50')
        
        # Configurar evento de cierre
        self.ventana_vs.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_vs)
        
        # Título
        titulo = tk.Label(self.ventana_vs,
                         text=f"📋 Lista de VS del {self.nombre_torneo or 'Torneo'}",
                         bg='#2c3e50',
                         fg='#ecf0f1',
                         font=('Arial', 16, 'bold'))
        titulo.pack(pady=20)
        
        # Frame para la lista con scroll
        frame_lista = tk.Frame(self.ventana_vs, bg='#34495e')
        frame_lista.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Canvas y scrollbar
        canvas = tk.Canvas(frame_lista, bg='#34495e')
        scrollbar_vs = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#34495e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_vs.set)
        
        # Mostrar todas las rondas
        for ronda_num, ronda in enumerate(self.rondas):
            nombre_ronda = self.obtener_nombre_ronda(ronda_num, len(ronda))
            
            # Título de la ronda
            titulo_ronda = tk.Label(scrollable_frame,
                                  text=f"🏆 {nombre_ronda}",
                                  bg='#34495e',
                                  fg='#f39c12',
                                  font=('Arial', 14, 'bold'))
            titulo_ronda.pack(pady=(20, 10))
            
            # Enfrentamientos de la ronda
            for i, enfrentamiento in enumerate(ronda, 1):
                estado = "✅ Completado" if enfrentamiento['completado'] else "⏳ Pendiente"
                ganador_text = f" - Ganador: {enfrentamiento['ganador']}" if enfrentamiento['ganador'] else ""
                
                texto = f"🥊 {i}. {enfrentamiento['participante1']} VS {enfrentamiento['participante2']} {estado}{ganador_text}"
                
                label_vs = tk.Label(scrollable_frame,
                                  text=texto,
                                  bg='#34495e',
                                  fg='#ecf0f1',
                                  font=('Arial', 10),
                                  wraplength=600,
                                  justify='left')
                label_vs.pack(pady=2, padx=10, anchor='w')
        
        # Mostrar participante libre si existe
        if self.participante_libre:
            libre_label = tk.Label(scrollable_frame,
                                 text=f"🎯 Participante Libre: {self.participante_libre}",
                                 bg='#34495e',
                                 fg='#e74c3c',
                                 font=('Arial', 12, 'bold'))
            libre_label.pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_vs.pack(side="right", fill="y")
        
        # Botón para ir a tabla
        ttk.Button(self.ventana_vs,
                  text="🏆 Ir a Tabla del Torneo",
                  command=self.mostrar_tabla_torneo,
                  style='Success.TButton').pack(pady=10)

    def mostrar_tabla_torneo(self):
        if not self.rondas:
            messagebox.showwarning("Advertencia", "Primero genera los enfrentamientos")
            return
        
        # Verificar si ya existe la ventana y está abierta
        if self.ventana_tabla and self.ventana_tabla.winfo_exists():
            self.ventana_tabla.lift()  # Traer al frente
            self.ventana_tabla.focus()
            self.actualizar_tabla_torneo()  # Actualizar contenido
            return
        
        # Crear ventana de tabla de torneo
        self.ventana_tabla = tk.Toplevel(self.root)
        self.ventana_tabla.title(f"Tabla del Torneo - {self.nombre_torneo or 'Torneo'} | Dani666")
        self.ventana_tabla.geometry("1000x800")
        self.ventana_tabla.configure(bg='#1a1a1a')
        
        # Configurar evento de cierre
        self.ventana_tabla.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_tabla)
        
        # Banner en la ventana de tabla
        banner_tabla = tk.Frame(self.ventana_tabla, bg='#FFD700', height=30)
        banner_tabla.pack(fill='x')
        banner_tabla.pack_propagate(False)
        
        tk.Label(banner_tabla,
                text="⚡ DANI666 - Dani Store ⚡",
                bg='#FFD700',
                fg='#1a1a1a',
                font=('Arial', 12, 'bold')).pack(expand=True)
        
        # Título principal
        titulo_principal = tk.Label(self.ventana_tabla,
                                  text="🏆 Tabla de Participantes",
                                  bg='#1a1a1a',
                                  fg='#FFD700',
                                  font=('Arial', 20, 'bold'))
        titulo_principal.pack(pady=20)
        
        # Frame para botones de control
        control_frame = tk.Frame(self.ventana_tabla, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=30, pady=(0, 10))
        
        ttk.Button(control_frame,
                  text="🔄 Actualizar Tabla",
                  command=self.actualizar_tabla_torneo,
                  style='Custom.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(control_frame,
                  text="➡️ Generar Siguiente Ronda",
                  command=self.generar_siguiente_ronda,
                  style='Success.TButton').pack(side='left')
        
        # Frame principal para la tabla con scroll
        self.frame_tabla = tk.Frame(self.ventana_tabla, bg='#2a2a2a', relief='raised', bd=2)
        self.frame_tabla.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Crear tabla estilo torneo de karate
        self.crear_tabla_torneo_completa()

    def crear_tabla_torneo_completa(self):
        # Limpiar frame anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()
        
        # Canvas para scroll
        self.canvas_tabla = tk.Canvas(self.frame_tabla, bg='#2a2a2a')
        scrollbar_tabla = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.canvas_tabla.yview)
        scrollable_frame = tk.Frame(self.canvas_tabla, bg='#2a2a2a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_tabla.configure(scrollregion=self.canvas_tabla.bbox("all"))
        )
        
        self.canvas_tabla.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas_tabla.configure(yscrollcommand=scrollbar_tabla.set)
        
        # Habilitar scroll con ruedita del mouse
        def _on_mousewheel(event):
            self.canvas_tabla.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas_tabla.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas_tabla.unbind_all("<MouseWheel>")
        
        # Vincular eventos de mouse para scroll
        self.canvas_tabla.bind('<Enter>', _bind_to_mousewheel)
        self.canvas_tabla.bind('<Leave>', _unbind_from_mousewheel)
        
        # Mostrar todas las rondas
        for ronda_num, ronda in enumerate(self.rondas):
            nombre_ronda = self.obtener_nombre_ronda(ronda_num, len(ronda))
            
            # Título de la ronda
            titulo_ronda = tk.Label(scrollable_frame,
                                  text=f"🥋 {nombre_ronda.upper()} - {len(ronda)} Enfrentamientos",
                                  bg='#2a2a2a',
                                  fg='#DC143C',
                                  font=('Arial', 14, 'bold'))
            titulo_ronda.pack(pady=(20, 10))
            
            # Crear enfrentamientos de la ronda
            for i, enfrentamiento in enumerate(ronda):
                self.crear_enfrentamiento_widget(scrollable_frame, enfrentamiento, i, ronda_num)
        
        # Mostrar participante libre si existe
        if self.participante_libre:
            libre_frame = tk.Frame(scrollable_frame, bg='#FFD700', relief='solid', bd=2)
            libre_frame.pack(fill='x', padx=20, pady=10)
            
            # Frame interno para el participante libre con botón de edición
            libre_inner_frame = tk.Frame(libre_frame, bg='#FFD700')
            libre_inner_frame.pack(fill='x', padx=10, pady=10)
            
            libre_label = tk.Label(libre_inner_frame,
                                 text=f"🎯 PARTICIPANTE LIBRE: {self.participante_libre}",
                                 bg='#FFD700',
                                 fg='#1a1a1a',
                                 font=('Arial', 12, 'bold'))
            libre_label.pack(side='left', fill='x', expand=True)
            
            # Botón de edición para participante libre
            edit_libre_btn = tk.Button(libre_inner_frame,
                                     text="✏️ Editar",
                                     bg='#FF8C00',
                                     fg='white',
                                     font=('Arial', 10, 'bold'),
                                     relief='flat',
                                     command=self.editar_participante_libre)
            edit_libre_btn.pack(side='right', padx=10)
        
        # Información del torneo
        self.crear_info_torneo(scrollable_frame)
        
        # Empaquetar canvas y scrollbar
        self.canvas_tabla.pack(side="left", fill="both", expand=True)
        scrollbar_tabla.pack(side="right", fill="y")

    def crear_enfrentamiento_widget(self, parent, enfrentamiento, indice, ronda_num):
        # Frame principal del enfrentamiento
        enfrentamiento_frame = tk.Frame(parent, bg='#1a1a1a', relief='solid', bd=2)
        enfrentamiento_frame.pack(fill='x', padx=20, pady=5)
        
        # Número del enfrentamiento
        num_label = tk.Label(enfrentamiento_frame,
                           text=f"#{indice + 1}",
                           bg='#DC143C',
                           fg='white',
                           font=('Arial', 12, 'bold'),
                           width=4)
        num_label.pack(side='left', padx=5, pady=5)
        
        # Frame para participantes
        participantes_frame = tk.Frame(enfrentamiento_frame, bg='#1a1a1a')
        participantes_frame.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        
        # Participante 1 con botón de edición y victorias
        p1_container = tk.Frame(participantes_frame, bg='#1a1a1a')
        p1_container.pack(side='left', fill='x', expand=True, padx=2)
        
        p1_color = '#FFD700' if enfrentamiento['ganador'] == enfrentamiento['participante1'] else '#1E90FF'
        p1_frame = tk.Frame(p1_container, bg=p1_color, relief='raised', bd=1)
        p1_frame.pack(fill='x')
        
        # Frame interno para botón y edición
        p1_inner_frame = tk.Frame(p1_frame, bg=p1_color)
        p1_inner_frame.pack(fill='x', padx=2, pady=2)
        
        # Color del texto según si es ganador o no
        p1_text_color = '#1a1a1a' if enfrentamiento['ganador'] == enfrentamiento['participante1'] else 'white'
        
        p1_button = tk.Button(p1_inner_frame,
                            text=enfrentamiento['participante1'],
                            bg=p1_color,
                            fg=p1_text_color,
                            font=('Arial', 10, 'bold'),
                            relief='flat',
                            command=lambda: self.seleccionar_ganador_directo(ronda_num, indice, enfrentamiento['participante1']))
        p1_button.pack(side='top', fill='x', pady=2)
        
        # Frame para victorias y edición
        p1_controls_frame = tk.Frame(p1_inner_frame, bg=p1_color)
        p1_controls_frame.pack(fill='x', pady=2)
        
        # Casilla de victorias para participante 1
        tk.Label(p1_controls_frame, text="Victorias:", bg=p1_color, fg=p1_text_color, font=('Arial', 8)).pack(side='left')
        
        p1_victorias_var = tk.StringVar(value=str(enfrentamiento.get('victorias_p1', 0)))
        p1_victorias_entry = tk.Entry(p1_controls_frame, 
                                    textvariable=p1_victorias_var,
                                    width=4, 
                                    font=('Arial', 9),
                                    justify='center')
        p1_victorias_entry.pack(side='left', padx=2)
        # Actualizar datos inmediatamente cuando se escriba (pero sin actualizar la tabla)
        p1_victorias_entry.bind('<KeyRelease>', 
                              lambda e: self.actualizar_victorias_silencioso(ronda_num, indice, 'victorias_p1', p1_victorias_var.get()))
        p1_victorias_entry.bind('<FocusOut>', 
                              lambda e: self.actualizar_victorias_silencioso(ronda_num, indice, 'victorias_p1', p1_victorias_var.get()))
        p1_victorias_entry.bind('<Return>', 
                              lambda e: self.actualizar_victorias_silencioso(ronda_num, indice, 'victorias_p1', p1_victorias_var.get()))
        
        # Botón de edición para participante 1
        edit_p1_btn = tk.Button(p1_controls_frame,
                              text="✏️",
                              bg='#f39c12',
                              fg='white',
                              font=('Arial', 7, 'bold'),
                              relief='flat',
                              width=2,
                              command=lambda: self.editar_participante(ronda_num, indice, 'participante1'))
        edit_p1_btn.pack(side='right', padx=2)
        
        # VS
        vs_label = tk.Label(participantes_frame,
                          text="⚔️\nVS",
                          bg='#1a1a1a',
                          fg='#FFD700',
                          font=('Arial', 9, 'bold'))
        vs_label.pack(side='left', padx=5)
        
        # Participante 2 con botón de edición y victorias
        p2_container = tk.Frame(participantes_frame, bg='#1a1a1a')
        p2_container.pack(side='right', fill='x', expand=True, padx=2)
        
        p2_color = '#FFD700' if enfrentamiento['ganador'] == enfrentamiento['participante2'] else '#DC143C'
        p2_frame = tk.Frame(p2_container, bg=p2_color, relief='raised', bd=1)
        p2_frame.pack(fill='x')
        
        # Frame interno para botón y edición
        p2_inner_frame = tk.Frame(p2_frame, bg=p2_color)
        p2_inner_frame.pack(fill='x', padx=2, pady=2)
        
        # Color del texto según si es ganador o no
        p2_text_color = '#1a1a1a' if enfrentamiento['ganador'] == enfrentamiento['participante2'] else 'white'
        
        p2_button = tk.Button(p2_inner_frame,
                            text=enfrentamiento['participante2'],
                            bg=p2_color,
                            fg=p2_text_color,
                            font=('Arial', 10, 'bold'),
                            relief='flat',
                            command=lambda: self.seleccionar_ganador_directo(ronda_num, indice, enfrentamiento['participante2']))
        p2_button.pack(side='top', fill='x', pady=2)
        
        # Frame para victorias y edición
        p2_controls_frame = tk.Frame(p2_inner_frame, bg=p2_color)
        p2_controls_frame.pack(fill='x', pady=2)
        
        # Casilla de victorias para participante 2
        tk.Label(p2_controls_frame, text="Victorias:", bg=p2_color, fg=p2_text_color, font=('Arial', 8)).pack(side='left')
        
        p2_victorias_var = tk.StringVar(value=str(enfrentamiento.get('victorias_p2', 0)))
        p2_victorias_entry = tk.Entry(p2_controls_frame, 
                                    textvariable=p2_victorias_var,
                                    width=4, 
                                    font=('Arial', 9),
                                    justify='center')
        p2_victorias_entry.pack(side='left', padx=2)
        # Actualizar datos inmediatamente cuando se escriba (pero sin actualizar la tabla)
        p2_victorias_entry.bind('<KeyRelease>', 
                              lambda e: self.actualizar_victorias_silencioso(ronda_num, indice, 'victorias_p2', p2_victorias_var.get()))
        p2_victorias_entry.bind('<FocusOut>', 
                              lambda e: self.actualizar_victorias_silencioso(ronda_num, indice, 'victorias_p2', p2_victorias_var.get()))
        p2_victorias_entry.bind('<Return>', 
                              lambda e: self.actualizar_victorias_silencioso(ronda_num, indice, 'victorias_p2', p2_victorias_var.get()))
        
        # Botón de edición para participante 2
        edit_p2_btn = tk.Button(p2_controls_frame,
                              text="✏️",
                              bg='#f39c12',
                              fg='white',
                              font=('Arial', 7, 'bold'),
                              relief='flat',
                              width=2,
                              command=lambda: self.editar_participante(ronda_num, indice, 'participante2'))
        edit_p2_btn.pack(side='right', padx=2)
        
        # Estado del enfrentamiento
        estado_frame = tk.Frame(enfrentamiento_frame, bg='#1a1a1a')
        estado_frame.pack(side='right', padx=5, pady=5)
        
        if enfrentamiento['completado']:
            v1 = enfrentamiento.get('victorias_p1', 0)
            v2 = enfrentamiento.get('victorias_p2', 0)
            estado_text = f"✅\nGanador:\n{enfrentamiento['ganador']}\n({v1} - {v2})"
            estado_color = '#228B22'
        else:
            v1 = enfrentamiento.get('victorias_p1', 0)
            v2 = enfrentamiento.get('victorias_p2', 0)
            estado_text = f"⏳\nPendiente\n({v1} - {v2})"
            estado_color = '#FF8C00'
        
        estado_label = tk.Label(estado_frame,
                              text=estado_text,
                              bg=estado_color,
                              fg='white',
                              font=('Arial', 8, 'bold'),
                              width=12)
        estado_label.pack()
        
        # Botón para determinar ganador automáticamente
        if not enfrentamiento['completado']:
            auto_ganador_btn = tk.Button(estado_frame,
                                       text="🏆 Auto",
                                       bg='#FFD700',
                                       fg='#1a1a1a',
                                       font=('Arial', 7, 'bold'),
                                       relief='flat',
                                       command=lambda: self.seleccionar_ganador_por_victorias(ronda_num, indice))
            auto_ganador_btn.pack(pady=2)

    def seleccionar_ganador(self, ronda_num, enfrentamiento_indice, ganador):
        # Obtener el enfrentamiento actual para verificar que el ganador sea válido
        enfrentamiento = self.rondas[ronda_num][enfrentamiento_indice]
        
        # Verificar que el ganador sea uno de los participantes del enfrentamiento
        if ganador not in [enfrentamiento['participante1'], enfrentamiento['participante2']]:
            # Si el nombre no coincide exactamente, buscar por el nombre actualizado
            if ganador == enfrentamiento['participante1']:
                ganador = enfrentamiento['participante1']
            elif ganador == enfrentamiento['participante2']:
                ganador = enfrentamiento['participante2']
        
        # Actualizar el enfrentamiento
        self.rondas[ronda_num][enfrentamiento_indice]['ganador'] = ganador
        self.rondas[ronda_num][enfrentamiento_indice]['completado'] = True
        
        # Actualizar la tabla solo cuando se selecciona un ganador
        self.actualizar_tabla_torneo()
        
        # Actualizar la ventana de VS si está abierta
        if self.ventana_vs and self.ventana_vs.winfo_exists():
            self.actualizar_ventana_vs()
        
        # Verificar si la ronda está completa
        ronda_completa = all(e['completado'] for e in self.rondas[ronda_num])
        
        if ronda_completa:
            # Verificar si es realmente la final (sin participante libre y solo 1 enfrentamiento)
            nombre_ronda = self.obtener_nombre_ronda(ronda_num, len(self.rondas[ronda_num]))
            
            # Es la final REAL solo si:
            # 1. Solo hay 1 enfrentamiento en esta ronda
            # 2. NO hay participante libre
            es_final_real = (len(self.rondas[ronda_num]) == 1 and self.participante_libre is None)
            
            if es_final_real:
                # ¡Es la final real! Mostrar celebración del campeón
                self.mostrar_celebracion_campeon(ganador)
            else:
                # Ronda normal completada - NO mostrar mensaje para no interrumpir
                # El usuario puede ver el estado en la tabla y generar la siguiente ronda cuando quiera
                print(f"DEBUG: {nombre_ronda} completada. Listo para generar siguiente ronda.")
        
        # Guardar automáticamente después de seleccionar ganador
        self.guardar_torneo_automatico()

    def generar_siguiente_ronda(self):
        if not self.rondas:
            messagebox.showwarning("Advertencia", "No hay rondas generadas")
            return
        
        # Verificar que la ronda actual esté completa
        ronda_actual = self.rondas[-1]
        if not all(e['completado'] for e in ronda_actual):
            messagebox.showwarning("Advertencia", "Completa todos los enfrentamientos de la ronda actual")
            return
        
        # Obtener ganadores de la ronda actual
        ganadores = [e['ganador'] for e in ronda_actual]
        
        # Verificar si hay suficientes participantes para continuar
        # IMPORTANTE: No agregar el participante libre a ganadores aún para el conteo
        total_participantes = len(ganadores) + (1 if self.participante_libre else 0)
        
        print(f"DEBUG: Ganadores: {ganadores}")
        print(f"DEBUG: Participante libre: {self.participante_libre}")
        print(f"DEBUG: Total participantes: {total_participantes}")
        
        if total_participantes < 2:
            # ¡Tenemos un campeón! (esto solo debería pasar si algo salió mal)
            campeon = ganadores[0] if ganadores else self.participante_libre
            self.mostrar_celebracion_campeon(campeon)
            return
        elif total_participantes == 2:
            # Solo quedan 2 participantes, generar la final automáticamente
            if len(ganadores) == 1 and self.participante_libre:
                # 1 ganador + 1 libre = FINAL (Ejemplo: Pedro + Dani)
                participante_libre_final = self.participante_libre
                final_enfrentamiento = {
                    'participante1': ganadores[0],
                    'participante2': participante_libre_final,
                    'ganador': None,
                    'completado': False,
                    'victorias_p1': 0,
                    'victorias_p2': 0
                }
                
                nueva_ronda = [final_enfrentamiento]
                self.rondas.append(nueva_ronda)
                self.participante_libre = None  # Ya no hay participante libre
                
                # Actualizar tabla
                self.actualizar_tabla_torneo()
                
                # Final generada automáticamente - solo imprimir en consola
                print(f"DEBUG: ¡FINAL GENERADA AUTOMÁTICAMENTE! {ganadores[0]} VS {participante_libre_final}")
                return
            elif len(ganadores) == 2 and not self.participante_libre:
                # 2 ganadores, sin libre = FINAL
                final_enfrentamiento = {
                    'participante1': ganadores[0],
                    'participante2': ganadores[1],
                    'ganador': None,
                    'completado': False,
                    'victorias_p1': 0,
                    'victorias_p2': 0
                }
                
                nueva_ronda = [final_enfrentamiento]
                self.rondas.append(nueva_ronda)
                
                # Actualizar tabla
                self.actualizar_tabla_torneo()
                
                # Final generada automáticamente - solo imprimir en consola
                print(f"DEBUG: ¡FINAL GENERADA AUTOMÁTICAMENTE! {ganadores[0]} VS {ganadores[1]}")
                return
        
        # Si llegamos aquí, necesitamos crear una nueva ronda normal
        # Encontrar al participante con más victorias de la ronda actual para que sea el nuevo libre
        mejor_participante = self.encontrar_mejor_participante_ronda(ronda_actual)
        
        # Crear lista de todos los participantes que avanzan
        todos_participantes = ganadores.copy()
        if self.participante_libre:
            todos_participantes.append(self.participante_libre)
        
        print(f"DEBUG: Todos los participantes que avanzan: {todos_participantes}")
        print(f"DEBUG: Mejor participante de la ronda: {mejor_participante}")
        
        # Aplicar lógica según el número de participantes restantes
        if total_participantes > 3:
            # Más de 3 participantes: aplicar lógica del mejor participante
            if mejor_participante and mejor_participante in todos_participantes:
                todos_participantes.remove(mejor_participante)
                self.participante_libre = mejor_participante
                ganadores = todos_participantes
                print(f"DEBUG: Nuevo Participante Libre - {mejor_participante} tiene más victorias")
            else:
                # Si no hay mejor participante claro, usar el sistema normal
                ganadores = todos_participantes
                if len(ganadores) % 2 == 1:
                    self.participante_libre = ganadores.pop()
                    messagebox.showinfo("Participante Libre", 
                                      f"🎯 {self.participante_libre} pasa automáticamente a la siguiente ronda")
                else:
                    self.participante_libre = None
        elif total_participantes == 3:
            # Exactamente 3 participantes: aplicar lógica del mejor participante para semifinal
            if mejor_participante and mejor_participante in todos_participantes:
                todos_participantes.remove(mejor_participante)
                self.participante_libre = mejor_participante
                ganadores = todos_participantes
                print(f"DEBUG: Semifinal - {mejor_participante} pasa libre a la final por más victorias")
            else:
                # Si no hay mejor participante claro, usar el sistema normal
                ganadores = todos_participantes
                if len(ganadores) % 2 == 1:
                    self.participante_libre = ganadores.pop()
                else:
                    self.participante_libre = None
        else:
            # 2 participantes o menos: usar sistema normal
            ganadores = todos_participantes
            self.participante_libre = None
        
        # Crear nueva ronda
        nueva_ronda = []
        for i in range(0, len(ganadores), 2):
            enfrentamiento = {
                'participante1': ganadores[i],
                'participante2': ganadores[i + 1],
                'ganador': None,
                'completado': False,
                'victorias_p1': 0,
                'victorias_p2': 0
            }
            nueva_ronda.append(enfrentamiento)
        
        self.rondas.append(nueva_ronda)
        
        # Actualizar tabla
        self.actualizar_tabla_torneo()
        
        nombre_ronda = self.obtener_nombre_ronda(len(self.rondas) - 1, len(nueva_ronda))
        print(f"DEBUG: {nombre_ronda} generada con {len(nueva_ronda)} enfrentamientos")
        
        # Guardar automáticamente después de generar siguiente ronda
        self.guardar_torneo_automatico()

    def obtener_nombre_ronda(self, ronda_num, num_enfrentamientos):
        # Si ya tenemos un nombre fijo para esta ronda, usarlo
        if ronda_num < len(self.nombres_rondas):
            return self.nombres_rondas[ronda_num]
        
        # Si no tenemos nombre fijo, calcularlo y guardarlo
        nombre = self.calcular_nombre_ronda(ronda_num, num_enfrentamientos)
        
        # Asegurar que la lista tenga el tamaño correcto
        while len(self.nombres_rondas) <= ronda_num:
            self.nombres_rondas.append("")
        
        # Guardar el nombre fijo
        self.nombres_rondas[ronda_num] = nombre
        return nombre
    
    def calcular_nombre_ronda(self, ronda_num, num_enfrentamientos):
        # Si es la primera ronda (ronda_num == 0), usar "ELIMINATORIAS INICIALES"
        if ronda_num == 0:
            return "ELIMINATORIAS INICIALES"
        
        # Lógica simple y directa basada en el número de enfrentamientos
        if num_enfrentamientos == 1:
            # Solo 1 enfrentamiento
            if self.participante_libre is None:
                # No hay participante libre = FINAL REAL
                return "FINAL"
            else:
                # Hay participante libre = SEMIFINALES
                return "SEMIFINALES"
        elif num_enfrentamientos == 2:
            # 2 enfrentamientos = CUARTOS DE FINAL
            return "CUARTOS DE FINAL"
        elif num_enfrentamientos == 4:
            # 4 enfrentamientos = OCTAVOS DE FINAL
            return "OCTAVOS DE FINAL"
        elif num_enfrentamientos == 8:
            # 8 enfrentamientos = DIECISEISAVOS DE FINAL
            return "DIECISEISAVOS DE FINAL"
        elif num_enfrentamientos >= 16:
            # 16 o más enfrentamientos = TREINTAIDOSAVOS DE FINAL
            return "TREINTAIDOSAVOS DE FINAL"
        else:
            # Para casos especiales (3, 5, 6, 7 enfrentamientos)
            if num_enfrentamientos == 3:
                return "CUARTOS DE FINAL"
            elif num_enfrentamientos >= 5 and num_enfrentamientos <= 7:
                return "OCTAVOS DE FINAL"
            else:
                return f"RONDA {ronda_num + 1}"

    def actualizar_tabla_torneo(self):
        if hasattr(self, 'ventana_tabla') and self.ventana_tabla and self.ventana_tabla.winfo_exists():
            self.actualizar_tabla_torneo_con_posicion()

    def cerrar_ventana_tabla(self):
        if self.ventana_tabla:
            self.ventana_tabla.destroy()
            self.ventana_tabla = None

    def cerrar_ventana_vs(self):
        if self.ventana_vs:
            self.ventana_vs.destroy()
            self.ventana_vs = None

    def editar_participante(self, ronda_num, enfrentamiento_indice, campo):
        """Editar el nombre de un participante en un enfrentamiento"""
        enfrentamiento = self.rondas[ronda_num][enfrentamiento_indice]
        nombre_actual = enfrentamiento[campo]
        
        nuevo_nombre = simpledialog.askstring(
            "Editar Participante",
            f"Editar nombre del participante:\n\nNombre actual: {nombre_actual}",
            initialvalue=nombre_actual
        )
        
        if nuevo_nombre and nuevo_nombre.strip():
            nombre_limpio = nuevo_nombre.strip()
            
            # Verificar si el nuevo nombre es el del participante libre
            if self.participante_libre and nombre_limpio == self.participante_libre:
                respuesta = messagebox.askyesno(
                    "Intercambio con Participante Libre",
                    f"El nombre '{nombre_limpio}' es el participante libre actual.\n\n"
                    f"¿Quieres intercambiar los participantes?\n\n"
                    f"• '{nombre_actual}' (en enfrentamiento) → '{nombre_limpio}' (en enfrentamiento)\n"
                    f"• '{nombre_limpio}' (libre) → '{nombre_actual}' (libre)\n\n"
                    f"Esto cambiará:\n"
                    f"En enfrentamiento: {nombre_actual} → {nombre_limpio}\n"
                    f"Participante libre: {nombre_limpio} → {nombre_actual}"
                )
                
                if respuesta:
                    # Realizar el intercambio
                    # 1. Cambiar el participante en el enfrentamiento
                    enfrentamiento[campo] = nombre_limpio
                    
                    # 2. Si este participante era el ganador, actualizar también el ganador
                    if enfrentamiento['ganador'] == nombre_actual:
                        enfrentamiento['ganador'] = nombre_limpio
                    
                    # 3. Cambiar el participante libre
                    self.participante_libre = nombre_actual
                    
                    # AUTO-GUARDADO: Guardar inmediatamente después del intercambio
                    self.guardar_torneo_automatico()
                    
                    # Actualizar las ventanas
                    self.actualizar_tabla_torneo()
                    if self.ventana_vs and self.ventana_vs.winfo_exists():
                        self.actualizar_ventana_vs()
                    
                    messagebox.showinfo(
                        "Intercambio Realizado",
                        f"✅ Intercambio completado exitosamente:\n\n"
                        f"🔄 En enfrentamiento: {nombre_actual} → {nombre_limpio}\n"
                        f"🔄 Participante libre: {nombre_limpio} → {nombre_actual}\n\n"
                        f"Los enfrentamientos se han actualizado automáticamente."
                    )
                else:
                    # No hacer el intercambio
                    return
            else:
                # Verificar si el nuevo nombre ya existe en la misma ronda
                participante_encontrado = None
                
                # Solo buscar en la misma ronda del enfrentamiento que se está editando
                ronda_actual = self.rondas[ronda_num]
                for e_num, enf in enumerate(ronda_actual):
                    # Saltar el enfrentamiento actual
                    if e_num == enfrentamiento_indice:
                        continue
                        
                    if enf['participante1'] == nombre_limpio or enf['participante2'] == nombre_limpio:
                        participante_encontrado = nombre_limpio
                        break
                
                if participante_encontrado:
                    nombre_ronda = self.obtener_nombre_ronda(ronda_num, len(self.rondas[ronda_num]))
                    messagebox.showwarning(
                        "Nombre Duplicado",
                        f"El nombre '{nombre_limpio}' ya existe en otro enfrentamiento de la {nombre_ronda.lower()}.\n\n"
                        f"Por favor elige un nombre diferente o usa la función de intercambio "
                        f"con el participante libre si es necesario."
                    )
                    return
                else:
                    # No hay conflicto, simplemente cambiar el nombre
                    enfrentamiento[campo] = nombre_limpio
                    
                    # Si este participante era el ganador, actualizar también el ganador
                    if enfrentamiento['ganador'] == nombre_actual:
                        enfrentamiento['ganador'] = nombre_limpio
                    
                    # AUTO-GUARDADO: Guardar inmediatamente después de editar participante
                    self.guardar_torneo_automatico()
                    
                    # Actualizar las ventanas
                    self.actualizar_tabla_torneo()
                    if self.ventana_vs and self.ventana_vs.winfo_exists():
                        self.actualizar_ventana_vs()
                    
                    messagebox.showinfo("Éxito", f"Participante actualizado:\n{nombre_actual} → {nombre_limpio}")

    def editar_participante_libre(self):
        """Editar el nombre del participante libre"""
        if not self.participante_libre:
            return
        
        nombre_actual = self.participante_libre
        
        nuevo_nombre = simpledialog.askstring(
            "Editar Participante Libre",
            f"Editar nombre del participante libre:\n\nNombre actual: {nombre_actual}",
            initialvalue=nombre_actual
        )
        
        if nuevo_nombre and nuevo_nombre.strip():
            nombre_limpio = nuevo_nombre.strip()
            
            # Verificar si el nuevo nombre ya existe en la ronda actual (la más reciente)
            participante_encontrado = None
            ronda_encontrada = None
            enfrentamiento_encontrado = None
            campo_encontrado = None
            
            # Solo buscar en la ronda actual (la última ronda generada)
            if self.rondas:
                ronda_actual_num = len(self.rondas) - 1
                ronda_actual = self.rondas[ronda_actual_num]
                
                for enf_num, enfrentamiento in enumerate(ronda_actual):
                    if enfrentamiento['participante1'] == nombre_limpio:
                        participante_encontrado = nombre_limpio
                        ronda_encontrada = ronda_actual_num
                        enfrentamiento_encontrado = enf_num
                        campo_encontrado = 'participante1'
                        break
                    elif enfrentamiento['participante2'] == nombre_limpio:
                        participante_encontrado = nombre_limpio
                        ronda_encontrada = ronda_actual_num
                        enfrentamiento_encontrado = enf_num
                        campo_encontrado = 'participante2'
                        break
            
            if participante_encontrado:
                # Obtener el nombre de la ronda actual
                nombre_ronda_actual = self.obtener_nombre_ronda(ronda_encontrada, len(self.rondas[ronda_encontrada]))
                
                # Preguntar si quiere hacer el intercambio
                respuesta = messagebox.askyesno(
                    "Intercambio de Participantes",
                    f"El nombre '{nombre_limpio}' ya existe en la {nombre_ronda_actual.lower()}.\n\n"
                    f"¿Quieres intercambiar los participantes?\n\n"
                    f"• '{nombre_actual}' (libre) → '{nombre_limpio}' (libre)\n"
                    f"• '{nombre_limpio}' (en {nombre_ronda_actual.lower()}) → '{nombre_actual}' (en {nombre_ronda_actual.lower()})\n\n"
                    f"Esto cambiará:\n"
                    f"Participante libre: {nombre_actual} → {nombre_limpio}\n"
                    f"En {nombre_ronda_actual.lower()}: {nombre_limpio} → {nombre_actual}"
                )
                
                if respuesta:
                    # Realizar el intercambio
                    # 1. Cambiar el participante en el enfrentamiento
                    enfrentamiento_afectado = self.rondas[ronda_encontrada][enfrentamiento_encontrado]
                    enfrentamiento_afectado[campo_encontrado] = nombre_actual
                    
                    # 2. Si el participante era ganador, actualizar el ganador
                    if enfrentamiento_afectado['ganador'] == nombre_limpio:
                        enfrentamiento_afectado['ganador'] = nombre_actual
                    
                    # 3. Cambiar el participante libre
                    self.participante_libre = nombre_limpio
                    
                    # AUTO-GUARDADO: Guardar inmediatamente después del intercambio
                    self.guardar_torneo_automatico()
                    
                    # Actualizar las ventanas
                    self.actualizar_tabla_torneo()
                    if self.ventana_vs and self.ventana_vs.winfo_exists():
                        self.actualizar_ventana_vs()
                    
                    messagebox.showinfo(
                        "Intercambio Realizado",
                        f"✅ Intercambio completado exitosamente:\n\n"
                        f"🔄 Participante libre: {nombre_actual} → {nombre_limpio}\n"
                        f"🔄 En enfrentamiento: {nombre_limpio} → {nombre_actual}\n\n"
                        f"Los enfrentamientos se han actualizado automáticamente."
                    )
                else:
                    # No hacer el intercambio, mantener el nombre original
                    return
            else:
                # No hay conflicto, simplemente cambiar el nombre
                self.participante_libre = nombre_limpio
                
                # AUTO-GUARDADO: Guardar inmediatamente después de editar participante libre
                self.guardar_torneo_automatico()
                
                # Actualizar las ventanas
                self.actualizar_tabla_torneo()
                if self.ventana_vs and self.ventana_vs.winfo_exists():
                    self.actualizar_ventana_vs()
                
                messagebox.showinfo("Éxito", f"Participante libre actualizado:\n{nombre_actual} → {nombre_limpio}")

    def actualizar_ventana_vs(self):
        """Actualizar el contenido de la ventana de VS"""
        if not (self.ventana_vs and self.ventana_vs.winfo_exists()):
            return
        
        # Limpiar contenido actual (excepto título y botón)
        for widget in self.ventana_vs.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                # Buscar el frame de la lista
                for child in widget.winfo_children():
                    if isinstance(child, tk.Canvas):
                        # Encontramos el canvas, actualizar su contenido
                        self.cerrar_ventana_vs()
                        self.mostrar_lista_vs()
                        return

    def mostrar_celebracion_campeon(self, campeon):
        """Mostrar una celebración elegante para el campeón del torneo"""
        # Crear ventana de celebración más grande y elegante
        ventana_celebracion = tk.Toplevel(self.root)
        ventana_celebracion.title("🏆 ¡CAMPEÓN DEL TORNEO! 🏆")
        ventana_celebracion.geometry("700x650")
        ventana_celebracion.configure(bg='#0a0a1a')
        ventana_celebracion.resizable(False, False)
        
        # Centrar la ventana
        ventana_celebracion.transient(self.root)
        ventana_celebracion.grab_set()
        
        # Frame principal con diseño profesional
        main_frame = tk.Frame(ventana_celebracion, bg='#0a0a1a')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Banner superior elegante
        banner_superior = tk.Frame(main_frame, bg='#ffd700', height=8)
        banner_superior.pack(fill='x', pady=(0, 20))
        banner_superior.pack_propagate(False)
        
        # Título principal más elegante
        titulo_frame = tk.Frame(main_frame, bg='#0a0a1a')
        titulo_frame.pack(fill='x', pady=(0, 25))
        
        # Efectos decorativos superiores
        decoracion_top = tk.Label(titulo_frame,
                                text="✨ 🏆 ✨ 🥇 ✨ 🏆 ✨",
                                bg='#0a0a1a',
                                fg='#ffd700',
                                font=('Arial', 20, 'bold'))
        decoracion_top.pack(pady=(0, 15))
        
        # Título principal profesional
        felicidades_label = tk.Label(titulo_frame,
                                   text="¡FELICIDADES GANASTE EL TORNEO!",
                                   bg='#0a0a1a',
                                   fg='#ffd700',
                                   font=('Arial', 26, 'bold'))
        felicidades_label.pack()
        
        # Frame del campeón con diseño premium
        campeon_frame = tk.Frame(main_frame, bg='#1a2332', relief='solid', bd=3)
        campeon_frame.pack(fill='x', pady=25, padx=15)
        
        # Borde dorado interno
        borde_dorado = tk.Frame(campeon_frame, bg='#ffd700', height=3)
        borde_dorado.pack(fill='x')
        borde_dorado.pack_propagate(False)
        
        # Contenido del campeón
        contenido_campeon = tk.Frame(campeon_frame, bg='#1a2332')
        contenido_campeon.pack(fill='both', expand=True, padx=20, pady=25)
        
        # Corona más grande y elegante
        corona_label = tk.Label(contenido_campeon,
                              text="👑",
                              bg='#1a2332',
                              fg='#ffd700',
                              font=('Arial', 60))
        corona_label.pack(pady=(0, 15))
        
        # Nombre del campeón con estilo premium
        campeon_label = tk.Label(contenido_campeon,
                                text=campeon,
                                bg='#1a2332',
                                fg='#ffffff',
                                font=('Arial', 28, 'bold'),
                                wraplength=550)
        campeon_label.pack(pady=(0, 15))
        

        
        # Subtítulo elegante
        subtitulo_label = tk.Label(contenido_campeon,
                                 text="CAMPEÓN DEL TORNEO",
                                 bg='#1a2332',
                                 fg='#ffd700',
                                 font=('Arial', 18, 'bold'))
        subtitulo_label.pack()
        
        # Información del torneo (solo si existe nombre)
        if self.nombre_torneo and self.nombre_torneo.strip():
            torneo_frame = tk.Frame(main_frame, bg='#2d1810', relief='solid', bd=2)
            torneo_frame.pack(fill='x', pady=(0, 15), padx=20)
            
            torneo_label = tk.Label(torneo_frame,
                                  text=f"🏆 {self.nombre_torneo.upper()} 🏆",
                                  bg='#2d1810',
                                  fg='#ffa500',
                                  font=('Arial', 16, 'bold'),
                                  pady=12)
            torneo_label.pack()
        

        
        # Estadísticas del torneo con diseño mejorado
        stats_frame = tk.Frame(main_frame, bg='#1a1a3a', relief='solid', bd=2)
        stats_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        stats_title = tk.Label(stats_frame,
                             text="📊 ESTADÍSTICAS DEL TORNEO",
                             bg='#1a1a3a',
                             fg='#ffffff',
                             font=('Arial', 14, 'bold'))
        stats_title.pack(pady=(15, 10))
        
        # Estadísticas en formato más elegante
        total_participantes = len(self.participantes)
        total_rondas = len(self.rondas)
        total_enfrentamientos = sum(len(ronda) for ronda in self.rondas)
        
        stats_container = tk.Frame(stats_frame, bg='#1a1a3a')
        stats_container.pack(pady=(0, 15))
        
        # Crear estadísticas en columnas
        stats_data = [
            ("👥", "Participantes", total_participantes),
            ("🎯", "Rondas", total_rondas),
            ("⚔️", "Enfrentamientos", total_enfrentamientos)
        ]
        
        for i, (emoji, label, valor) in enumerate(stats_data):
            stat_frame = tk.Frame(stats_container, bg='#1a1a3a')
            stat_frame.pack(side='left', padx=20)
            
            tk.Label(stat_frame, text=emoji, bg='#1a1a3a', fg='#ffd700', 
                    font=('Arial', 16, 'bold')).pack()
            tk.Label(stat_frame, text=str(valor), bg='#1a1a3a', fg='#ffffff', 
                    font=('Arial', 14, 'bold')).pack()
            tk.Label(stat_frame, text=label, bg='#1a1a3a', fg='#cccccc', 
                    font=('Arial', 10)).pack()
        
        # Efectos visuales finales
        efectos_frame = tk.Frame(main_frame, bg='#0a0a1a')
        efectos_frame.pack(fill='x', pady=15)
        
        efectos_label = tk.Label(efectos_frame,
                               text="🎊 ✨ 🎉 ⭐ 🏆 ⭐ 🎉 ✨ 🎊",
                               bg='#0a0a1a',
                               fg='#ffd700',
                               font=('Arial', 18))
        efectos_label.pack()
        
        # Banner inferior
        banner_inferior = tk.Frame(main_frame, bg='#ffd700', height=5)
        banner_inferior.pack(fill='x', pady=(15, 0))
        banner_inferior.pack_propagate(False)
        
        # Botón para cerrar con diseño premium
        boton_frame = tk.Frame(main_frame, bg='#0a0a1a')
        boton_frame.pack(fill='x', pady=(20, 0))
        
        cerrar_btn = tk.Button(boton_frame,
                             text="🏆 ¡EXCELENTE TORNEO! 🏆",
                             bg='#ffd700',
                             fg='#1a1a1a',
                             font=('Arial', 16, 'bold'),
                             relief='raised',
                             bd=4,
                             padx=30,
                             pady=12,
                             cursor='hand2',
                             command=ventana_celebracion.destroy)
        cerrar_btn.pack()
        
        # Efecto de animación mejorado
        self.animar_celebracion(ventana_celebracion, felicidades_label, 0)

    def animar_celebracion(self, ventana, label, contador):
        """Crear un efecto de parpadeo para la celebración"""
        if not ventana.winfo_exists():
            return
            
        if contador < 6:  # Parpadear 3 veces
            if contador % 2 == 0:
                label.config(fg='#ff6b6b')  # Rojo brillante
            else:
                label.config(fg='#ffd700')  # Dorado
            
            ventana.after(500, lambda: self.animar_celebracion(ventana, label, contador + 1))
        else:
            label.config(fg='#ffd700')  # Volver al dorado final

    def encontrar_mejor_participante_ronda(self, ronda):
        """Encontrar al participante con más victorias en la ronda"""
        mejor_participante = None
        max_victorias = -1
        
        # Revisar todos los enfrentamientos de la ronda
        for enfrentamiento in ronda:
            v1 = enfrentamiento.get('victorias_p1', 0)
            v2 = enfrentamiento.get('victorias_p2', 0)
            
            # Verificar participante 1
            if v1 > max_victorias:
                max_victorias = v1
                mejor_participante = enfrentamiento['participante1']
            
            # Verificar participante 2
            if v2 > max_victorias:
                max_victorias = v2
                mejor_participante = enfrentamiento['participante2']
        
        # Solo devolver si realmente tiene victorias (más de 0)
        if max_victorias > 0:
            return mejor_participante
        else:
            return None

    def actualizar_victorias_silencioso(self, ronda_num, enfrentamiento_indice, campo_victorias, valor):
        """Actualizar el número de victorias sin actualizar la tabla y guardar automáticamente"""
        try:
            # Permitir valores vacíos temporalmente
            if valor.strip() == "":
                victorias = 0
            else:
                # Verificar que sea un número válido
                victorias = int(valor)
                if victorias < 0:
                    victorias = 0
            
            # Actualizar las victorias en el enfrentamiento silenciosamente
            self.rondas[ronda_num][enfrentamiento_indice][campo_victorias] = victorias
            
            # AUTO-GUARDADO: Guardar inmediatamente cuando se modifiquen las victorias
            self.guardar_torneo_automatico()
            
            # NO actualizar la tabla para evitar interrupciones
            # Los cambios se verán cuando se actualice la tabla manualmente o se seleccione ganador
            
        except (ValueError, IndexError):
            # Si hay error, mantener el valor anterior
            pass

    def actualizar_tabla_torneo_con_posicion(self):
        """Actualizar la tabla manteniendo la posición del scroll y valores de entrada"""
        if hasattr(self, 'ventana_tabla') and self.ventana_tabla and self.ventana_tabla.winfo_exists():
            # Guardar la posición actual del scroll si existe
            scroll_position = None
            if hasattr(self, 'canvas_tabla'):
                try:
                    scroll_position = self.canvas_tabla.canvasy(0)
                except:
                    scroll_position = None
            
            # Actualizar la tabla
            self.crear_tabla_torneo_completa()
            
            # Restaurar la posición del scroll
            if scroll_position is not None and hasattr(self, 'canvas_tabla'):
                try:
                    self.root.after(50, lambda: self.canvas_tabla.yview_moveto(scroll_position / self.canvas_tabla.bbox("all")[3]))
                except:
                    pass

    def guardar_valores_victorias_actuales(self):
        """Guardar todos los valores actuales de las casillas de victorias antes de actualizar"""
        if not (hasattr(self, 'ventana_tabla') and self.ventana_tabla and self.ventana_tabla.winfo_exists()):
            return
        
        try:
            # Buscar todas las casillas de victorias y guardar sus valores en los datos
            def buscar_entries(widget):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Entry):
                        # Intentar extraer información del widget para saber a qué enfrentamiento pertenece
                        try:
                            valor = child.get().strip()
                            if valor.isdigit():
                                # Aquí necesitaríamos una forma de identificar a qué enfrentamiento pertenece
                                # Por ahora, vamos a recorrer todos los enfrentamientos y actualizar
                                pass
                        except:
                            pass
                    elif hasattr(child, 'winfo_children'):
                        buscar_entries(child)
            
            if hasattr(self, 'canvas_tabla'):
                buscar_entries(self.canvas_tabla)
                
        except Exception as e:
            print(f"DEBUG: Error guardando valores: {e}")

    def actualizar_enfrentamiento_especifico(self, ronda_num, enfrentamiento_indice):
        """Actualizar solo un enfrentamiento específico sin recargar toda la tabla"""
        if not (hasattr(self, 'ventana_tabla') and self.ventana_tabla and self.ventana_tabla.winfo_exists()):
            return
        
        # Por ahora, hacer una actualización completa pero manteniendo posición
        # En el futuro se podría implementar una actualización más granular
        self.actualizar_tabla_torneo_con_posicion()

    def seleccionar_ganador_directo(self, ronda_num, enfrentamiento_indice, ganador):
        """Seleccionar ganador directamente y actualizar solo este enfrentamiento"""
        enfrentamiento = self.rondas[ronda_num][enfrentamiento_indice]
        
        # Actualizar el enfrentamiento
        enfrentamiento['ganador'] = ganador
        enfrentamiento['completado'] = True
        
        # AUTO-GUARDADO: Guardar inmediatamente cuando se seleccione un ganador
        self.guardar_torneo_automatico()
        
        # Actualizar SOLO este enfrentamiento específico, no toda la tabla
        self.actualizar_enfrentamiento_especifico(ronda_num, enfrentamiento_indice)
        
        # Verificar si la ronda está completa para posibles acciones adicionales
        ronda_completa = all(e['completado'] for e in self.rondas[ronda_num])
        if ronda_completa:
            nombre_ronda = self.obtener_nombre_ronda(ronda_num, len(self.rondas[ronda_num]))
            es_final_real = (len(self.rondas[ronda_num]) == 1 and self.participante_libre is None)
            
            if es_final_real:
                self.mostrar_celebracion_campeon(ganador)
            else:
                print(f"DEBUG: {nombre_ronda} completada. Listo para generar siguiente ronda.")

    def seleccionar_ganador_por_victorias(self, ronda_num, enfrentamiento_indice):
        """Determinar el ganador basado en las victorias y actualizar solo este enfrentamiento"""
        enfrentamiento = self.rondas[ronda_num][enfrentamiento_indice]
        
        v1 = enfrentamiento.get('victorias_p1', 0)
        v2 = enfrentamiento.get('victorias_p2', 0)
        
        print(f"DEBUG: Victorias antes de seleccionar ganador - P1: {v1}, P2: {v2}")
        
        if v1 == v2:
            # Empate, mostrar selector sin anuncio previo
            self.mostrar_selector_ganador_empate(ronda_num, enfrentamiento_indice)
            return
        
        # Determinar ganador por victorias directamente
        if v1 > v2:
            ganador = enfrentamiento['participante1']
        else:
            ganador = enfrentamiento['participante2']
        
        print(f"DEBUG: Ganador seleccionado: {ganador}")
        
        # Actualizar el enfrentamiento
        enfrentamiento['ganador'] = ganador
        enfrentamiento['completado'] = True
        
        # AUTO-GUARDADO: Guardar inmediatamente cuando se determine un ganador por victorias
        self.guardar_torneo_automatico()
        
        # Actualizar SOLO este enfrentamiento específico, no toda la tabla
        self.actualizar_enfrentamiento_especifico(ronda_num, enfrentamiento_indice)
        
        # Verificar si la ronda está completa para posibles acciones adicionales
        ronda_completa = all(e['completado'] for e in self.rondas[ronda_num])
        if ronda_completa:
            nombre_ronda = self.obtener_nombre_ronda(ronda_num, len(self.rondas[ronda_num]))
            es_final_real = (len(self.rondas[ronda_num]) == 1 and self.participante_libre is None)
            
            if es_final_real:
                self.mostrar_celebracion_campeon(ganador)
            else:
                print(f"DEBUG: {nombre_ronda} completada. Listo para generar siguiente ronda.")

    def mostrar_selector_ganador_empate(self, ronda_num, enfrentamiento_indice):
        """Mostrar ventana para seleccionar ganador en caso de empate"""
        enfrentamiento = self.rondas[ronda_num][enfrentamiento_indice]
        
        # Crear ventana de selección más pequeña y directa
        ventana_empate = tk.Toplevel(self.root)
        ventana_empate.title("Empate - Seleccionar Ganador")
        ventana_empate.geometry("350x200")
        ventana_empate.configure(bg='#2c3e50')
        ventana_empate.transient(self.root)
        ventana_empate.grab_set()
        
        # Título más simple
        titulo = tk.Label(ventana_empate,
                         text=f"🤝 Empate ({enfrentamiento.get('victorias_p1', 0)}-{enfrentamiento.get('victorias_p2', 0)})",
                         bg='#2c3e50',
                         fg='#f39c12',
                         font=('Arial', 14, 'bold'))
        titulo.pack(pady=15)
        
        # Botones para seleccionar ganador directamente
        botones_frame = tk.Frame(ventana_empate, bg='#2c3e50')
        botones_frame.pack(pady=20)
        
        # Botón participante 1
        btn_p1 = tk.Button(botones_frame,
                          text=f"🏆 {enfrentamiento['participante1']}",
                          bg='#3498db',
                          fg='white',
                          font=('Arial', 11, 'bold'),
                          padx=15,
                          pady=8,
                          command=lambda: [
                              self.seleccionar_ganador(ronda_num, enfrentamiento_indice, enfrentamiento['participante1']),
                              ventana_empate.destroy()
                          ])
        btn_p1.pack(pady=5)
        
        # Botón participante 2
        btn_p2 = tk.Button(botones_frame,
                          text=f"🏆 {enfrentamiento['participante2']}",
                          bg='#27ae60',
                          fg='white',
                          font=('Arial', 11, 'bold'),
                          padx=15,
                          pady=8,
                          command=lambda: [
                              self.seleccionar_ganador(ronda_num, enfrentamiento_indice, enfrentamiento['participante2']),
                              ventana_empate.destroy()
                          ])
        btn_p2.pack(pady=5)

    def crear_info_torneo(self, parent):
        info_frame = tk.Frame(parent, bg='#2a2a2a', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=20, padx=20)
        
        # Banner de información
        info_banner = tk.Frame(info_frame, bg='#FFD700', height=25)
        info_banner.pack(fill='x')
        info_banner.pack_propagate(False)
        
        tk.Label(info_banner,
                text="📊 ESTADÍSTICAS DEL TORNEO - DANI666",
                bg='#FFD700',
                fg='#1a1a1a',
                font=('Arial', 10, 'bold')).pack(expand=True)
        
        total_participantes = len(self.participantes)
        rondas_completadas = sum(1 for ronda in self.rondas if all(e['completado'] for e in ronda))
        
        info_text = f"""
🏆 Torneo: {self.nombre_torneo or 'Sin nombre'}
👥 Total de Participantes Iniciales: {total_participantes}
🎯 Rondas Generadas: {len(self.rondas)}
✅ Rondas Completadas: {rondas_completadas}
⏳ Participante Libre: {self.participante_libre or 'Ninguno'}
        """
        
        info_label = tk.Label(info_frame,
                            text=info_text,
                            bg='#2a2a2a',
                            fg='#FFFFFF',
                            font=('Arial', 10),
                            justify='left')
        info_label.pack(pady=15)

    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RuletaTorneo()
    app.ejecutar()