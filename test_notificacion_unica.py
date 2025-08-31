#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de Notificación Única
Envía una notificación de prueba inmediatamente
"""

import json
import os
from datetime import datetime

# Importar librerías para notificaciones de Windows
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

try:
    import win10toast
    WIN10TOAST_AVAILABLE = True
except ImportError:
    WIN10TOAST_AVAILABLE = False

def enviar_notificacion_prueba():
    """Enviar una notificación de prueba"""
    print("🧪 PRUEBA DE NOTIFICACIÓN ÚNICA")
    print("=" * 40)
    
    # Verificar dependencias
    if not PLYER_AVAILABLE and not WIN10TOAST_AVAILABLE:
        print("❌ ERROR: No se encontraron librerías de notificaciones")
        return False
    
    titulo = "🧪 PRUEBA - Gestor Suscripciones"
    mensaje = "✅ ¡Las notificaciones funcionan correctamente!\n🔔 Sistema listo para usar"
    
    try:
        if WIN10TOAST_AVAILABLE:
            toaster = win10toast.ToastNotifier()
            icon_path = None
            if os.path.exists('gestor_icon.ico'):
                icon_path = 'gestor_icon.ico'
            
            print("📤 Enviando notificación con win10toast...")
            toaster.show_toast(
                title=titulo,
                msg=mensaje,
                icon_path=icon_path,
                duration=10,
                threaded=False  # No threaded para esperar
            )
            print("✅ Notificación enviada correctamente")
            return True
            
        elif PLYER_AVAILABLE:
            print("📤 Enviando notificación con plyer...")
            notification.notify(
                title=titulo,
                message=mensaje,
                app_name="Gestor Suscripciones",
                timeout=10
            )
            print("✅ Notificación enviada correctamente")
            return True
        
    except Exception as e:
        print(f"❌ Error enviando notificación: {e}")
        return False

def verificar_y_notificar_vencidas():
    """Verificar suscripciones vencidas y enviar notificaciones"""
    print("\n🔍 VERIFICANDO SUSCRIPCIONES VENCIDAS")
    print("=" * 40)
    
    archivo_datos = "suscripciones_data.json"
    
    if not os.path.exists(archivo_datos):
        print("❌ No se encontró archivo de suscripciones")
        return
    
    try:
        with open(archivo_datos, 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return
    
    ahora = datetime.now()
    notificaciones_enviadas = 0
    
    for suscripcion in suscripciones:
        if not suscripcion.get('activa', True):
            continue
        
        fecha_vencimiento_str = suscripcion.get('fecha_vencimiento')
        if not fecha_vencimiento_str or fecha_vencimiento_str == 'Indefinido':
            continue
        
        try:
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d %H:%M:%S')
            diferencia = fecha_vencimiento - ahora
            minutos_restantes = int(diferencia.total_seconds() / 60)
            
            usuario = suscripcion.get('usuario', 'Usuario')
            servicio = suscripcion.get('servicio', 'Servicio')
            
            # Notificar si vence pronto o ya venció
            if minutos_restantes <= 2:  # 2 minutos o menos
                print(f"📺 {usuario} - {servicio}: {minutos_restantes} minutos")
                enviar_notificacion_vencimiento(usuario, servicio, minutos_restantes)
                notificaciones_enviadas += 1
                
        except Exception as e:
            print(f"❌ Error procesando suscripción: {e}")
    
    if notificaciones_enviadas == 0:
        print("✅ No hay suscripciones próximas a vencer")
    else:
        print(f"📤 {notificaciones_enviadas} notificaciones enviadas")

def enviar_notificacion_vencimiento(usuario, servicio, minutos_restantes):
    """Enviar notificación de vencimiento"""
    if minutos_restantes <= 0:
        titulo = "🚨 SUSCRIPCIÓN VENCIDA"
        if minutos_restantes == 0:
            mensaje = f"⚠️ {usuario} - {servicio}\n🔔 ¡VENCE AHORA!"
        else:
            mensaje = f"💔 {usuario} - {servicio}\n📉 Vencida hace {abs(minutos_restantes)} minutos"
    elif minutos_restantes == 1:
        titulo = "⚠️ VENCE EN 1 MINUTO"
        mensaje = f"📅 {usuario} - {servicio}\n⏰ ¡Solo queda 1 minuto!"
    elif minutos_restantes == 2:
        titulo = "📋 VENCE EN 2 MINUTOS"
        mensaje = f"📺 {usuario} - {servicio}\n⏳ Quedan 2 minutos"
    
    try:
        if WIN10TOAST_AVAILABLE:
            toaster = win10toast.ToastNotifier()
            icon_path = None
            if os.path.exists('gestor_icon.ico'):
                icon_path = 'gestor_icon.ico'
            
            toaster.show_toast(
                title=titulo,
                msg=mensaje,
                icon_path=icon_path,
                duration=10,
                threaded=False
            )
            print(f"✅ Notificación enviada: {titulo}")
            
        elif PLYER_AVAILABLE:
            notification.notify(
                title=titulo,
                message=mensaje,
                app_name="Gestor Suscripciones",
                timeout=10
            )
            print(f"✅ Notificación enviada: {titulo}")
            
    except Exception as e:
        print(f"❌ Error enviando notificación: {e}")

def main():
    print("🧪 PRUEBA DE NOTIFICACIONES")
    print("=" * 50)
    
    # 1. Prueba básica de notificación
    print("1️⃣ Enviando notificación de prueba...")
    if enviar_notificacion_prueba():
        print("✅ Sistema de notificaciones funcional")
    else:
        print("❌ Error en sistema de notificaciones")
        return
    
    # 2. Verificar suscripciones vencidas
    print("\n2️⃣ Verificando suscripciones...")
    verificar_y_notificar_vencidas()
    
    print("\n" + "=" * 50)
    print("🎯 RESULTADO:")
    print("✅ Si viste las notificaciones, el sistema funciona")
    print("🚀 Ahora puedes usar el servicio completo")
    print("💡 Para servicio continuo: python servicio_notificaciones.py")

if __name__ == "__main__":
    main()