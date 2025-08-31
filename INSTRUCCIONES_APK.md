# 📱 INSTRUCCIONES PARA CREAR APK DE DANISTORE

## 🔧 Requisitos previos:

### En Windows:
1. Instalar Python 3.8+
2. Instalar Git
3. Instalar Java JDK 8
4. Configurar variables de entorno

### En Linux/Ubuntu:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

## 🚀 Pasos para generar APK:

1. **Ejecutar el script automático:**
   ```bash
   python crear_apk.py
   ```

2. **O manualmente:**
   ```bash
   # Instalar dependencias
   pip install kivy[base] buildozer cython pillow
   
   # Generar APK
   buildozer android debug
   ```

## 📁 Archivos importantes:

- `danistore_app.py` - Aplicación principal
- `buildozer.spec` - Configuración de la APK
- `main.py` - Punto de entrada
- `iconos_android/` - Iconos de la aplicación

## 📱 Resultado:

La APK se generará en: `bin/danistore-1.0-arm64-v8a-debug.apk`

## 🔧 Solución de problemas:

1. **Error de permisos**: Ejecutar como administrador
2. **Falta Java**: Instalar OpenJDK 8
3. **Falta Android SDK**: Buildozer lo descarga automáticamente
4. **Error de memoria**: Cerrar otras aplicaciones

## 📲 Instalación en Android:

1. Habilitar "Fuentes desconocidas" en Android
2. Transferir el archivo .apk al teléfono
3. Instalar tocando el archivo
4. ¡Listo para usar!

## ✨ Características de la APK:

- ✅ Interfaz optimizada para móviles
- ✅ Notificaciones nativas de Android
- ✅ Copia automática al portapapeles
- ✅ Almacenamiento local de datos
- ✅ Iconos profesionales
- ✅ Tema oscuro elegante

¡Tu DaniStore estará listo para Android! 🎉
