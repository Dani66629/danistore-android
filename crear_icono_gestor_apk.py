#!/usr/bin/env python3
"""
Crear icono para la APK del Gestor de Suscripciones
"""

from PIL import Image, ImageDraw, ImageFont
import os

def crear_icono_gestor():
    """Crear icono para el gestor de suscripciones"""
    
    # Crear imagen de 512x512 (tamaño estándar para iconos de Android)
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fondo circular dorado
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(255, 215, 0, 255),  # Dorado
                outline=(255, 255, 255, 255), 
                width=8)
    
    # Fondo interior negro
    inner_margin = 60
    draw.ellipse([inner_margin, inner_margin, size-inner_margin, size-inner_margin], 
                fill=(26, 26, 26, 255))  # Negro DaniStore
    
    # Intentar cargar fuente, si no usar la por defecto
    try:
        # Fuente grande para el emoji
        font_emoji = ImageFont.truetype("arial.ttf", 120)
        font_text = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 32)
    except:
        try:
            font_emoji = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_small = ImageFont.load_default()
        except:
            font_emoji = None
            font_text = None
            font_small = None
    
    # Dibujar emoji de gestión (📋)
    emoji_text = "📋"
    if font_emoji:
        # Calcular posición centrada para el emoji
        bbox = draw.textbbox((0, 0), emoji_text, font=font_emoji)
        emoji_width = bbox[2] - bbox[0]
        emoji_height = bbox[3] - bbox[1]
        emoji_x = (size - emoji_width) // 2
        emoji_y = (size - emoji_height) // 2 - 40
        
        draw.text((emoji_x, emoji_y), emoji_text, 
                 fill=(255, 215, 0, 255), font=font_emoji)
    
    # Texto "GESTOR"
    text_gestor = "GESTOR"
    if font_text:
        bbox = draw.textbbox((0, 0), text_gestor, font=font_text)
        text_width = bbox[2] - bbox[0]
        text_x = (size - text_width) // 2
        text_y = size - 120
        
        draw.text((text_x, text_y), text_gestor, 
                 fill=(255, 255, 255, 255), font=font_text)
    
    # Texto "DaniStore"
    text_dani = "DaniStore"
    if font_small:
        bbox = draw.textbbox((0, 0), text_dani, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x = (size - text_width) // 2
        text_y = size - 70
        
        draw.text((text_x, text_y), text_dani, 
                 fill=(255, 215, 0, 255), font=font_small)
    
    # Crear directorio si no existe
    icon_dir = "iconos_android"
    if not os.path.exists(icon_dir):
        os.makedirs(icon_dir)
    
    # Guardar icono principal
    icon_path = os.path.join(icon_dir, "gestor_icon.png")
    img.save(icon_path, "PNG")
    print(f"✅ Icono principal creado: {icon_path}")
    
    # Crear versiones de diferentes tamaños para Android
    sizes = [
        (36, "ldpi"),
        (48, "mdpi"), 
        (72, "hdpi"),
        (96, "xhdpi"),
        (144, "xxhdpi"),
        (192, "xxxhdpi")
    ]
    
    for size_px, density in sizes:
        resized = img.resize((size_px, size_px), Image.Resampling.LANCZOS)
        density_path = os.path.join(icon_dir, f"gestor_icon_{density}.png")
        resized.save(density_path, "PNG")
        print(f"✅ Icono {density} creado: {density_path}")
    
    print(f"\n🎉 ¡Todos los iconos creados exitosamente!")
    print(f"📁 Ubicación: {os.path.abspath(icon_dir)}")
    
    return icon_path

if __name__ == "__main__":
    crear_icono_gestor()