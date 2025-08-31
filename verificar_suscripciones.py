#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Suscripciones
Muestra el estado actual de todas las suscripciones
"""

import json
import os
from datetime import datetime

def verificar_suscripciones():
    print("🔍 VERIFICADOR DE SUSCRIPCIONES")
    print("=" * 50)
    
    archivo_datos = "suscripciones_data.json"
    
    if not os.path.exists(archivo_datos):
        print("❌ No se encontró archivo de suscripciones")
        print("💡 Agrega suscripciones primero con el gestor principal")
        return
    
    try:
        with open(archivo_datos, 'r', encoding='utf-8') as f:
            suscripciones = json.load(f)
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return
    
    if not suscripciones:
        print("📭 No hay suscripciones guardadas")
        return
    
    print(f"📋 Encontradas {len(suscripciones)} suscripciones:")
    print()
    
    ahora = datetime.now()
    
    for i, sub in enumerate(suscripciones, 1):
        usuario = sub.get('usuario', 'N/A')
        servicio = sub.get('servicio', 'N/A')
        activa = sub.get('activa', True)
        fecha_inicio_str = sub.get('fecha_inicio', 'N/A')
        fecha_vencimiento_str = sub.get('fecha_vencimiento', 'N/A')
        
        print(f"📺 {i}. {usuario} - {servicio}")
        print(f"   Estado: {'✅ Activa' if activa else '❌ Inactiva'}")
        
        if fecha_inicio_str != 'N/A':
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d %H:%M:%S')
                print(f"   📅 Inicio: {fecha_inicio.strftime('%d/%m/%Y %H:%M')}")
            except:
                print(f"   📅 Inicio: {fecha_inicio_str}")
        
        if fecha_vencimiento_str != 'N/A' and fecha_vencimiento_str != 'Indefinido':
            try:
                fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d %H:%M:%S')
                print(f"   ⏰ Vence: {fecha_vencimiento.strftime('%d/%m/%Y %H:%M')}")
                
                # Calcular tiempo restante
                diferencia = fecha_vencimiento - ahora
                if diferencia.total_seconds() > 0:
                    minutos_restantes = int(diferencia.total_seconds() / 60)
                    if minutos_restantes < 60:
                        print(f"   ⏳ Tiempo restante: {minutos_restantes} minutos")
                    else:
                        horas = minutos_restantes // 60
                        minutos = minutos_restantes % 60
                        print(f"   ⏳ Tiempo restante: {horas}h {minutos}m")
                else:
                    minutos_vencida = int(abs(diferencia.total_seconds()) / 60)
                    print(f"   💔 Vencida hace: {minutos_vencida} minutos")
                    
            except Exception as e:
                print(f"   ⏰ Vence: {fecha_vencimiento_str}")
                print(f"   ❌ Error calculando tiempo: {e}")
        else:
            print(f"   ⏰ Vence: {fecha_vencimiento_str}")
        
        notas = sub.get('notas', '')
        if notas:
            print(f"   📝 Notas: {notas}")
        
        print()
    
    print("=" * 50)
    print("🚀 Para probar notificaciones:")
    print("   python servicio_notificaciones_test.py")

if __name__ == "__main__":
    verificar_suscripciones()