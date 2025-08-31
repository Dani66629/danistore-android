#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servicio de Notificaciones - VERSIÓN DE PRUEBA
Verifica cada minuto para testing
Gestor de Suscripciones - Dani666
"""

import json
import os
import time
import threading
from datetime import datetime, timedelta
import sys

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

class ServicioNotificacionesTest:
    def __init__(self):
        self.archivo_datos = "suscripciones_data.json"
        self.ejecutando = True
        self.intervalo_verificacion = 60  # 1 minuto para pruebas
        
        # Configurar notificador
        if WIN10TOAST_AVAILABLE:
            self.toaster = win10toast.ToastNotifier()
        
        print("🧪 SERVICIO DE NOTIFICACIONES - MODO PRUEBA")
        print("=" * 50)
        print(f"⏰ Verificando cada {self.intervalo_verificacion} segundos (1 minuto)")
        print("🔔 Notificará suscripciones que venzan en:")
        print("   • 0 minutos (vence ahora)")
        print("   • 1 minuto")
        print("   • 2 minutos")
        print("   • Ya vencidas")
        print("💡 Para detener: Ctrl+C")
        print("=" * 50)
    
    def cargar_suscripciones(self):
        """Cargar suscripciones desde el archivo"""
        if not os.path.exists(self.archivo_datos):
            print("⚠️ No se encontró archivo de suscripciones")
            return []
        
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                suscripciones = json.load(f)
                print(f"📋 Cargadas {len(suscripciones)} suscripciones")
                return suscripciones
        except Exception as e:
            print(f"❌ Error cargando suscripciones: {e}")
            return []
    
    def enviar_notificacion_windows(self, titulo, mensaje):
        """Enviar notificación nativa de Windows"""
        try:
            if WIN10TOAST_AVAILABLE:
                # Usar win10toast para notificaciones más nativas
                icon_path = None
                if os.path.exists('gestor_icon.ico'):
                    icon_path = 'gestor_icon.ico'
                
                self.toaster.show_toast(
                    title=titulo,
                    msg=mensaje,
                    icon_path=icon_path,
                    duration=10,
                    threaded=True
                )
                print(f"✅ Notificación enviada: {titulo}")
                return True
                
            elif PLYER_AVAILABLE:
                # Usar plyer como alternativa
                notification.notify(
                    title=titulo,
                    message=mensaje,
                    app_name="Gestor Suscripciones",
                    timeout=10
                )
                print(f"✅ Notificación enviada: {titulo}")
                return True
            
        except Exception as e:
            print(f"❌ Error enviando notificación: {e}")
        
        return False
    
    def verificar_vencimientos(self):
        """Verificar suscripciones próximas a vencer"""
        suscripciones = self.cargar_suscripciones()
        if not suscripciones:
            print("📭 No hay suscripciones para verificar")
            return
        
        ahora = datetime.now()
        notificaciones_enviadas = 0
        
        print(f"\n🔍 Verificando vencimientos... {ahora.strftime('%H:%M:%S')}")
        
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
                
                print(f"   📺 {usuario} - {servicio}: {minutos_restantes} minutos restantes")
                
                # Verificar si debe notificar (0, 1, 2 minutos o ya vencida)
                if minutos_restantes in [0, 1, 2] or minutos_restantes < 0:
                    self.enviar_notificacion_vencimiento(suscripcion, minutos_restantes)
                    notificaciones_enviadas += 1
                    
            except Exception as e:
                print(f"❌ Error procesando {usuario}: {e}")
        
        if notificaciones_enviadas > 0:
            print(f"📤 {notificaciones_enviadas} notificaciones enviadas")
        else:
            print("✅ No hay notificaciones pendientes")
    
    def enviar_notificacion_vencimiento(self, suscripcion, minutos_restantes):
        """Enviar notificación específica de vencimiento"""
        usuario = suscripcion.get('usuario', 'Usuario')
        servicio = suscripcion.get('servicio', 'Servicio')
        
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
        
        # Enviar notificación
        self.enviar_notificacion_windows(titulo, mensaje)
    
    def ejecutar_servicio(self):
        """Ejecutar el servicio en bucle continuo"""
        print("🚀 Iniciando monitoreo de prueba...")
        
        while self.ejecutando:
            try:
                self.verificar_vencimientos()
                
                # Esperar 1 minuto
                print(f"⏳ Esperando {self.intervalo_verificacion} segundos hasta la próxima verificación...")
                for i in range(self.intervalo_verificacion):
                    if not self.ejecutando:
                        break
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo servicio de prueba...")
                self.ejecutando = False
                break
            except Exception as e:
                print(f"❌ Error en el servicio: {e}")
                time.sleep(10)  # Esperar 10 segundos antes de reintentar
    
    def detener(self):
        """Detener el servicio"""
        self.ejecutando = False

def main():
    """Función principal"""
    print("🧪 SERVICIO DE NOTIFICACIONES - MODO PRUEBA")
    print("=" * 60)
    
    # Verificar dependencias
    if not PLYER_AVAILABLE and not WIN10TOAST_AVAILABLE:
        print("❌ ERROR: No se encontraron librerías de notificaciones")
        print("💡 Instalar con: pip install plyer win10toast")
        return
    
    # Crear y ejecutar servicio
    servicio = ServicioNotificacionesTest()
    
    try:
        servicio.ejecutar_servicio()
    except KeyboardInterrupt:
        print("\n🛑 Servicio detenido por el usuario")
    finally:
        servicio.detener()
        print("✅ Servicio de prueba finalizado")

if __name__ == "__main__":
    main()