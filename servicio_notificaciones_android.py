#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVICIO DE NOTIFICACIONES ANDROID - SEGUNDO PLANO
Sistema que funciona aunque la app esté cerrada
"""

import json
import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import sys

class ServicioNotificacionesAndroid:
    def __init__(self):
        self.archivo_datos = "suscripciones_data.json"
        self.archivo_log = "notificaciones.log"
        self.ejecutando = True
        self.notificaciones_enviadas = set()
        self.intervalo_verificacion = 60  # 60 segundos
        
    def log(self, mensaje):
        """Escribir log con timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {mensaje}"
        print(log_msg)
        
        try:
            with open(self.archivo_log, 'a', encoding='utf-8') as f:
                f.write(log_msg + '\n')
        except:
            pass
    
    def cargar_suscripciones(self):
        """Cargar suscripciones del archivo"""
        if not os.path.exists(self.archivo_datos):
            return []
        
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"❌ Error cargando suscripciones: {e}")
            return []
    
    def verificar_vencimientos(self):
        """Verificar suscripciones vencidas"""
        suscripciones = self.cargar_suscripciones()
        ahora = datetime.now()
        vencidas = []
        
        self.log(f"🔍 Verificando {len(suscripciones)} suscripciones...")
        
        for suscripcion in suscripciones:
            if not suscripcion.get('activa', True):
                continue
                
            fecha_venc_str = suscripcion.get('fecha_vencimiento')
            if not fecha_venc_str or fecha_venc_str == 'Indefinido':
                continue
            
            try:
                fecha_venc = datetime.strptime(fecha_venc_str, '%Y-%m-%d %H:%M:%S')
                
                # Si ya venció
                if fecha_venc <= ahora:
                    usuario = suscripcion.get('usuario', 'Usuario')
                    servicio = suscripcion.get('servicio', 'Servicio')
                    clave_notif = f"{usuario}_{servicio}_vencida"
                    
                    if clave_notif not in self.notificaciones_enviadas:
                        vencidas.append(suscripcion)
                        self.notificaciones_enviadas.add(clave_notif)
                        self.log(f"🚨 VENCIDA: {usuario} - {servicio}")
                        
            except ValueError as e:
                self.log(f"❌ Error procesando fecha: {e}")
                continue
        
        return vencidas
    
    def mostrar_notificacion_avanzada(self, suscripciones_vencidas):
        """Mostrar notificación avanzada y atractiva"""
        if not suscripciones_vencidas:
            return
        
        self.log(f"🔔 Mostrando notificación para {len(suscripciones_vencidas)} suscripciones")
        
        try:
            # Crear ventana principal temporal
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            
            # Crear ventana de notificación personalizada
            notif = tk.Toplevel(root)
            notif.title("🚨 ALERTA CRÍTICA - SUSCRIPCIONES")
            notif.geometry("500x400")
            notif.configure(bg='#1a1a1a')
            
            # Configurar ventana para que esté siempre al frente
            notif.attributes('-topmost', True)
            notif.attributes('-toolwindow', True)  # No aparece en taskbar
            notif.grab_set()  # Modal
            
            # Centrar en pantalla
            notif.update_idletasks()
            x = (notif.winfo_screenwidth() // 2) - (500 // 2)
            y = (notif.winfo_screenheight() // 2) - (400 // 2)
            notif.geometry(f"500x400+{x}+{y}")
            
            # Frame principal con borde
            main_frame = tk.Frame(notif, bg='#FF4444', bd=3, relief='raised')
            main_frame.pack(fill='both', expand=True, padx=5, pady=5)
            
            content_frame = tk.Frame(main_frame, bg='#1a1a1a')
            content_frame.pack(fill='both', expand=True, padx=3, pady=3)
            
            # Título animado
            titulo = tk.Label(content_frame,
                            text="🚨 ¡ALERTA CRÍTICA! 🚨",
                            bg='#1a1a1a',
                            fg='#FF4444',
                            font=('Arial', 18, 'bold'))
            titulo.pack(pady=15)
            
            # Subtítulo
            tk.Label(content_frame,
                    text="SUSCRIPCIONES VENCIDAS",
                    bg='#1a1a1a',
                    fg='#FFD700',
                    font=('Arial', 14, 'bold')).pack(pady=5)
            
            # Frame para lista con scroll
            lista_frame = tk.Frame(content_frame, bg='#1a1a1a')
            lista_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            canvas = tk.Canvas(lista_frame, bg='#1a1a1a', highlightthickness=0)
            scrollbar = tk.Scrollbar(lista_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')
            
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
            
            # Mostrar cada suscripción vencida
            for i, suscripcion in enumerate(suscripciones_vencidas):
                usuario = suscripcion.get('usuario', 'Usuario')
                servicio = suscripcion.get('servicio', 'Servicio')
                
                # Frame para cada suscripción
                item_frame = tk.Frame(scrollable_frame, bg='#2a2a2a', relief='solid', bd=2)
                item_frame.pack(fill='x', pady=8, padx=5)
                
                # Número de alerta
                tk.Label(item_frame,
                        text=f"⚠️ ALERTA #{i+1}",
                        bg='#2a2a2a',
                        fg='#FF6600',
                        font=('Arial', 12, 'bold')).pack(anchor='w', padx=15, pady=(10, 2))
                
                # Usuario
                tk.Label(item_frame,
                        text=f"👤 CLIENTE: {usuario}",
                        bg='#2a2a2a',
                        fg='#00FF88',
                        font=('Arial', 11, 'bold')).pack(anchor='w', padx=15, pady=2)
                
                # Servicio
                tk.Label(item_frame,
                        text=f"📺 SERVICIO: {servicio}",
                        bg='#2a2a2a',
                        fg='white',
                        font=('Arial', 11, 'bold')).pack(anchor='w', padx=15, pady=2)
                
                # Estado crítico
                tk.Label(item_frame,
                        text="💔 ESTADO: VENCIDA - RENOVAR YA",
                        bg='#2a2a2a',
                        fg='#FF0000',
                        font=('Arial', 10, 'bold')).pack(anchor='w', padx=15, pady=(2, 10))
            
            # Configurar scroll
            def configure_scroll(event=None):
                canvas.configure(scrollregion=canvas.bbox('all'))
                canvas.itemconfig(canvas_frame, width=canvas.winfo_width())
            
            scrollable_frame.bind('<Configure>', configure_scroll)
            canvas.bind('<Configure>', configure_scroll)
            
            # Botones de acción
            botones_frame = tk.Frame(content_frame, bg='#1a1a1a')
            botones_frame.pack(pady=20)
            
            def cerrar_y_abrir_gestor():
                notif.destroy()
                root.destroy()
                # Intentar abrir el gestor principal
                try:
                    os.system('python gestor_suscripciones.py')
                except:
                    pass
            
            tk.Button(botones_frame,
                     text="🔄 ABRIR GESTOR",
                     bg='#007bff',
                     fg='white',
                     font=('Arial', 12, 'bold'),
                     command=cerrar_y_abrir_gestor,
                     padx=25, pady=10).pack(side='left', padx=10)
            
            tk.Button(botones_frame,
                     text="✅ ENTENDIDO",
                     bg='#28a745',
                     fg='white',
                     font=('Arial', 12, 'bold'),
                     command=lambda: [notif.destroy(), root.destroy()],
                     padx=25, pady=10).pack(side='left', padx=10)
            
            # Efecto de parpadeo del título
            def parpadear():
                current_color = titulo.cget('fg')
                new_color = '#FFFF00' if current_color == '#FF4444' else '#FF4444'
                titulo.config(fg=new_color)
                notif.after(500, parpadear)
            
            parpadear()
            
            # Sonidos de alerta
            try:
                for _ in range(5):
                    notif.bell()
                    notif.after(300)
            except:
                pass
            
            # Mostrar ventana
            notif.mainloop()
            
        except Exception as e:
            self.log(f"❌ Error mostrando notificación avanzada: {e}")
            # Fallback a notificación simple
            self.mostrar_notificacion_simple(suscripciones_vencidas)
    
    def mostrar_notificacion_simple(self, suscripciones_vencidas):
        """Notificación simple como fallback"""
        mensaje = "🚨 ¡SUSCRIPCIONES VENCIDAS!\n\n"
        for suscripcion in suscripciones_vencidas:
            usuario = suscripcion.get('usuario', 'Usuario')
            servicio = suscripcion.get('servicio', 'Servicio')
            mensaje += f"👤 {usuario} - 📺 {servicio}\n"
        mensaje += "\n¡RENOVAR INMEDIATAMENTE!"
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("🚨 ALERTA CRÍTICA", mensaje)
            root.destroy()
        except:
            pass
    
    def ejecutar_servicio(self):
        """Ejecutar servicio en segundo plano"""
        self.log("🚀 Iniciando servicio de notificaciones Android...")
        self.log(f"⏰ Verificación cada {self.intervalo_verificacion} segundos")
        
        while self.ejecutando:
            try:
                vencidas = self.verificar_vencimientos()
                
                if vencidas:
                    self.log(f"🔔 Encontradas {len(vencidas)} suscripciones vencidas")
                    self.mostrar_notificacion_avanzada(vencidas)
                else:
                    self.log("✅ No hay suscripciones vencidas")
                
                # Esperar antes de la próxima verificación
                time.sleep(self.intervalo_verificacion)
                
            except KeyboardInterrupt:
                self.log("🛑 Servicio detenido por usuario")
                break
            except Exception as e:
                self.log(f"❌ Error en servicio: {e}")
                time.sleep(self.intervalo_verificacion)
    
    def detener_servicio(self):
        """Detener servicio"""
        self.ejecutando = False
        self.log("🛑 Deteniendo servicio...")

def main():
    print("🎯 SERVICIO DE NOTIFICACIONES ANDROID")
    print("=" * 50)
    print("Este servicio funciona en segundo plano")
    print("y notifica aunque la app esté cerrada.")
    print()
    print("Para detener: Ctrl+C")
    print("=" * 50)
    
    servicio = ServicioNotificacionesAndroid()
    
    try:
        servicio.ejecutar_servicio()
    except KeyboardInterrupt:
        servicio.detener_servicio()
        print("\n🛑 Servicio detenido")

if __name__ == "__main__":
    main()