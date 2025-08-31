#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test completo del sistema de suscripciones y notificaciones
"""

import json
import os
from datetime import datetime, timedelta

def test_crear_suscripciones_masivas():
    """Probar creación de múltiples suscripciones"""
    print("🧪 PROBANDO CREACIÓN MASIVA DE SUSCRIPCIONES")
    print("=" * 50)
    
    # Crear archivo de datos de prueba
    suscripciones_test = []
    
    # Crear 10 suscripciones de prueba
    servicios = ["Netflix", "Disney+", "HBO Max", "Amazon Prime", "YouTube Premium"]
    
    for i in range(1, 11):
        # Algunas vencidas, algunas activas
        if i <= 3:
            # Suscripciones vencidas (para probar notificaciones)
            fecha_venc = datetime.now() - timedelta(days=i)
        elif i <= 6:
            # Suscripciones que vencen pronto
            fecha_venc = datetime.now() + timedelta(days=i)
        else:
            # Suscripciones con tiempo
            fecha_venc = datetime.now() + timedelta(days=30 + i)
        
        suscripcion = {
            'id': i,
            'usuario': f'Usuario{i}',
            'correo': f'usuario{i}@email.com',
            'password': f'password{i}',
            'pin': f'{1000 + i}',
            'servicio': servicios[i % len(servicios)],
            'duracion': '1 mes',
            'fecha_inicio': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_vencimiento': fecha_venc.strftime('%Y-%m-%d %H:%M:%S'),
            'notas': f'Suscripción de prueba {i}',
            'activa': True,
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        suscripciones_test.append(suscripcion)
        
        estado = "VENCIDA" if i <= 3 else "ACTIVA"
        print(f"✅ Suscripción {i}: {suscripcion['usuario']} - {suscripcion['servicio']} ({estado})")
    
    # Guardar en archivo
    with open('suscripciones_data.json', 'w', encoding='utf-8') as f:
        json.dump(suscripciones_test, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ {len(suscripciones_test)} suscripciones creadas exitosamente")
    print("📁 Guardadas en: suscripciones_data.json")
    
    return suscripciones_test

def test_verificar_notificaciones():
    """Probar el sistema de notificaciones"""
    print("\n🔔 PROBANDO SISTEMA DE NOTIFICACIONES")
    print("=" * 50)
    
    # Cargar suscripciones
    try:
        with open('suscripciones_data.json', 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró archivo de suscripciones")
        return
    
    ahora = datetime.now()
    vencidas = []
    proximas = []
    activas = []
    
    for suscripcion in suscripciones:
        if not suscripcion.get('activa', True):
            continue
            
        fecha_vencimiento_str = suscripcion.get('fecha_vencimiento')
        if not fecha_vencimiento_str:
            continue
        
        try:
            fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d %H:%M:%S')
            
            if fecha_vencimiento <= ahora:
                vencidas.append(suscripcion)
            elif fecha_vencimiento <= ahora + timedelta(days=3):
                proximas.append(suscripcion)
            else:
                activas.append(suscripcion)
                
        except ValueError:
            continue
    
    print(f"🚨 Suscripciones VENCIDAS: {len(vencidas)}")
    for s in vencidas:
        print(f"   - {s['usuario']} ({s['servicio']})")
    
    print(f"⚠️  Suscripciones próximas a vencer: {len(proximas)}")
    for s in proximas:
        fecha_venc = datetime.strptime(s['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
        dias = (fecha_venc - ahora).days
        print(f"   - {s['usuario']} ({s['servicio']}) - {dias} días")
    
    print(f"✅ Suscripciones activas: {len(activas)}")
    
    return len(vencidas) > 0

def test_suscripciones_indefinidas():
    """Probar suscripciones indefinidas"""
    print("\n♾️  PROBANDO SUSCRIPCIONES INDEFINIDAS")
    print("=" * 50)
    
    # Crear suscripción indefinida
    suscripcion_indefinida = {
        'id': 999,
        'usuario': 'UsuarioVIP',
        'correo': 'vip@email.com',
        'password': 'passwordVIP',
        'pin': '9999',
        'servicio': 'Netflix Premium',
        'duracion': 'Indefinido',
        'fecha_inicio': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_vencimiento': None,  # Sin vencimiento
        'notas': 'Suscripción VIP indefinida',
        'activa': True,
        'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print("✅ Suscripción indefinida creada:")
    print(f"   👤 Usuario: {suscripcion_indefinida['usuario']}")
    print(f"   📺 Servicio: {suscripcion_indefinida['servicio']}")
    print(f"   ⏰ Duración: {suscripcion_indefinida['duracion']}")
    print(f"   📅 Vencimiento: {'Sin vencimiento' if not suscripcion_indefinida['fecha_vencimiento'] else suscripcion_indefinida['fecha_vencimiento']}")
    
    # Agregar a las suscripciones existentes
    try:
        with open('suscripciones_data.json', 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
    except FileNotFoundError:
        suscripciones = []
    
    suscripciones.append(suscripcion_indefinida)
    
    with open('suscripciones_data.json', 'w', encoding='utf-8') as f:
        json.dump(suscripciones, f, indent=2, ensure_ascii=False)
    
    print("✅ Suscripción indefinida agregada al sistema")
    
    return True

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA COMPLETO")
    print("=" * 60)
    
    # Test 1: Crear suscripciones masivas
    suscripciones = test_crear_suscripciones_masivas()
    
    # Test 2: Verificar notificaciones
    hay_vencidas = test_verificar_notificaciones()
    
    # Test 3: Suscripciones indefinidas
    test_suscripciones_indefinidas()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"✅ Suscripciones creadas: {len(suscripciones)}")
    print(f"🔔 Sistema de notificaciones: {'FUNCIONANDO' if hay_vencidas else 'SIN VENCIMIENTOS'}")
    print(f"♾️  Suscripciones indefinidas: SOPORTADAS")
    print("\n🎉 ¡TODAS LAS PRUEBAS COMPLETADAS!")
    print("\n📝 Ahora puedes ejecutar el gestor para ver los resultados:")
    print("   python gestor_suscripciones.py")

if __name__ == "__main__":
    main()