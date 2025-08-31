#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para probar los nuevos campos: correo, contraseña y PIN
"""

import json
import os
from datetime import datetime, timedelta

def crear_suscripcion_completa():
    """Crear una suscripción con todos los campos nuevos"""
    archivo = "suscripciones_data.json"
    
    # Cargar existentes
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
    else:
        suscripciones = []
    
    # Crear suscripción completa
    ahora = datetime.now()
    vence_en = ahora + timedelta(days=30)
    
    nueva = {
        'id': len(suscripciones) + 1,
        'usuario': 'Cliente_VIP',
        'correo': 'cliente@gmail.com',
        'password': 'MiPassword123',
        'pin': '1234',
        'servicio': 'Netflix',
        'duracion': '1 mes',
        'fecha_inicio': ahora.strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_vencimiento': vence_en.strftime('%Y-%m-%d %H:%M:%S'),
        'activa': True,
        'notas': 'Cliente VIP con todos los datos completos',
        'fecha_creacion': ahora.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    suscripciones.append(nueva)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(suscripciones, f, indent=2, ensure_ascii=False)
    
    print("✅ Suscripción completa creada:")
    print(f"   👤 Usuario: {nueva['usuario']}")
    print(f"   📧 Correo: {nueva['correo']}")
    print(f"   🔒 Contraseña: {nueva['password']}")
    print(f"   📱 PIN: {nueva['pin']}")
    print(f"   📺 Servicio: {nueva['servicio']}")
    print(f"   📅 Vence: {vence_en.strftime('%d/%m/%Y')}")
    print()
    print("🧪 Ahora ejecuta el gestor y verifica:")
    print("   1. Los nuevos campos aparecen en el formulario")
    print("   2. La suscripción muestra correo y PIN")
    print("   3. Al editar se pueden modificar todos los campos")
    print()
    print("🚀 Comando: python gestor_suscripciones.py")

def verificar_campos_existentes():
    """Verificar qué campos tienen las suscripciones existentes"""
    archivo = "suscripciones_data.json"
    
    if not os.path.exists(archivo):
        print("❌ No existe archivo de suscripciones")
        return
    
    with open(archivo, 'r', encoding='utf-8') as f:
        suscripciones = json.load(f)
    
    print(f"🔍 Verificando {len(suscripciones)} suscripciones...")
    print()
    
    for i, suscripcion in enumerate(suscripciones):
        usuario = suscripcion.get('usuario', 'Sin usuario')
        servicio = suscripcion.get('servicio', 'Sin servicio')
        correo = suscripcion.get('correo', 'No tiene')
        password = suscripcion.get('password', 'No tiene')
        pin = suscripcion.get('pin', 'No tiene')
        
        print(f"📋 Suscripción {i+1}:")
        print(f"   👤 Usuario: {usuario}")
        print(f"   📺 Servicio: {servicio}")
        print(f"   📧 Correo: {correo}")
        print(f"   🔒 Contraseña: {'***' if password != 'No tiene' else 'No tiene'}")
        print(f"   📱 PIN: {pin}")
        print()

if __name__ == "__main__":
    print("🧪 TEST DE NUEVOS CAMPOS")
    print("=" * 40)
    
    print("\n1️⃣ Verificando campos existentes...")
    verificar_campos_existentes()
    
    print("\n2️⃣ Creando suscripción completa...")
    crear_suscripcion_completa()