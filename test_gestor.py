#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba Simple del Gestor de Suscripciones
"""

import os
import json
from datetime import datetime

def probar_gestor():
    print("🧪 PRUEBA DEL GESTOR DE SUSCRIPCIONES")
    print("=" * 50)
    
    # Verificar que el archivo principal existe
    if os.path.exists('gestor_suscripciones.py'):
        print("✅ Archivo principal encontrado")
    else:
        print("❌ Archivo principal NO encontrado")
        return
    
    # Verificar que se puede importar
    try:
        import gestor_suscripciones
        print("✅ Módulo se puede importar")
    except Exception as e:
        print(f"❌ Error importando módulo: {e}")
        return
    
    print("\n" + "=" * 50)
    print("🚀 Para ejecutar el gestor:")
    print("   python gestor_suscripciones.py")
    print("\n✨ MEJORAS RECIENTES:")
    print("   📜 Scrollbar en formulario de nueva suscripción")
    print("   🎯 Botón principal '➕ AGREGAR SUSCRIPCIÓN' optimizado")
    print("   🎨 Interfaz más limpia y funcional")
    print("   ✅ Navegación fluida en formularios largos")
    print("   🖱️ Scroll con rueda del mouse")
    print("\n🆕 DURACIÓN PERSONALIZADA AVANZADA:")
    print("   ⏱️ MINUTOS: Campo para minutos exactos")
    print("   🕐 HORAS: Campos para horas + minutos adicionales")
    print("   📅 DÍAS: Campos para días + horas adicionales")
    print("   📆 MESES: Campos para meses + días adicionales")
    print("   🗓️ AÑOS: Campos para años + meses adicionales")
    print("   🧮 Cálculo automático del tiempo total")
    print("   📊 Ejemplos dinámicos en tiempo real")
    print("\n🎬 INTERFAZ OPTIMIZADA:")
    print("   📱 Scroll suave en formulario")
    print("   🎯 Un solo botón de agregar (más claro)")
    print("   📏 Altura fija con scroll automático")
    print("\n🔔 SISTEMA DE NOTIFICACIONES INDEPENDIENTE:")
    print("   🚀 Servicio en segundo plano")
    print("   📢 Notificaciones nativas de Windows")
    print("   ⏰ Funciona sin tener el gestor abierto")
    print("   🔄 Verificación automática cada hora")
    print("   💻 Inicio automático con Windows")
    print("\n📋 ARCHIVOS DE NOTIFICACIONES:")
    print("   • servicio_notificaciones.py - Servicio principal")
    print("   • instalar_notificaciones.py - Instalador de dependencias")
    print("   • iniciar_servicio.py - Iniciador del servicio")
    print("   • configurar_inicio_automatico.py - Configurar inicio con Windows")
    print("   • NOTIFICACIONES_GUIA.md - Guía completa")

if __name__ == "__main__":
    probar_gestor()