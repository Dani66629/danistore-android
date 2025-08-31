#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba específica para la funcionalidad personalizada
"""

import tkinter as tk
from tkinter import ttk

def test_personalizado():
    """Crear una ventana de prueba simple para verificar la funcionalidad"""
    root = tk.Tk()
    root.title("Prueba - Duración Personalizada")
    root.geometry("400x500")
    root.configure(bg='#2a2a2a')
    
    # Combo de duración
    tk.Label(root, text="Duración:", bg='#2a2a2a', fg='white').pack(pady=10)
    combo_duracion = ttk.Combobox(root, 
                                 values=["1 mes", "2 meses", "Personalizado"],
                                 state='readonly')
    combo_duracion.pack(pady=5)
    combo_duracion.set("1 mes")
    
    # Frame personalizado
    custom_frame = tk.Frame(root, bg='#2a2a2a')
    
    # Selector de unidad
    tk.Label(custom_frame, text="Unidad:", bg='#2a2a2a', fg='white').pack(pady=5)
    combo_unidad = ttk.Combobox(custom_frame,
                               values=["Minutos", "Horas", "Días", "Meses", "Años"],
                               state='readonly')
    combo_unidad.pack(pady=5)
    combo_unidad.set("Días")
    
    # Frame para campos
    campos_frame = tk.Frame(custom_frame, bg='#2a2a2a')
    campos_frame.pack(pady=10)
    
    def crear_campos():
        # Limpiar
        for widget in campos_frame.winfo_children():
            widget.destroy()
            
        unidad = combo_unidad.get()
        
        if unidad == "Días":
            tk.Label(campos_frame, text="Días:", bg='#2a2a2a', fg='white').pack()
            entry_dias = tk.Entry(campos_frame, bg='#3a3a3a', fg='white')
            entry_dias.pack(pady=2)
            
            tk.Label(campos_frame, text="Horas extra:", bg='#2a2a2a', fg='white').pack(pady=(10,0))
            entry_horas = tk.Entry(campos_frame, bg='#3a3a3a', fg='white')
            entry_horas.pack(pady=2)
        
        elif unidad == "Horas":
            tk.Label(campos_frame, text="Horas:", bg='#2a2a2a', fg='white').pack()
            entry_horas = tk.Entry(campos_frame, bg='#3a3a3a', fg='white')
            entry_horas.pack(pady=2)
            
            tk.Label(campos_frame, text="Minutos extra:", bg='#2a2a2a', fg='white').pack(pady=(10,0))
            entry_minutos = tk.Entry(campos_frame, bg='#3a3a3a', fg='white')
            entry_minutos.pack(pady=2)
    
    def on_duracion_change(event=None):
        if combo_duracion.get() == "Personalizado":
            custom_frame.pack(pady=20)
            crear_campos()
        else:
            custom_frame.pack_forget()
    
    def on_unidad_change(event=None):
        crear_campos()
    
    combo_duracion.bind('<<ComboboxSelected>>', on_duracion_change)
    combo_unidad.bind('<<ComboboxSelected>>', on_unidad_change)
    
    # Inicializar campos
    crear_campos()
    
    tk.Label(root, text="Selecciona 'Personalizado' para ver los campos", 
             bg='#2a2a2a', fg='yellow').pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    test_personalizado()