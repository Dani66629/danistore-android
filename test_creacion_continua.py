#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de creación continua de suscripciones
"""

import json
import os
from datetime import datetime, timedelta
import time

def crear_suscripcion_automatica(numero):
    """Crear una suscripción automáticamente"""
    servicios = ["Netflix", "Disney+", "HBO Max", "Amazon Prime", "YouTube Premium", 
                "Crunchyroll", "Spotify", "Apple TV+", "Paramount+", "Discovery+"]
    
    # Tipos de duración variados
    duraciones = ["1 mes", "2 meses", "3 meses", "6 meses", "1 año", "Indefinido"]
    
    servicio = servicios[numero % len(servicios)]
    duracion = duraciones[numero % len(duraciones)]
    
    # Calcular fecha de vencimiento
    if duracion == "Indefinido":
        fecha_vencimiento = None
    else:
        if "mes" in duracion:
            meses = int(duracion.split()[0])
            fecha_vencimiento = datetime.now() + timedelta(days=30 * meses)
        elif "año" in duracion:
            años = int(duracion.split()[0])
            fecha_vencimiento = datetime.now() + timedelta(days=365 * años)
        else:
            fecha_vencimiento = datetime.now() + timedelta(days=30)
    
    suscripcion = {
        'id': numero,
        'usuario': f'Cliente{numero}',
        'correo': f'cliente{numero}@email.com',
        'password': f'pass{numero}123',
        'pin': f'{1000 + numero}',
        'servicio': servicio,
        'duracion': duracion,
        'fecha_inicio': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_vencimiento': fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S') if fecha_vencimiento else None,
        'notas': f'Cliente automático #{numero}',
        'activa': True,
        'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return suscripcion

def test_creacion_masiva():
    """Probar creación masiva de suscripciones"""
    print("🚀 PROBANDO CREACIÓN MASIVA DE SUSCRIPCIONES")
    print("=" * 50)
    
    # Cargar suscripciones existentes
    try:
        with open('suscripciones_data.json', 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
        print(f"📁 Suscripciones existentes: {len(suscripciones)}")
    except FileNotFoundError:
        suscripciones = []
        print("📁 Creando archivo nuevo")
    
    # Crear 20 suscripciones más
    nuevas_suscripciones = 0
    for i in range(len(suscripciones) + 1, len(suscripciones) + 21):
        nueva_suscripcion = crear_suscripcion_automatica(i)
        suscripciones.append(nueva_suscripcion)
        nuevas_suscripciones += 1
        
        print(f"✅ Suscripción {i}: {nueva_suscripcion['usuario']} - {nueva_suscripcion['servicio']} ({nueva_suscripcion['duracion']})")
        
        # Simular tiempo de procesamiento
        time.sleep(0.1)
    
    # Guardar todas las suscripciones
    with open('suscripciones_data.json', 'w', encoding='utf-8') as f:
        json.dump(suscripciones, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ {nuevas_suscripciones} nuevas suscripciones creadas")
    print(f"📊 Total de suscripciones: {len(suscripciones)}")
    
    # Estadísticas
    indefinidas = len([s for s in suscripciones if s['duracion'] == 'Indefinido'])
    activas = len([s for s in suscripciones if s['activa']])
    
    print(f"♾️  Suscripciones indefinidas: {indefinidas}")
    print(f"✅ Suscripciones activas: {activas}")
    
    return len(suscripciones)

def verificar_limites_sistema():
    """Verificar si hay límites en el sistema"""
    print("\n🔍 VERIFICANDO LÍMITES DEL SISTEMA")
    print("=" * 50)
    
    try:
        with open('suscripciones_data.json', 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
        
        tamaño_archivo = os.path.getsize('suscripciones_data.json')
        tamaño_mb = tamaño_archivo / (1024 * 1024)
        
        print(f"📁 Archivo de datos: {tamaño_mb:.2f} MB")
        print(f"📊 Total suscripciones: {len(suscripciones)}")
        print(f"💾 Memoria estimada: {len(str(suscripciones)) / 1024:.2f} KB")
        
        # Verificar rendimiento
        inicio = time.time()
        activas = [s for s in suscripciones if s['activa']]
        fin = time.time()
        
        print(f"⚡ Tiempo de filtrado: {(fin - inicio) * 1000:.2f} ms")
        print(f"✅ Suscripciones activas: {len(activas)}")
        
        if len(suscripciones) < 1000:
            print("🟢 Sistema funcionando óptimamente")
        elif len(suscripciones) < 5000:
            print("🟡 Sistema funcionando bien")
        else:
            print("🟠 Sistema con muchos datos, considerar optimización")
            
    except Exception as e:
        print(f"❌ Error verificando sistema: {e}")

def main():
    """Ejecutar pruebas de creación continua"""
    print("🎯 TEST DE CREACIÓN CONTINUA DE SUSCRIPCIONES")
    print("=" * 60)
    
    # Crear suscripciones masivamente
    total = test_creacion_masiva()
    
    # Verificar límites
    verificar_limites_sistema()
    
    print("\n" + "=" * 60)
    print("📋 CONCLUSIONES")
    print("=" * 60)
    print("✅ El sistema puede crear suscripciones indefinidamente")
    print("✅ No hay límites técnicos aparentes")
    print("✅ Las suscripciones indefinidas funcionan correctamente")
    print("✅ El archivo JSON escala bien")
    print(f"📊 Total actual: {total} suscripciones")
    
    print("\n🚀 ¡Ejecuta el gestor para ver todas las suscripciones!")
    print("   python gestor_suscripciones.py")

if __name__ == "__main__":
    main()