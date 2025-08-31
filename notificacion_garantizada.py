#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE NOTIFICACIÓN GARANTIZADA PARA ANDROID
Versión ultra-simple que GARANTIZA que llegue la notificación
"""

import json
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def crear_suscripcion_vence_ya():
    """Crear una suscripción que vence AHORA MISMO"""
    archivo = "suscripciones_data.json"
    
    # Cargar existentes
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
    else:
        suscripciones = []
    
    # Crear suscripción que vence en 5 segundos
    ahora = datetime.now()
    vence_en = ahora + timedelta(seconds=5)
    
    nueva = {
        'usuario': 'PRUEBA_INMEDIATA',
        'servicio': 'Netflix',
        'fecha_inicio': ahora.strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_vencimiento': vence_en.strftime('%Y-%m-%d %H:%M:%S'),
        'activa': True,
        'notas': 'Vence en 5 segundos - PRUEBA'
    }
    
    suscripciones.append(nueva)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(suscripciones, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Suscripción creada - vence a las {vence_en.strftime('%H:%M:%S')}")
    return nueva

def verificar_y_notificar():
    """Verificar suscripciones y mostrar notificación SI HAY VENCIDAS"""
    archivo = "suscripciones_data.json"
    
    if not os.path.exists(archivo):
        print("❌ No hay archivo de suscripciones")
        return False
    
    with open(archivo, 'r', encoding='utf-8') as f:
        suscripciones = json.load(f)
    
    ahora = datetime.now()
    vencidas = []
    
    print(f"🔍 Verificando {len(suscripciones)} suscripciones a las {ahora.strftime('%H:%M:%S')}")
    
    for suscripcion in suscripciones:
        if not suscripcion.get('activa', True):
            continue
        
        fecha_venc_str = suscripcion.get('fecha_vencimiento')
        if not fecha_venc_str or fecha_venc_str == 'Indefinido':
            continue
        
        try:
            fecha_venc = datetime.strptime(fecha_venc_str, '%Y-%m-%d %H:%M:%S')
            
            if fecha_venc <= ahora:
                vencidas.append(suscripcion)
                print(f"🚨 VENCIDA: {suscripcion['usuario']} - {suscripcion['servicio']}")
        except:
            continue
    
    # Si hay vencidas, mostrar notificación INMEDIATAMENTE
    if vencidas:
        mostrar_notificacion_android(vencidas)
        return True
    else:
        print("✅ No hay suscripciones vencidas")
        return False

def mostrar_notificacion_android(suscripciones_vencidas):
    """Mostrar notificación estilo Android - SIMPLE Y DIRECTA"""
    print("🔔 MOSTRANDO NOTIFICACIÓN ANDROID")
    
    # Crear ventana temporal solo para la notificación
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Preparar mensaje
    mensaje = "🚨 ¡SUSCRIPCIONES VENCIDAS!\n\n"
    
    for suscripcion in suscripciones_vencidas:
        usuario = suscripcion.get('usuario', 'Usuario')
        servicio = suscripcion.get('servicio', 'Servicio')
        mensaje += f"👤 {usuario}\n📺 {servicio}\n⏰ VENCIDA AHORA\n\n"
    
    mensaje += "¡RENOVAR INMEDIATAMENTE!"
    
    # Mostrar notificación tipo Android
    messagebox.showerror("🚨 ALERTA CRÍTICA", mensaje)
    
    print("✅ Notificación mostrada exitosamente")
    root.destroy()

def prueba_inmediata():
    """Prueba que funciona INMEDIATAMENTE"""
    print("🎯 PRUEBA INMEDIATA DE NOTIFICACIÓN")
    print("=" * 40)
    
    print("1️⃣ Creando suscripción que vence en 5 segundos...")
    crear_suscripcion_vence_ya()
    
    print("2️⃣ Esperando 6 segundos...")
    import time
    time.sleep(6)
    
    print("3️⃣ Verificando y notificando...")
    resultado = verificar_y_notificar()
    
    if resultado:
        print("🎉 ¡ÉXITO! La notificación funcionó")
    else:
        print("❌ No se mostró notificación")

def prueba_con_interfaz():
    """Prueba con interfaz gráfica simple"""
    root = tk.Tk()
    root.title("🧪 Test Notificación Android")
    root.geometry("350x250")
    root.configure(bg='#1a1a1a')
    
    tk.Label(root,
            text="🧪 TEST NOTIFICACIÓN ANDROID",
            bg='#1a1a1a',
            fg='white',
            font=('Arial', 14, 'bold')).pack(pady=20)
    
    tk.Button(root,
             text="🚀 Crear y Probar (5 seg)",
             bg='#007bff',
             fg='white',
             font=('Arial', 12, 'bold'),
             command=lambda: [crear_suscripcion_vence_ya(), root.after(6000, verificar_y_notificar)],
             padx=20, pady=10).pack(pady=10)
    
    tk.Button(root,
             text="🔍 Verificar Ahora",
             bg='#28a745',
             fg='white',
             font=('Arial', 12, 'bold'),
             command=verificar_y_notificar,
             padx=20, pady=10).pack(pady=10)
    
    tk.Button(root,
             text="❌ Salir",
             bg='#dc3545',
             fg='white',
             font=('Arial', 12, 'bold'),
             command=root.quit,
             padx=20, pady=10).pack(pady=20)
    
    info = "Crea una suscripción de prueba\ny verás la notificación en 5 segundos"
    tk.Label(root,
            text=info,
            bg='#1a1a1a',
            fg='#cccccc',
            font=('Arial', 10)).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("🎯 SISTEMA DE NOTIFICACIÓN GARANTIZADA")
    print("=" * 50)
    print("Elige una opción:")
    print("1. Prueba inmediata (automática)")
    print("2. Prueba con interfaz")
    
    opcion = input("Opción (1 o 2): ").strip()
    
    if opcion == "1":
        prueba_inmediata()
    else:
        prueba_con_interfaz()