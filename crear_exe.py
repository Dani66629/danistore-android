"""
Script para crear el ejecutable (.exe) de la Ruleta de Torneos Dani666
"""
import os
import subprocess
import sys

def instalar_dependencias():
    """Instalar las dependencias necesarias"""
    print("🔧 Instalando dependencias necesarias...")
    
    dependencias = [
        'pyinstaller',
        'pillow'
    ]
    
    for dep in dependencias:
        try:
            print(f"   Instalando {dep}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"   ✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"   ❌ Error instalando {dep}")
            return False
    
    return True

def crear_icono():
    """Crear el icono si no existe"""
    if not os.path.exists('torneo_icon.ico'):
        print("🎨 Creando icono profesional de torneo...")
        try:
            subprocess.check_call([sys.executable, 'crear_icono.py'])
            print("   ✅ Icono creado exitosamente")
        except subprocess.CalledProcessError:
            print("   ❌ Error creando el icono")
            return False
    else:
        print("   ✅ Icono ya existe")
    
    return True

def crear_spec_file():
    """Crear archivo .spec personalizado para PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ruleta_torneo.py'],
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
    name='Dani666_Ruleta_Torneos',
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
    icon='torneo_icon.ico',
    version_file='version_info.txt'
)
'''
    
    with open('ruleta_torneo.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado")

def crear_version_info():
    """Crear archivo de información de versión"""
    version_content = '''# UTF-8
#
# Para más detalles sobre los campos fijos FileInfo, ver:
# https://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
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
        StringStruct(u'FileDescription', u'Sistema Profesional de Torneos'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'Dani666_Ruleta_Torneos'),
        StringStruct(u'LegalCopyright', u'© 2024 Dani666. Todos los derechos reservados.'),
        StringStruct(u'OriginalFilename', u'Dani666_Ruleta_Torneos.exe'),
        StringStruct(u'ProductName', u'Dani666 Tournament System'),
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
    print("   Esto puede tomar varios minutos...")
    
    try:
        # Usar el archivo .spec personalizado
        cmd = [
            'pyinstaller',
            '--clean',
            '--noconfirm',
            'ruleta_torneo.spec'
        ]
        
        subprocess.check_call(cmd)
        print("   ✅ Compilación exitosa!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error en la compilación: {e}")
        return False

def limpiar_archivos():
    """Limpiar archivos temporales"""
    print("🧹 Limpiando archivos temporales...")
    
    archivos_temp = [
        'ruleta_torneo.spec',
        'version_info.txt'
    ]
    
    carpetas_temp = [
        'build',
        '__pycache__'
    ]
    
    for archivo in archivos_temp:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f"   🗑️ Eliminado: {archivo}")
    
    import shutil
    for carpeta in carpetas_temp:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
            print(f"   🗑️ Eliminado: {carpeta}")

def main():
    """Función principal"""
    print("🎯 CREADOR DE EJECUTABLE - DANI666 TOURNAMENT SYSTEM")
    print("=" * 60)
    
    # Verificar que existe el archivo principal
    if not os.path.exists('ruleta_torneo.py'):
        print("❌ Error: No se encuentra ruleta_torneo.py")
        print("   Asegúrate de ejecutar este script en la misma carpeta.")
        return
    
    # Paso 1: Instalar dependencias
    if not instalar_dependencias():
        print("❌ Error instalando dependencias. Abortando.")
        return
    
    # Paso 2: Crear icono
    if not crear_icono():
        print("❌ Error creando icono. Abortando.")
        return
    
    # Paso 3: Crear archivos de configuración
    crear_spec_file()
    crear_version_info()
    
    # Paso 4: Compilar
    if not compilar_exe():
        print("❌ Error compilando ejecutable. Abortando.")
        return
    
    # Paso 5: Limpiar
    limpiar_archivos()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("🎉 ¡EJECUTABLE CREADO EXITOSAMENTE!")
    print("=" * 60)
    print("📁 Ubicación: dist/Dani666_Ruleta_Torneos.exe")
    print("🎨 Icono: Trofeo de torneo profesional incluido")
    print("💼 Información: Dani666 Tournament System v1.0")
    print("\n🚀 ¡Tu aplicación está lista para distribuir!")
    print("\n📋 Archivos creados:")
    print("   - dist/Dani666_Ruleta_Torneos.exe (ejecutable principal)")
    print("   - torneo_icon.ico (icono)")
    print("   - torneo_icon.png (icono para visualización)")

if __name__ == "__main__":
    main()