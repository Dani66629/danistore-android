#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST SIMPLE DE NOTIFICACIONES PARA ANDROID
Sistema básico que garantiza notificaciones cuando vence una suscripción
"""

import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import time

class NotificadorAndroid:
    def __init__(self):
        self.archivo_datos = "suscripciones_data.json"
        self.verificando = False
        self.root = None
        
    def cargar_suscripciones(self):
        """Cargar suscripciones del archivo"""
        if not os.path.exists(self.archivo_datos):
            return []
        
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def crear_suscripcion_prueba(self, minutos=1):
        """Crear suscripción de prueba que vence en X minutos"""
        suscripciones = self.cargar_suscripciones()
        
        ahora = datetime.now()
        vencimiento = ahora + timedelta(minutes=minutos)
        
        nueva = {
            'usuario': 'TEST_ANDROID',
            'servicio': 'Netflix',
            'fecha_inicio': ahora.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_vencimiento': vencimiento.strftime('%Y-%m-%d %H:%M:%S'),
            'activa': True,
            'notas': f'Prueba Android - vence en {minutos} minutos'
        }
        
        suscripciones.append(nueva)
        
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            json.dump(suscripciones, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Suscripción creada - vence a las {vencimiento.strftime('%H:%M:%S')}")
        return nueva
    
    def verificar_vencimientos(self):
        """Verificar si hay suscripciones vencidas"""
        suscripciones = self.cargar_suscripciones()
        ahora = datetime.now()
        vencidas = []
        
        print(f"🔍 Verificando a las {ahora.strftime('%H:%M:%S')}")
        
        for suscripcion in suscripciones:
            if not suscripcion.get('activa', True):
                continue
                
            fecha_venc_str = suscripcion.get('fecha_vencimiento')
            if not fecha_venc_str or fecha_venc_str == 'Indefinido':
                continue
            
            try:
                fecha_venc = datetime.strptime(fecha_venc_str, '%Y-%m-%d %H:%M:%S')
                
                # Si ya venció o vence en menos de 1 minuto
                if fecha_venc <= ahora:
                    vencidas.append(suscripcion)
                    print(f"🚨 VENCIDA: {suscripcion['usuario']} - {suscripcion['servicio']}")
                    
            except ValueError:
                continue
        
        return vencidas
    
    def mostrar_notificacion_simple(self, suscripciones_vencidas):
        """Mostrar notificación simple y directa"""
        if not suscripciones_vencidas:
            return
        
        # Crear ventana principal si no existe
        if not self.root:
            self.root = tk.Tk()
            self.root.withdraw()  # Ocultar ventana principal
        
        mensaje = "🚨 SUSCRIPCIONES VENCIDAS:\n\n"
        for suscripcion in suscripciones_vencidas:
            usuario = suscripcion.get('usuario', 'Usuario')
            servicio = suscripcion.get('servicio', 'Servicio')
            mensaje += f"👤 {usuario}\n📺 {servicio}\n⏰ VENCIDA\n\n"
        
        mensaje += "¡RENOVAR INMEDIATAMENTE!"
        
        # Mostrar mensaje emergente
        messagebox.showwarning("🚨 SUSCRIPCIONES VENCIDAS", mensaje)
        print("✅ Notificación mostrada")
    
    def iniciar_monitoreo(self, intervalo_segundos=30):
        """Iniciar monitoreo continuo"""
        print(f"🚀 Iniciando monitoreo cada {intervalo_segundos} segundos")
        self.verificando = True
        
        def monitorear():
            while self.verificando:
                try:
                    vencidas = self.verificar_vencimientos()
                    if vencidas:
                        # Ejecutar notificación en el hilo principal
                        if self.root:
                            self.root.after(0, lambda: self.mostrar_notificacion_simple(vencidas))
                    
                    time.sleep(intervalo_segundos)
                except Exception as e:
                    print(f"❌ Error en monitoreo: {e}")
                    time.sleep(intervalo_segundos)
        
        # Iniciar monitoreo en hilo separado
        hilo_monitor = threading.Thread(target=monitorear, daemon=True)
        hilo_monitor.start()
    
    def detener_monitoreo(self):
        """Detener monitoreo"""
        self.verificando = False
        print("🛑 Monitoreo detenido")
    
    def ejecutar_prueba_completa(self):
        """Ejecutar prueba completa del sistema"""
        print("🎯 PRUEBA COMPLETA DE NOTIFICACIONES ANDROID")
        print("=" * 50)
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Test Notificaciones Android")
        self.root.geometry("400x300")
        self.root.configure(bg='#2a2a2a')
        
        # Título
        tk.Label(self.root, 
                text="🧪 TEST NOTIFICACIONES ANDROID", 
                bg='#2a2a2a', 
                fg='white', 
                font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Botones de prueba
        tk.Button(self.root,
                 text="🚀 Crear Suscripción (1 min)",
                 bg='#007bff',
                 fg='white',
                 font=('Arial', 12),
                 command=lambda: self.crear_suscripcion_prueba(1),
                 padx=20, pady=10).pack(pady=10)
        
        tk.Button(self.root,
                 text="⚡ Crear Suscripción (30 seg)",
                 bg='#ff6600',
                 fg='white',
                 font=('Arial', 12),
                 command=lambda: self.crear_suscripcion_prueba(0.5),
                 padx=20, pady=10).pack(pady=10)
        
        tk.Button(self.root,
                 text="🔍 Verificar Ahora",
                 bg='#28a745',
                 fg='white',
                 font=('Arial', 12),
                 command=self.verificar_manual,
                 padx=20, pady=10).pack(pady=10)
        
        tk.Button(self.root,
                 text="🛑 Salir",
                 bg='#dc3545',
                 fg='white',
                 font=('Arial', 12),
                 command=self.salir,
                 padx=20, pady=10).pack(pady=20)
        
        # Información
        info_text = "1. Crea una suscripción de prueba\n2. Espera el tiempo indicado\n3. Verás la notificación automáticamente"
        tk.Label(self.root,
                text=info_text,
                bg='#2a2a2a',
                fg='#cccccc',
                font=('Arial', 10),
                justify='left').pack(pady=20)
        
        # Iniciar monitoreo
        self.iniciar_monitoreo(10)  # Cada 10 segundos
        
        # Ejecutar interfaz
        self.root.mainloop()
    
    def verificar_manual(self):
        """Verificación manual"""
        vencidas = self.verificar_vencimientos()
        if vencidas:
            self.mostrar_notificacion_simple(vencidas)
        else:
            messagebox.showinfo("✅ Sin Vencimientos", "No hay suscripciones vencidas")
    
    def salir(self):
        """Salir de la aplicación"""
        self.detener_monitoreo()
        if self.root:
            self.root.quit()
            self.root.destroy()

def main():
    notificador = NotificadorAndroid()
    notificador.ejecutar_prueba_completa()

if __name__ == "__main__":
    main()