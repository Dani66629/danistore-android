#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurador de Inicio Automático
Gestor de Suscripciones - Dani666
"""

import os
import sys
import winreg
import shutil

def agregar_al_registro_inicio():
    """Agregar el servicio al registro de inicio de Windows"""
    try:
        # Ruta del script actual
        script_dir = os.path.dirname(os.path.abspath(__file__))
        servicio_path = os.path.join(script_dir, "servicio_notificaciones.py")
        python_path = sys.executable.replace("python.exe", "pythonw.exe")
        
        # Comando completo
        comando = f'"{python_path}" "{servicio_path}"'
        
        # Abrir clave del registro
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Agregar entrada
        winreg.SetValueEx(
            key,
            "GestorSuscripcionesDani666",
            0,
            winreg.REG_SZ,
            comando
        )
        
        winreg.CloseKey(key)
        return True
        
    except Exception as e:
        print(f"❌ Error configurando inicio automático: {e}")
        return False

def remover_del_registro_inicio():
    """Remover el servicio del registro de inicio"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.DeleteValue(key, "GestorSuscripcionesDani666")
        winreg.CloseKey(key)
        return True
        
    except FileNotFoundError:
        print("⚠️ El servicio no estaba configurado para inicio automático")
        return True
    except Exception as e:
        print(f"❌ Error removiendo inicio automático: {e}")
        return False

def verificar_inicio_automatico():
    """Verificar si el inicio automático está configurado"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        
        valor, tipo = winreg.QueryValueEx(key, "GestorSuscripcionesDani666")
        winreg.CloseKey(key)
        return True, valor
        
    except FileNotFoundError:
        return False, None
    except Exception:
        return False, None

def crear_acceso_directo_escritorio():
    """Crear acceso directo en el escritorio"""
    try:
        import win32com.client
        
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "Gestor Suscripciones - Notificaciones.lnk")
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{os.path.abspath("iniciar_servicio.py")}"'
        shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(__file__))
        shortcut.IconLocation = os.path.abspath("gestor_icon.ico") if os.path.exists("gestor_icon.ico") else ""
        shortcut.save()
        
        return True
    except ImportError:
        print("⚠️ Para crear accesos directos instala: pip install pywin32")
        return False
    except Exception as e:
        print(f"❌ Error creando acceso directo: {e}")
        return False

def main():
    print("⚙️ CONFIGURADOR DE INICIO AUTOMÁTICO")
    print("=" * 50)
    
    # Verificar estado actual
    configurado, comando = verificar_inicio_automatico()
    
    if configurado:
        print("✅ Inicio automático YA CONFIGURADO")
        print(f"📍 Comando: {comando}")
        print()
        print("🎯 Opciones:")
        print("1. Desactivar inicio automático")
        print("2. Reconfigurar inicio automático")
        print("3. Crear acceso directo en escritorio")
        print("4. Salir")
    else:
        print("❌ Inicio automático NO CONFIGURADO")
        print()
        print("🎯 Opciones:")
        print("1. Activar inicio automático")
        print("2. Crear acceso directo en escritorio")
        print("3. Salir")
    
    try:
        opcion = input("\nSelecciona una opción: ").strip()
        
        if not configurado and opcion == "1":
            print("🔄 Configurando inicio automático...")
            if agregar_al_registro_inicio():
                print("✅ Inicio automático configurado correctamente")
                print("🔔 El servicio se iniciará automáticamente con Windows")
            else:
                print("❌ Error configurando inicio automático")
        
        elif configurado and opcion == "1":
            print("🔄 Desactivando inicio automático...")
            if remover_del_registro_inicio():
                print("✅ Inicio automático desactivado")
            else:
                print("❌ Error desactivando inicio automático")
        
        elif (configurado and opcion == "2") or (not configurado and opcion == "1"):
            print("🔄 Configurando inicio automático...")
            if agregar_al_registro_inicio():
                print("✅ Inicio automático configurado correctamente")
            else:
                print("❌ Error configurando inicio automático")
        
        elif (configurado and opcion == "3") or (not configurado and opcion == "2"):
            print("🔄 Creando acceso directo...")
            if crear_acceso_directo_escritorio():
                print("✅ Acceso directo creado en el escritorio")
            else:
                print("❌ Error creando acceso directo")
        
        else:
            print("❌ Saliendo...")
    
    except KeyboardInterrupt:
        print("\n❌ Cancelado por el usuario")

if __name__ == "__main__":
    main()