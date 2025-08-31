#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de la aplicación Kivy antes de generar APK
"""

import sys
import os

def test_kivy_import():
    """Probar importación de Kivy"""
    print("🧪 PROBANDO IMPORTACIÓN DE KIVY")
    print("=" * 50)
    
    try:
        import kivy
        print(f"✅ Kivy versión: {kivy.__version__}")
        
        from kivy.app import App
        print("✅ kivy.app importado")
        
        from kivy.uix.boxlayout import BoxLayout
        print("✅ kivy.uix.boxlayout importado")
        
        from kivy.uix.label import Label
        print("✅ kivy.uix.label importado")
        
        from kivy.uix.button import Button
        print("✅ kivy.uix.button importado")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando Kivy: {e}")
        return False

def test_app_import():
    """Probar importación de la aplicación"""
    print("\n🧪 PROBANDO IMPORTACIÓN DE DANISTORE APP")
    print("=" * 50)
    
    try:
        from danistore_app import DaniStoreApp
        print("✅ DaniStoreApp importado correctamente")
        
        app = DaniStoreApp()
        print("✅ Instancia de DaniStoreApp creada")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando DaniStoreApp: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creando instancia: {e}")
        return False

def test_archivos_necesarios():
    """Verificar archivos necesarios para APK"""
    print("\n🧪 VERIFICANDO ARCHIVOS PARA APK")
    print("=" * 50)
    
    archivos = {
        'main.py': 'Punto de entrada principal',
        'danistore_app.py': 'Aplicación Kivy',
        'buildozer.spec': 'Configuración de Buildozer',
        'iconos_android/danistore_icon.png': 'Icono de la aplicación'
    }
    
    todos_ok = True
    for archivo, descripcion in archivos.items():
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo)
            print(f"✅ {archivo} ({tamaño} bytes) - {descripcion}")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO - {descripcion}")
            todos_ok = False
    
    return todos_ok

def crear_app_simple():
    """Crear una versión simple para probar"""
    print("\n🧪 CREANDO APP DE PRUEBA SIMPLE")
    print("=" * 50)
    
    app_simple = '''#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text='¡DaniStore funciona!\\n\\nLa aplicación está lista\\npara convertir a APK')

if __name__ == '__main__':
    TestApp().run()
'''
    
    with open('test_simple.py', 'w', encoding='utf-8') as f:
        f.write(app_simple)
    
    print("✅ App de prueba creada: test_simple.py")
    print("🚀 Ejecuta: python test_simple.py")

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS PRE-APK DANISTORE")
    print("=" * 60)
    
    # Test 1: Kivy
    kivy_ok = test_kivy_import()
    
    # Test 2: App
    app_ok = test_app_import()
    
    # Test 3: Archivos
    archivos_ok = test_archivos_necesarios()
    
    # Test 4: App simple
    crear_app_simple()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    if kivy_ok:
        print("✅ Kivy: FUNCIONANDO")
    else:
        print("❌ Kivy: ERROR")
    
    if app_ok:
        print("✅ DaniStore App: FUNCIONANDO")
    else:
        print("❌ DaniStore App: ERROR")
    
    if archivos_ok:
        print("✅ Archivos APK: COMPLETOS")
    else:
        print("❌ Archivos APK: INCOMPLETOS")
    
    if kivy_ok and app_ok and archivos_ok:
        print("\n🎉 ¡TODO LISTO PARA GENERAR APK!")
        print("\n🚀 COMANDOS PARA GENERAR APK:")
        print("   buildozer android debug")
        print("   # O en Linux/Mac:")
        print("   buildozer android release")
    else:
        print("\n⚠️  HAY PROBLEMAS QUE RESOLVER ANTES DE GENERAR APK")
    
    print("\n📱 PRÓXIMOS PASOS:")
    print("1. Probar app simple: python test_simple.py")
    print("2. Probar app completa: python danistore_app.py")
    print("3. Generar APK: buildozer android debug")
    print("4. Instalar APK en Android")

if __name__ == "__main__":
    main()