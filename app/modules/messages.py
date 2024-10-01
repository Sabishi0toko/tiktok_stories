# app/modules/messages.py

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


def show_status_message(status_label, message, msg_type):
    """
    Muestra un mensaje de estado en la interfaz de usuario.
    :param status_label: La etiqueta de estado a actualizar.
    :param message: El mensaje a mostrar.
    :param msg_type: El tipo de mensaje ('error', 'success', 'warning', 'info', u otro).
    """
    if isinstance(status_label, QLabel):
        if msg_type == "error":
            status_label.setStyleSheet("background-color: red; color: white;")
        elif msg_type == "success":
            status_label.setStyleSheet("background-color: green; color: white;")
        elif msg_type == "warning":
            status_label.setStyleSheet("background-color: yellow; color: black;")
        elif msg_type == "info":
            status_label.setStyleSheet("background-color: blue; color: white;")
        else:
            status_label.setStyleSheet("background-color: white; color: black;")

        # Establecer el texto del mensaje
        status_label.setText(message)
        status_label.setAlignment(Qt.AlignCenter)
    else:
        # Imprimir en la consola si no hay una etiqueta de estado configurada
        print(f"[{msg_type.upper()}] {message}")


def set_status_label(status_label, new_status_label):
    """
    Configura la etiqueta de estado para actualizar los mensajes.
    :param status_label: La etiqueta de estado actual.
    :param new_status_label: La nueva etiqueta de estado a actualizar.
    """
    return new_status_label



