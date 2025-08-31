#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crear suscripción de prueba que vence INMEDIATAMENTE
Para probar el sistema de notificaciones Android
"""

import json
import os
from datetime import datetime, timedelta

def crear_suscripcion_vencida():
    """Crear una suscripción que ya está vencida"""
    archivo = "suscripciones_data.json"
    
    # Cargar existentes
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
    else:
        suscripciones = []
    
    # Crear suscripción que venció hace 1 minuto
    ahora = datetime.now()
    vencida_hace = ahora - timedelta(minutes=1)
    
    nueva = {
        'usuario': 'ANDROID_TEST',
        'servicio': 'Netflix',
        'fecha_inicio': (ahora - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_vencimiento': vencida_hace.strftime('%Y-%m-%d %H:%M:%S'),
        'activa': True,
        'notas': 'Suscripción de prueba VENCIDA para Android'
    }
    
    suscripciones.append(nueva)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(suscripciones, f, indent=2, ensure_ascii=False)
    
    print("✅ Suscripción VENCIDA creada:")
    print(f"   👤 Usuario: ANDROID_TEST")
    print(f"   📺 Servicio: Netflix")
    print(f"   ⏰ Venció: {vencida_hace.strftime('%H:%M:%S')} (hace 1 minuto)")
    print()
    print("🚀 Ahora ejecuta el gestor:")
    print("   python gestor_suscripciones.py")
    print()
    print("📱 Deberías ver INMEDIATAMENTE:")
    print("   1. Mensaje en consola: 'VENCIDA: ANDROID_TEST - Netflix'")
    print("   2. Ventana emergente con alerta crítica")
    print("   3. Notificación estilo Android")

if __name__ == "__main__":
    crear_suscripcion_vencida()