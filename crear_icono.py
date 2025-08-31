"""
Script para crear un icono profesional de torneo para la aplicación
"""
from PIL import Image, ImageDraw
import math

def crear_icono_torneo():
    # Crear imagen de 256x256 para alta calidad
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Centro de la imagen
    center = size // 2
    
    # Colores profesionales para torneo
    color_fondo = '#0a0a1a'      # Azul muy oscuro
    color_dorado = '#FFD700'     # Dorado principal
    color_plata = '#C0C0C0'      # Plata
    color_bronce = '#CD7F32'     # Bronce
    color_borde = '#FFFFFF'      # Blanco para contraste
    
    # Fondo circular con gradiente simulado
    margin = 8
    # Círculo exterior (borde)
    draw.ellipse([0, 0, size, size], fill=color_dorado)
    # Círculo interior (fondo)
    draw.ellipse([margin, margin, size-margin, size-margin], fill=color_fondo)
    
    # Dibujar copa/trofeo principal
    copa_width = 120
    copa_height = 140
    copa_x = center - copa_width // 2
    copa_y = center - copa_height // 2 - 10
    
    # Base del trofeo
    base_width = 80
    base_height = 20
    base_x = center - base_width // 2
    base_y = copa_y + copa_height - 10
    draw.rectangle([base_x, base_y, base_x + base_width, base_y + base_height], 
                  fill=color_dorado, outline=color_borde, width=2)
    
    # Stem del trofeo
    stem_width = 12
    stem_height = 30
    stem_x = center - stem_width // 2
    stem_y = base_y - stem_height
    draw.rectangle([stem_x, stem_y, stem_x + stem_width, stem_y + stem_height], 
                  fill=color_dorado, outline=color_borde, width=1)
    
    # Copa principal (cuerpo)
    copa_body_width = 70
    copa_body_height = 80
    copa_body_x = center - copa_body_width // 2
    copa_body_y = stem_y - copa_body_height
    
    # Dibujar copa como elipse
    draw.ellipse([copa_body_x, copa_body_y, 
                 copa_body_x + copa_body_width, copa_body_y + copa_body_height], 
                fill=color_dorado, outline=color_borde, width=3)
    
    # Asas de la copa
    asa_width = 15
    asa_height = 40
    # Asa izquierda
    asa_left_x = copa_body_x - asa_width
    asa_left_y = copa_body_y + 20
    draw.ellipse([asa_left_x, asa_left_y, asa_left_x + asa_width, asa_left_y + asa_height], 
                outline=color_borde, width=4, fill=None)
    
    # Asa derecha
    asa_right_x = copa_body_x + copa_body_width
    asa_right_y = copa_body_y + 20
    draw.ellipse([asa_right_x, asa_right_y, asa_right_x + asa_width, asa_right_y + asa_height], 
                outline=color_borde, width=4, fill=None)
    
    # Detalles decorativos en la copa
    detail_y = copa_body_y + 25
    draw.ellipse([copa_body_x + 10, detail_y, copa_body_x + copa_body_width - 10, detail_y + 8], 
                fill=color_plata, outline=color_borde, width=1)
    
    detail_y2 = copa_body_y + 40
    draw.ellipse([copa_body_x + 15, detail_y2, copa_body_x + copa_body_width - 15, detail_y2 + 6], 
                fill=color_bronce, outline=color_borde, width=1)
    
    # Corona en la parte superior
    corona_y = copa_body_y - 25
    corona_points = []
    num_picos = 5
    corona_width = 50
    corona_height = 20
    
    for i in range(num_picos * 2):
        x = center - corona_width // 2 + (i * corona_width // (num_picos * 2 - 1))
        if i % 2 == 0:  # Picos altos
            y = corona_y
        else:  # Picos bajos
            y = corona_y + corona_height // 2
        corona_points.append((x, y))
    
    # Cerrar la corona
    corona_points.append((center + corona_width // 2, corona_y + corona_height))
    corona_points.append((center - corona_width // 2, corona_y + corona_height))
    
    draw.polygon(corona_points, fill=color_dorado, outline=color_borde, width=2)
    
    # Añadir texto "1st" en la copa
    try:
        from PIL import ImageFont
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_small = ImageFont.truetype("arial.ttf", 16)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Texto principal
        text = "1st"
        bbox = draw.textbbox((0, 0), text, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = center - text_width // 2
        text_y = copa_body_y + copa_body_height // 2 - text_height // 2
        
        draw.text((text_x, text_y), text, fill=color_fondo, font=font_large)
        
    except:
        pass
    
    # Estrellas decorativas alrededor
    star_positions = [
        (50, 50), (206, 50), (50, 206), (206, 206),
        (30, 128), (226, 128), (128, 30), (128, 226)
    ]
    
    for star_x, star_y in star_positions:
        # Dibujar estrella simple
        star_size = 8
        star_points = []
        for i in range(10):  # 5 puntas, 2 puntos por punta
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = star_size
            else:
                radius = star_size // 2
            x = star_x + radius * math.cos(angle - math.pi/2)
            y = star_y + radius * math.sin(angle - math.pi/2)
            star_points.append((x, y))
        
        draw.polygon(star_points, fill=color_dorado, outline=color_borde, width=1)
    
    # Guardar en diferentes tamaños para el .ico
    sizes = [256, 128, 64, 32, 16]
    images = []
    
    for s in sizes:
        if s == 256:
            images.append(img)
        else:
            resized = img.resize((s, s), Image.Resampling.LANCZOS)
            images.append(resized)
    
    # Guardar como .ico
    img.save('torneo_icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
    
    # También guardar como PNG para visualización
    img.save('torneo_icon.png', format='PNG')
    
    print("✅ Icono de torneo creado exitosamente:")
    print("   - torneo_icon.ico (para el .exe)")
    print("   - torneo_icon.png (para visualización)")

if __name__ == "__main__":
    try:
        crear_icono_torneo()
    except ImportError:
        print("❌ Error: Se necesita instalar Pillow")
        print("Ejecuta: pip install Pillow")
    except Exception as e:
        print(f"❌ Error creando el icono: {e}")