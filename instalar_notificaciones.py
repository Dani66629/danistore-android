#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador de Dependencias para Notificaciones
Gestor de Suscripciones - Dani666
"""

import subprocess
import sys
import os

def instalar_dependencia(paquete):
    """Instalar un paquete usando pip"""
    try:
        print(f"📦 Instalando {paquete}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
        print(f"✅ {paquete} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {paquete}: {e}")
        return False

def verificar_instalacion():
    """Verificar que las dependencias estén instaladas"""
    dependencias = {
        'plyer': 'Notificaciones multiplataforma',
        'win10toast': 'Notificaciones nativas de Windows 10/11'
    }
    
    print("🔍 Verificando dependencias...")
    
    for paquete, descripcion in dependencias.items():
        try:
            __import__(paquete)
            print(f"✅ {paquete} - {descripcion}")
        except ImportError:
            print(f"❌ {paquete} - {descripcion} (NO INSTALADO)")
            return False
    
    return True

def main():
    print("=" * 60)
    print("📦 INSTALADOR DE NOTIFICACIONES")
    print("   Gestor de Suscripciones - Dani666")
    print("=" * 60)
    
    # Lista de dependencias necesarias
    dependencias = ['plyer', 'win10toast']
    
    print("🎯 Dependencias a instalar:")
    print("   • plyer - Notificaciones multiplataforma")
    print("   • win10toast - Notificaciones nativas Windows")
    print()
    
    # Instalar dependencias
    exito = True
    for dep in dependencias:
        if not instalar_dependencia(dep):
            exito = False
    
    print("\n" + "=" * 60)
    
    if exito:
        print("🎉 ¡INSTALACIÓN COMPLETADA!")
        print("✅ Todas las dependencias instaladas correctamente")
        print()
        print("🚀 Ahora puedes ejecutar:")
        print("   python servicio_notificaciones.py")
        print()
        print("💡 Para ejecutar en segundo plano:")
        print("   pythonw servicio_notificaciones.py")
    else:
        print("❌ INSTALACIÓN INCOMPLETA")
        print("⚠️ Algunas dependencias no se pudieron instalar")
        print("💡 Intenta ejecutar como administrador")
    
    print("=" * 60)

if __name__ == "__main__":
    main()