#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador de Dependencias para Gestor de Suscripciones - Dani666
"""

import subprocess
import sys
import os

def instalar_dependencia(nombre_paquete, descripcion):
    """Instalar una dependencia específica"""
    print(f"📦 Instalando {descripcion}...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', nombre_paquete], 
                      check=True, capture_output=True, text=True)
        print(f"✅ {descripcion} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {descripcion}: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 INSTALADOR DE DEPENDENCIAS - GESTOR DE SUSCRIPCIONES DANI666")
    print("=" * 70)
    
    # Lista de dependencias
    dependencias = [
        ("pillow", "Pillow (para manejo de imágenes e iconos)"),
        ("pystray", "Pystray (para minimizar a la bandeja del sistema)"),
        ("pyinstaller", "PyInstaller (para crear ejecutables)")
    ]
    
    print("📋 Dependencias a instalar:")
    for paquete, desc in dependencias:
        print(f"   • {desc}")
    
    print("\n🚀 Iniciando instalación...\n")
    
    # Instalar cada dependencia
    exitosos = 0
    for paquete, descripcion in dependencias:
        if instalar_dependencia(paquete, descripcion):
            exitosos += 1
        print()  # Línea en blanco
    
    # Resultado final
    print("=" * 70)
    if exitosos == len(dependencias):
        print("🎉 ¡TODAS LAS DEPENDENCIAS INSTALADAS EXITOSAMENTE!")
        print("\n✅ Funcionalidades disponibles:")
        print("   • 🔔 Notificaciones automáticas")
        print("   • 📱 Minimizar a la bandeja del sistema")
        print("   • 🎨 Iconos personalizados")
        print("   • 📦 Crear ejecutables")
        print("\n🚀 Ya puedes ejecutar: python gestor_suscripciones.py")
    else:
        print(f"⚠️ Se instalaron {exitosos} de {len(dependencias)} dependencias")
        print("\n💡 Algunas funcionalidades pueden no estar disponibles:")
        if exitosos < len(dependencias):
            print("   • Sin pystray: No se puede minimizar a la bandeja")
            print("   • Sin pillow: Iconos limitados")
            print("   • Sin pyinstaller: No se pueden crear ejecutables")
        print("\n🔄 Puedes intentar instalar manualmente:")
        for paquete, _ in dependencias:
            print(f"   pip install {paquete}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()