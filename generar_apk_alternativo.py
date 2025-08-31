#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador alternativo de APK para DaniStore
Incluye instrucciones detalladas y soluciones
"""

import os
import sys
import subprocess

def verificar_buildozer():
    """Verificar instalación de Buildozer"""
    print("🔍 VERIFICANDO BUILDOZER")
    print("=" * 50)
    
    try:
        result = subprocess.run(['buildozer', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Buildozer instalado correctamente")
            print(f"Versión: {result.stdout.strip()}")
            return True
        else:
            print("❌ Buildozer instalado pero con errores")
            return False
    except FileNotFoundError:
        print("❌ Buildozer no encontrado")
        return False

def instalar_buildozer_windows():
    """Instalar Buildozer en Windows"""
    print("\n📦 INSTALANDO BUILDOZER PARA WINDOWS")
    print("=" * 50)
    
    comandos = [
        [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
        [sys.executable, '-m', 'pip', 'install', 'buildozer'],
        [sys.executable, '-m', 'pip', 'install', 'kivy[base]'],
        [sys.executable, '-m', 'pip', 'install', 'cython'],
    ]
    
    for cmd in comandos:
        print(f"Ejecutando: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            print("✅ Comando exitoso")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: {e}")
            return False
    
    return True

def crear_apk_linux():
    """Crear APK en Linux/WSL"""
    print("\n🐧 GENERANDO APK EN LINUX")
    print("=" * 50)
    
    script_linux = '''#!/bin/bash
# Script para generar APK en Linux

echo "🚀 GENERANDO DANISTORE APK"
echo "=========================="

# Verificar dependencias
echo "📦 Instalando dependencias..."
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalar Python dependencies
pip3 install --user buildozer cython kivy[base]

# Generar APK
echo "📱 Generando APK..."
buildozer android debug

echo "✅ APK generada en bin/"
ls -la bin/
'''
    
    with open('generar_apk_linux.sh', 'w') as f:
        f.write(script_linux)
    
    print("✅ Script creado: generar_apk_linux.sh")
    print("🐧 Para usar en Linux/WSL:")
    print("   chmod +x generar_apk_linux.sh")
    print("   ./generar_apk_linux.sh")

def crear_exe_windows():
    """Crear ejecutable para Windows como alternativa"""
    print("\n🪟 CREANDO EJECUTABLE PARA WINDOWS")
    print("=" * 50)
    
    try:
        # Instalar PyInstaller
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        
        # Crear ejecutable
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--icon=iconos_android/danistore_icon.png',
            '--name=DaniStore',
            'danistore_app.py'
        ]
        
        print(f"Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable creado exitosamente")
            print("📁 Busca DaniStore.exe en la carpeta dist/")
            return True
        else:
            print("❌ Error creando ejecutable:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def crear_instrucciones_completas():
    """Crear instrucciones detalladas"""
    print("\n📋 CREANDO INSTRUCCIONES COMPLETAS")
    print("=" * 50)
    
    instrucciones = '''# 📱 CÓMO GENERAR LA APK DE DANISTORE

## 🚨 PROBLEMA ACTUAL
Buildozer tiene problemas en Windows. Aquí tienes las soluciones:

## ✅ SOLUCIÓN 1: USAR LINUX/WSL (RECOMENDADO)

### Paso 1: Instalar WSL en Windows
```bash
# En PowerShell como administrador
wsl --install
```

### Paso 2: En WSL/Linux
```bash
# Clonar archivos o copiar a WSL
# Instalar dependencias
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalar Python packages
pip3 install --user buildozer cython kivy[base]

# Generar APK
buildozer android debug
```

### Resultado:
- APK generada en: `bin/danistore-1.0-arm64-v8a-debug.apk`

## ✅ SOLUCIÓN 2: USAR GITHUB ACTIONS (AUTOMÁTICO)

### Crear archivo `.github/workflows/build-apk.yml`:
```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y openjdk-8-jdk
        pip install buildozer cython kivy[base]
    - name: Build APK
      run: buildozer android debug
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: danistore-apk
        path: bin/*.apk
```

## ✅ SOLUCIÓN 3: USAR SERVICIO ONLINE

### Repl.it o CodeSpaces:
1. Subir archivos a Repl.it
2. Ejecutar en terminal Linux
3. Descargar APK generada

## ✅ SOLUCIÓN 4: EJECUTABLE WINDOWS (ALTERNATIVA)

Si no puedes generar APK, usa el ejecutable:
```bash
python generar_apk_alternativo.py
```

Esto crea `DaniStore.exe` que funciona igual en Windows.

## 📱 ARCHIVOS NECESARIOS PARA APK

Asegúrate de tener:
- ✅ `main.py` - Punto de entrada
- ✅ `danistore_app.py` - Aplicación principal
- ✅ `buildozer.spec` - Configuración
- ✅ `iconos_android/danistore_icon.png` - Icono

## 🎯 RESULTADO FINAL

Una vez generada, la APK:
- 📱 Se instala en cualquier Android 5.0+
- 💾 Tamaño: ~20-50 MB
- ✅ Funciona completamente offline
- 🔔 Incluye notificaciones nativas
- 📋 Gestión completa de suscripciones
- 💬 Integración WhatsApp

## 🆘 SI TIENES PROBLEMAS

1. **Windows**: Usa WSL o GitHub Actions
2. **Linux**: Funciona directamente
3. **Mac**: Funciona con algunos ajustes
4. **Online**: Usa Repl.it o CodeSpaces

## 📞 CONTACTO

Si necesitas ayuda específica, comparte:
- Sistema operativo
- Mensajes de error
- Archivos que tienes

¡Tu DaniStore APK está al alcance! 🚀
'''
    
    with open('COMO_GENERAR_APK.md', 'w', encoding='utf-8') as f:
        f.write(instrucciones)
    
    print("✅ Instrucciones creadas: COMO_GENERAR_APK.md")

def main():
    """Función principal"""
    print("🚀 GENERADOR ALTERNATIVO DE APK DANISTORE")
    print("=" * 60)
    
    # Verificar Buildozer
    buildozer_ok = verificar_buildozer()
    
    if not buildozer_ok:
        print("\n⚠️  Buildozer no funciona correctamente en Windows")
        print("🔧 Intentando soluciones alternativas...")
        
        # Crear script para Linux
        crear_apk_linux()
        
        # Crear ejecutable para Windows
        respuesta = input("\n¿Crear ejecutable Windows como alternativa? (s/n): ").lower()
        if respuesta == 's':
            crear_exe_windows()
    
    # Crear instrucciones completas
    crear_instrucciones_completas()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN")
    print("=" * 60)
    
    if buildozer_ok:
        print("✅ Buildozer funcionando - Puedes generar APK")
        print("🚀 Comando: buildozer android debug")
    else:
        print("❌ Buildozer con problemas en Windows")
        print("✅ Script Linux creado: generar_apk_linux.sh")
        print("✅ Instrucciones completas: COMO_GENERAR_APK.md")
    
    print("\n🎯 OPCIONES DISPONIBLES:")
    print("1. 🐧 Usar WSL/Linux (Recomendado)")
    print("2. 🌐 Usar GitHub Actions (Automático)")
    print("3. 💻 Usar ejecutable Windows (Alternativa)")
    print("4. ☁️  Usar servicio online (Repl.it)")
    
    print("\n📱 RESULTADO FINAL:")
    print("Una vez generada, tendrás danistore.apk listo para Android!")

if __name__ == "__main__":
    main()