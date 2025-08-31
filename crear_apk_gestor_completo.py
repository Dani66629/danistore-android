#!/usr/bin/env python3
"""
Script completo para crear APK del Gestor de Suscripciones DaniStore
Incluye todas las opciones: Local, GitHub Actions, y Online
"""

import os
import sys
import subprocess
import platform
import json
from datetime import datetime

def mostrar_banner():
    """Mostrar banner de DaniStore"""
    print("=" * 60)
    print("🎬 DANISTORE - GENERADOR DE APK GESTOR SUSCRIPCIONES 🎬")
    print("=" * 60)
    print("📱 Convierte tu gestor en una app Android profesional")
    print("🚀 Múltiples métodos de generación disponibles")
    print("💎 Tu éxito es nuestro éxito")
    print("=" * 60)
    print()

def verificar_sistema():
    """Verificar el sistema y dependencias"""
    print("🔍 VERIFICANDO SISTEMA...")
    print("-" * 30)
    
    # Sistema operativo
    sistema = platform.system()
    print(f"💻 Sistema: {sistema} {platform.release()}")
    
    # Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"🐍 Python: {python_version}")
    
    # Verificar archivos necesarios
    archivos_necesarios = {
        'gestor_suscripciones.py': 'Gestor principal (Tkinter)',
        'danistore_app.py': 'App para Android (Kivy)',
        'buildozer.spec': 'Configuración APK'
    }
    
    print("\n📋 ARCHIVOS NECESARIOS:")
    todos_presentes = True
    
    for archivo, descripcion in archivos_necesarios.items():
        if os.path.exists(archivo):
            size = os.path.getsize(archivo) / 1024
            print(f"✅ {archivo}: {size:.1f} KB - {descripcion}")
        else:
            print(f"❌ {archivo}: No encontrado - {descripcion}")
            todos_presentes = False
    
    # Archivos opcionales
    archivos_opcionales = {
        'gestor_icon.png': 'Icono principal',
        'iconos_android/gestor_icon.png': 'Icono para Android',
        'suscripciones_data.json': 'Datos de prueba'
    }
    
    print("\n📁 ARCHIVOS OPCIONALES:")
    for archivo, descripcion in archivos_opcionales.items():
        if os.path.exists(archivo):
            size = os.path.getsize(archivo) / 1024
            print(f"✅ {archivo}: {size:.1f} KB - {descripcion}")
        else:
            print(f"⚠️ {archivo}: No encontrado - {descripcion}")
    
    return todos_presentes

def mostrar_opciones():
    """Mostrar opciones disponibles"""
    print("\n🚀 MÉTODOS DE GENERACIÓN DE APK:")
    print("=" * 40)
    
    print("\n1️⃣ GITHUB ACTIONS (Recomendado)")
    print("   ✅ Automático y gratuito")
    print("   ✅ No requiere configuración local")
    print("   ✅ APK optimizada y firmada")
    print("   ✅ Historial de builds")
    print("   📋 Requisitos: Cuenta GitHub")
    
    print("\n2️⃣ BUILDOZER LOCAL")
    print("   ✅ Control total del proceso")
    print("   ✅ Builds offline")
    print("   ⚠️ Requiere configuración compleja")
    print("   📋 Requisitos: Linux/macOS (WSL en Windows)")
    
    print("\n3️⃣ REPLIT ONLINE")
    print("   ✅ Sin instalaciones locales")
    print("   ✅ Entorno Linux completo")
    print("   ✅ Gratis y fácil")
    print("   📋 Requisitos: Navegador web")
    
    print("\n4️⃣ VERIFICAR CONFIGURACIÓN")
    print("   🔍 Revisar archivos y configuración")
    print("   🛠️ Preparar entorno")
    
    print("\n5️⃣ AYUDA Y DOCUMENTACIÓN")
    print("   📚 Guías detalladas")
    print("   🔧 Solución de problemas")

def opcion_github_actions():
    """Configurar y usar GitHub Actions"""
    print("\n🚀 GITHUB ACTIONS - GENERACIÓN AUTOMÁTICA")
    print("=" * 45)
    
    print("\n📋 PASOS A SEGUIR:")
    print("1. 📤 Subir código a GitHub")
    print("2. ⚙️ GitHub Actions se ejecuta automáticamente")
    print("3. 📱 Descargar APK desde 'Artifacts'")
    
    print("\n🔧 ¿QUIERES CONFIGURAR AUTOMÁTICAMENTE?")
    respuesta = input("Ejecutar script de configuración? (s/n): ").lower().strip()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        try:
            print("\n🚀 Ejecutando configuración automática...")
            subprocess.run([sys.executable, 'subir_a_github_gestor.py'])
        except FileNotFoundError:
            print("❌ Script de configuración no encontrado")
            print("📋 CONFIGURACIÓN MANUAL:")
            mostrar_instrucciones_github_manual()
    else:
        mostrar_instrucciones_github_manual()

def mostrar_instrucciones_github_manual():
    """Mostrar instrucciones manuales para GitHub"""
    print("\n📋 CONFIGURACIÓN MANUAL DE GITHUB:")
    print("-" * 35)
    
    print("\n1️⃣ CREAR REPOSITORIO:")
    print("   • Ve a https://github.com/new")
    print("   • Nombre: 'danistore-gestor-suscripciones'")
    print("   • Descripción: 'Gestor de Suscripciones DaniStore'")
    print("   • Público (para GitHub Actions gratis)")
    print("   • NO inicializar con README")
    
    print("\n2️⃣ SUBIR CÓDIGO:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Gestor DaniStore inicial'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/USUARIO/REPO.git")
    print("   git push -u origin main")
    
    print("\n3️⃣ VERIFICAR GITHUB ACTIONS:")
    print("   • Ve a tu repositorio → pestaña 'Actions'")
    print("   • El workflow se ejecutará automáticamente")
    print("   • Tiempo estimado: 10-15 minutos")
    
    print("\n4️⃣ DESCARGAR APK:")
    print("   • Actions → Último workflow → Artifacts")
    print("   • Descarga 'DaniStore-Gestor-APK'")

def opcion_buildozer_local():
    """Generar APK con Buildozer local"""
    print("\n🏗️ BUILDOZER LOCAL - GENERACIÓN DIRECTA")
    print("=" * 40)
    
    sistema = platform.system()
    
    if sistema == "Windows":
        print("⚠️ WINDOWS DETECTADO:")
        print("Buildozer funciona mejor en Linux/macOS")
        print("\n📋 OPCIONES PARA WINDOWS:")
        print("1. 🐧 Usar WSL (Windows Subsystem for Linux)")
        print("2. 🐳 Usar Docker")
        print("3. ☁️ Usar método online (Replit)")
        
        continuar = input("\n¿Continuar de todos modos? (s/n): ").lower().strip()
        if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
            return
    
    print("\n🔧 INSTALANDO DEPENDENCIAS...")
    
    # Verificar si existe el script local
    if os.path.exists('generar_gestor_apk.py'):
        try:
            subprocess.run([sys.executable, 'generar_gestor_apk.py'])
        except Exception as e:
            print(f"❌ Error ejecutando script local: {e}")
    else:
        print("❌ Script generar_gestor_apk.py no encontrado")
        print("\n📋 INSTALACIÓN MANUAL:")
        print("pip install buildozer kivy[base] cython pillow")
        print("buildozer android debug")

def opcion_replit_online():
    """Instrucciones para Replit"""
    print("\n☁️ REPLIT ONLINE - SIN INSTALACIONES")
    print("=" * 38)
    
    print("\n📋 PASOS DETALLADOS:")
    print("1️⃣ CREAR CUENTA:")
    print("   • Ve a https://replit.com")
    print("   • Regístrate gratis")
    print("   • Verifica tu email")
    
    print("\n2️⃣ CREAR PROYECTO:")
    print("   • 'Create Repl' → 'Python'")
    print("   • Nombre: 'danistore-gestor'")
    print("   • Descripción: 'Gestor Suscripciones APK'")
    
    print("\n3️⃣ SUBIR ARCHIVOS:")
    archivos_subir = [
        'danistore_app.py',
        'buildozer.spec',
        'gestor_icon.png (opcional)'
    ]
    
    for archivo in archivos_subir:
        print(f"   📁 {archivo}")
    
    print("\n4️⃣ EJECUTAR EN TERMINAL:")
    comandos = [
        "pip install buildozer",
        "pip install kivy[base]",
        "pip install cython",
        "buildozer android debug"
    ]
    
    for i, cmd in enumerate(comandos, 1):
        print(f"   {i}. {cmd}")
    
    print("\n5️⃣ DESCARGAR APK:")
    print("   • Carpeta 'bin/' → archivo .apk")
    print("   • Clic derecho → Download")
    
    print("\n⏱️ TIEMPO ESTIMADO: 15-20 minutos")
    print("💡 TIP: Replit es la opción más fácil para principiantes")

def opcion_verificar():
    """Verificar configuración completa"""
    print("\n🔍 VERIFICACIÓN COMPLETA DEL SISTEMA")
    print("=" * 38)
    
    # Verificar archivos
    print("\n📋 VERIFICANDO ARCHIVOS...")
    archivos_estado = {}
    
    archivos_criticos = {
        'gestor_suscripciones.py': 'Aplicación principal',
        'danistore_app.py': 'Versión Android (Kivy)',
        'buildozer.spec': 'Configuración APK'
    }
    
    for archivo, desc in archivos_criticos.items():
        existe = os.path.exists(archivo)
        archivos_estado[archivo] = existe
        status = "✅" if existe else "❌"
        print(f"{status} {archivo} - {desc}")
    
    # Verificar buildozer.spec
    if archivos_estado.get('buildozer.spec'):
        print("\n🔧 VERIFICANDO BUILDOZER.SPEC...")
        try:
            with open('buildozer.spec', 'r', encoding='utf-8') as f:
                content = f.read()
                
            checks = {
                'title = DaniStore': 'Título configurado',
                'package.name = gestorsuscripciones': 'Nombre del paquete',
                'source.main = danistore_app.py': 'Archivo principal',
                'requirements = python3,kivy': 'Dependencias básicas'
            }
            
            for check, desc in checks.items():
                if check.split('=')[0].strip() in content:
                    print(f"✅ {desc}")
                else:
                    print(f"⚠️ {desc} - Revisar configuración")
                    
        except Exception as e:
            print(f"❌ Error leyendo buildozer.spec: {e}")
    
    # Verificar dependencias Python
    print("\n🐍 VERIFICANDO DEPENDENCIAS PYTHON...")
    dependencias = ['kivy', 'buildozer', 'pillow', 'cython']
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep} instalado")
        except ImportError:
            print(f"❌ {dep} no instalado")
    
    # Verificar Git
    print("\n📦 VERIFICANDO GIT...")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git: {result.stdout.strip()}")
        else:
            print("❌ Git no encontrado")
    except FileNotFoundError:
        print("❌ Git no instalado")
    
    # Resumen
    print("\n📊 RESUMEN DE VERIFICACIÓN:")
    archivos_ok = sum(archivos_estado.values())
    total_archivos = len(archivos_estado)
    
    if archivos_ok == total_archivos:
        print("✅ Todos los archivos necesarios están presentes")
        print("🚀 ¡Listo para generar APK!")
    else:
        print(f"⚠️ {archivos_ok}/{total_archivos} archivos encontrados")
        print("📋 Completa los archivos faltantes antes de continuar")

def opcion_ayuda():
    """Mostrar ayuda y documentación"""
    print("\n📚 AYUDA Y DOCUMENTACIÓN")
    print("=" * 28)
    
    print("\n🔧 SOLUCIÓN DE PROBLEMAS COMUNES:")
    
    problemas = {
        "❌ 'buildozer' no reconocido": [
            "pip install --upgrade buildozer",
            "Reiniciar terminal",
            "Verificar PATH de Python"
        ],
        "❌ Error de permisos Android SDK": [
            "Usar Linux/macOS o WSL",
            "Configurar variables de entorno",
            "Usar método online (Replit)"
        ],
        "❌ APK no se genera": [
            "Verificar buildozer.spec",
            "Revisar logs de error",
            "Usar GitHub Actions"
        ],
        "❌ Error de dependencias": [
            "pip install -r requirements.txt",
            "Usar entorno virtual",
            "Actualizar pip y setuptools"
        ]
    }
    
    for problema, soluciones in problemas.items():
        print(f"\n{problema}:")
        for i, solucion in enumerate(soluciones, 1):
            print(f"   {i}. {solucion}")
    
    print("\n📖 DOCUMENTACIÓN ADICIONAL:")
    docs = {
        "🏗️ Buildozer": "https://buildozer.readthedocs.io/",
        "📱 Kivy": "https://kivy.org/doc/stable/",
        "🤖 GitHub Actions": "https://docs.github.com/actions",
        "☁️ Replit": "https://docs.replit.com/"
    }
    
    for nombre, url in docs.items():
        print(f"   {nombre}: {url}")
    
    print("\n💡 CONSEJOS IMPORTANTES:")
    consejos = [
        "🐧 Linux/macOS son mejores para Buildozer",
        "☁️ Usa métodos online si tienes problemas locales",
        "🔄 GitHub Actions es la opción más confiable",
        "📱 Prueba la APK en dispositivo real",
        "💾 Haz backup de tus archivos importantes"
    ]
    
    for consejo in consejos:
        print(f"   {consejo}")

def main():
    """Función principal"""
    mostrar_banner()
    
    # Verificar sistema básico
    if not verificar_sistema():
        print("\n❌ ARCHIVOS CRÍTICOS FALTANTES")
        print("📋 Asegúrate de tener:")
        print("   • gestor_suscripciones.py")
        print("   • danistore_app.py") 
        print("   • buildozer.spec")
        print("\n🔧 Ejecuta la opción 4 para más detalles")
    
    while True:
        mostrar_opciones()
        
        print("\n" + "=" * 40)
        opcion = input("🎯 Selecciona una opción (1-5) o 'q' para salir: ").strip().lower()
        
        if opcion in ['q', 'quit', 'salir', 'exit']:
            print("\n👋 ¡Gracias por usar DaniStore!")
            print("🚀 ¡Que tengas éxito con tu gestor de suscripciones!")
            break
        elif opcion == '1':
            opcion_github_actions()
        elif opcion == '2':
            opcion_buildozer_local()
        elif opcion == '3':
            opcion_replit_online()
        elif opcion == '4':
            opcion_verificar()
        elif opcion == '5':
            opcion_ayuda()
        else:
            print("❌ Opción no válida. Selecciona 1-5 o 'q'")
        
        input("\n⏸️ Presiona Enter para continuar...")
        print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Proceso cancelado por el usuario!")
        print("🚀 ¡Vuelve cuando quieras generar tu APK!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("🔧 Ejecuta la opción 5 para obtener ayuda")
    
    input("\nPresiona Enter para salir...")