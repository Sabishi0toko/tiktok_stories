# app/modules/audio/write_file_configuration.py

import os
from tkinter import messagebox
from app.utils.utils import write  # Importar la función write
from app.modules.messages import show_status_message, set_status_label

def write_file_configuration(audio_config, text_entry, speed_scale, pitch_scale, status_label):
    """Guarda la configuración de la aplicación en archivos."""
    show_status_message(status_label, "Verificando configuración...", "info")

    try:
        # Obtener la configuración de voz
        voice_name, country_id, gender_mf, error_message = audio_config.get_voice_configuration()
        text = text_entry.get("1.0", "end-1c").strip()
        speed = speed_scale.get()  # Obtener la velocidad seleccionada            
        pitch = pitch_scale.get()  # Obtener el tono seleccionada            

        if error_message:
            # Mostrar el mensaje de error en un cuadro de diálogo
            messagebox.showerror("Error", error_message)
            show_status_message(status_label, "Error en la configuración de voz", "error")
        elif not text:
            # Mostrar el mensaje de error si el campo de texto está vacío
            messagebox.showerror("Error", "El campo de texto está vacío. Por favor, ingrese algún texto.")
            show_status_message(status_label, "Campo de texto vacío", "error")
        else:
            # Mostrar la configuración de voz en un cuadro de diálogo
            messagebox.showinfo("Configuración de Voz", f"Configuración de voz: {voice_name}")
            show_status_message(status_label, "Configuración de voz aceptada", "success")
            # Crear o actualizar los archivos de configuración usando la función write
            write('text_for_user.txt', text)
            write('voice_config.txt', voice_name)
            write('country_code.txt', country_id)
            write('gender.txt', gender_mf)
            write('speed.txt', str(speed))
            write('pitch.txt', str(pitch))

            print(f"Archivos de configuración creados/actualizados exitosamente.")
            show_status_message(status_label, "Archivos de configuración guardados", "success")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        show_status_message(status_label, "Error al guardar los archivos", "error")
