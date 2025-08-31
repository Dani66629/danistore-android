#!/usr/bin/env python3
"""
Script para generar APK del Gestor de Suscripciones DaniStore
Versión optimizada para GitHub Actions y local
"""

import os
import sys
import subprocess
import platform
import shutil

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
        "pip install pillow",
        "pip install pyjnius"
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

def verificar_archivos():
    """Verificar que todos los archivos necesarios existen"""
    print("\n📋 Verificando archivos necesarios...")
    
    archivos_necesarios = [
        'danistore_app.py',
        'buildozer.spec'
    ]
    
    # Verificar archivos principales
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✅ {archivo}: Encontrado")
        else:
            print(f"❌ {archivo}: No encontrado")
            return False
    
    # Verificar icono (crear uno por defecto si no existe)
    icono_path = 'iconos_android/gestor_icon.png'
    if os.path.exists(icono_path):
        print(f"✅ {icono_path}: Encontrado")
    else:
        print(f"⚠️ {icono_path}: No encontrado, usando icono por defecto")
        crear_icono_por_defecto()
    
    return True

def crear_icono_por_defecto():
    """Crear un icono por defecto si no existe"""
    try:
        os.makedirs('iconos_android', exist_ok=True)
        
        # Copiar icono existente si hay uno disponible
        iconos_posibles = ['gestor_icon.png', 'torneo_icon.png', 'icon.png']
        for icono in iconos_posibles:
            if os.path.exists(icono):
                shutil.copy2(icono, 'iconos_android/gestor_icon.png')
                print(f"✅ Icono copiado desde {icono}")
                return
        
        print("⚠️ No se encontró icono, buildozer usará uno por defecto")
    except Exception as e:
        print(f"⚠️ Error creando icono: {e}")

def generar_apk():
    """Genera el APK usando Buildozer"""
    print("\n🚀 Generando APK del Gestor de Suscripciones...")
    
    try:
        # Limpiar build anterior si existe
        if os.path.exists('.buildozer'):
            print("🧹 Limpiando build anterior...")
            subprocess.run(['buildozer', 'android', 'clean'], 
                         capture_output=True, text=True)
        
        # Ejecutar buildozer
        print("🔨 Ejecutando: buildozer android debug")
        print("⏳ Esto puede tomar varios minutos...")
        
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
            print("\n✅ APK generada exitosamente!")
            
            # Buscar el APK generado
            bin_dir = "bin"
            if os.path.exists(bin_dir):
                apk_files = [f for f in os.listdir(bin_dir) if f.endswith('.apk')]
                if apk_files:
                    apk_path = os.path.join(bin_dir, apk_files[0])
                    size = os.path.getsize(apk_path) / (1024 * 1024)  # MB
                    print(f"📱 APK: {apk_path} ({size:.1f} MB)")
                    
                    # Renombrar APK con nombre más descriptivo
                    nuevo_nombre = "DaniStore_Gestor_Suscripciones.apk"
                    nuevo_path = os.path.join(bin_dir, nuevo_nombre)
                    
                    try:
                        os.rename(apk_path, nuevo_path)
                        print(f"📱 APK renombrada: {nuevo_path}")
                        apk_path = nuevo_path
                    except:
                        pass
                    
                    return apk_path
            
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
    print("🏗️  GENERADOR DE APK - GESTOR DE SUSCRIPCIONES DANISTORE")
    print("=" * 60)
    
    # Verificar sistema operativo
    if platform.system() == "Windows":
        print("⚠️  NOTA: Buildozer funciona mejor en Linux/macOS")
        print("   Considera usar WSL (Windows Subsystem for Linux)")
        print()
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ Faltan dependencias. Instala Python, pip y git primero.")
        return False
    
    # Verificar archivos
    if not verificar_archivos():
        print("\n❌ Faltan archivos necesarios.")
        return False
    
    # Instalar Buildozer
    if not instalar_buildozer():
        print("\n❌ Error instalando Buildozer")
        return False
    
    # Generar APK
    apk_path = generar_apk()
    if not apk_path:
        print("\n❌ Error generando APK")
        return False
    
    print("\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
    print("\n📋 RESUMEN:")
    print(f"📱 App: DaniStore - Gestor de Suscripciones")
    print(f"📁 APK: {apk_path if isinstance(apk_path, str) else 'bin/*.apk'}")
    print(f"🎯 Funciones: Gestión completa de suscripciones de streaming")
    
    print("\n📋 SIGUIENTES PASOS:")
    print("1. 📱 Transfiere la APK a tu dispositivo Android")
    print("2. ⚙️  Habilita 'Fuentes desconocidas' en Configuración > Seguridad")
    print("3. 📲 Instala la APK tocándola en tu dispositivo")
    print("4. 🚀 ¡Disfruta gestionando tus suscripciones!")
    
    print("\n💡 CARACTERÍSTICAS DE LA APP:")
    print("• ➕ Agregar nuevas suscripciones")
    print("• 📋 Ver lista de suscripciones activas")
    print("• 📱 Generar mensajes para WhatsApp")
    print("• 🔔 Notificaciones de vencimiento")
    print("• 🗑️ Eliminar suscripciones")
    print("• 💾 Guardado automático de datos")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nPresiona Enter para salir...")
    sys.exit(0 if success else 1)