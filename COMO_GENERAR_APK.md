# 📱 CÓMO GENERAR LA APK DE DANISTORE

## 🚨 PROBLEMA ACTUAL
Buildozer tiene problemas en Windows. Aquí tienes las soluciones:

## ✅ SOLUCIÓN 1: USAR LINUX/WSL (RECOMENDADO)

### Paso 1: Instalar WSL en Windows
```bash
# En PowerShell como administrador
wsl --install
```

### Paso 2: En WSL/Linux
```bash
# Clonar archivos o copiar a WSL
# Instalar dependencias
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalar Python packages
pip3 install --user buildozer cython kivy[base]

# Generar APK
buildozer android debug
```

### Resultado:
- APK generada en: `bin/danistore-1.0-arm64-v8a-debug.apk`

## ✅ SOLUCIÓN 2: USAR GITHUB ACTIONS (AUTOMÁTICO)

### Crear archivo `.github/workflows/build-apk.yml`:
```yaml
name: Build APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y openjdk-8-jdk
        pip install buildozer cython kivy[base]
    - name: Build APK
      run: buildozer android debug
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: danistore-apk
        path: bin/*.apk
```

## ✅ SOLUCIÓN 3: USAR SERVICIO ONLINE

### Repl.it o CodeSpaces:
1. Subir archivos a Repl.it
2. Ejecutar en terminal Linux
3. Descargar APK generada

## ✅ SOLUCIÓN 4: EJECUTABLE WINDOWS (ALTERNATIVA)

Si no puedes generar APK, usa el ejecutable:
```bash
python generar_apk_alternativo.py
```

Esto crea `DaniStore.exe` que funciona igual en Windows.

## 📱 ARCHIVOS NECESARIOS PARA APK

Asegúrate de tener:
- ✅ `main.py` - Punto de entrada
- ✅ `danistore_app.py` - Aplicación principal
- ✅ `buildozer.spec` - Configuración
- ✅ `iconos_android/danistore_icon.png` - Icono

## 🎯 RESULTADO FINAL

Una vez generada, la APK:
- 📱 Se instala en cualquier Android 5.0+
- 💾 Tamaño: ~20-50 MB
- ✅ Funciona completamente offline
- 🔔 Incluye notificaciones nativas
- 📋 Gestión completa de suscripciones
- 💬 Integración WhatsApp

## 🆘 SI TIENES PROBLEMAS

1. **Windows**: Usa WSL o GitHub Actions
2. **Linux**: Funciona directamente
3. **Mac**: Funciona con algunos ajustes
4. **Online**: Usa Repl.it o CodeSpaces

## 📞 CONTACTO

Si necesitas ayuda específica, comparte:
- Sistema operativo
- Mensajes de error
- Archivos que tienes

¡Tu DaniStore APK está al alcance! 🚀
