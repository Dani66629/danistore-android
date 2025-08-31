#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de prueba para el botón de WhatsApp con el nuevo mensaje
"""

import tkinter as tk
from datetime import datetime, timedelta

def test_mensaje_whatsapp():
    """Probar el formato del mensaje de WhatsApp"""
    
    # Datos de prueba
    usuario = "Juan Pérez"
    servicio = "Netflix"
    correo = "juan.perez@email.com"
    password = "MiPassword123"
    pin = "1234"
    fecha_venc_str = "30/09/2025"
    
    # Generar mensaje profesional y elegante
    mensaje = f"""🎬 ¡Tu cuenta {servicio} está lista! 🎬

✨ DATOS DE ACCESO ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 PERFIL: {usuario}
📧 CORREO: {correo}
🔒 CONTRASEÑA: {password}
📱 PIN: {pin}

━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 VÁLIDA HASTA: {fecha_venc_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 ¡DISFRUTA TU ENTRETENIMIENTO! 🔥

📌 IMPORTANTE:
• Guarda estos datos en un lugar seguro
• No compartas tu información con terceros
• Recuerda que es para UN SOLO DISPOSITIVO para evitar la expulsión de tu perfil
• Si adquiriste para 1 o más dispositivos, ignora el mensaje anterior
• Cualquier duda, contáctame

💎 Gracias por confiar en DaniStore
🚀 ¡Tu entretenimiento sin límites!"""

    print("=" * 50)
    print("PREVIEW DEL MENSAJE DE WHATSAPP")
    print("=" * 50)
    print(mensaje)
    print("=" * 50)
    print(f"Longitud del mensaje: {len(mensaje)} caracteres")
    print("✅ Mensaje generado exitosamente!")

if __name__ == "__main__":
    test_mensaje_whatsapp()