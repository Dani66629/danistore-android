#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servicio de Notificaciones en Segundo Plano
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

class ServicioNotificaciones:
    def __init__(self):
        self.archivo_datos = "suscripciones_data.json"
        self.archivo_config = "notificaciones_config.json"
        self.ejecutando = True
        self.intervalo_verificacion = 3600  # 1 hora en segundos
        
        # Configurar notificador
        if WIN10TOAST_AVAILABLE:
            self.toaster = win10toast.ToastNotifier()
        
        # Cargar configuración
        self.cargar_configuracion()
        
        print("🔔 Servicio de Notificaciones iniciado")
        print(f"📅 Verificando cada {self.intervalo_verificacion//60} minutos")
        print("💡 Para detener: Ctrl+C")
    
    def cargar_configuracion(self):
        """Cargar configuración de notificaciones"""
        config_default = {
            "activo": True,
            "intervalo_minutos": 60,
            "notificar_dias_antes": [0, 1, 3],  # Hoy, mañana, 3 días antes
            "sonido": True,
            "duracion_notificacion": 10
        }
        
        if os.path.exists(self.archivo_config):
            try:
                with open(self.archivo_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Actualizar valores
                    self.intervalo_verificacion = config.get("intervalo_minutos", 60) * 60
                    self.dias_notificar = config.get("notificar_dias_antes", [0, 1, 3])
                    self.sonido_activo = config.get("sonido", True)
                    self.duracion = config.get("duracion_notificacion", 10)
            except:
                self.guardar_configuracion(config_default)
        else:
            self.guardar_configuracion(config_default)
    
    def guardar_configuracion(self, config):
        """Guardar configuración"""
        try:
            with open(self.archivo_config, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando configuración: {e}")
    
    def cargar_suscripciones(self):
        """Cargar suscripciones desde el archivo"""
        if not os.path.exists(self.archivo_datos):
            return []
        
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error cargando suscripciones: {e}")
            return []
    
    def enviar_notificacion_windows(self, titulo, mensaje, icono="info"):
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
                    duration=self.duracion,
                    threaded=True
                )
                return True
                
            elif PLYER_AVAILABLE:
                # Usar plyer como alternativa
                notification.notify(
                    title=titulo,
                    message=mensaje,
                    app_name="Gestor Suscripciones",
                    timeout=self.duracion
                )
                return True
            
        except Exception as e:
            print(f"❌ Error enviando notificación: {e}")
        
        return False
    
    def verificar_vencimientos(self):
        """Verificar suscripciones próximas a vencer"""
        suscripciones = self.cargar_suscripciones()
        if not suscripciones:
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
                dias_restantes = (fecha_vencimiento - ahora).days
                
                # Verificar si debe notificar
                if dias_restantes in self.dias_notificar:
                    self.enviar_notificacion_vencimiento(suscripcion, dias_restantes)
                    notificaciones_enviadas += 1
                    
            except Exception as e:
                print(f"❌ Error procesando suscripción {suscripcion.get('usuario', 'N/A')}: {e}")
        
        if notificaciones_enviadas > 0:
            print(f"📤 {notificaciones_enviadas} notificaciones enviadas")
    
    def enviar_notificacion_vencimiento(self, suscripcion, dias_restantes):
        """Enviar notificación específica de vencimiento"""
        usuario = suscripcion.get('usuario', 'Usuario')
        servicio = suscripcion.get('servicio', 'Servicio')
        
        if dias_restantes == 0:
            titulo = "🚨 SUSCRIPCIÓN VENCE HOY"
            mensaje = f"⚠️ {usuario} - {servicio}\n🔔 Vence HOY - ¡Renovar ahora!"
        elif dias_restantes == 1:
            titulo = "⚠️ SUSCRIPCIÓN VENCE MAÑANA"
            mensaje = f"📅 {usuario} - {servicio}\n⏰ Vence mañana - Preparar renovación"
        elif dias_restantes < 0:
            titulo = "❌ SUSCRIPCIÓN VENCIDA"
            mensaje = f"💔 {usuario} - {servicio}\n📉 Vencida hace {abs(dias_restantes)} días"
        else:
            titulo = f"📋 SUSCRIPCIÓN VENCE EN {dias_restantes} DÍAS"
            mensaje = f"📺 {usuario} - {servicio}\n⏳ Quedan {dias_restantes} días"
        
        # Enviar notificación
        if self.enviar_notificacion_windows(titulo, mensaje):
            print(f"✅ Notificación enviada: {usuario} - {servicio} ({dias_restantes} días)")
    
    def ejecutar_servicio(self):
        """Ejecutar el servicio en bucle continuo"""
        print("🚀 Iniciando monitoreo de suscripciones...")
        
        while self.ejecutando:
            try:
                print(f"🔍 Verificando vencimientos... {datetime.now().strftime('%H:%M:%S')}")
                self.verificar_vencimientos()
                
                # Esperar el intervalo configurado
                for i in range(self.intervalo_verificacion):
                    if not self.ejecutando:
                        break
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo servicio...")
                self.ejecutando = False
                break
            except Exception as e:
                print(f"❌ Error en el servicio: {e}")
                time.sleep(60)  # Esperar 1 minuto antes de reintentar
    
    def detener(self):
        """Detener el servicio"""
        self.ejecutando = False

def main():
    """Función principal"""
    print("=" * 60)
    print("🔔 SERVICIO DE NOTIFICACIONES - GESTOR SUSCRIPCIONES")
    print("=" * 60)
    
    # Verificar dependencias
    if not PLYER_AVAILABLE and not WIN10TOAST_AVAILABLE:
        print("❌ ERROR: No se encontraron librerías de notificaciones")
        print("💡 Instalar con: pip install plyer win10toast")
        return
    
    # Crear y ejecutar servicio
    servicio = ServicioNotificaciones()
    
    try:
        servicio.ejecutar_servicio()
    except KeyboardInterrupt:
        print("\n🛑 Servicio detenido por el usuario")
    finally:
        servicio.detener()
        print("✅ Servicio finalizado")

if __name__ == "__main__":
    main()