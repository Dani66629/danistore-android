#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de la funcionalidad personalizada
"""

def verificar_personalizado():
    print("🔍 VERIFICACIÓN DE DURACIÓN PERSONALIZADA")
    print("=" * 50)
    
    print("✅ Pasos para probar:")
    print("1. Ejecutar: python gestor_suscripciones.py")
    print("2. En 'Duración de la Suscripción' seleccionar 'Personalizado'")
    print("3. Debería aparecer:")
    print("   - Selector de unidad (Minutos, Horas, Días, Meses, Años)")
    print("   - Campos específicos según la unidad seleccionada")
    print("   - Ejemplo de cálculo en tiempo real")
    
    print("\n🎯 CAMPOS ESPERADOS POR UNIDAD:")
    print("⏱️ MINUTOS:")
    print("   - Campo: Minutos")
    
    print("🕐 HORAS:")
    print("   - Campo: Horas")
    print("   - Campo: Minutos adicionales")
    
    print("📅 DÍAS:")
    print("   - Campo: Días")
    print("   - Campo: Horas adicionales")
    
    print("📆 MESES:")
    print("   - Campo: Meses")
    print("   - Campo: Días adicionales")
    
    print("🗓️ AÑOS:")
    print("   - Campo: Años")
    print("   - Campo: Meses adicionales")
    
    print("\n🚀 EJECUTAR AHORA:")
    print("python gestor_suscripciones.py")

if __name__ == "__main__":
    verificar_personalizado()