#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para verificar que los botones del gestor funcionan correctamente
"""

import json
import os
from datetime import datetime, timedelta

def crear_suscripcion_test():
    """Crear una suscripción de prueba con ID para probar botones"""
    archivo = "suscripciones_data.json"
    
    # Cargar existentes
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
    else:
        suscripciones = []
    
    # Crear suscripción activa para probar botones
    ahora = datetime.now()
    vence_en = ahora + timedelta(days=30)  # Vence en 30 días
    
    nueva = {
        'id': len(suscripciones) + 1,
        'usuario': 'TEST_BOTONES',
        'servicio': 'Netflix',
        'duracion': '1 mes',
        'fecha_inicio': ahora.strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_vencimiento': vence_en.strftime('%Y-%m-%d %H:%M:%S'),
        'activa': True,
        'notas': 'Suscripción para probar botones',
        'fecha_creacion': ahora.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    suscripciones.append(nueva)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(suscripciones, f, indent=2, ensure_ascii=False)
    
    print("✅ Suscripción de prueba creada:")
    print(f"   👤 Usuario: TEST_BOTONES")
    print(f"   📺 Servicio: Netflix")
    print(f"   🆔 ID: {nueva['id']}")
    print(f"   📅 Vence: {vence_en.strftime('%d/%m/%Y')}")
    print()
    print("🧪 Ahora ejecuta el gestor y prueba:")
    print("   1. Botón RENOVAR - debe abrir ventana de renovación")
    print("   2. Botón EDITAR - debe abrir ventana de edición")
    print("   3. Botón ELIMINAR - debe pedir confirmación")
    print()
    print("🚀 Comando: python gestor_suscripciones.py")

def verificar_ids():
    """Verificar que todas las suscripciones tengan ID"""
    archivo = "suscripciones_data.json"
    
    if not os.path.exists(archivo):
        print("❌ No existe archivo de suscripciones")
        return
    
    with open(archivo, 'r', encoding='utf-8') as f:
        suscripciones = json.load(f)
    
    print(f"🔍 Verificando {len(suscripciones)} suscripciones...")
    
    sin_id = []
    for i, suscripcion in enumerate(suscripciones):
        if 'id' not in suscripcion:
            sin_id.append(i)
            print(f"❌ Suscripción {i+1} sin ID: {suscripcion.get('usuario', 'Sin usuario')} - {suscripcion.get('servicio', 'Sin servicio')}")
        else:
            print(f"✅ ID {suscripcion['id']}: {suscripcion.get('usuario', 'Sin usuario')} - {suscripcion.get('servicio', 'Sin servicio')}")
    
    if sin_id:
        print(f"\n⚠️ {len(sin_id)} suscripciones sin ID")
        print("El gestor las arreglará automáticamente al cargar")
    else:
        print("\n✅ Todas las suscripciones tienen ID")

if __name__ == "__main__":
    print("🧪 TEST DE BOTONES DEL GESTOR")
    print("=" * 40)
    
    print("\n1️⃣ Verificando IDs existentes...")
    verificar_ids()
    
    print("\n2️⃣ Creando suscripción de prueba...")
    crear_suscripcion_test()