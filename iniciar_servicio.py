#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iniciador del Servicio de Notificaciones
Gestor de Suscripciones - Dani666
"""

import subprocess
import sys
import os
import time

def verificar_dependencias():
    """Verificar que las dependencias estén instaladas"""
    try:
        import plyer
        import win10toast
        return True
    except ImportError:
        return False

def ejecutar_servicio_segundo_plano():
    """Ejecutar el servicio en segundo plano"""
    try:
        # Usar pythonw para ejecutar sin ventana de consola
        if sys.platform == "win32":
            subprocess.Popen([
                sys.executable.replace("python.exe", "pythonw.exe"),
                "servicio_notificaciones.py"
            ], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen([sys.executable, "servicio_notificaciones.py"])
        
        return True
    except Exception as e:
        print(f"❌ Error iniciando servicio: {e}")
        return False

def main():
    print("🚀 INICIADOR DEL SERVICIO DE NOTIFICACIONES")
    print("=" * 50)
    
    # Verificar que el archivo del servicio existe
    if not os.path.exists("servicio_notificaciones.py"):
        print("❌ Error: No se encuentra servicio_notificaciones.py")
        return
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("❌ Dependencias no instaladas")
        print("💡 Ejecuta primero: python instalar_notificaciones.py")
        return
    
    # Verificar si hay suscripciones
    if not os.path.exists("suscripciones_data.json"):
        print("⚠️ No hay suscripciones guardadas")
        print("💡 Agrega suscripciones primero con el gestor principal")
        print("   python gestor_suscripciones.py")
        return
    
    print("✅ Todo listo para iniciar el servicio")
    print()
    
    # Preguntar modo de ejecución
    print("🎯 Selecciona el modo de ejecución:")
    print("1. Segundo plano (sin ventana) - Recomendado")
    print("2. Ventana visible (para debug)")
    print("3. Cancelar")
    
    try:
        opcion = input("\nOpción (1-3): ").strip()
        
        if opcion == "1":
            print("🔄 Iniciando servicio en segundo plano...")
            if ejecutar_servicio_segundo_plano():
                print("✅ Servicio iniciado correctamente")
                print("🔔 Las notificaciones aparecerán automáticamente")
                print("💡 Para detener: Busca 'python' en el Administrador de Tareas")
            else:
                print("❌ Error iniciando el servicio")
        
        elif opcion == "2":
            print("🔄 Iniciando servicio con ventana visible...")
            subprocess.run([sys.executable, "servicio_notificaciones.py"])
        
        elif opcion == "3":
            print("❌ Cancelado por el usuario")
        
        else:
            print("❌ Opción no válida")
    
    except KeyboardInterrupt:
        print("\n❌ Cancelado por el usuario")

if __name__ == "__main__":
    main()