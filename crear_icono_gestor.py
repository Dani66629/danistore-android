#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creador de Icono para Gestor de Suscripciones - Dani666
"""

from PIL import Image, ImageDraw, ImageFont
import os

def crear_icono_gestor():
    """Crear icono para el gestor de suscripciones"""
    # Crear imagen de 256x256 para alta calidad
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colores Dani666
    color_fondo = '#1a1a1a'
    color_amarillo = '#FFD700'
    color_rojo = '#FF4444'
    color_verde = '#90EE90'
    
    # Fondo circular
    margin = 10
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=color_fondo, outline=color_amarillo, width=8)
    
    # Símbolo de suscripción (TV/Monitor)
    tv_margin = 40
    tv_width = size - (tv_margin * 2)
    tv_height = int(tv_width * 0.6)
    tv_x = tv_margin
    tv_y = tv_margin + 20
    
    # Pantalla principal
    draw.rectangle([tv_x, tv_y, tv_x + tv_width, tv_y + tv_height], 
                   fill=color_fondo, outline=color_amarillo, width=6)
    
    # Pantalla interna
    screen_margin = 15
    draw.rectangle([tv_x + screen_margin, tv_y + screen_margin, 
                   tv_x + tv_width - screen_margin, tv_y + tv_height - screen_margin], 
                   fill=color_verde, outline=None)
    
    # Base del TV
    base_width = int(tv_width * 0.3)
    base_height = 15
    base_x = tv_x + (tv_width - base_width) // 2
    base_y = tv_y + tv_height + 5
    draw.rectangle([base_x, base_y, base_x + base_width, base_y + base_height], 
                   fill=color_amarillo)
    
    # Símbolo de play en la pantalla
    play_size = 30
    play_x = tv_x + (tv_width - play_size) // 2
    play_y = tv_y + (tv_height - play_size) // 2
    
    # Triángulo de play
    play_points = [
        (play_x, play_y),
        (play_x, play_y + play_size),
        (play_x + play_size, play_y + play_size // 2)
    ]
    draw.polygon(play_points, fill=color_rojo)
    
    # Texto "SUB" en la parte inferior
    try:
        # Intentar cargar fuente del sistema
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        # Usar fuente por defecto si no encuentra arial
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Texto principal
    text = "SUB"
    text_bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (size - text_width) // 2
    text_y = size - 60
    
    # Sombra del texto
    draw.text((text_x + 2, text_y + 2), text, font=font_large, fill='#000000')
    # Texto principal
    draw.text((text_x, text_y), text, font=font_large, fill=color_amarillo)
    
    # Indicador de notificación (círculo rojo)
    notif_size = 20
    notif_x = size - 40
    notif_y = 30
    draw.ellipse([notif_x, notif_y, notif_x + notif_size, notif_y + notif_size], 
                 fill=color_rojo, outline='white', width=2)
    
    # Número en la notificación
    draw.text((notif_x + 6, notif_y + 2), "!", font=font_small, fill='white')
    
    # Guardar en diferentes tamaños
    sizes = [256, 128, 64, 32, 16]
    images = []
    
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Guardar como ICO
    img.save('gestor_icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
    print("✅ Icono ICO creado: gestor_icon.ico")
    
    # Guardar como PNG para visualización
    img.save('gestor_icon.png', format='PNG')
    print("✅ Icono PNG creado: gestor_icon.png")
    
    return True

if __name__ == "__main__":
    try:
        crear_icono_gestor()
        print("🎨 ¡Icono del Gestor de Suscripciones creado exitosamente!")
        print("📁 Archivos generados:")
        print("   - gestor_icon.ico (para la aplicación)")
        print("   - gestor_icon.png (para visualización)")
    except Exception as e:
        print(f"❌ Error creando icono: {e}")
        print("💡 Asegúrate de tener Pillow instalado: pip install Pillow")