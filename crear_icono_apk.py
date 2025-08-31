#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Crear icono profesional para la APK de DaniStore
"""

from PIL import Image, ImageDraw, ImageFont
import os

def crear_icono_danistore():
    """Crear icono profesional para DaniStore APK"""
    print("🎨 CREANDO ICONO PROFESIONAL PARA DANISTORE APK")
    print("=" * 50)
    
    # Tamaños de iconos para Android
    tamaños = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192,
        'launcher': 512  # Para Google Play Store
    }
    
    # Crear directorio para iconos
    if not os.path.exists('iconos_android'):
        os.makedirs('iconos_android')
    
    for densidad, tamaño in tamaños.items():
        # Crear imagen base
        img = Image.new('RGBA', (tamaño, tamaño), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colores del tema
        color_fondo = '#1a1a1a'  # Negro elegante
        color_acento = '#FFD700'  # Dorado
        color_streaming = '#FF6B35'  # Naranja vibrante
        color_texto = '#FFFFFF'  # Blanco
        
        # Crear fondo con gradiente circular
        centro = tamaño // 2
        radio_max = centro - 4
        
        # Fondo principal (círculo negro elegante)
        draw.ellipse([4, 4, tamaño-4, tamaño-4], fill=color_fondo, outline=color_acento, width=max(1, tamaño//48))
        
        # Círculo interno dorado
        radio_interno = int(radio_max * 0.85)
        draw.ellipse([centro-radio_interno, centro-radio_interno, 
                     centro+radio_interno, centro+radio_interno], 
                     outline=color_acento, width=max(1, tamaño//64))
        
        # Símbolo de streaming (play + ondas)
        # Triángulo de play
        play_size = tamaño // 6
        play_x = centro - play_size // 3
        play_y = centro
        
        puntos_play = [
            (play_x - play_size//2, play_y - play_size//2),
            (play_x - play_size//2, play_y + play_size//2),
            (play_x + play_size//2, play_y)
        ]
        draw.polygon(puntos_play, fill=color_streaming)
        
        # Ondas de streaming (círculos concéntricos)
        for i in range(3):
            radio_onda = play_size + (i * tamaño // 12)
            if centro + radio_onda < tamaño - 8:
                draw.arc([centro-radio_onda, centro-radio_onda,
                         centro+radio_onda, centro+radio_onda],
                         start=-30, end=30, fill=color_acento, width=max(1, tamaño//96))
                draw.arc([centro-radio_onda, centro-radio_onda,
                         centro+radio_onda, centro+radio_onda],
                         start=150, end=210, fill=color_acento, width=max(1, tamaño//96))
        
        # Texto "DS" (DaniStore) si el tamaño lo permite
        if tamaño >= 96:
            try:
                # Intentar usar fuente del sistema
                font_size = max(tamaño // 8, 12)
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Posicionar texto en la parte inferior
            texto = "DS"
            bbox = draw.textbbox((0, 0), texto, font=font)
            texto_width = bbox[2] - bbox[0]
            texto_height = bbox[3] - bbox[1]
            
            texto_x = centro - texto_width // 2
            texto_y = centro + tamaño // 4
            
            if texto_y + texto_height < tamaño - 8:
                # Sombra del texto
                draw.text((texto_x + 1, texto_y + 1), texto, fill='#000000', font=font)
                # Texto principal
                draw.text((texto_x, texto_y), texto, fill=color_acento, font=font)
        
        # Guardar icono
        nombre_archivo = f'iconos_android/ic_launcher_{densidad}.png'
        img.save(nombre_archivo, 'PNG')
        print(f"✅ Icono creado: {nombre_archivo} ({tamaño}x{tamaño})")
    
    # Crear icono adicional para el escritorio
    icono_escritorio = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw_escritorio = ImageDraw.Draw(icono_escritorio)
    
    # Fondo con gradiente
    for y in range(256):
        color_r = int(26 + (255-26) * (y/256) * 0.1)
        color_g = int(26 + (215-26) * (y/256) * 0.3)
        color_b = int(26 + (0-26) * (y/256) * 0.1)
        draw_escritorio.line([(0, y), (256, y)], fill=(color_r, color_g, color_b))
    
    # Elementos decorativos
    draw_escritorio.ellipse([20, 20, 236, 236], fill='#1a1a1a', outline='#FFD700', width=4)
    draw_escritorio.ellipse([40, 40, 216, 216], outline='#FF6B35', width=2)
    
    # Símbolo principal más grande
    centro_desk = 128
    play_size_desk = 40
    play_x_desk = centro_desk - 8
    
    puntos_play_desk = [
        (play_x_desk - play_size_desk//2, centro_desk - play_size_desk//2),
        (play_x_desk - play_size_desk//2, centro_desk + play_size_desk//2),
        (play_x_desk + play_size_desk//2, centro_desk)
    ]
    draw_escritorio.polygon(puntos_play_desk, fill='#FF6B35')
    
    # Ondas más elaboradas
    for i in range(4):
        radio_onda_desk = play_size_desk + (i * 25)
        draw_escritorio.arc([centro_desk-radio_onda_desk, centro_desk-radio_onda_desk,
                           centro_desk+radio_onda_desk, centro_desk+radio_onda_desk],
                           start=-45, end=45, fill='#FFD700', width=3)
        draw_escritorio.arc([centro_desk-radio_onda_desk, centro_desk-radio_onda_desk,
                           centro_desk+radio_onda_desk, centro_desk+radio_onda_desk],
                           start=135, end=225, fill='#FFD700', width=3)
    
    # Texto "DaniStore"
    try:
        font_titulo = ImageFont.truetype("arial.ttf", 24)
        font_subtitulo = ImageFont.truetype("arial.ttf", 16)
    except:
        font_titulo = ImageFont.load_default()
        font_subtitulo = ImageFont.load_default()
    
    # Título
    titulo = "DaniStore"
    bbox_titulo = draw_escritorio.textbbox((0, 0), titulo, font=font_titulo)
    titulo_width = bbox_titulo[2] - bbox_titulo[0]
    titulo_x = centro_desk - titulo_width // 2
    titulo_y = centro_desk + 60
    
    draw_escritorio.text((titulo_x + 2, titulo_y + 2), titulo, fill='#000000', font=font_titulo)
    draw_escritorio.text((titulo_x, titulo_y), titulo, fill='#FFD700', font=font_titulo)
    
    # Subtítulo
    subtitulo = "Streaming"
    bbox_subtitulo = draw_escritorio.textbbox((0, 0), subtitulo, font=font_subtitulo)
    subtitulo_width = bbox_subtitulo[2] - bbox_subtitulo[0]
    subtitulo_x = centro_desk - subtitulo_width // 2
    subtitulo_y = titulo_y + 30
    
    draw_escritorio.text((subtitulo_x + 1, subtitulo_y + 1), subtitulo, fill='#000000', font=font_subtitulo)
    draw_escritorio.text((subtitulo_x, subtitulo_y), subtitulo, fill='#FF6B35', font=font_subtitulo)
    
    icono_escritorio.save('iconos_android/danistore_icon.png', 'PNG')
    print("✅ Icono de escritorio creado: iconos_android/danistore_icon.png")
    
    print(f"\n🎉 ¡{len(tamaños) + 1} iconos creados exitosamente!")
    return True

if __name__ == "__main__":
    crear_icono_danistore()