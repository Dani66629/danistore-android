#!/usr/bin/env python3
"""
Script para subir el Gestor de Suscripciones a GitHub y generar APK automáticamente
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def verificar_git():
    """Verificar que git esté instalado y configurado"""
    print("🔍 Verificando Git...")
    
    try:
        # Verificar git
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git no está instalado")
            return False
        print(f"✅ {result.stdout.strip()}")
        
        # Verificar configuración
        try:
            name = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
            email = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
            
            if name.returncode == 0 and email.returncode == 0:
                print(f"✅ Usuario: {name.stdout.strip()}")
                print(f"✅ Email: {email.stdout.strip()}")
            else:
                print("⚠️ Git no está configurado completamente")
                configurar_git()
        except:
            print("⚠️ Error verificando configuración de Git")
            configurar_git()
        
        return True
        
    except FileNotFoundError:
        print("❌ Git no está instalado")
        return False

def configurar_git():
    """Configurar Git si no está configurado"""
    print("\n🔧 Configurando Git...")
    
    nombre = input("👤 Ingresa tu nombre para Git: ").strip()
    email = input("📧 Ingresa tu email para Git: ").strip()
    
    if nombre and email:
        subprocess.run(['git', 'config', '--global', 'user.name', nombre])
        subprocess.run(['git', 'config', '--global', 'user.email', email])
        print("✅ Git configurado correctamente")
    else:
        print("❌ Configuración cancelada")

def verificar_archivos_gestor():
    """Verificar archivos específicos del gestor"""
    print("\n📋 Verificando archivos del gestor...")
    
    archivos_principales = [
        'gestor_suscripciones.py',
        'danistore_app.py',
        'buildozer.spec'
    ]
    
    archivos_opcionales = [
        'gestor_icon.png',
        'gestor_icon.ico',
        'iconos_android/gestor_icon.png',
        'suscripciones_data.json'
    ]
    
    # Verificar archivos principales
    for archivo in archivos_principales:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo) / 1024  # KB
            print(f"✅ {archivo}: {size:.1f} KB")
        else:
            print(f"❌ {archivo}: No encontrado")
            return False
    
    # Verificar archivos opcionales
    for archivo in archivos_opcionales:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo) / 1024  # KB
            print(f"✅ {archivo}: {size:.1f} KB (opcional)")
    
    return True

def inicializar_repositorio():
    """Inicializar repositorio Git si no existe"""
    print("\n🔧 Configurando repositorio...")
    
    if not os.path.exists('.git'):
        print("📁 Inicializando repositorio Git...")
        subprocess.run(['git', 'init'])
        
        # Crear .gitignore
        gitignore_content = """# Archivos de construcción
.buildozer/
bin/
build/
dist/

# Archivos de Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so

# Archivos del sistema
.DS_Store
Thumbs.db

# Archivos de datos sensibles (opcional)
# suscripciones_data.json

# Logs
*.log

# Archivos temporales
*.tmp
*.temp
"""
        
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        print("✅ .gitignore creado")
    
    # Agregar archivos
    print("📦 Agregando archivos al repositorio...")
    subprocess.run(['git', 'add', '.'])
    
    # Commit inicial
    mensaje_commit = f"🚀 Gestor de Suscripciones DaniStore - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    result = subprocess.run(['git', 'commit', '-m', mensaje_commit], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Commit realizado")
    else:
        print("⚠️ No hay cambios para commit o ya está actualizado")

def configurar_repositorio_remoto():
    """Configurar repositorio remoto en GitHub"""
    print("\n🌐 Configurando repositorio remoto...")
    
    # Verificar si ya existe un remoto
    result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
    
    if 'origin' in result.stdout:
        print("✅ Repositorio remoto ya configurado:")
        print(result.stdout)
        return True
    
    print("\n📋 OPCIONES PARA REPOSITORIO REMOTO:")
    print("1. 🆕 Crear nuevo repositorio en GitHub")
    print("2. 🔗 Conectar a repositorio existente")
    print("3. ⏭️ Saltar configuración remota")
    
    opcion = input("\nSelecciona una opción (1-3): ").strip()
    
    if opcion == "1":
        print("\n🆕 CREAR NUEVO REPOSITORIO:")
        print("1. Ve a https://github.com/new")
        print("2. Nombre sugerido: 'danistore-gestor-suscripciones'")
        print("3. Descripción: 'Gestor de Suscripciones de Streaming - DaniStore'")
        print("4. Marca como 'Public' para usar GitHub Actions gratis")
        print("5. NO inicialices con README (ya tienes archivos)")
        
        repo_url = input("\n🔗 Pega la URL del repositorio (https://github.com/usuario/repo.git): ").strip()
        
        if repo_url:
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
            print("✅ Repositorio remoto configurado")
            return True
    
    elif opcion == "2":
        repo_url = input("🔗 URL del repositorio existente: ").strip()
        if repo_url:
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
            print("✅ Repositorio remoto configurado")
            return True
    
    elif opcion == "3":
        print("⏭️ Configuración remota saltada")
        return False
    
    return False

def subir_a_github():
    """Subir código a GitHub"""
    print("\n🚀 Subiendo código a GitHub...")
    
    try:
        # Verificar rama actual
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
        rama_actual = result.stdout.strip()
        
        if not rama_actual:
            rama_actual = 'main'
            subprocess.run(['git', 'checkout', '-b', 'main'])
        
        print(f"📍 Rama actual: {rama_actual}")
        
        # Push al repositorio
        print("📤 Subiendo archivos...")
        result = subprocess.run(['git', 'push', '-u', 'origin', rama_actual], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Código subido exitosamente a GitHub")
            print("\n🎯 SIGUIENTE PASO:")
            print("1. Ve a tu repositorio en GitHub")
            print("2. Haz clic en 'Actions'")
            print("3. El workflow se ejecutará automáticamente")
            print("4. Descarga la APK desde 'Artifacts'")
            return True
        else:
            print(f"❌ Error subiendo código: {result.stderr}")
            
            # Intentar con autenticación
            print("\n🔐 Puede que necesites autenticación...")
            print("Opciones:")
            print("1. Configura un Personal Access Token")
            print("2. Usa GitHub CLI: gh auth login")
            print("3. Configura SSH keys")
            
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def mostrar_instrucciones_github_actions():
    """Mostrar instrucciones para GitHub Actions"""
    print("\n📋 INSTRUCCIONES PARA GITHUB ACTIONS:")
    print("=" * 50)
    
    print("\n🔧 CONFIGURACIÓN AUTOMÁTICA:")
    print("✅ El workflow ya está configurado en .github/workflows/build-apk.yml")
    print("✅ Se ejecutará automáticamente cuando subas cambios")
    
    print("\n🚀 PROCESO AUTOMÁTICO:")
    print("1. 📥 GitHub descarga tu código")
    print("2. 🐍 Instala Python y dependencias")
    print("3. 📦 Instala Buildozer y Kivy")
    print("4. 🏗️ Compila la APK para Android")
    print("5. 📱 Sube la APK como artefacto")
    
    print("\n📥 DESCARGAR APK:")
    print("1. Ve a tu repositorio en GitHub")
    print("2. Haz clic en 'Actions'")
    print("3. Selecciona el workflow más reciente")
    print("4. Descarga desde 'Artifacts'")
    
    print("\n⚡ TRIGGERS AUTOMÁTICOS:")
    print("• Push a main/master")
    print("• Cambios en gestor_suscripciones.py")
    print("• Cambios en danistore_app.py")
    print("• Cambios en buildozer.spec")
    print("• Ejecución manual desde GitHub")

def main():
    """Función principal"""
    print("🚀 SUBIR GESTOR DE SUSCRIPCIONES A GITHUB")
    print("=" * 50)
    print("📱 Generación automática de APK con GitHub Actions")
    print()
    
    # Verificar Git
    if not verificar_git():
        print("\n❌ Instala Git primero: https://git-scm.com/downloads")
        return False
    
    # Verificar archivos del gestor
    if not verificar_archivos_gestor():
        print("\n❌ Faltan archivos necesarios del gestor")
        return False
    
    # Inicializar repositorio
    inicializar_repositorio()
    
    # Configurar repositorio remoto
    remoto_configurado = configurar_repositorio_remoto()
    
    if remoto_configurado:
        # Subir a GitHub
        if subir_a_github():
            mostrar_instrucciones_github_actions()
            
            print("\n🎉 ¡PROCESO COMPLETADO!")
            print("\n📋 RESUMEN:")
            print("✅ Código subido a GitHub")
            print("✅ GitHub Actions configurado")
            print("✅ APK se generará automáticamente")
            
            print("\n🔗 ENLACES ÚTILES:")
            print("• GitHub Actions: https://github.com/features/actions")
            print("• Buildozer: https://buildozer.readthedocs.io/")
            print("• Kivy: https://kivy.org/")
            
            return True
        else:
            print("\n❌ Error subiendo a GitHub")
            return False
    else:
        print("\n⚠️ Repositorio remoto no configurado")
        print("Configúralo manualmente y ejecuta:")
        print("git push -u origin main")
        return False

if __name__ == "__main__":
    success = main()
    input("\nPresiona Enter para salir...")
    sys.exit(0 if success else 1)