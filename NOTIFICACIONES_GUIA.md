# 🔔 SISTEMA DE NOTIFICACIONES EN SEGUNDO PLANO
## Gestor de Suscripciones - Dani666

### 🎯 **¿QUÉ HACE?**
El sistema de notificaciones funciona **independientemente** del gestor principal, enviando alertas de Windows incluso cuando el programa no está abierto.

---

## 🚀 **INSTALACIÓN Y CONFIGURACIÓN**

### **1. Instalar Dependencias**
```bash
python instalar_notificaciones.py
```
**Instala automáticamente:**
- `plyer` - Notificaciones multiplataforma
- `win10toast` - Notificaciones nativas de Windows

### **2. Iniciar el Servicio**

#### **Opción A: Script Python**
```bash
python iniciar_servicio.py
```

#### **Opción B: Archivo Batch (Doble clic)**
```
iniciar_notificaciones.bat
```

#### **Opción C: Directo en Segundo Plano**
```bash
pythonw servicio_notificaciones.py
```

---

## ⚙️ **CONFIGURACIÓN AUTOMÁTICA**

### **Inicio Automático con Windows**
```bash
python configurar_inicio_automatico.py
```

**Opciones disponibles:**
- ✅ Activar inicio automático
- ❌ Desactivar inicio automático  
- 🖥️ Crear acceso directo en escritorio

---

## 🔔 **TIPOS DE NOTIFICACIONES**

### **🚨 VENCE HOY**
- **Título:** "🚨 SUSCRIPCIÓN VENCE HOY"
- **Mensaje:** "⚠️ Usuario - Servicio\n🔔 Vence HOY - ¡Renovar ahora!"

### **⚠️ VENCE MAÑANA**
- **Título:** "⚠️ SUSCRIPCIÓN VENCE MAÑANA"
- **Mensaje:** "📅 Usuario - Servicio\n⏰ Vence mañana - Preparar renovación"

### **❌ YA VENCIDA**
- **Título:** "❌ SUSCRIPCIÓN VENCIDA"
- **Mensaje:** "💔 Usuario - Servicio\n📉 Vencida hace X días"

### **📋 PRÓXIMA A VENCER**
- **Título:** "📋 SUSCRIPCIÓN VENCE EN X DÍAS"
- **Mensaje:** "📺 Usuario - Servicio\n⏳ Quedan X días"

---

## ⚙️ **CONFIGURACIÓN AVANZADA**

### **Archivo: `notificaciones_config.json`**
```json
{
  "activo": true,
  "intervalo_minutos": 60,
  "notificar_dias_antes": [0, 1, 3],
  "sonido": true,
  "duracion_notificacion": 10
}
```

**Parámetros:**
- `activo`: Activar/desactivar notificaciones
- `intervalo_minutos`: Frecuencia de verificación (60 = cada hora)
- `notificar_dias_antes`: Días antes del vencimiento para notificar
- `sonido`: Activar sonido en notificaciones
- `duracion_notificacion`: Duración en segundos de la notificación

---

## 🎬 **CASOS DE USO**

### **📱 Para Vendedores de Streaming:**
1. **Agregar clientes** con el gestor principal
2. **Iniciar servicio** en segundo plano
3. **Recibir alertas automáticas** para renovaciones
4. **Contactar clientes** antes del vencimiento

### **👤 Para Uso Personal:**
1. **Agregar tus suscripciones**
2. **Configurar inicio automático**
3. **Recibir recordatorios** de renovación
4. **Nunca perder** una suscripción

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **❌ No aparecen notificaciones**
1. Verificar que el servicio esté ejecutándose
2. Revisar que hay suscripciones próximas a vencer
3. Comprobar configuración en `notificaciones_config.json`

### **❌ Error al instalar dependencias**
1. Ejecutar como administrador
2. Actualizar pip: `python -m pip install --upgrade pip`
3. Instalar manualmente: `pip install plyer win10toast`

### **❌ Servicio no inicia automáticamente**
1. Ejecutar `configurar_inicio_automatico.py`
2. Verificar permisos de registro de Windows
3. Comprobar ruta de Python en el registro

---

## 📋 **COMANDOS RÁPIDOS**

### **Instalar todo:**
```bash
python instalar_notificaciones.py
python iniciar_servicio.py
python configurar_inicio_automatico.py
```

### **Verificar estado:**
```bash
python servicio_notificaciones.py
```

### **Detener servicio:**
- **Ctrl+C** en la ventana del servicio
- **Administrador de Tareas** → Buscar "python" → Finalizar proceso

---

## 🎉 **RESULTADO FINAL**

✅ **Notificaciones automáticas** cada hora
✅ **Funcionamiento independiente** del gestor principal  
✅ **Inicio automático** con Windows
✅ **Alertas nativas** de Windows 10/11
✅ **Configuración personalizable**
✅ **Perfecto para vendedores** de streaming

**🚀 ¡Nunca más perderás una renovación de suscripción!** 🎬