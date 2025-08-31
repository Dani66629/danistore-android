#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para crear la APK de DaniStore
"""

import os
import subprocess
import sys

def instalar_dependencias():
    """Instalar dependencias necesarias"""
    print("📦 INSTALANDO DEPENDENCIAS PARA APK")
    print("=" * 50)
    
    dependencias = [
        'kivy[base]',
        'buildozer',
        'cython',
        'pillow'
    ]
    
    for dep in dependencias:
        print(f"📥 Instalando {dep}...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)
            print(f"✅ {dep} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"❌ Error instalando {dep}")
            return False
    
    return True

def verificar_archivos():
    """Verificar que todos los archivos necesarios existen"""
    print("\n🔍 VERIFICANDO ARCHIVOS NECESARIOS")
    print("=" * 50)
    
    archivos_necesarios = [
        'danistore_app.py',
        'buildozer.spec',
        'iconos_android/danistore_icon.png'
    ]
    
    todos_existen = True
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            todos_existen = False
    
    return todos_existen

def crear_main_py():
    """Crear main.py que apunte a danistore_app.py"""
    print("\n📝 CREANDO ARCHIVO MAIN.PY")
    print("=" * 50)
    
    contenido_main = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Punto de entrada principal para DaniStore Android
"""

from danistore_app import DaniStoreApp

if __name__ == '__main__':
    DaniStoreApp().run()
'''
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(contenido_main)
    
    print("✅ main.py creado correctamente")

def generar_apk():
    """Generar la APK usando Buildozer"""
    print("\n🚀 GENERANDO APK CON BUILDOZER")
    print("=" * 50)
    
    print("⚠️  NOTA: Este proceso puede tomar varios minutos...")
    print("⚠️  La primera vez descargará Android SDK/NDK (varios GB)")
    
    try:
        # Inicializar buildozer (solo la primera vez)
        print("🔧 Inicializando Buildozer...")
        subprocess.run(['buildozer', 'init'], check=False)
        
        # Generar APK en modo debug
        print("📱 Generando APK...")
        resultado = subprocess.run(['buildozer', 'android', 'debug'], 
                                 capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✅ APK generada exitosamente!")
            print("📁 Busca el archivo .apk en la carpeta bin/")
            return True
        else:
            print("❌ Error generando APK:")
            print(resultado.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ Buildozer no encontrado. Instalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'buildozer'])
        return generar_apk()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def crear_instrucciones():
    """Crear archivo con instrucciones"""
    print("\n📋 CREANDO INSTRUCCIONES")
    print("=" * 50)
    
    instrucciones = """# 📱 INSTRUCCIONES PARA CREAR APK DE DANISTORE

## 🔧 Requisitos previos:

### En Windows:
1. Instalar Python 3.8+
2. Instalar Git
3. Instalar Java JDK 8
4. Configurar variables de entorno

### En Linux/Ubuntu:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

## 🚀 Pasos para generar APK:

1. **Ejecutar el script automático:**
   ```bash
   python crear_apk.py
   ```

2. **O manualmente:**
   ```bash
   # Instalar dependencias
   pip install kivy[base] buildozer cython pillow
   
   # Generar APK
   buildozer android debug
   ```

## 📁 Archivos importantes:

- `danistore_app.py` - Aplicación principal
- `buildozer.spec` - Configuración de la APK
- `main.py` - Punto de entrada
- `iconos_android/` - Iconos de la aplicación

## 📱 Resultado:

La APK se generará en: `bin/danistore-1.0-arm64-v8a-debug.apk`

## 🔧 Solución de problemas:

1. **Error de permisos**: Ejecutar como administrador
2. **Falta Java**: Instalar OpenJDK 8
3. **Falta Android SDK**: Buildozer lo descarga automáticamente
4. **Error de memoria**: Cerrar otras aplicaciones

## 📲 Instalación en Android:

1. Habilitar "Fuentes desconocidas" en Android
2. Transferir el archivo .apk al teléfono
3. Instalar tocando el archivo
4. ¡Listo para usar!

## ✨ Características de la APK:

- ✅ Interfaz optimizada para móviles
- ✅ Notificaciones nativas de Android
- ✅ Copia automática al portapapeles
- ✅ Almacenamiento local de datos
- ✅ Iconos profesionales
- ✅ Tema oscuro elegante

¡Tu DaniStore estará listo para Android! 🎉
"""
    
    with open('INSTRUCCIONES_APK.md', 'w', encoding='utf-8') as f:
        f.write(instrucciones)
    
    print("✅ Instrucciones creadas: INSTRUCCIONES_APK.md")

def main():
    """Función principal"""
    print("🚀 CREADOR DE APK DANISTORE")
    print("=" * 60)
    
    # Paso 1: Verificar archivos
    if not verificar_archivos():
        print("\n❌ Faltan archivos necesarios. Ejecuta primero:")
        print("   python crear_icono_apk.py")
        return
    
    # Paso 2: Crear main.py
    crear_main_py()
    
    # Paso 3: Crear instrucciones
    crear_instrucciones()
    
    # Paso 4: Preguntar si instalar dependencias
    respuesta = input("\n¿Instalar dependencias ahora? (s/n): ").lower()
    if respuesta == 's':
        if not instalar_dependencias():
            print("❌ Error instalando dependencias")
            return
    
    # Paso 5: Preguntar si generar APK
    respuesta = input("\n¿Generar APK ahora? (s/n): ").lower()
    if respuesta == 's':
        if generar_apk():
            print("\n🎉 ¡APK CREADA EXITOSAMENTE!")
            print("📁 Busca el archivo en la carpeta bin/")
        else:
            print("\n❌ Error generando APK")
    
    print("\n📋 RESUMEN:")
    print("✅ Aplicación Android creada: danistore_app.py")
    print("✅ Configuración APK: buildozer.spec")
    print("✅ Punto de entrada: main.py")
    print("✅ Instrucciones: INSTRUCCIONES_APK.md")
    print("\n🚀 Para generar la APK manualmente:")
    print("   buildozer android debug")

if __name__ == "__main__":
    main()