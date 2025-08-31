#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creador de Ejecutable para Gestor de Suscripciones - Dani666
"""

import os
import sys
import subprocess
import shutil

def instalar_dependencias():
    """Instalar las dependencias necesarias"""
    print("🔧 Instalando dependencias necesarias...")
    
    dependencias = ['pyinstaller', 'pillow']
    
    for dep in dependencias:
        try:
            print(f"   📦 Instalando {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                         check=True, capture_output=True)
            print(f"   ✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error instalando {dep}: {e}")
            return False
    
    return True

def crear_icono():
    """Crear el icono si no existe"""
    if not os.path.exists('gestor_icon.ico'):
        print("🎨 Creando icono...")
        try:
            subprocess.run([sys.executable, 'crear_icono_gestor.py'], check=True)
            print("✅ Icono creado exitosamente")
        except subprocess.CalledProcessError:
            print("⚠️ No se pudo crear el icono, continuando sin él")
    else:
        print("✅ Icono ya existe")
    
    return True

def crear_spec_file():
    """Crear archivo .spec personalizado para PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gestor_suscripciones.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GestorSuscripciones_Dani666',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='gestor_icon.ico' if os.path.exists('gestor_icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
'''
    
    with open('gestor_suscripciones.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado")

def crear_version_info():
    """Crear archivo de información de versión"""
    version_content = '''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Dani666'),
        StringStruct(u'FileDescription', u'Gestor de Suscripciones de Streaming'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'GestorSuscripciones'),
        StringStruct(u'LegalCopyright', u'© 2025 Dani666. Todos los derechos reservados.'),
        StringStruct(u'OriginalFilename', u'GestorSuscripciones_Dani666.exe'),
        StringStruct(u'ProductName', u'Gestor de Suscripciones Dani666'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_content)
    
    print("✅ Archivo de versión creado")

def compilar_exe():
    """Compilar el ejecutable usando PyInstaller"""
    print("🚀 Compilando ejecutable...")
    
    try:
        # Usar el archivo .spec personalizado
        cmd = [sys.executable, '-m', 'PyInstaller', '--clean', 'gestor_suscripciones.spec']
        
        print("   📝 Comando: " + " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Compilación exitosa")
            return True
        else:
            print(f"❌ Error en compilación:")
            print(f"   STDOUT: {result.stdout}")
            print(f"   STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        return False

def limpiar_archivos():
    """Limpiar archivos temporales"""
    print("🧹 Limpiando archivos temporales...")
    
    archivos_limpiar = [
        'gestor_suscripciones.spec',
        'version_info.txt'
    ]
    
    carpetas_limpiar = [
        'build',
        '__pycache__'
    ]
    
    # Limpiar archivos
    for archivo in archivos_limpiar:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"   🗑️ Eliminado: {archivo}")
            except Exception as e:
                print(f"   ⚠️ No se pudo eliminar {archivo}: {e}")
    
    # Limpiar carpetas
    for carpeta in carpetas_limpiar:
        if os.path.exists(carpeta):
            try:
                shutil.rmtree(carpeta)
                print(f"   🗑️ Eliminado: {carpeta}")
            except Exception as e:
                print(f"   ⚠️ No se pudo eliminar {carpeta}: {e}")

def main():
    """Función principal"""
    print("🎯 CREADOR DE EJECUTABLE - GESTOR DE SUSCRIPCIONES DANI666")
    print("=" * 60)
    
    # Verificar que existe el archivo principal
    if not os.path.exists('gestor_suscripciones.py'):
        print("❌ Error: No se encontró gestor_suscripciones.py")
        print("   Asegúrate de ejecutar este script en la misma carpeta que gestor_suscripciones.py")
        return
    
    # Paso 1: Instalar dependencias
    print("\n📦 PASO 1: Instalando dependencias...")
    if not instalar_dependencias():
        print("❌ Error instalando dependencias. Abortando.")
        return
    
    # Paso 2: Crear icono
    print("\n🎨 PASO 2: Preparando icono...")
    crear_icono()
    
    # Paso 3: Crear archivos de configuración
    print("\n⚙️ PASO 3: Creando archivos de configuración...")
    crear_spec_file()
    crear_version_info()
    
    # Paso 4: Compilar
    print("\n🚀 PASO 4: Compilando ejecutable...")
    if not compilar_exe():
        print("❌ Error en la compilación. Revisa los errores arriba.")
        return
    
    # Paso 5: Limpiar
    print("\n🧹 PASO 5: Limpiando archivos temporales...")
    limpiar_archivos()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("🎉 ¡EJECUTABLE CREADO EXITOSAMENTE!")
    print("=" * 60)
    
    if os.path.exists('dist/GestorSuscripciones_Dani666.exe'):
        exe_size = os.path.getsize('dist/GestorSuscripciones_Dani666.exe') / (1024*1024)
        print(f"📁 Ubicación: dist/GestorSuscripciones_Dani666.exe")
        print(f"📏 Tamaño: {exe_size:.1f} MB")
        print(f"🎯 Listo para distribuir!")
        
        print("\n📋 ARCHIVOS GENERADOS:")
        print("   - dist/GestorSuscripciones_Dani666.exe (ejecutable principal)")
        if os.path.exists('gestor_icon.ico'):
            print("   - gestor_icon.ico (icono)")
        if os.path.exists('gestor_icon.png'):
            print("   - gestor_icon.png (icono para visualización)")
    else:
        print("❌ No se encontró el ejecutable generado")

if __name__ == "__main__":
    main()