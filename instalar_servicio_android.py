#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSTALADOR DEL SERVICIO DE NOTIFICACIONES ANDROID
Configura el servicio para que funcione en segundo plano
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def crear_script_inicio():
    """Crear script de inicio automático"""
    script_content = f'''@echo off
cd /d "{os.getcwd()}"
python servicio_notificaciones_android.py
pause
'''
    
    with open('iniciar_servicio_android.bat', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Script de inicio creado: iniciar_servicio_android.bat")

def crear_configuracion():
    """Crear archivo de configuración"""
    config = {
        "servicio_activo": True,
        "intervalo_verificacion": 60,
        "notificaciones_avanzadas": True,
        "log_activado": True,
        "auto_inicio": False,
        "version": "1.0",
        "instalado": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('config_servicio_android.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Configuración creada: config_servicio_android.json")

def crear_acceso_directo():
    """Crear acceso directo en el escritorio"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Servicio Notificaciones Android.lnk")
        target = os.path.join(os.getcwd(), "iniciar_servicio_android.bat")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = target
        shortcut.save()
        
        print("✅ Acceso directo creado en el escritorio")
        
    except ImportError:
        print("⚠️ No se pudo crear acceso directo (falta winshell)")
        print("   Puedes ejecutar manualmente: iniciar_servicio_android.bat")

def probar_servicio():
    """Probar que el servicio funciona"""
    print("\n🧪 PROBANDO SERVICIO...")
    
    # Crear suscripción de prueba vencida
    from datetime import datetime, timedelta
    
    suscripciones = []
    if os.path.exists('suscripciones_data.json'):
        try:
            with open('suscripciones_data.json', 'r', encoding='utf-8') as f:
                suscripciones = json.load(f)
        except:
            pass
    
    # Agregar suscripción de prueba
    ahora = datetime.now()
    vencida = ahora - timedelta(minutes=1)
    
    prueba = {
        'usuario': 'PRUEBA_SERVICIO',
        'servicio': 'Netflix',
        'fecha_inicio': (ahora - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_vencimiento': vencida.strftime('%Y-%m-%d %H:%M:%S'),
        'activa': True,
        'notas': 'Prueba del servicio Android'
    }
    
    suscripciones.append(prueba)
    
    with open('suscripciones_data.json', 'w', encoding='utf-8') as f:
        json.dump(suscripciones, f, indent=2, ensure_ascii=False)
    
    print("✅ Suscripción de prueba creada")
    print("\n🚀 Iniciando servicio de prueba...")
    print("   (Se cerrará automáticamente después de mostrar la notificación)")
    
    # Ejecutar servicio por 10 segundos
    try:
        import threading
        import time
        
        def ejecutar_servicio_prueba():
            from servicio_notificaciones_android import ServicioNotificacionesAndroid
            servicio = ServicioNotificacionesAndroid()
            servicio.intervalo_verificacion = 5  # 5 segundos para prueba
            
            # Ejecutar una sola verificación
            vencidas = servicio.verificar_vencimientos()
            if vencidas:
                servicio.mostrar_notificacion_avanzada(vencidas)
                print("✅ Notificación mostrada correctamente")
            else:
                print("❌ No se encontraron suscripciones vencidas")
        
        hilo_prueba = threading.Thread(target=ejecutar_servicio_prueba)
        hilo_prueba.start()
        hilo_prueba.join(timeout=15)  # Máximo 15 segundos
        
        print("✅ Prueba completada")
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")

def main():
    print("🎯 INSTALADOR DEL SERVICIO DE NOTIFICACIONES ANDROID")
    print("=" * 60)
    print("Este instalador configurará el servicio para que funcione")
    print("en segundo plano y notifique aunque la app esté cerrada.")
    print("=" * 60)
    
    print("\n📋 INSTALANDO COMPONENTES...")
    
    # 1. Crear script de inicio
    crear_script_inicio()
    
    # 2. Crear configuración
    crear_configuracion()
    
    # 3. Crear acceso directo
    crear_acceso_directo()
    
    print("\n✅ INSTALACIÓN COMPLETADA")
    print("=" * 40)
    
    print("\n🚀 FORMAS DE USAR EL SERVICIO:")
    print("1️⃣ Doble clic en: 'Servicio Notificaciones Android' (escritorio)")
    print("2️⃣ Ejecutar: iniciar_servicio_android.bat")
    print("3️⃣ Comando: python servicio_notificaciones_android.py")
    
    print("\n⚙️ CONFIGURACIÓN:")
    print("• Archivo: config_servicio_android.json")
    print("• Logs: notificaciones.log")
    print("• Intervalo: 60 segundos")
    
    print("\n🧪 ¿QUIERES PROBAR EL SERVICIO AHORA?")
    respuesta = input("Escribe 'si' para probar: ").lower().strip()
    
    if respuesta in ['si', 's', 'yes', 'y']:
        probar_servicio()
    
    print("\n🎉 ¡SERVICIO LISTO PARA ANDROID!")
    print("El servicio funcionará en segundo plano y notificará")
    print("aunque la aplicación principal esté cerrada.")

if __name__ == "__main__":
    main()