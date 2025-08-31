import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import threading
import time
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
try:
    import pystray
    from PIL import Image
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False

class GestorSuscripciones:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DaniStore - Streaming")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        # Configurar icono si existe
        try:
            if os.path.exists('gestor_icon.ico'):
                self.root.iconbitmap('gestor_icon.ico')
        except:
            pass  # Si no se puede cargar el icono, continuar sin él
        
        # Variables
        self.suscripciones = []
        self.archivo_datos = "suscripciones_data.json"
        self.notificaciones_activas = True
        self.minimizado_bandeja = False
        self.tray_icon = None
        
        # Sistema de notificaciones integrado
        self.verificacion_activa = True
        self.intervalo_verificacion = 60  # 60 segundos para pruebas (cambiar a 3600 para producción)
        self.ultima_verificacion = None
        self.notificaciones_enviadas = set()  # Para evitar duplicados
        
        # Servicios de streaming disponibles
        self.servicios = [
            "Netflix", "Disney+", "HBO Max", "Amazon Prime", 
            "YouTube Premium", "Crunchyroll", "Spotify", "Apple TV+",
            "Paramount+", "Peacock", "Hulu", "Star+", "Pluto TV",
            "Tubi", "Funimation", "VRV", "Otro"
        ]
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Cargar datos existentes
        self.cargar_datos()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Iniciar hilo de notificaciones
        self.iniciar_monitor_notificaciones()
        
        # Actualizar título con contador
        self.actualizar_titulo()
        
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores Dani666
        style.configure('Title.TLabel', 
                       background='#1a1a1a', 
                       foreground='#FFD700', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Custom.TButton',
                       background='#FFD700',
                       foreground='#1a1a1a',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background='#228B22',
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Danger.TButton',
                       background='#DC143C',
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
    def crear_interfaz(self):
        # Banner superior
        banner_frame = tk.Frame(self.root, bg='#FFD700', height=40)
        banner_frame.pack(fill='x')
        banner_frame.pack_propagate(False)
        
        tk.Label(banner_frame,
                text="📺 DANISTORE - STREAMING",
                bg='#FFD700',
                fg='#1a1a1a',
                font=('Arial', 14, 'bold')).pack(expand=True)
        
        # Título principal
        titulo_frame = tk.Frame(self.root, bg='#1a1a1a')
        titulo_frame.pack(fill='x', pady=20)
        
        tk.Label(titulo_frame,
                text="🎬 Control de Cuentas de Streaming",
                bg='#1a1a1a',
                fg='#FFD700',
                font=('Arial', 18, 'bold')).pack()
        
        tk.Label(titulo_frame,
                text="💪 ¡Dani, domina tus ventas y nunca pierdas un cliente! 🚀",
                bg='#1a1a1a',
                fg='#CCCCCC',
                font=('Arial', 12)).pack(pady=(5, 0))
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Columna izquierda - Formulario
        self.crear_formulario(main_frame)
        
        # Columna derecha - Lista de suscripciones
        self.crear_lista_suscripciones(main_frame)
        
        # Frame inferior - Botones de acción
        self.crear_botones_accion()
        
    def crear_formulario(self, parent):
        # Frame contenedor principal
        form_container = tk.Frame(parent, bg='#2a2a2a', relief='solid', bd=2)
        form_container.pack(side='left', fill='y', padx=(0, 10), pady=10)
        
        # Título del formulario (fijo en la parte superior)
        titulo_frame = tk.Frame(form_container, bg='#2a2a2a')
        titulo_frame.pack(fill='x')
        
        tk.Label(titulo_frame,
                text="➕ Nueva Suscripción",
                bg='#2a2a2a',
                fg='#FFD700',
                font=('Arial', 14, 'bold')).pack(pady=15)
        
        # Frame para el área scrollable
        scroll_container = tk.Frame(form_container, bg='#2a2a2a')
        scroll_container.pack(fill='both', expand=True, padx=5, pady=(0, 5))
        
        # Canvas para el scroll
        self.form_canvas = tk.Canvas(scroll_container, 
                                    bg='#2a2a2a', 
                                    highlightthickness=0,
                                    width=320,
                                    height=500)
        
        # Scrollbar
        form_scrollbar = tk.Scrollbar(scroll_container, 
                                     orient='vertical', 
                                     command=self.form_canvas.yview)
        
        # Frame scrollable dentro del canvas
        form_frame = tk.Frame(self.form_canvas, bg='#2a2a2a')
        
        # Configurar el canvas
        self.form_canvas.configure(yscrollcommand=form_scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        self.form_canvas.pack(side='left', fill='both', expand=True)
        form_scrollbar.pack(side='right', fill='y')
        
        # Crear ventana en el canvas
        canvas_frame = self.form_canvas.create_window((0, 0), window=form_frame, anchor='nw')
        
        # Función para actualizar el scroll region
        def configure_scroll_region(event=None):
            self.form_canvas.configure(scrollregion=self.form_canvas.bbox('all'))
            # Ajustar el ancho del frame al canvas
            canvas_width = self.form_canvas.winfo_width()
            self.form_canvas.itemconfig(canvas_frame, width=canvas_width)
        
        form_frame.bind('<Configure>', configure_scroll_region)
        self.form_canvas.bind('<Configure>', configure_scroll_region)
        
        # Bind para scroll con rueda del mouse
        def on_mousewheel(event):
            self.form_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.form_canvas.bind("<MouseWheel>", on_mousewheel)
        form_frame.bind("<MouseWheel>", on_mousewheel)
        
        # Campo Usuario
        tk.Label(form_frame,
                text="👤 Nombre de Usuario:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(10, 5))
        
        self.entry_usuario = tk.Entry(form_frame,
                                     font=('Arial', 11),
                                     width=25,
                                     bg='#3a3a3a',
                                     fg='white',
                                     insertbackground='white')
        self.entry_usuario.pack(padx=15, pady=(0, 10))
        
        # Campo Correo
        tk.Label(form_frame,
                text="📧 Correo Electrónico:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(10, 5))
        
        self.entry_correo = tk.Entry(form_frame,
                                   font=('Arial', 11),
                                   width=25,
                                   bg='#3a3a3a',
                                   fg='white',
                                   insertbackground='white')
        self.entry_correo.pack(padx=15, pady=(0, 10))
        
        # Campo Contraseña
        tk.Label(form_frame,
                text="🔒 Contraseña:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(10, 5))
        
        self.entry_password = tk.Entry(form_frame,
                                     font=('Arial', 11),
                                     width=25,
                                     bg='#3a3a3a',
                                     fg='white',
                                     insertbackground='white',
                                     show='*')  # Ocultar contraseña
        self.entry_password.pack(padx=15, pady=(0, 10))
        
        # Campo PIN del Perfil
        tk.Label(form_frame,
                text="📱 PIN del Perfil:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(10, 5))
        
        self.entry_pin = tk.Entry(form_frame,
                                font=('Arial', 11),
                                width=25,
                                bg='#3a3a3a',
                                fg='white',
                                insertbackground='white')
        self.entry_pin.pack(padx=15, pady=(0, 10))
        
        # Campo Servicio
        tk.Label(form_frame,
                text="📺 Servicio de Streaming:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(10, 5))
        
        self.combo_servicio = ttk.Combobox(form_frame,
                                          values=self.servicios,
                                          font=('Arial', 11),
                                          width=22,
                                          state='readonly')
        self.combo_servicio.pack(padx=15, pady=(0, 10))
        self.combo_servicio.set("Netflix")
        
        # Campo Duración
        tk.Label(form_frame,
                text="⏰ Duración de la Suscripción:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(10, 5))
        
        duracion_frame = tk.Frame(form_frame, bg='#2a2a2a')
        duracion_frame.pack(padx=15, pady=(0, 10))
        
        self.combo_duracion = ttk.Combobox(duracion_frame,
                                          values=["1 mes", "2 meses", "3 meses", "6 meses", 
                                                 "1 año", "2 años", "Indefinido", "Personalizado"],
                                          font=('Arial', 11),
                                          width=15,
                                          state='readonly')
        self.combo_duracion.pack(side='left')
        self.combo_duracion.set("1 mes")
        self.combo_duracion.bind('<<ComboboxSelected>>', self.on_duracion_change)
        
        # Frame para duración personalizada (inicialmente oculto)
        self.custom_frame = tk.Frame(form_frame, bg='#2a2a2a')
        
        tk.Label(self.custom_frame,
                text="⏰ Tiempo personalizado:",
                bg='#2a2a2a',
                fg='#FFD700',
                font=('Arial', 10, 'bold')).pack(anchor='w', pady=(5, 10))
        
        # Selector de unidad principal
        unidad_frame = tk.Frame(self.custom_frame, bg='#2a2a2a')
        unidad_frame.pack(fill='x', pady=5)
        
        tk.Label(unidad_frame,
                text="Seleccionar unidad:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.combo_unidad_custom = ttk.Combobox(unidad_frame,
                                               values=["Minutos", "Horas", "Días", "Meses", "Años"],
                                               font=('Arial', 10),
                                               width=12,
                                               state='readonly')
        self.combo_unidad_custom.pack(anchor='w', pady=2)
        self.combo_unidad_custom.set("Días")
        self.combo_unidad_custom.bind('<<ComboboxSelected>>', self.on_unidad_custom_change)
        
        # Frame para campos específicos (se actualiza según la unidad)
        self.campos_custom_frame = tk.Frame(self.custom_frame, bg='#2a2a2a')
        self.campos_custom_frame.pack(fill='x', pady=10)
        
        # Inicializar campos
        self.crear_campos_custom()
        
        # Ejemplo de cálculo
        self.label_ejemplo = tk.Label(self.custom_frame,
                                     text="Ejemplo: 30 días",
                                     bg='#2a2a2a',
                                     fg='#90EE90',
                                     font=('Arial', 8))
        self.label_ejemplo.pack(anchor='w', pady=(10, 5))
        
        # Campo Fecha de Inicio (opcional)
        tk.Label(form_frame,
                text="📅 Fecha de Inicio (opcional):",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(15, 5))
        
        fecha_frame = tk.Frame(form_frame, bg='#2a2a2a')
        fecha_frame.pack(padx=15, pady=(0, 10))
        
        tk.Button(fecha_frame,
                 text="📅 Hoy",
                 bg='#4CAF50',
                 fg='white',
                 font=('Arial', 9),
                 command=self.usar_fecha_hoy).pack(side='left', padx=(0, 5))
        
        tk.Button(fecha_frame,
                 text="📅 Elegir",
                 bg='#2196F3',
                 fg='white',
                 font=('Arial', 9),
                 command=self.elegir_fecha).pack(side='left')
        
        self.label_fecha = tk.Label(form_frame,
                                   text="Fecha: Hoy",
                                   bg='#2a2a2a',
                                   fg='#90EE90',
                                   font=('Arial', 9))
        self.label_fecha.pack(padx=15, pady=(5, 15))
        
        self.fecha_inicio = datetime.now()
        
        # Campo Notas (opcional)
        tk.Label(form_frame,
                text="📝 Notas (opcional):",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(10, 5))
        
        # Frame contenedor para notas y botón
        notas_container = tk.Frame(form_frame, bg='#2a2a2a')
        notas_container.pack(padx=15, pady=(0, 10), fill='x')
        
        # Frame para el texto con scrollbar
        text_frame = tk.Frame(notas_container, bg='#2a2a2a')
        text_frame.pack(fill='both', expand=True)
        
        # Campo de texto para notas con scrollbar
        self.text_notas = tk.Text(text_frame,
                                 font=('Arial', 9),
                                 width=25,
                                 height=2,  # Más compacto
                                 bg='#3a3a3a',
                                 fg='white',
                                 insertbackground='white',
                                 wrap='word')
        
        # Scrollbar para el texto
        scrollbar_notas = tk.Scrollbar(text_frame, orient='vertical', command=self.text_notas.yview)
        self.text_notas.configure(yscrollcommand=scrollbar_notas.set)
        
        # Empaquetar texto y scrollbar
        self.text_notas.pack(side='left', fill='both', expand=True)
        scrollbar_notas.pack(side='right', fill='y')
        
        # Frame para botones
        botones_frame = tk.Frame(form_frame, bg='#2a2a2a')
        botones_frame.pack(pady=20)
        
        # Botón Agregar Suscripción
        tk.Button(botones_frame,
                 text="➕ AGREGAR SUSCRIPCIÓN",
                 bg='#FFD700',
                 fg='#1a1a1a',
                 font=('Arial', 12, 'bold'),
                 command=self.agregar_suscripcion,
                 relief='raised',
                 bd=3,
                 padx=20,
                 pady=15).pack(pady=(0, 10))
        
        # Botón WhatsApp
        tk.Button(botones_frame,
                 text="📱 COPIAR PARA WHATSAPP",
                 bg='#25D366',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 command=self.copiar_para_whatsapp,
                 relief='raised',
                 bd=3,
                 padx=20,
                 pady=10).pack()
        
        # Inicializar campos personalizados si es necesario
        self.on_duracion_change()
        
    def crear_lista_suscripciones(self, parent):
        lista_frame = tk.Frame(parent, bg='#2a2a2a', relief='solid', bd=2)
        lista_frame.pack(side='right', fill='both', expand=True, padx=(10, 0), pady=10)
        
        # Título de la lista
        header_frame = tk.Frame(lista_frame, bg='#2a2a2a')
        header_frame.pack(fill='x', pady=15)
        
        tk.Label(header_frame,
                text="📋 Suscripciones Activas",
                bg='#2a2a2a',
                fg='#FFD700',
                font=('Arial', 14, 'bold')).pack(side='left')
        
        # Contador
        self.label_contador = tk.Label(header_frame,
                                      text="(0 activas)",
                                      bg='#2a2a2a',
                                      fg='#90EE90',
                                      font=('Arial', 10))
        self.label_contador.pack(side='right')
        
        # Frame con scroll para la lista
        scroll_frame = tk.Frame(lista_frame, bg='#2a2a2a')
        scroll_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Canvas y scrollbar
        self.canvas_lista = tk.Canvas(scroll_frame, bg='#1a1a1a')
        scrollbar_lista = tk.Scrollbar(scroll_frame, orient="vertical", command=self.canvas_lista.yview)
        self.scrollable_frame_lista = tk.Frame(self.canvas_lista, bg='#1a1a1a')
        
        self.scrollable_frame_lista.bind(
            "<Configure>",
            lambda e: self.canvas_lista.configure(scrollregion=self.canvas_lista.bbox("all"))
        )
        
        self.canvas_lista.create_window((0, 0), window=self.scrollable_frame_lista, anchor="nw")
        self.canvas_lista.configure(yscrollcommand=scrollbar_lista.set)
        
        # Empaquetar canvas y scrollbar
        self.canvas_lista.pack(side="left", fill="both", expand=True)
        scrollbar_lista.pack(side="right", fill="y")
        
        # Actualizar lista
        self.actualizar_lista()
        
    def crear_botones_accion(self):
        botones_frame = tk.Frame(self.root, bg='#1a1a1a')
        botones_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Botones izquierda
        left_buttons = tk.Frame(botones_frame, bg='#1a1a1a')
        left_buttons.pack(side='left')
        
        ttk.Button(left_buttons,
                  text="🔔 Verificar Vencimientos",
                  command=self.verificar_vencimientos_manual,
                  style='Custom.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(left_buttons,
                  text="🔔 Verificar Vencimientos",
                  command=self.verificar_vencimientos_manual,
                  style='Custom.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(left_buttons,
                  text="📊 Estadísticas",
                  command=self.mostrar_estadisticas,
                  style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(left_buttons,
                  text="📱 Minimizar a Bandeja",
                  command=self.minimizar_a_bandeja,
                  style='Custom.TButton').pack(side='left', padx=(0, 10))
        
        # Botones derecha
        right_buttons = tk.Frame(botones_frame, bg='#1a1a1a')
        right_buttons.pack(side='right')
        
        ttk.Button(right_buttons,
                  text="💾 Exportar Datos",
                  command=self.exportar_datos,
                  style='Custom.TButton').pack(side='right', padx=(10, 0))
        
        ttk.Button(right_buttons,
                  text="🗑️ Limpiar Vencidas",
                  command=self.limpiar_vencidas,
                  style='Danger.TButton').pack(side='right', padx=(10, 0))
    
    def on_duracion_change(self, event=None):
        """Manejar cambio en la duración"""
        if self.combo_duracion.get() == "Personalizado":
            # Empaquetar después del frame de duración
            duracion_frame = self.combo_duracion.master
            self.custom_frame.pack(after=duracion_frame, padx=15, pady=(5, 10), fill='x')
            self.crear_campos_custom()  # Crear los campos específicos
            self.actualizar_ejemplo_custom()
        else:
            self.custom_frame.pack_forget()
    
    def crear_campos_custom(self):
        """Crear campos específicos según la unidad seleccionada"""
        # Limpiar campos existentes
        for widget in self.campos_custom_frame.winfo_children():
            widget.destroy()
        
        unidad = self.combo_unidad_custom.get()
        
        if unidad == "Minutos":
            self.crear_campos_minutos()
        elif unidad == "Horas":
            self.crear_campos_horas()
        elif unidad == "Días":
            self.crear_campos_dias()
        elif unidad == "Meses":
            self.crear_campos_meses()
        elif unidad == "Años":
            self.crear_campos_años()
        
        # Forzar actualización de la interfaz
        self.campos_custom_frame.update_idletasks()
    
    def crear_campos_minutos(self):
        """Crear campos para minutos"""
        tk.Label(self.campos_custom_frame,
                text="⏱️ Minutos:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.entry_minutos = tk.Entry(self.campos_custom_frame,
                                     font=('Arial', 10),
                                     width=8,
                                     bg='#3a3a3a',
                                     fg='white',
                                     insertbackground='white')
        self.entry_minutos.pack(anchor='w', pady=2)
        self.entry_minutos.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
    
    def crear_campos_horas(self):
        """Crear campos para horas y minutos"""
        # Horas
        tk.Label(self.campos_custom_frame,
                text="🕐 Horas:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.entry_horas = tk.Entry(self.campos_custom_frame,
                                   font=('Arial', 10),
                                   width=8,
                                   bg='#3a3a3a',
                                   fg='white',
                                   insertbackground='white')
        self.entry_horas.pack(anchor='w', pady=2)
        self.entry_horas.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
        
        # Minutos adicionales
        tk.Label(self.campos_custom_frame,
                text="⏱️ Minutos adicionales:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9)).pack(anchor='w', pady=(10, 0))
        
        self.entry_minutos_extra = tk.Entry(self.campos_custom_frame,
                                           font=('Arial', 10),
                                           width=8,
                                           bg='#3a3a3a',
                                           fg='white',
                                           insertbackground='white')
        self.entry_minutos_extra.pack(anchor='w', pady=2)
        self.entry_minutos_extra.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
    
    def crear_campos_dias(self):
        """Crear campos para días y horas"""
        # Días
        tk.Label(self.campos_custom_frame,
                text="📅 Días:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.entry_dias = tk.Entry(self.campos_custom_frame,
                                  font=('Arial', 10),
                                  width=8,
                                  bg='#3a3a3a',
                                  fg='white',
                                  insertbackground='white')
        self.entry_dias.pack(anchor='w', pady=2)
        self.entry_dias.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
        
        # Horas adicionales
        tk.Label(self.campos_custom_frame,
                text="🕐 Horas adicionales:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9)).pack(anchor='w', pady=(10, 0))
        
        self.entry_horas_extra = tk.Entry(self.campos_custom_frame,
                                         font=('Arial', 10),
                                         width=8,
                                         bg='#3a3a3a',
                                         fg='white',
                                         insertbackground='white')
        self.entry_horas_extra.pack(anchor='w', pady=2)
        self.entry_horas_extra.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
    
    def crear_campos_meses(self):
        """Crear campos para meses y días"""
        # Meses
        tk.Label(self.campos_custom_frame,
                text="📆 Meses:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.entry_meses = tk.Entry(self.campos_custom_frame,
                                   font=('Arial', 10),
                                   width=8,
                                   bg='#3a3a3a',
                                   fg='white',
                                   insertbackground='white')
        self.entry_meses.pack(anchor='w', pady=2)
        self.entry_meses.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
        
        # Días adicionales
        tk.Label(self.campos_custom_frame,
                text="📅 Días adicionales:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9)).pack(anchor='w', pady=(10, 0))
        
        self.entry_dias_extra = tk.Entry(self.campos_custom_frame,
                                        font=('Arial', 10),
                                        width=8,
                                        bg='#3a3a3a',
                                        fg='white',
                                        insertbackground='white')
        self.entry_dias_extra.pack(anchor='w', pady=2)
        self.entry_dias_extra.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
    
    def crear_campos_años(self):
        """Crear campos para años y meses"""
        # Años
        tk.Label(self.campos_custom_frame,
                text="🗓️ Años:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        self.entry_años = tk.Entry(self.campos_custom_frame,
                                  font=('Arial', 10),
                                  width=8,
                                  bg='#3a3a3a',
                                  fg='white',
                                  insertbackground='white')
        self.entry_años.pack(anchor='w', pady=2)
        self.entry_años.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
        
        # Meses adicionales
        tk.Label(self.campos_custom_frame,
                text="📆 Meses adicionales:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 9)).pack(anchor='w', pady=(10, 0))
        
        self.entry_meses_extra = tk.Entry(self.campos_custom_frame,
                                         font=('Arial', 10),
                                         width=8,
                                         bg='#3a3a3a',
                                         fg='white',
                                         insertbackground='white')
        self.entry_meses_extra.pack(anchor='w', pady=2)
        self.entry_meses_extra.bind('<KeyRelease>', self.actualizar_ejemplo_custom)
    
    def on_unidad_custom_change(self, event=None):
        """Manejar cambio en la unidad personalizada"""
        self.crear_campos_custom()
        self.actualizar_ejemplo_custom()
    
    def actualizar_ejemplo_custom(self, event=None):
        """Actualizar el ejemplo de tiempo personalizado"""
        try:
            unidad = self.combo_unidad_custom.get()
            total_minutos = 0
            
            if unidad == "Minutos":
                minutos = int(self.entry_minutos.get() or "0")
                total_minutos = minutos
                ejemplo = f"{minutos} minutos"
                
            elif unidad == "Horas":
                horas = int(self.entry_horas.get() or "0")
                minutos_extra = int(self.entry_minutos_extra.get() or "0")
                total_minutos = (horas * 60) + minutos_extra
                ejemplo = f"{horas}h {minutos_extra}min = {total_minutos} minutos"
                
            elif unidad == "Días":
                dias = int(self.entry_dias.get() or "0")
                horas_extra = int(self.entry_horas_extra.get() or "0")
                total_minutos = (dias * 24 * 60) + (horas_extra * 60)
                ejemplo = f"{dias} días {horas_extra}h = {total_minutos//60//24} días {(total_minutos//60)%24}h"
                
            elif unidad == "Meses":
                meses = int(self.entry_meses.get() or "0")
                dias_extra = int(self.entry_dias_extra.get() or "0")
                total_minutos = (meses * 30 * 24 * 60) + (dias_extra * 24 * 60)
                total_dias = total_minutos // (24 * 60)
                ejemplo = f"{meses} meses {dias_extra} días = {total_dias} días total"
                
            elif unidad == "Años":
                años = int(self.entry_años.get() or "0")
                meses_extra = int(self.entry_meses_extra.get() or "0")
                total_minutos = (años * 365 * 24 * 60) + (meses_extra * 30 * 24 * 60)
                total_dias = total_minutos // (24 * 60)
                ejemplo = f"{años} años {meses_extra} meses = {total_dias} días total"
            
            self.label_ejemplo.config(text=f"Ejemplo: {ejemplo}")
            
        except ValueError:
            self.label_ejemplo.config(text="Ingresa números válidos")
    
    def usar_fecha_hoy(self):
        """Usar la fecha de hoy como inicio"""
        self.fecha_inicio = datetime.now()
        self.label_fecha.config(text=f"Fecha: {self.fecha_inicio.strftime('%d/%m/%Y')}")
    
    def elegir_fecha(self):
        """Elegir fecha personalizada"""
        from tkinter import simpledialog
        
        fecha_str = simpledialog.askstring(
            "Fecha de Inicio",
            "Ingresa la fecha de inicio (DD/MM/YYYY):",
            initialvalue=datetime.now().strftime('%d/%m/%Y')
        )
        
        if fecha_str:
            try:
                self.fecha_inicio = datetime.strptime(fecha_str, '%d/%m/%Y')
                self.label_fecha.config(text=f"Fecha: {fecha_str}")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/YYYY")
    
    def calcular_fecha_vencimiento(self, fecha_inicio, duracion):
        """Calcular fecha de vencimiento según la duración"""
        if duracion == "Indefinido":
            return None
        elif duracion == "Personalizado":
            try:
                unidad = self.combo_unidad_custom.get()
                total_minutos = 0
                
                if unidad == "Minutos":
                    minutos = int(self.entry_minutos.get() or "0")
                    total_minutos = minutos
                    
                elif unidad == "Horas":
                    horas = int(self.entry_horas.get() or "0")
                    minutos_extra = int(self.entry_minutos_extra.get() or "0")
                    total_minutos = (horas * 60) + minutos_extra
                    
                elif unidad == "Días":
                    dias = int(self.entry_dias.get() or "0")
                    horas_extra = int(self.entry_horas_extra.get() or "0")
                    total_minutos = (dias * 24 * 60) + (horas_extra * 60)
                    
                elif unidad == "Meses":
                    meses = int(self.entry_meses.get() or "0")
                    dias_extra = int(self.entry_dias_extra.get() or "0")
                    total_minutos = (meses * 30 * 24 * 60) + (dias_extra * 24 * 60)
                    
                elif unidad == "Años":
                    años = int(self.entry_años.get() or "0")
                    meses_extra = int(self.entry_meses_extra.get() or "0")
                    total_minutos = (años * 365 * 24 * 60) + (meses_extra * 30 * 24 * 60)
                
                if total_minutos <= 0:
                    messagebox.showerror("Error", "Debe ingresar al menos un valor mayor a 0")
                    return None
                
                return fecha_inicio + timedelta(minutes=total_minutos)
                    
            except ValueError:
                messagebox.showerror("Error", "Ingrese números válidos en todos los campos")
                return None
        else:
            # Parsear duración estándar
            if "mes" in duracion:
                meses = int(duracion.split()[0])
                # Aproximación: 1 mes = 30 días
                return fecha_inicio + timedelta(days=meses * 30)
            elif "año" in duracion:
                años = int(duracion.split()[0])
                return fecha_inicio + timedelta(days=años * 365)
        
        return None
    
    def agregar_suscripcion(self):
        """Agregar nueva suscripción"""
        # Validar campos
        usuario = self.entry_usuario.get().strip()
        correo = self.entry_correo.get().strip()
        password = self.entry_password.get().strip()
        pin = self.entry_pin.get().strip()
        servicio = self.combo_servicio.get()
        duracion = self.combo_duracion.get()
        notas = self.text_notas.get("1.0", tk.END).strip()
        
        if not usuario:
            messagebox.showerror("Error", "El nombre de usuario es obligatorio")
            return
        
        if not servicio:
            messagebox.showerror("Error", "Seleccione un servicio")
            return
        
        # Calcular fecha de vencimiento
        fecha_vencimiento = self.calcular_fecha_vencimiento(self.fecha_inicio, duracion)
        
        if duracion != "Indefinido" and fecha_vencimiento is None:
            return  # Error ya mostrado en calcular_fecha_vencimiento
        
        # Crear suscripción
        suscripcion = {
            'id': len(self.suscripciones) + 1,
            'usuario': usuario,
            'correo': correo,
            'password': password,
            'pin': pin,
            'servicio': servicio,
            'duracion': duracion,
            'fecha_inicio': self.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_vencimiento': fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S') if fecha_vencimiento else None,
            'notas': notas,
            'activa': True,
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Agregar a la lista
        self.suscripciones.append(suscripcion)
        
        # Guardar datos
        self.guardar_datos()
        
        # Actualizar interfaz
        self.actualizar_lista()
        
        # Limpiar formulario
        self.limpiar_formulario()
        
        # Mostrar confirmación
        venc_text = fecha_vencimiento.strftime('%d/%m/%Y') if fecha_vencimiento else "Sin vencimiento"
        messagebox.showinfo(
            "Suscripción Agregada",
            f"✅ Suscripción agregada exitosamente:\n\n"
            f"👤 Usuario: {usuario}\n"
            f"📺 Servicio: {servicio}\n"
            f"⏰ Duración: {duracion}\n"
            f"📅 Vence: {venc_text}"
        )
    
    def limpiar_formulario(self):
        """Limpiar campos del formulario"""
        self.entry_usuario.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_pin.delete(0, tk.END)
        self.combo_servicio.set("Netflix")
        self.combo_duracion.set("1 mes")
        self.text_notas.delete("1.0", tk.END)
        self.combo_unidad_custom.set("Días")
        self.custom_frame.pack_forget()
        self.usar_fecha_hoy()
        
        # Limpiar todos los campos personalizados posibles
        campos_custom = ['entry_minutos', 'entry_horas', 'entry_minutos_extra', 
                        'entry_dias', 'entry_horas_extra', 'entry_meses', 
                        'entry_dias_extra', 'entry_años', 'entry_meses_extra']
        
        for campo in campos_custom:
            try:
                if hasattr(self, campo):
                    widget = getattr(self, campo)
                    if widget.winfo_exists():
                        widget.delete(0, tk.END)
            except:
                pass  # Ignorar errores de widgets que ya no existen
    
    def actualizar_lista(self):
        """Actualizar la lista de suscripciones"""
        # Limpiar lista actual
        for widget in self.scrollable_frame_lista.winfo_children():
            widget.destroy()
        
        # Filtrar suscripciones activas
        suscripciones_activas = [s for s in self.suscripciones if s['activa']]
        
        # Actualizar contador
        self.label_contador.config(text=f"({len(suscripciones_activas)} activas)")
        
        if not suscripciones_activas:
            # Mostrar mensaje cuando no hay suscripciones
            no_subs_label = tk.Label(self.scrollable_frame_lista,
                                   text="📭 No hay suscripciones activas\n\nAgrega una nueva suscripción para comenzar",
                                   bg='#1a1a1a',
                                   fg='#CCCCCC',
                                   font=('Arial', 12),
                                   justify='center')
            no_subs_label.pack(expand=True, pady=50)
            return
        
        # Ordenar por fecha de vencimiento (próximas a vencer primero)
        suscripciones_ordenadas = sorted(suscripciones_activas, 
                                       key=lambda x: x['fecha_vencimiento'] if x['fecha_vencimiento'] else '9999-12-31')
        
        # Mostrar cada suscripción
        for i, suscripcion in enumerate(suscripciones_ordenadas):
            self.crear_widget_suscripcion(self.scrollable_frame_lista, suscripcion, i)
        
        # Actualizar título con contador
        self.actualizar_titulo()
    
    def actualizar_titulo(self):
        """Actualizar el título de la ventana con información de estado"""
        try:
            # Contar suscripciones por estado
            activas = len([s for s in self.suscripciones if s['activa']])
            vencimientos_proximos = len(self.obtener_vencimientos_proximos(7))
            criticas = len([s for s in self.suscripciones if s['activa'] and s['fecha_vencimiento'] and 
                           (datetime.strptime(s['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S') - datetime.now()).days <= 1])
            
            # Crear título dinámico
            titulo_base = "DaniStore - Streaming"
            
            if criticas > 0:
                titulo = f"{titulo_base} 🚨 {criticas} CRÍTICAS"
            elif vencimientos_proximos > 0:
                titulo = f"{titulo_base} ⚠️ {vencimientos_proximos} próximas"
            elif activas > 0:
                titulo = f"{titulo_base} ✅ {activas} activas"
            else:
                titulo = titulo_base
            
            self.root.title(titulo)
        except Exception as e:
            self.root.title("DaniStore - Streaming")
    
    def crear_widget_suscripcion(self, parent, suscripcion, indice):
        """Crear widget para mostrar una suscripción"""
        # Determinar estado y color
        estado_info = self.obtener_estado_suscripcion(suscripcion)
        
        # Frame principal
        suscripcion_frame = tk.Frame(parent, bg=estado_info['color_bg'], relief='solid', bd=2)
        suscripcion_frame.pack(fill='x', padx=5, pady=5)
        
        # Frame interno
        inner_frame = tk.Frame(suscripcion_frame, bg=estado_info['color_bg'])
        inner_frame.pack(fill='x', padx=10, pady=8)
        
        # Información principal (lado izquierdo)
        info_frame = tk.Frame(inner_frame, bg=estado_info['color_bg'])
        info_frame.pack(side='left', fill='x', expand=True)
        
        # Usuario y servicio
        titulo_label = tk.Label(info_frame,
                              text=f"👤 {suscripcion['usuario']} - 📺 {suscripcion['servicio']}",
                              bg=estado_info['color_bg'],
                              fg=estado_info['color_text'],
                              font=('Arial', 12, 'bold'))
        titulo_label.pack(anchor='w')
        
        # Información de cuenta
        cuenta_info = []
        if suscripcion.get('correo'):
            cuenta_info.append(f"📧 {suscripcion['correo']}")
        if suscripcion.get('pin'):
            cuenta_info.append(f"📱 PIN: {suscripcion['pin']}")
        
        if cuenta_info:
            cuenta_text = " | ".join(cuenta_info)
            cuenta_label = tk.Label(info_frame,
                                  text=cuenta_text,
                                  bg=estado_info['color_bg'],
                                  fg=estado_info['color_text_secondary'],
                                  font=('Arial', 9))
            cuenta_label.pack(anchor='w', pady=(2, 0))
        
        # Fechas
        fecha_inicio = datetime.strptime(suscripcion['fecha_inicio'], '%Y-%m-%d %H:%M:%S')
        fecha_inicio_str = fecha_inicio.strftime('%d/%m/%Y')
        
        if suscripcion['fecha_vencimiento']:
            fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
            fecha_venc_str = fecha_venc.strftime('%d/%m/%Y')
            fechas_text = f"📅 Inicio: {fecha_inicio_str} | 🔚 Vence: {fecha_venc_str}"
        else:
            fechas_text = f"📅 Inicio: {fecha_inicio_str} | ♾️ Sin vencimiento"
        
        fechas_label = tk.Label(info_frame,
                              text=fechas_text,
                              bg=estado_info['color_bg'],
                              fg=estado_info['color_text_secondary'],
                              font=('Arial', 9))
        fechas_label.pack(anchor='w', pady=(2, 0))
        
        # Estado y tiempo restante
        estado_label = tk.Label(info_frame,
                              text=estado_info['texto'],
                              bg=estado_info['color_bg'],
                              fg=estado_info['color_estado'],
                              font=('Arial', 10, 'bold'))
        estado_label.pack(anchor='w', pady=(2, 0))
        
        # Notas si existen
        if suscripcion['notas']:
            notas_label = tk.Label(info_frame,
                                 text=f"📝 {suscripcion['notas'][:50]}{'...' if len(suscripcion['notas']) > 50 else ''}",
                                 bg=estado_info['color_bg'],
                                 fg=estado_info['color_text_secondary'],
                                 font=('Arial', 8))
            notas_label.pack(anchor='w', pady=(2, 0))
        
        # Botones (lado derecho)
        botones_frame = tk.Frame(inner_frame, bg=estado_info['color_bg'])
        botones_frame.pack(side='right', padx=10)
        
        # Botón Renovar
        renovar_btn = tk.Button(botones_frame,
                              text="🔄 Renovar",
                              bg='#4CAF50',
                              fg='white',
                              font=('Arial', 9, 'bold'),
                              command=lambda s=suscripcion: self.renovar_suscripcion(s.get('id', s.get('usuario', '') + s.get('servicio', ''))))
        renovar_btn.pack(pady=2)
        
        # Botón Editar
        editar_btn = tk.Button(botones_frame,
                             text="✏️ Editar",
                             bg='#FF9800',
                             fg='white',
                             font=('Arial', 9, 'bold'),
                             command=lambda s=suscripcion: self.editar_suscripcion(s.get('id', s.get('usuario', '') + s.get('servicio', ''))))
        editar_btn.pack(pady=2)
        
        # Botón Eliminar
        eliminar_btn = tk.Button(botones_frame,
                               text="🗑️ Eliminar",
                               bg='#F44336',
                               fg='white',
                               font=('Arial', 9, 'bold'),
                               command=lambda s=suscripcion: self.eliminar_suscripcion(s.get('id', s.get('usuario', '') + s.get('servicio', ''))))
        eliminar_btn.pack(pady=2)
        
        # Botón Copiar para WhatsApp
        whatsapp_btn = tk.Button(botones_frame,
                               text="📱 WhatsApp",
                               bg='#25D366',
                               fg='white',
                               font=('Arial', 9, 'bold'),
                               command=lambda s=suscripcion: self.copiar_para_whatsapp(s))
        whatsapp_btn.pack(pady=2)
    
    def copiar_para_whatsapp(self, suscripcion=None):
        """Generar y copiar mensaje profesional para WhatsApp"""
        try:
            # Si no se pasa suscripción, usar los datos del formulario
            if suscripcion is None:
                usuario = self.entry_usuario.get().strip()
                servicio = self.combo_servicio.get()
                correo = self.entry_correo.get().strip()
                password = self.entry_password.get().strip()
                pin = self.entry_pin.get().strip()
                
                # Validar que al menos usuario y servicio estén llenos
                if not usuario or not servicio:
                    from tkinter import messagebox
                    messagebox.showerror("Error", "Completa al menos el Usuario y Servicio para generar el mensaje")
                    return
                
                # Calcular fecha de vencimiento
                duracion = self.combo_duracion.get()
                fecha_vencimiento = self.calcular_fecha_vencimiento(self.fecha_inicio, duracion)
                fecha_venc_str = fecha_vencimiento.strftime('%d/%m/%Y') if fecha_vencimiento else 'Sin vencimiento'
            else:
                # Usar datos de la suscripción existente
                usuario = suscripcion.get('usuario', 'Cliente')
                servicio = suscripcion.get('servicio', 'Servicio')
                correo = suscripcion.get('correo', 'No especificado')
                password = suscripcion.get('password', 'No especificada')
                pin = suscripcion.get('pin', 'No especificado')
                
                # Obtener fecha de vencimiento
                if suscripcion.get('fecha_vencimiento'):
                    fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
                    fecha_venc_str = fecha_venc.strftime('%d/%m/%Y')
                else:
                    fecha_venc_str = 'Sin vencimiento'
            
            # Generar mensaje profesional y elegante
            mensaje = f"""🎬 ¡Tu cuenta {servicio} está lista! 🎬

✨ DATOS DE ACCESO ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 PERFIL: {usuario}
📧 CORREO: {correo}
🔒 CONTRASEÑA: {password}
📱 PIN: {pin}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 VÁLIDA HASTA: {fecha_venc_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 ¡DISFRUTA TU ENTRETENIMIENTO! 🔥

📌 IMPORTANTE:
• Guarda estos datos en un lugar seguro
• No compartas tu información con terceros
• Recuerda que es para UN SOLO DISPOSITIVO para evitar la expulsión de tu perfil
• Si adquiriste para 1 o más dispositivos, ignora el mensaje anterior
• Cualquier duda, contáctame

� Gracias por confiar en DaniStore
🚀 ¡Tu entretenimiento sin límites!"""

            # Copiar al portapapeles
            import pyperclip
            pyperclip.copy(mensaje)
            
            # Mostrar confirmación
            from tkinter import messagebox
            messagebox.showinfo(
                "📱 Copiado para WhatsApp",
                f"✅ Mensaje copiado al portapapeles\n\n"
                f"📱 Servicio: {servicio}\n"
                f"👤 Cliente: {usuario}\n\n"
                f"🚀 ¡Listo para enviar por WhatsApp!"
            )
            
        except ImportError:
            # Si no está pyperclip, mostrar el mensaje para copiar manualmente
            self.mostrar_mensaje_manual(suscripcion)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al copiar mensaje: {e}")
    
    def mostrar_mensaje_manual(self, suscripcion):
        """Mostrar mensaje en ventana para copiar manualmente"""
        # Generar mensaje
        usuario = suscripcion.get('usuario', 'Cliente')
        servicio = suscripcion.get('servicio', 'Servicio')
        correo = suscripcion.get('correo', 'No especificado')
        password = suscripcion.get('password', 'No especificada')
        pin = suscripcion.get('pin', 'No especificado')
        
        if suscripcion.get('fecha_vencimiento'):
            fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
            fecha_venc_str = fecha_venc.strftime('%d/%m/%Y')
        else:
            fecha_venc_str = 'Sin vencimiento'
        
        mensaje = f"""🎬 ¡Tu cuenta {servicio} está lista! 🎬

✨ DATOS DE ACCESO ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 PERFIL: {usuario}
📧 CORREO: {correo}
🔒 CONTRASEÑA: {password}
📱 PIN: {pin}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 VÁLIDA HASTA: {fecha_venc_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 ¡DISFRUTA TU ENTRETENIMIENTO! 🔥

📌 IMPORTANTE:
• Guarda estos datos en un lugar seguro
• No compartas tu información con terceros
• Cualquier duda, contáctame

💎 Gracias por confiar en DaniStore
🚀 ¡Tu entretenimiento sin límites!"""
        
        # Crear ventana para mostrar el mensaje
        ventana_mensaje = tk.Toplevel(self.root)
        ventana_mensaje.title("📱 Mensaje para WhatsApp")
        ventana_mensaje.geometry("500x600")
        ventana_mensaje.configure(bg='#1a1a1a')
        ventana_mensaje.transient(self.root)
        ventana_mensaje.grab_set()
        
        # Título
        tk.Label(ventana_mensaje,
                text="📱 MENSAJE PARA WHATSAPP",
                bg='#1a1a1a',
                fg='#25D366',
                font=('Arial', 14, 'bold')).pack(pady=15)
        
        # Área de texto
        text_frame = tk.Frame(ventana_mensaje, bg='#1a1a1a')
        text_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        text_area = tk.Text(text_frame,
                           bg='#2a2a2a',
                           fg='white',
                           font=('Arial', 10),
                           wrap='word',
                           selectbackground='#4a4a4a')
        text_area.pack(fill='both', expand=True)
        
        # Insertar mensaje
        text_area.insert('1.0', mensaje)
        text_area.config(state='normal')  # Permitir selección
        
        # Botones
        botones_frame = tk.Frame(ventana_mensaje, bg='#1a1a1a')
        botones_frame.pack(pady=15)
        
        def seleccionar_todo():
            text_area.select_range('1.0', 'end')
            text_area.focus()
        
        tk.Button(botones_frame,
                 text="📋 Seleccionar Todo",
                 bg='#25D366',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 command=seleccionar_todo,
                 padx=20).pack(side='left', padx=10)
        
        tk.Button(botones_frame,
                 text="✅ Cerrar",
                 bg='#4CAF50',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 command=ventana_mensaje.destroy,
                 padx=20).pack(side='left', padx=10)
        
        # Seleccionar todo automáticamente
        text_area.select_range('1.0', 'end')
        text_area.focus()
    
    def obtener_estado_suscripcion(self, suscripcion):
        """Obtener información del estado de la suscripción"""
        if not suscripcion['fecha_vencimiento']:
            return {
                'texto': '♾️ Sin vencimiento',
                'color_bg': '#2a4a2a',
                'color_text': '#90EE90',
                'color_text_secondary': '#CCCCCC',
                'color_estado': '#90EE90'
            }
        
        fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
        ahora = datetime.now()
        diferencia = fecha_venc - ahora
        
        if diferencia.days < 0:
            # Vencida
            dias_vencida = abs(diferencia.days)
            return {
                'texto': f'❌ Vencida hace {dias_vencida} día{"s" if dias_vencida != 1 else ""}',
                'color_bg': '#4a2a2a',
                'color_text': '#FFB6C1',
                'color_text_secondary': '#CCCCCC',
                'color_estado': '#FF6B6B'
            }
        elif diferencia.days <= 3:
            # Por vencer (crítico)
            return {
                'texto': f'⚠️ Vence en {diferencia.days} día{"s" if diferencia.days != 1 else ""} - ¡CRÍTICO!',
                'color_bg': '#4a3a2a',
                'color_text': '#FFD700',
                'color_text_secondary': '#CCCCCC',
                'color_estado': '#FF8C00'
            }
        elif diferencia.days <= 7:
            # Por vencer (advertencia)
            return {
                'texto': f'⚡ Vence en {diferencia.days} días',
                'color_bg': '#3a3a4a',
                'color_text': '#87CEEB',
                'color_text_secondary': '#CCCCCC',
                'color_estado': '#FFA500'
            }
        else:
            # Activa
            return {
                'texto': f'✅ Activa - {diferencia.days} días restantes',
                'color_bg': '#2a4a2a',
                'color_text': '#90EE90',
                'color_text_secondary': '#CCCCCC',
                'color_estado': '#90EE90'
            }
    
    def renovar_suscripcion(self, suscripcion_id):
        """Renovar una suscripción"""
        # Buscar por ID o por combinación usuario+servicio
        suscripcion = None
        for s in self.suscripciones:
            if (s.get('id') == suscripcion_id or 
                (s.get('usuario', '') + s.get('servicio', '')) == suscripcion_id):
                suscripcion = s
                break
        if not suscripcion:
            return
        
        # Ventana de renovación
        ventana_renovar = tk.Toplevel(self.root)
        ventana_renovar.title("🔄 Renovar Suscripción")
        ventana_renovar.geometry("400x300")
        ventana_renovar.configure(bg='#2a2a2a')
        ventana_renovar.transient(self.root)
        ventana_renovar.grab_set()
        
        # Título
        tk.Label(ventana_renovar,
                text=f"🔄 Renovar: {suscripcion['usuario']} - {suscripcion['servicio']}",
                bg='#2a2a2a',
                fg='#FFD700',
                font=('Arial', 12, 'bold')).pack(pady=20)
        
        # Nueva duración
        tk.Label(ventana_renovar,
                text="⏰ Nueva duración:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        combo_nueva_duracion = ttk.Combobox(ventana_renovar,
                                          values=["1 mes", "2 meses", "3 meses", "6 meses", 
                                                 "1 año", "2 años", "Indefinido"],
                                          font=('Arial', 11),
                                          width=15,
                                          state='readonly')
        combo_nueva_duracion.pack(pady=5)
        combo_nueva_duracion.set("1 mes")
        
        # Fecha de inicio de renovación
        tk.Label(ventana_renovar,
                text="📅 Renovar desde:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(pady=(15, 5))
        
        fecha_renovacion = tk.StringVar()
        
        def usar_hoy():
            fecha_renovacion.set("hoy")
            label_fecha_renovar.config(text="Fecha: Hoy")
        
        def usar_vencimiento():
            if suscripcion['fecha_vencimiento']:
                fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
                fecha_renovacion.set("vencimiento")
                label_fecha_renovar.config(text=f"Fecha: {fecha_venc.strftime('%d/%m/%Y')}")
            else:
                usar_hoy()
        
        botones_fecha_frame = tk.Frame(ventana_renovar, bg='#2a2a2a')
        botones_fecha_frame.pack(pady=5)
        
        tk.Button(botones_fecha_frame,
                 text="📅 Desde Hoy",
                 bg='#4CAF50',
                 fg='white',
                 font=('Arial', 9),
                 command=usar_hoy).pack(side='left', padx=5)
        
        tk.Button(botones_fecha_frame,
                 text="📅 Desde Vencimiento",
                 bg='#2196F3',
                 fg='white',
                 font=('Arial', 9),
                 command=usar_vencimiento).pack(side='left', padx=5)
        
        label_fecha_renovar = tk.Label(ventana_renovar,
                                     text="Fecha: Hoy",
                                     bg='#2a2a2a',
                                     fg='#90EE90',
                                     font=('Arial', 9))
        label_fecha_renovar.pack(pady=5)
        
        usar_hoy()  # Por defecto desde hoy
        
        def confirmar_renovacion():
            nueva_duracion = combo_nueva_duracion.get()
            if not nueva_duracion:
                messagebox.showerror("Error", "Seleccione una duración")
                return
            
            # Determinar fecha de inicio
            if fecha_renovacion.get() == "vencimiento" and suscripcion['fecha_vencimiento']:
                fecha_inicio_renovacion = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
            else:
                fecha_inicio_renovacion = datetime.now()
            
            # Calcular nueva fecha de vencimiento
            if nueva_duracion == "Indefinido":
                nueva_fecha_vencimiento = None
            elif "mes" in nueva_duracion:
                meses = int(nueva_duracion.split()[0])
                nueva_fecha_vencimiento = fecha_inicio_renovacion + timedelta(days=meses * 30)
            elif "año" in nueva_duracion:
                años = int(nueva_duracion.split()[0])
                nueva_fecha_vencimiento = fecha_inicio_renovacion + timedelta(days=años * 365)
            
            # Actualizar suscripción
            suscripcion['duracion'] = nueva_duracion
            suscripcion['fecha_inicio'] = fecha_inicio_renovacion.strftime('%Y-%m-%d %H:%M:%S')
            suscripcion['fecha_vencimiento'] = nueva_fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S') if nueva_fecha_vencimiento else None
            suscripcion['activa'] = True
            
            # Guardar y actualizar
            self.guardar_datos()
            self.actualizar_lista()
            
            ventana_renovar.destroy()
            
            venc_text = nueva_fecha_vencimiento.strftime('%d/%m/%Y') if nueva_fecha_vencimiento else "Sin vencimiento"
            messagebox.showinfo(
                "Renovación Exitosa",
                f"✅ Suscripción renovada exitosamente:\n\n"
                f"👤 Usuario: {suscripcion['usuario']}\n"
                f"📺 Servicio: {suscripcion['servicio']}\n"
                f"⏰ Nueva duración: {nueva_duracion}\n"
                f"📅 Nuevo vencimiento: {venc_text}"
            )
        
        # Botones
        botones_frame = tk.Frame(ventana_renovar, bg='#2a2a2a')
        botones_frame.pack(pady=20)
        
        tk.Button(botones_frame,
                 text="✅ Renovar",
                 bg='#4CAF50',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 command=confirmar_renovacion).pack(side='left', padx=10)
        
        tk.Button(botones_frame,
                 text="❌ Cancelar",
                 bg='#F44336',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 command=ventana_renovar.destroy).pack(side='left', padx=10)
    
    def editar_suscripcion(self, suscripcion_id):
        """Editar una suscripción"""
        # Buscar por ID o por combinación usuario+servicio
        suscripcion = None
        for s in self.suscripciones:
            if (s.get('id') == suscripcion_id or 
                (s.get('usuario', '') + s.get('servicio', '')) == suscripcion_id):
                suscripcion = s
                break
        if not suscripcion:
            return
        
        # Ventana de edición
        ventana_editar = tk.Toplevel(self.root)
        ventana_editar.title("✏️ Editar Suscripción")
        ventana_editar.geometry("450x600")
        ventana_editar.configure(bg='#2a2a2a')
        ventana_editar.transient(self.root)
        ventana_editar.grab_set()
        
        # Título
        tk.Label(ventana_editar,
                text="✏️ Editar Suscripción",
                bg='#2a2a2a',
                fg='#FFD700',
                font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Campo Usuario
        tk.Label(ventana_editar,
                text="👤 Nombre de Usuario:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        entry_usuario_edit = tk.Entry(ventana_editar,
                                     font=('Arial', 11),
                                     width=25,
                                     bg='#3a3a3a',
                                     fg='white',
                                     insertbackground='white')
        entry_usuario_edit.pack(pady=5)
        entry_usuario_edit.insert(0, suscripcion['usuario'])
        
        # Campo Correo
        tk.Label(ventana_editar,
                text="📧 Correo Electrónico:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        entry_correo_edit = tk.Entry(ventana_editar,
                                   font=('Arial', 11),
                                   width=25,
                                   bg='#3a3a3a',
                                   fg='white',
                                   insertbackground='white')
        entry_correo_edit.pack(pady=5)
        entry_correo_edit.insert(0, suscripcion.get('correo', ''))
        
        # Campo Contraseña
        tk.Label(ventana_editar,
                text="🔒 Contraseña:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        entry_password_edit = tk.Entry(ventana_editar,
                                     font=('Arial', 11),
                                     width=25,
                                     bg='#3a3a3a',
                                     fg='white',
                                     insertbackground='white',
                                     show='*')
        entry_password_edit.pack(pady=5)
        entry_password_edit.insert(0, suscripcion.get('password', ''))
        
        # Campo PIN
        tk.Label(ventana_editar,
                text="📱 PIN del Perfil:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        entry_pin_edit = tk.Entry(ventana_editar,
                                font=('Arial', 11),
                                width=25,
                                bg='#3a3a3a',
                                fg='white',
                                insertbackground='white')
        entry_pin_edit.pack(pady=5)
        entry_pin_edit.insert(0, suscripcion.get('pin', ''))
        
        # Campo Servicio
        tk.Label(ventana_editar,
                text="📺 Servicio:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        combo_servicio_edit = ttk.Combobox(ventana_editar,
                                          values=self.servicios,
                                          font=('Arial', 11),
                                          width=22,
                                          state='readonly')
        combo_servicio_edit.pack(pady=5)
        combo_servicio_edit.set(suscripcion['servicio'])
        
        # Campo Notas
        tk.Label(ventana_editar,
                text="📝 Notas:",
                bg='#2a2a2a',
                fg='#CCCCCC',
                font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        text_notas_edit = tk.Text(ventana_editar,
                                 font=('Arial', 10),
                                 width=30,
                                 height=4,
                                 bg='#3a3a3a',
                                 fg='white',
                                 insertbackground='white')
        text_notas_edit.pack(pady=5)
        text_notas_edit.insert("1.0", suscripcion['notas'])
        
        def guardar_cambios():
            nuevo_usuario = entry_usuario_edit.get().strip()
            nuevo_correo = entry_correo_edit.get().strip()
            nuevo_password = entry_password_edit.get().strip()
            nuevo_pin = entry_pin_edit.get().strip()
            nuevo_servicio = combo_servicio_edit.get()
            nuevas_notas = text_notas_edit.get("1.0", tk.END).strip()
            
            if not nuevo_usuario:
                messagebox.showerror("Error", "El nombre de usuario es obligatorio")
                return
            
            # Actualizar suscripción
            suscripcion['usuario'] = nuevo_usuario
            suscripcion['correo'] = nuevo_correo
            suscripcion['password'] = nuevo_password
            suscripcion['pin'] = nuevo_pin
            suscripcion['servicio'] = nuevo_servicio
            suscripcion['notas'] = nuevas_notas
            
            # Guardar y actualizar
            self.guardar_datos()
            self.actualizar_lista()
            
            ventana_editar.destroy()
            messagebox.showinfo("Éxito", "Suscripción actualizada exitosamente")
        
        # Botones
        botones_frame = tk.Frame(ventana_editar, bg='#2a2a2a')
        botones_frame.pack(pady=20)
        
        tk.Button(botones_frame,
                 text="💾 Guardar",
                 bg='#4CAF50',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 command=guardar_cambios).pack(side='left', padx=10)
        
        tk.Button(botones_frame,
                 text="❌ Cancelar",
                 bg='#F44336',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 command=ventana_editar.destroy).pack(side='left', padx=10)
    
    def eliminar_suscripcion(self, suscripcion_id):
        """Eliminar una suscripción"""
        # Buscar por ID o por combinación usuario+servicio
        suscripcion = None
        for s in self.suscripciones:
            if (s.get('id') == suscripcion_id or 
                (s.get('usuario', '') + s.get('servicio', '')) == suscripcion_id):
                suscripcion = s
                break
        if not suscripcion:
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar la suscripción?\n\n"
            f"👤 Usuario: {suscripcion['usuario']}\n"
            f"📺 Servicio: {suscripcion['servicio']}\n\n"
            f"Esta acción no se puede deshacer."
        )
        
        if respuesta:
            # Marcar como inactiva en lugar de eliminar (para mantener historial)
            suscripcion['activa'] = False
            
            # Guardar y actualizar
            self.guardar_datos()
            self.actualizar_lista()
            
            messagebox.showinfo("Éxito", "Suscripción eliminada exitosamente")
    
    def verificar_vencimientos_manual(self):
        """Verificar vencimientos manualmente"""
        vencimientos = self.obtener_vencimientos_proximos()
        
        if not vencimientos:
            messagebox.showinfo(
                "Sin Vencimientos",
                "🎉 ¡Excelente!\n\nNo hay suscripciones próximas a vencer en los próximos 7 días."
            )
            return
        
        # Mostrar ventana con vencimientos
        self.mostrar_ventana_vencimientos(vencimientos)
    
    def obtener_vencimientos_proximos(self, dias_adelante=7):
        """Obtener suscripciones que vencen en los próximos días"""
        vencimientos = []
        ahora = datetime.now()
        
        for suscripcion in self.suscripciones:
            if not suscripcion['activa'] or not suscripcion['fecha_vencimiento']:
                continue
            
            fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
            diferencia = fecha_venc - ahora
            
            # Incluir vencidas y próximas a vencer
            if diferencia.days <= dias_adelante:
                vencimientos.append({
                    'suscripcion': suscripcion,
                    'dias_restantes': diferencia.days,
                    'vencida': diferencia.days < 0
                })
        
        return sorted(vencimientos, key=lambda x: x['dias_restantes'])
    
    def mostrar_ventana_vencimientos(self, vencimientos):
        """Mostrar ventana con vencimientos próximos"""
        ventana_venc = tk.Toplevel(self.root)
        ventana_venc.title("🔔 Vencimientos Próximos")
        ventana_venc.geometry("600x500")
        ventana_venc.configure(bg='#2a2a2a')
        ventana_venc.transient(self.root)
        
        # Título
        tk.Label(ventana_venc,
                text="🔔 Suscripciones Próximas a Vencer",
                bg='#2a2a2a',
                fg='#FFD700',
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Frame con scroll
        scroll_frame = tk.Frame(ventana_venc, bg='#2a2a2a')
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        canvas_venc = tk.Canvas(scroll_frame, bg='#1a1a1a')
        scrollbar_venc = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas_venc.yview)
        scrollable_frame_venc = tk.Frame(canvas_venc, bg='#1a1a1a')
        
        scrollable_frame_venc.bind(
            "<Configure>",
            lambda e: canvas_venc.configure(scrollregion=canvas_venc.bbox("all"))
        )
        
        canvas_venc.create_window((0, 0), window=scrollable_frame_venc, anchor="nw")
        canvas_venc.configure(yscrollcommand=scrollbar_venc.set)
        
        # Mostrar cada vencimiento
        for venc in vencimientos:
            suscripcion = venc['suscripcion']
            dias = venc['dias_restantes']
            
            # Determinar color según urgencia
            if venc['vencida']:
                color_bg = '#4a2a2a'
                color_text = '#FFB6C1'
                icono = '❌'
                estado_text = f"Vencida hace {abs(dias)} día{'s' if abs(dias) != 1 else ''}"
            elif dias <= 1:
                color_bg = '#4a3a2a'
                color_text = '#FFD700'
                icono = '🚨'
                estado_text = "¡Vence HOY!" if dias == 0 else "¡Vence MAÑANA!"
            elif dias <= 3:
                color_bg = '#4a3a2a'
                color_text = '#FFA500'
                icono = '⚠️'
                estado_text = f"Vence en {dias} días - CRÍTICO"
            else:
                color_bg = '#3a3a4a'
                color_text = '#87CEEB'
                icono = '⚡'
                estado_text = f"Vence en {dias} días"
            
            # Frame del vencimiento
            venc_frame = tk.Frame(scrollable_frame_venc, bg=color_bg, relief='solid', bd=2)
            venc_frame.pack(fill='x', padx=5, pady=5)
            
            inner_frame = tk.Frame(venc_frame, bg=color_bg)
            inner_frame.pack(fill='x', padx=15, pady=10)
            
            # Información
            tk.Label(inner_frame,
                    text=f"{icono} {suscripcion['usuario']} - {suscripcion['servicio']}",
                    bg=color_bg,
                    fg=color_text,
                    font=('Arial', 12, 'bold')).pack(anchor='w')
            
            tk.Label(inner_frame,
                    text=estado_text,
                    bg=color_bg,
                    fg=color_text,
                    font=('Arial', 10, 'bold')).pack(anchor='w', pady=(2, 0))
            
            fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
            tk.Label(inner_frame,
                    text=f"📅 Fecha de vencimiento: {fecha_venc.strftime('%d/%m/%Y')}",
                    bg=color_bg,
                    fg='#CCCCCC',
                    font=('Arial', 9)).pack(anchor='w', pady=(2, 0))
        
        canvas_venc.pack(side="left", fill="both", expand=True)
        scrollbar_venc.pack(side="right", fill="y")
        
        # Botón cerrar
        tk.Button(ventana_venc,
                 text="✅ Entendido",
                 bg='#4CAF50',
                 fg='white',
                 font=('Arial', 12, 'bold'),
                 command=ventana_venc.destroy).pack(pady=20)
    
    def mostrar_estadisticas(self):
        """Mostrar estadísticas del sistema"""
        # Calcular estadísticas
        total_suscripciones = len([s for s in self.suscripciones if s['activa']])
        vencidas = len([s for s in self.suscripciones if s['activa'] and s['fecha_vencimiento'] and 
                       datetime.strptime(s['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S') < datetime.now()])
        proximas_vencer = len(self.obtener_vencimientos_proximos(7)) - vencidas
        indefinidas = len([s for s in self.suscripciones if s['activa'] and not s['fecha_vencimiento']])
        
        # Servicios más usados
        servicios_count = {}
        for s in self.suscripciones:
            if s['activa']:
                servicios_count[s['servicio']] = servicios_count.get(s['servicio'], 0) + 1
        
        servicio_top = max(servicios_count.items(), key=lambda x: x[1]) if servicios_count else ("Ninguno", 0)
        
        # Ventana de estadísticas
        ventana_stats = tk.Toplevel(self.root)
        ventana_stats.title("📊 Estadísticas")
        ventana_stats.geometry("500x400")
        ventana_stats.configure(bg='#2a2a2a')
        ventana_stats.transient(self.root)
        
        # Título
        tk.Label(ventana_stats,
                text="📊 Estadísticas del Sistema",
                bg='#2a2a2a',
                fg='#FFD700',
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Frame de estadísticas
        stats_frame = tk.Frame(ventana_stats, bg='#1a1a1a', relief='solid', bd=2)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Estadísticas generales
        tk.Label(stats_frame,
                text="📈 Resumen General",
                bg='#1a1a1a',
                fg='#FFD700',
                font=('Arial', 14, 'bold')).pack(pady=(15, 10))
        
        stats_text = f"""
📊 Total de suscripciones activas: {total_suscripciones}
❌ Suscripciones vencidas: {vencidas}
⚠️ Próximas a vencer (7 días): {proximas_vencer}
♾️ Suscripciones indefinidas: {indefinidas}
✅ Suscripciones al día: {total_suscripciones - vencidas - proximas_vencer}

🏆 Servicio más usado: {servicio_top[0]} ({servicio_top[1]} suscripciones)
        """
        
        tk.Label(stats_frame,
                text=stats_text,
                bg='#1a1a1a',
                fg='#CCCCCC',
                font=('Arial', 11),
                justify='left').pack(pady=10)
        
        # Servicios detallados
        if servicios_count:
            tk.Label(stats_frame,
                    text="📺 Distribución por Servicio",
                    bg='#1a1a1a',
                    fg='#FFD700',
                    font=('Arial', 12, 'bold')).pack(pady=(15, 10))
            
            servicios_ordenados = sorted(servicios_count.items(), key=lambda x: x[1], reverse=True)
            servicios_text = "\n".join([f"• {servicio}: {cantidad}" for servicio, cantidad in servicios_ordenados[:5]])
            
            tk.Label(stats_frame,
                    text=servicios_text,
                    bg='#1a1a1a',
                    fg='#90EE90',
                    font=('Arial', 10),
                    justify='left').pack(pady=5)
        
        # Botón cerrar
        tk.Button(ventana_stats,
                 text="✅ Cerrar",
                 bg='#4CAF50',
                 fg='white',
                 font=('Arial', 12, 'bold'),
                 command=ventana_stats.destroy).pack(pady=20)
    
    def exportar_datos(self):
        """Exportar datos a archivo de texto"""
        try:
            fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"suscripciones_export_{fecha_actual}.txt"
            
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("📺 REPORTE DE SUSCRIPCIONES - DANI666\n")
                f.write("=" * 60 + "\n")
                f.write(f"📅 Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                
                suscripciones_activas = [s for s in self.suscripciones if s['activa']]
                f.write(f"📊 Total de suscripciones activas: {len(suscripciones_activas)}\n\n")
                
                if suscripciones_activas:
                    f.write("DETALLE DE SUSCRIPCIONES:\n")
                    f.write("-" * 60 + "\n")
                    
                    for i, suscripcion in enumerate(suscripciones_activas, 1):
                        f.write(f"\n{i}. 👤 {suscripcion['usuario']} - 📺 {suscripcion['servicio']}\n")
                        
                        fecha_inicio = datetime.strptime(suscripcion['fecha_inicio'], '%Y-%m-%d %H:%M:%S')
                        f.write(f"   📅 Inicio: {fecha_inicio.strftime('%d/%m/%Y')}\n")
                        
                        if suscripcion['fecha_vencimiento']:
                            fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
                            f.write(f"   🔚 Vencimiento: {fecha_venc.strftime('%d/%m/%Y')}\n")
                            
                            diferencia = fecha_venc - datetime.now()
                            if diferencia.days < 0:
                                f.write(f"   ❌ Estado: Vencida hace {abs(diferencia.days)} días\n")
                            elif diferencia.days <= 3:
                                f.write(f"   ⚠️ Estado: Vence en {diferencia.days} días - CRÍTICO\n")
                            else:
                                f.write(f"   ✅ Estado: {diferencia.days} días restantes\n")
                        else:
                            f.write(f"   ♾️ Vencimiento: Sin vencimiento\n")
                            f.write(f"   ✅ Estado: Activa indefinidamente\n")
                        
                        f.write(f"   ⏰ Duración: {suscripcion['duracion']}\n")
                        
                        if suscripcion['notas']:
                            f.write(f"   📝 Notas: {suscripcion['notas']}\n")
                        
                        f.write("-" * 40 + "\n")
                
                f.write(f"\n📄 Archivo generado por DaniStore - Streaming\n")
                f.write("=" * 60 + "\n")
            
            messagebox.showinfo(
                "Exportación Exitosa",
                f"✅ Datos exportados exitosamente:\n\n📄 Archivo: {nombre_archivo}\n📁 Ubicación: Carpeta actual"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar datos: {str(e)}")
    
    def limpiar_vencidas(self):
        """Limpiar suscripciones vencidas"""
        vencidas = [s for s in self.suscripciones if s['activa'] and s['fecha_vencimiento'] and 
                   datetime.strptime(s['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S') < datetime.now()]
        
        if not vencidas:
            messagebox.showinfo("Sin Vencidas", "No hay suscripciones vencidas para limpiar.")
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar Limpieza",
            f"¿Estás seguro de que quieres marcar como inactivas {len(vencidas)} suscripciones vencidas?\n\n"
            f"Esta acción las ocultará de la lista principal pero mantendrá el historial."
        )
        
        if respuesta:
            for suscripcion in vencidas:
                suscripcion['activa'] = False
            
            self.guardar_datos()
            self.actualizar_lista()
            
            messagebox.showinfo("Limpieza Exitosa", f"✅ {len(vencidas)} suscripciones vencidas han sido limpiadas.")
    
    def iniciar_monitor_notificaciones(self):
        """Iniciar el hilo de monitoreo de notificaciones"""
        def monitor():
            while self.notificaciones_activas:
                try:
                    self.verificar_notificaciones()
                    time.sleep(3600)  # Verificar cada hora
                except Exception as e:
                    print(f"Error en monitor de notificaciones: {e}")
                    time.sleep(3600)
        
        hilo_monitor = threading.Thread(target=monitor, daemon=True)
        hilo_monitor.start()
    
    def verificar_notificaciones(self):
        """Verificar y mostrar notificaciones de vencimientos - SISTEMA GARANTIZADO ANDROID"""
        if not self.notificaciones_activas:
            return
        
        ahora = datetime.now()
        suscripciones_vencidas = []
        
        print(f"🔍 Verificando notificaciones... {ahora.strftime('%H:%M:%S')}")
        
        for suscripcion in self.suscripciones:
            if not suscripcion.get('activa', True):
                continue
                
            fecha_vencimiento_str = suscripcion.get('fecha_vencimiento')
            if not fecha_vencimiento_str or fecha_vencimiento_str == 'Indefinido':
                continue
            
            try:
                fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d %H:%M:%S')
                
                # Si ya venció, agregar a la lista
                if fecha_vencimiento <= ahora:
                    usuario = suscripcion.get('usuario', 'Usuario')
                    servicio = suscripcion.get('servicio', 'Servicio')
                    
                    # Crear clave única para evitar duplicados
                    clave_notif = f"{usuario}_{servicio}_vencida"
                    
                    if not hasattr(self, 'notificaciones_enviadas'):
                        self.notificaciones_enviadas = set()
                    
                    if clave_notif not in self.notificaciones_enviadas:
                        suscripciones_vencidas.append(suscripcion)
                        self.notificaciones_enviadas.add(clave_notif)
                        print(f"🚨 VENCIDA: {usuario} - {servicio}")
                    
            except ValueError as e:
                print(f"❌ Error procesando fecha: {e}")
                continue
        
        # Mostrar notificaciones SOLO si hay suscripciones vencidas
        if suscripciones_vencidas:
            self.mostrar_notificacion_android_garantizada(suscripciones_vencidas)
        else:
            print("✅ No hay suscripciones vencidas")
    
    def mostrar_notificacion_android_garantizada(self, suscripciones_vencidas):
        """Mostrar notificación garantizada estilo Android"""
        print("🔔 MOSTRANDO NOTIFICACIÓN ANDROID GARANTIZADA")
        
        # Preparar mensaje simple y directo
        mensaje = "🚨 ¡SUSCRIPCIONES VENCIDAS!\n\n"
        
        for suscripcion in suscripciones_vencidas:
            usuario = suscripcion.get('usuario', 'Usuario')
            servicio = suscripcion.get('servicio', 'Servicio')
            mensaje += f"👤 {usuario}\n📺 {servicio}\n⏰ VENCIDA AHORA\n\n"
        
        mensaje += "¡RENOVAR INMEDIATAMENTE!"
        
        # Mostrar notificación tipo Android usando messagebox
        from tkinter import messagebox
        messagebox.showerror("🚨 ALERTA CRÍTICA", mensaje)
        
        print("✅ Notificación Android mostrada exitosamente")
    
    def mostrar_notificacion_critica(self, vencimientos):
        """Mostrar notificación crítica de vencimientos - MÉTODO LEGACY"""
        # Redirigir al método garantizado
        suscripciones_vencidas = [v['suscripcion'] for v in vencimientos]
        self.mostrar_notificacion_android_garantizada(suscripciones_vencidas)
        
        # Mensaje principal
        if len(vencimientos) == 1:
            venc = vencimientos[0]
            suscripcion = venc['suscripcion']
            dias = venc['dias']
            
            if dias < 0:
                mensaje = f"❌ SUSCRIPCIÓN VENCIDA\n\n👤 Usuario: {suscripcion['usuario']}\n📺 Servicio: {suscripcion['servicio']}\n\n⏰ Vencida hace {abs(dias)} día{'s' if abs(dias) != 1 else ''}"
            elif dias == 0:
                mensaje = f"🚨 VENCE HOY\n\n👤 Usuario: {suscripcion['usuario']}\n📺 Servicio: {suscripcion['servicio']}\n\n⏰ La suscripción vence HOY"
            else:
                mensaje = f"⚠️ VENCE MAÑANA\n\n👤 Usuario: {suscripcion['usuario']}\n📺 Servicio: {suscripcion['servicio']}\n\n⏰ La suscripción vence MAÑANA"
        else:
            mensaje = f"🚨 MÚLTIPLES VENCIMIENTOS\n\n{len(vencimientos)} suscripciones requieren atención inmediata.\n\nHaz clic en 'Ver Detalles' para más información."
        
        tk.Label(notif,
                text=mensaje,
                bg='#4a2a2a',
                fg='white',
                font=('Arial', 12),
                justify='center').pack(pady=20)
        
        # Botones
        botones_frame = tk.Frame(notif, bg='#4a2a2a')
        botones_frame.pack(pady=20)
        
        if len(vencimientos) > 1:
            tk.Button(botones_frame,
                     text="📋 Ver Detalles",
                     bg='#FF9800',
                     fg='white',
                     font=('Arial', 11, 'bold'),
                     command=lambda: [notif.destroy(), self.mostrar_ventana_vencimientos(vencimientos)]).pack(side='left', padx=10)
        
        tk.Button(botones_frame,
                 text="✅ Entendido",
                 bg='#4CAF50',
                 fg='white',
                 font=('Arial', 11, 'bold'),
                 command=notif.destroy).pack(side='left', padx=10)
        
        # Auto-cerrar después de 30 segundos
        notif.after(30000, lambda: notif.destroy() if notif.winfo_exists() else None)
        
        # Hacer sonar alerta del sistema
        try:
            notif.bell()
        except:
            pass
    
    def mostrar_ventana_vencimientos(self, vencimientos):
        """Mostrar ventana detallada de vencimientos múltiples"""
        ventana = tk.Toplevel(self.root)
        ventana.title("🚨 Vencimientos Críticos - Detalles")
        ventana.geometry("600x400")
        ventana.configure(bg='#2a2a2a')
        
        # Título
        tk.Label(ventana,
                text=f"🚨 {len(vencimientos)} Suscripciones Críticas",
                bg='#2a2a2a',
                fg='#FFD700',
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Frame con scroll para la lista
        canvas = tk.Canvas(ventana, bg='#2a2a2a')
        scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a2a2a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mostrar cada vencimiento
        for i, venc in enumerate(vencimientos):
            suscripcion = venc['suscripcion']
            dias = venc['dias']
            
            # Frame para cada suscripción
            item_frame = tk.Frame(scrollable_frame, bg='#4a2a2a', relief='solid', bd=2)
            item_frame.pack(fill='x', padx=10, pady=5)
            
            # Información
            info_frame = tk.Frame(item_frame, bg='#4a2a2a')
            info_frame.pack(fill='x', padx=10, pady=10)
            
            # Estado
            if dias < 0:
                estado_text = f"❌ VENCIDA hace {abs(dias)} día{'s' if abs(dias) != 1 else ''}"
                color_estado = '#FF4444'
            elif dias == 0:
                estado_text = "🚨 VENCE HOY"
                color_estado = '#FFD700'
            else:
                estado_text = "⚠️ VENCE MAÑANA"
                color_estado = '#FF9800'
            
            tk.Label(info_frame,
                    text=estado_text,
                    bg='#4a2a2a',
                    fg=color_estado,
                    font=('Arial', 12, 'bold')).pack(anchor='w')
            
            tk.Label(info_frame,
                    text=f"👤 {suscripcion['usuario']} - 📺 {suscripcion['servicio']}",
                    bg='#4a2a2a',
                    fg='white',
                    font=('Arial', 11)).pack(anchor='w', pady=(2, 0))
            
            if suscripcion['fecha_vencimiento']:
                fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
                tk.Label(info_frame,
                        text=f"📅 Fecha: {fecha_venc.strftime('%d/%m/%Y')}",
                        bg='#4a2a2a',
                        fg='#CCCCCC',
                        font=('Arial', 9)).pack(anchor='w')
            
            # Botón renovar
            tk.Button(info_frame,
                     text="🔄 Renovar Ahora",
                     bg='#4CAF50',
                     fg='white',
                     font=('Arial', 9, 'bold'),
                     command=lambda s=suscripcion: [ventana.destroy(), self.renovar_suscripcion(s.get('id', s.get('usuario', '') + s.get('servicio', '')))]).pack(anchor='w', pady=(5, 0))
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        # Botón cerrar
        tk.Button(ventana,
                 text="✅ Cerrar",
                 bg='#666666',
                 fg='white',
                 font=('Arial', 12, 'bold'),
                 command=ventana.destroy).pack(pady=20)
        notif.after(30000, lambda: notif.destroy() if notif.winfo_exists() else None)
    
    def guardar_datos(self):
        """Guardar datos en archivo JSON"""
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(self.suscripciones, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar datos: {str(e)}")
    
    def cargar_datos(self):
        """Cargar datos desde archivo JSON"""
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    self.suscripciones = json.load(f)
                
                # Agregar IDs si no existen
                ids_actualizados = False
                for i, suscripcion in enumerate(self.suscripciones):
                    if 'id' not in suscripcion:
                        suscripcion['id'] = i + 1
                        ids_actualizados = True
                
                # Guardar con IDs actualizados
                if ids_actualizados:
                    self.guardar_datos()
                        
        except Exception as e:
            print(f"Error cargando datos: {e}")
            self.suscripciones = []
    
    def minimizar_a_bandeja(self):
        """Minimizar la aplicación a la bandeja del sistema"""
        if not PYSTRAY_AVAILABLE:
            messagebox.showinfo("Información", 
                              "Para minimizar a la bandeja del sistema, instala:\n"
                              "pip install pystray pillow")
            return
        
        try:
            # Ocultar ventana
            self.root.withdraw()
            self.minimizado_bandeja = True
            
            # Crear icono para la bandeja
            if os.path.exists('gestor_icon.png'):
                image = Image.open('gestor_icon.png')
            else:
                # Crear imagen simple si no existe el icono
                image = Image.new('RGB', (64, 64), color='#FFD700')
            
            # Crear menú de la bandeja
            menu = pystray.Menu(
                pystray.MenuItem("🔔 Gestor de Suscripciones", self.mostrar_ventana),
                pystray.MenuItem("📊 Ver Estadísticas", self.mostrar_estadisticas),
                pystray.MenuItem("🔔 Verificar Vencimientos", self.verificar_vencimientos_manual),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("📤 Mostrar Ventana", self.mostrar_ventana),
                pystray.MenuItem("❌ Salir", self.salir_aplicacion)
            )
            
            # Crear icono de bandeja
            self.tray_icon = pystray.Icon("DaniStore", image, "DaniStore - Streaming", menu)
            
            # Ejecutar en hilo separado
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
            
            # Mostrar notificación de que se minimizó
            messagebox.showinfo("Minimizado", 
                              "✅ Aplicación minimizada a la bandeja del sistema\n\n"
                              "🔔 Seguirás recibiendo notificaciones automáticas\n"
                              "📤 Haz clic en el icono de la bandeja para volver")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error minimizando a bandeja: {e}")
            self.mostrar_ventana()
    
    def mostrar_ventana(self, icon=None, item=None):
        """Mostrar la ventana principal"""
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None
        
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.minimizado_bandeja = False
    
    def salir_aplicacion(self, icon=None, item=None):
        """Salir completamente de la aplicación"""
        if self.tray_icon:
            self.tray_icon.stop()
        self.on_closing()
    
    def on_closing(self):
        """Manejar cierre de la aplicación"""
        # Preguntar si quiere minimizar o cerrar
        if not self.minimizado_bandeja and PYSTRAY_AVAILABLE:
            respuesta = messagebox.askyesnocancel(
                "Cerrar Aplicación",
                "¿Qué deseas hacer?\n\n"
                "• SÍ: Minimizar a la bandeja (seguir recibiendo notificaciones)\n"
                "• NO: Cerrar completamente\n"
                "• CANCELAR: Volver a la aplicación"
            )
            
            if respuesta is True:  # Minimizar
                self.minimizar_a_bandeja()
                return
            elif respuesta is False:  # Cerrar
                pass  # Continuar con el cierre
            else:  # Cancelar
                return
        
        # Cerrar aplicación
        self.notificaciones_activas = False
        if self.tray_icon:
            self.tray_icon.stop()
        self.guardar_datos()
        self.root.destroy()
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Verificar vencimientos al iniciar
        self.root.after(2000, self.verificar_notificaciones)
        
        self.root.mainloop()

if __name__ == "__main__":
    app = GestorSuscripciones()
    app.ejecutar()