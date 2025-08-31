# 📱 DaniStore - Gestor de Suscripciones

> **Aplicación móvil para gestionar suscripciones de streaming de forma profesional**

![DaniStore](https://img.shields.io/badge/DaniStore-Gestor%20Suscripciones-gold?style=for-the-badge)
![Android](https://img.shields.io/badge/Android-APK-green?style=for-the-badge&logo=android)
![Python](https://img.shields.io/badge/Python-Kivy-blue?style=for-the-badge&logo=python)

## 🎯 Características Principales

### 📋 Gestión Completa
- ➕ **Agregar suscripciones** con datos completos
- 📱 **Generar mensajes** profesionales para WhatsApp
- 🔔 **Notificaciones** automáticas de vencimiento
- 💾 **Guardado automático** de todos los datos
- 🗑️ **Eliminar suscripciones** fácilmente

### 🎨 Interfaz Profesional
- 🌟 **Diseño DaniStore** con colores corporativos
- 📱 **Optimizada para móviles** Android
- 🎯 **Fácil de usar** e intuitiva
- ⚡ **Rápida y eficiente**

### 📺 Servicios Soportados
- Netflix, Disney+, HBO Max
- Amazon Prime, YouTube Premium
- Crunchyroll, Spotify, Apple TV+
- Y muchos más...

## 🚀 Generar APK Automáticamente

### Método 1: GitHub Actions (Recomendado)

1. **Sube tu código a GitHub:**
```bash
python subir_a_github_gestor.py
```

2. **El proceso automático:**
   - ✅ GitHub Actions detecta los cambios
   - 🏗️ Compila la APK automáticamente
   - 📱 Genera APK lista para instalar
   - 📥 Disponible en "Actions" → "Artifacts"

### Método 2: Local con Buildozer

```bash
python generar_gestor_apk.py
```

### Método 3: Online con Replit

1. Ve a [Replit.com](https://replit.com)
2. Crea nuevo proyecto Python
3. Sube los archivos del gestor
4. Ejecuta: `buildozer android debug`

## 📁 Estructura del Proyecto

```
📦 danistore-gestor/
├── 📱 danistore_app.py          # App principal para Android
├── 🖥️ gestor_suscripciones.py   # Versión desktop (Tkinter)
├── ⚙️ buildozer.spec            # Configuración APK
├── 🚀 subir_a_github_gestor.py  # Script para GitHub
├── 🏗️ generar_gestor_apk.py     # Generador local APK
├── 🎨 iconos_android/           # Iconos de la app
├── 🤖 .github/workflows/        # GitHub Actions
└── 📋 README_GESTOR.md          # Esta documentación
```

## 🔧 Instalación y Uso

### 📱 En Android

1. **Descarga la APK** desde GitHub Actions
2. **Habilita fuentes desconocidas** en Configuración
3. **Instala la APK** tocándola
4. **¡Disfruta gestionando tus suscripciones!**

### 🖥️ En PC (Desarrollo)

```bash
# Instalar dependencias
pip install kivy pillow buildozer

# Ejecutar versión desktop
python gestor_suscripciones.py

# Generar APK
python generar_gestor_apk.py
```

## 📱 Capturas de Pantalla

### 🏠 Pantalla Principal
- Formulario para agregar suscripciones
- Lista de suscripciones activas
- Botones de acción rápida

### 📝 Agregar Suscripción
- Usuario, correo, contraseña, PIN
- Selección de servicio de streaming
- Duración personalizable
- Fecha de inicio opcional

### 📱 Mensaje WhatsApp
```
🎬 ¡Tu cuenta Netflix está lista! 🎬

✨ DATOS DE ACCESO ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 PERFIL: Juan Pérez
📧 CORREO: juan@email.com
🔒 CONTRASEÑA: mi_password
📱 PIN: 1234

━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 VÁLIDA HASTA: 15/02/2025
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 ¡DISFRUTA TU ENTRETENIMIENTO! 🔥

💎 Gracias por confiar en DaniStore
🚀 ¡Tu entretenimiento sin límites!
```

## 🔔 Sistema de Notificaciones

### ⚡ Verificación Automática
- 🕐 Cada 60 segundos (configurable)
- 🚨 Alerta de suscripciones vencidas
- 📱 Notificaciones push en Android

### 📊 Estadísticas
- 📈 Total de suscripciones activas
- 📅 Próximos vencimientos
- 💰 Valor total gestionado

## 🛠️ Desarrollo

### 🔧 Tecnologías Utilizadas
- **Python 3.9+** - Lenguaje principal
- **Kivy** - Framework móvil multiplataforma
- **Buildozer** - Compilador para Android
- **GitHub Actions** - CI/CD automático

### 📦 Dependencias
```python
# requirements.txt
kivy[base]>=2.1.0
pillow>=8.0.0
buildozer>=1.4.0
plyer>=2.0.0
pyjnius>=1.4.0
```

### 🔄 Workflow de Desarrollo

1. **Desarrollo local** con `gestor_suscripciones.py`
2. **Adaptación móvil** en `danistore_app.py`
3. **Pruebas locales** con Kivy
4. **Push a GitHub** para compilación automática
5. **Descarga APK** desde Actions

## 🚀 GitHub Actions

### ⚙️ Configuración Automática
El workflow se ejecuta automáticamente cuando:
- 📤 Haces push a main/master
- 📝 Modificas archivos del gestor
- 🔧 Cambias buildozer.spec
- 🎯 Ejecutas manualmente desde GitHub

### 📋 Proceso de Compilación
```yaml
1. 📥 Checkout del código
2. 🐍 Configurar Python 3.9
3. 📦 Instalar dependencias del sistema
4. 🔧 Instalar Buildozer y Kivy
5. 🏗️ Compilar APK con Buildozer
6. 📱 Renombrar APK con versión
7. 📤 Subir como artefacto
```

## 📈 Roadmap

### 🔜 Próximas Características
- [ ] 🔐 Backup en la nube
- [ ] 📊 Dashboard de estadísticas
- [ ] 🔔 Notificaciones push mejoradas
- [ ] 🎨 Temas personalizables
- [ ] 📱 Widget para pantalla de inicio
- [ ] 💰 Calculadora de ganancias

### 🎯 Mejoras Planificadas
- [ ] 🚀 Optimización de rendimiento
- [ ] 🌐 Soporte para más idiomas
- [ ] 📱 Versión para iOS
- [ ] 🔄 Sincronización entre dispositivos

## 🤝 Contribuir

### 🛠️ Cómo Contribuir
1. 🍴 Fork el repositorio
2. 🌿 Crea una rama para tu feature
3. 💻 Desarrolla tu mejora
4. 🧪 Prueba los cambios
5. 📤 Envía un Pull Request

### 🐛 Reportar Bugs
- 📝 Usa GitHub Issues
- 📋 Incluye pasos para reproducir
- 📱 Especifica versión de Android
- 📸 Adjunta capturas si es posible

## 📞 Soporte

### 💬 Contacto
- 📧 **Email:** danistore@email.com
- 📱 **WhatsApp:** +1234567890
- 🌐 **Web:** danistore.com

### 📚 Documentación
- 📖 [Guía de Usuario](GUIA_USUARIO.md)
- 🔧 [Manual Técnico](MANUAL_TECNICO.md)
- 🚀 [Guía de Despliegue](GUIA_DESPLIEGUE.md)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

---

<div align="center">

**🎬 DaniStore - Tu éxito es nuestro éxito 🚀**

[![GitHub](https://img.shields.io/badge/GitHub-danistore--gestor-black?style=flat&logo=github)](https://github.com/usuario/danistore-gestor)
[![Android](https://img.shields.io/badge/Download-APK-green?style=flat&logo=android)](https://github.com/usuario/danistore-gestor/actions)

</div>