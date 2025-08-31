#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DaniStore - Gestor de Suscripciones para Android
Versión móvil optimizada con Kivy
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform

import json
import os
from datetime import datetime, timedelta

class DaniStoreApp(App):
    def __init__(self):
        super().__init__()
        self.suscripciones = []
        self.archivo_datos = "suscripciones_data.json"
        self.servicios = [
            "Netflix", "Disney+", "HBO Max", "Amazon Prime", 
            "YouTube Premium", "Crunchyroll", "Spotify", "Apple TV+"
        ]
        
    def build(self):
        self.title = "DaniStore - Streaming"
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='[color=FFD700][size=24]DaniStore - Streaming[/size][/color]\n[color=90EE90]¡Tu éxito es nuestro éxito![/color]',
            markup=True,
            size_hint_y=None,
            height=80,
            text_size=(None, None)
        )
        main_layout.add_widget(header)
        
        # Formulario
        form_layout = self.crear_formulario()
        main_layout.add_widget(form_layout)
        
        # Lista de suscripciones
        lista_layout = self.crear_lista()
        main_layout.add_widget(lista_layout)
        
        # Cargar datos
        self.cargar_datos()
        
        # Iniciar verificación de notificaciones
        Clock.schedule_interval(self.verificar_notificaciones, 60)
        
        return main_layout
    
    def crear_formulario(self):
        """Crear formulario de entrada"""
        form_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=400, spacing=5)
        
        # Usuario
        form_layout.add_widget(Label(text='👤 Usuario:', size_hint_y=None, height=30))
        self.entry_usuario = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.entry_usuario)
        
        # Correo
        form_layout.add_widget(Label(text='📧 Correo:', size_hint_y=None, height=30))
        self.entry_correo = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.entry_correo)
        
        # Contraseña
        form_layout.add_widget(Label(text='🔒 Contraseña:', size_hint_y=None, height=30))
        self.entry_password = TextInput(multiline=False, password=True, size_hint_y=None, height=40)
        form_layout.add_widget(self.entry_password)
        
        # PIN
        form_layout.add_widget(Label(text='📱 PIN:', size_hint_y=None, height=30))
        self.entry_pin = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.entry_pin)
        
        # Servicio
        form_layout.add_widget(Label(text='📺 Servicio:', size_hint_y=None, height=30))
        self.spinner_servicio = Spinner(
            text='Netflix',
            values=self.servicios,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.spinner_servicio)
        
        # Duración
        form_layout.add_widget(Label(text='⏰ Duración:', size_hint_y=None, height=30))
        self.spinner_duracion = Spinner(
            text='1 mes',
            values=['1 mes', '2 meses', '3 meses', '6 meses', '1 año', 'Indefinido'],
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.spinner_duracion)
        
        # Botones
        botones_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        btn_agregar = Button(
            text='➕ AGREGAR',
            background_color=(1, 0.84, 0, 1),  # Dorado
            size_hint_x=0.6
        )
        btn_agregar.bind(on_press=self.agregar_suscripcion)
        botones_layout.add_widget(btn_agregar)
        
        btn_whatsapp = Button(
            text='📱 WhatsApp',
            background_color=(0.15, 0.83, 0.4, 1),  # Verde WhatsApp
            size_hint_x=0.4
        )
        btn_whatsapp.bind(on_press=self.copiar_whatsapp)
        botones_layout.add_widget(btn_whatsapp)
        
        form_layout.add_widget(botones_layout)
        
        return form_layout
    
    def crear_lista(self):
        """Crear lista de suscripciones"""
        lista_layout = BoxLayout(orientation='vertical')
        
        # Título
        titulo = Label(
            text='📋 Suscripciones Activas',
            size_hint_y=None,
            height=40,
            color=(1, 0.84, 0, 1)  # Dorado
        )
        lista_layout.add_widget(titulo)
        
        # ScrollView para la lista
        scroll = ScrollView()
        self.lista_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.lista_container.bind(minimum_height=self.lista_container.setter('height'))
        
        scroll.add_widget(self.lista_container)
        lista_layout.add_widget(scroll)
        
        return lista_layout
    
    def agregar_suscripcion(self, instance):
        """Agregar nueva suscripción"""
        usuario = self.entry_usuario.text.strip()
        correo = self.entry_correo.text.strip()
        password = self.entry_password.text.strip()
        pin = self.entry_pin.text.strip()
        servicio = self.spinner_servicio.text
        duracion = self.spinner_duracion.text
        
        if not usuario:
            self.mostrar_popup("Error", "El usuario es obligatorio")
            return
        
        # Calcular fecha de vencimiento
        fecha_inicio = datetime.now()
        if duracion == "Indefinido":
            fecha_vencimiento = None
        else:
            if "mes" in duracion:
                meses = int(duracion.split()[0])
                fecha_vencimiento = fecha_inicio + timedelta(days=30 * meses)
            elif "año" in duracion:
                años = int(duracion.split()[0])
                fecha_vencimiento = fecha_inicio + timedelta(days=365 * años)
            else:
                fecha_vencimiento = fecha_inicio + timedelta(days=30)
        
        # Crear suscripción
        suscripcion = {
            'id': len(self.suscripciones) + 1,
            'usuario': usuario,
            'correo': correo,
            'password': password,
            'pin': pin,
            'servicio': servicio,
            'duracion': duracion,
            'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_vencimiento': fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S') if fecha_vencimiento else None,
            'activa': True,
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.suscripciones.append(suscripcion)
        self.guardar_datos()
        self.actualizar_lista()
        self.limpiar_formulario()
        
        self.mostrar_popup("Éxito", f"✅ Suscripción de {usuario} agregada")
    
    def copiar_whatsapp(self, instance):
        """Generar mensaje para WhatsApp"""
        usuario = self.entry_usuario.text.strip()
        servicio = self.spinner_servicio.text
        correo = self.entry_correo.text.strip()
        password = self.entry_password.text.strip()
        pin = self.entry_pin.text.strip()
        duracion = self.spinner_duracion.text
        
        if not usuario:
            self.mostrar_popup("Error", "Completa al menos el usuario")
            return
        
        # Calcular fecha de vencimiento
        if duracion == "Indefinido":
            fecha_venc_str = "Sin vencimiento"
        else:
            if "mes" in duracion:
                meses = int(duracion.split()[0])
                fecha_venc = datetime.now() + timedelta(days=30 * meses)
            elif "año" in duracion:
                años = int(duracion.split()[0])
                fecha_venc = datetime.now() + timedelta(days=365 * años)
            else:
                fecha_venc = datetime.now() + timedelta(days=30)
            fecha_venc_str = fecha_venc.strftime('%d/%m/%Y')
        
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
        
        # En Android, usar el clipboard
        if platform == 'android':
            from android.runnable import run_on_ui_thread
            from jnius import autoclass
            
            @run_on_ui_thread
            def copy_to_clipboard():
                ClipboardManager = autoclass('android.content.ClipboardManager')
                ClipData = autoclass('android.content.ClipData')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                activity = PythonActivity.mActivity
                clipboard = activity.getSystemService(activity.CLIPBOARD_SERVICE)
                clip = ClipData.newPlainText("DaniStore", mensaje)
                clipboard.setPrimaryClip(clip)
            
            copy_to_clipboard()
        
        self.mostrar_popup("WhatsApp", "✅ Mensaje copiado al portapapeles\n\n🚀 ¡Listo para enviar!")
    
    def actualizar_lista(self):
        """Actualizar lista de suscripciones"""
        self.lista_container.clear_widgets()
        
        for suscripcion in self.suscripciones:
            if not suscripcion.get('activa', True):
                continue
            
            # Container para cada suscripción
            item_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=120,
                padding=5,
                spacing=2
            )
            
            # Información principal
            info_text = f"👤 {suscripcion['usuario']} - 📺 {suscripcion['servicio']}"
            if suscripcion.get('fecha_vencimiento'):
                fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
                info_text += f"\n📅 Vence: {fecha_venc.strftime('%d/%m/%Y')}"
            else:
                info_text += "\n♾️ Sin vencimiento"
            
            info_label = Label(
                text=info_text,
                size_hint_y=None,
                height=60,
                text_size=(None, None)
            )
            item_layout.add_widget(info_label)
            
            # Botones
            botones_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
            
            btn_whatsapp = Button(
                text='📱 WhatsApp',
                size_hint_x=0.4,
                background_color=(0.15, 0.83, 0.4, 1)
            )
            btn_whatsapp.bind(on_press=lambda x, s=suscripcion: self.whatsapp_suscripcion(s))
            botones_layout.add_widget(btn_whatsapp)
            
            btn_eliminar = Button(
                text='🗑️ Eliminar',
                size_hint_x=0.3,
                background_color=(0.8, 0.2, 0.2, 1)
            )
            btn_eliminar.bind(on_press=lambda x, s=suscripcion: self.eliminar_suscripcion(s))
            botones_layout.add_widget(btn_eliminar)
            
            item_layout.add_widget(botones_layout)
            
            # Separador
            separador = Label(text='─' * 30, size_hint_y=None, height=20)
            item_layout.add_widget(separador)
            
            self.lista_container.add_widget(item_layout)
    
    def whatsapp_suscripcion(self, suscripcion):
        """Generar WhatsApp para suscripción específica"""
        usuario = suscripcion.get('usuario', 'Cliente')
        servicio = suscripcion.get('servicio', 'Servicio')
        correo = suscripcion.get('correo', 'No especificado')
        password = suscripcion.get('password', 'No especificada')
        pin = suscripcion.get('pin', 'No especificado')
        
        if suscripcion.get('fecha_vencimiento'):
            fecha_venc = datetime.strptime(suscripcion['fecha_vencimiento'], '%Y-%m-%d %H:%M:%S')
            fecha_venc_str = fecha_venc.strftime('%d/%m/%Y')
        else:
            fecha_venc_str = 'Sin vencimiento'
        
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
        
        # Copiar al portapapeles en Android
        if platform == 'android':
            from android.runnable import run_on_ui_thread
            from jnius import autoclass
            
            @run_on_ui_thread
            def copy_to_clipboard():
                ClipboardManager = autoclass('android.content.ClipboardManager')
                ClipData = autoclass('android.content.ClipData')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                activity = PythonActivity.mActivity
                clipboard = activity.getSystemService(activity.CLIPBOARD_SERVICE)
                clip = ClipData.newPlainText("DaniStore", mensaje)
                clipboard.setPrimaryClip(clip)
            
            copy_to_clipboard()
        
        self.mostrar_popup("WhatsApp", f"✅ Mensaje de {usuario} copiado\n\n🚀 ¡Listo para enviar!")
    
    def eliminar_suscripcion(self, suscripcion):
        """Eliminar suscripción"""
        suscripcion['activa'] = False
        self.guardar_datos()
        self.actualizar_lista()
        self.mostrar_popup("Eliminado", f"❌ Suscripción de {suscripcion['usuario']} eliminada")
    
    def verificar_notificaciones(self, dt):
        """Verificar suscripciones vencidas"""
        ahora = datetime.now()
        vencidas = []
        
        for suscripcion in self.suscripciones:
            if not suscripcion.get('activa', True):
                continue
            
            fecha_vencimiento_str = suscripcion.get('fecha_vencimiento')
            if not fecha_vencimiento_str:
                continue
            
            try:
                fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d %H:%M:%S')
                if fecha_vencimiento <= ahora:
                    vencidas.append(suscripcion)
            except ValueError:
                continue
        
        if vencidas:
            mensaje = "🚨 SUSCRIPCIONES VENCIDAS:\n\n"
            for s in vencidas:
                mensaje += f"👤 {s['usuario']} - 📺 {s['servicio']}\n"
            mensaje += "\n¡RENOVAR INMEDIATAMENTE!"
            
            self.mostrar_popup("⚠️ ALERTA", mensaje)
    
    def mostrar_popup(self, titulo, mensaje):
        """Mostrar popup de información"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(
            text=mensaje,
            text_size=(300, None),
            halign='center'
        )
        content.add_widget(label)
        
        btn_cerrar = Button(
            text='Cerrar',
            size_hint_y=None,
            height=40
        )
        content.add_widget(btn_cerrar)
        
        popup = Popup(
            title=titulo,
            content=content,
            size_hint=(0.8, 0.6)
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        popup.open()
    
    def limpiar_formulario(self):
        """Limpiar campos del formulario"""
        self.entry_usuario.text = ''
        self.entry_correo.text = ''
        self.entry_password.text = ''
        self.entry_pin.text = ''
        self.spinner_servicio.text = 'Netflix'
        self.spinner_duracion.text = '1 mes'
    
    def cargar_datos(self):
        """Cargar datos desde archivo"""
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    self.suscripciones = json.load(f)
                self.actualizar_lista()
        except Exception as e:
            print(f"Error cargando datos: {e}")
    
    def guardar_datos(self):
        """Guardar datos en archivo"""
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(self.suscripciones, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando datos: {e}")

if __name__ == '__main__':
    DaniStoreApp().run()