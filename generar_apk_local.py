#!/usr/bin/env python3
"""
Script para generar APK localmente usando Buildozer
Alternativa a GitHub Actions cuando hay problemas de configuración
"""

import os
import sys
import subprocess
import platform

def verificar_dependencias():
    """Verifica que las dependencias necesarias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    dependencias = {
        'python': 'python --version',
        'pip': 'pip --version',
        'git': 'git --version'
    }
    
    for dep, cmd in dependencias.items():
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {dep}: {result.stdout.strip()}")
            else:
                print(f"❌ {dep}: No encontrado")
                return False
        except FileNotFoundError:
            print(f"❌ {dep}: No encontrado")
            return False
    
    return True

def instalar_buildozer():
    """Instala Buildozer y dependencias"""
    print("\n📦 Instalando Buildozer y dependencias...")
    
    comandos = [
        "pip install --upgrade pip",
        "pip install buildozer",
        "pip install kivy[base]",
        "pip install cython",
        "pip install pillow"
    ]
    
    for cmd in comandos:
        print(f"Ejecutando: {cmd}")
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error ejecutando: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        else:
            print(f"✅ Completado: {cmd}")
    
    return True

def generar_apk():
    """Genera el APK usando Buildozer"""
    print("\n🚀 Generando APK...")
    
    # Verificar que existe buildozer.spec
    if not os.path.exists('buildozer.spec'):
        print("❌ No se encontró buildozer.spec")
        return False
    
    # Ejecutar buildozer
    print("Ejecutando: buildozer android debug")
    
    try:
        # Ejecutar buildozer en modo interactivo para manejar licencias
        process = subprocess.Popen(
            ['buildozer', 'android', 'debug'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Mostrar output en tiempo real
        for line in process.stdout:
            print(line.rstrip())
            
            # Auto-aceptar licencias si aparecen
            if "Accept? (y/N):" in line:
                process.stdin.write("y\n")
                process.stdin.flush()
        
        process.wait()
        
        if process.returncode == 0:
            print("✅ APK generada exitosamente!")
            
            # Buscar el APK generado
            bin_dir = "bin"
            if os.path.exists(bin_dir):
                apk_files = [f for f in os.listdir(bin_dir) if f.endswith('.apk')]
                if apk_files:
                    apk_path = os.path.join(bin_dir, apk_files[0])
                    size = os.path.getsize(apk_path) / (1024 * 1024)  # MB
                    print(f"📱 APK: {apk_path} ({size:.1f} MB)")
                    return True
            
            print("⚠️ APK generada pero no encontrada en bin/")
            return True
        else:
            print(f"❌ Error generando APK (código: {process.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando buildozer: {e}")
        return False

def main():
    """Función principal"""
    print("🏗️  GENERADOR DE APK LOCAL - DaniStore")
    print("=" * 50)
    
    # Verificar sistema operativo
    if platform.system() == "Windows":
        print("⚠️  NOTA: Buildozer funciona mejor en Linux/macOS")
        print("   Considera usar WSL (Windows Subsystem for Linux)")
        print()
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ Faltan dependencias. Instala Python, pip y git primero.")
        return False
    
    # Instalar Buildozer
    if not instalar_buildozer():
        print("\n❌ Error instalando Buildozer")
        return False
    
    # Generar APK
    if not generar_apk():
        print("\n❌ Error generando APK")
        return False
    
    print("\n🎉 ¡Proceso completado exitosamente!")
    print("\n📋 SIGUIENTES PASOS:")
    print("1. Busca tu APK en la carpeta 'bin/'")
    print("2. Transfiere el APK a tu dispositivo Android")
    print("3. Instala el APK (habilita 'Fuentes desconocidas')")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)