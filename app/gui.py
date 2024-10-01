# app/gui.py
import os
import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QComboBox,
    QFileDialog,
    QTextEdit,
    QMenu,
    QMainWindow,
    QSizePolicy,
    QScrollArea, QFrame, QGridLayout, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
import app.modules.video_utils as video_module
from .modules.audio_utils import AudioConfig
from .utils.utils import save_file, play, get_tmp_dir, get_save_dir
from app.modules.messages import show_status_message, set_status_label
from data.languages import languages_get

# Deshabilitar el uso de MIT-SHM y forzar backend de software
os.environ["QT_X11_NO_MITSHM"] = "1"
os.environ["QT_QUICK_BACKEND"] = "software"

# Inicializamos GStreamer
Gst.init(None)

class TextToSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_config = AudioConfig()    # Crear una instancia de AudioConfig
        self.setWindowTitle("Configuración de Idioma")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)
        self.idiomas = languages_get()
        self.temp_file_path = get_tmp_dir()

        # Inicializar GStreamer
        self.pipeline = Gst.Pipeline()

        # Configurar interfaz gráfica
        self.init_ui()

    def init_ui(self):
        # Crear un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Crear layout principal para agregar los widgets
        self.layout_principal = QVBoxLayout(central_widget)
        self.layout_principal.setContentsMargins(10, 10, 10, 10)  # Márgenes generales para todo el layout

        """ Agregar elementos de la ventana (widgets) """
        # Agregar espacio de ingreso de texto (88%)
        self.layout_principal.addWidget(self.window_widget())

        # Agregar Menus despeglables de idiomas
        self.layout_principal.addWidget(self.create_dropdown_menus())

        # Agregar controles de audio (10%)
        self.layout_principal.addWidget(self.init_audio_controls())

        # Agregar area de mensajes de estado (2%)
        self.layout_principal.addWidget(self.message_bg())

    def window_widget(self):
        # Crear el campo de texto con scrollbar (QTextEdit ya incluye un scrollbar por defecto)
        self.text_entry = QTextEdit(self)
        self.text_entry.setWordWrapMode(True)  # Habilitar ajuste de texto

        # Permitir que el QTextEdit se expanda dinámicamente
        self.text_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Agregar el QTextEdit al layout principal
        self.layout_principal.addWidget(self.text_entry)  # Cambiar 'self.layout()' por 'self.layout_principal'

        # Crear el menú contextual y configurarlo
        self.context_menu = QMenu(self)

        # Crear acciones y conectarlas a las funciones
        actions = {
            "Cortar": self.text_entry.cut,
            "Copiar": self.text_entry.copy,
            "Pegar": self.text_entry.paste,
            "Seleccionar todo": self.text_entry.selectAll
        }

        for name, slot in actions.items():
            self.context_menu.addAction(name, slot)

        # Asignar el menú contextual al campo de texto
        self.text_entry.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_entry.customContextMenuRequested.connect(lambda position: self.context_menu.exec_(self.text_entry.mapToGlobal(position)))

    def message_bg(self):
        # Crear un marco (QFrame) y etiqueta (QLabel) para el estado
        self.status_frame = QFrame(self)
        self.status_frame.setStyleSheet("background-color: white;")  # Establecer el color de fondo

        # Crear la etiqueta de estado
        self.status_label = QLabel("", self.status_frame)
        self.status_label.setStyleSheet("background-color: white;")  # Establecer el color de fondo

        # Crear un layout para el status_frame
        status_layout = QHBoxLayout(self.status_frame)
        status_layout.addWidget(self.status_label)

        # Asegurarse de que la etiqueta se expanda dentro del frame
        self.status_label.setAlignment(Qt.AlignCenter)

        # Añadir el marco de estado al layout principal (asumiendo que se pasa como parámetro)
        self.layout_principal.addWidget(self.status_frame)

    def create_dropdown_menus(self):
        """
        Función para crear los menús desplegables (idioma, país, género, estilo, voces)
        y añadirlos al layout de configuración.
        """
        # Crear un layout para los menús
        self.config_layout = QHBoxLayout()

        # Menú de idiomas
        self.language_menu = QComboBox(self)
        for idioma in self.idiomas:
            self.language_menu.addItem(idioma)
        self.language_menu.currentTextChanged.connect(self.update_country_menu)  # Actualizar al cambiar idioma
        self.config_layout.addWidget(self.language_menu)

        # Menú de países
        self.country_menu = QComboBox()
        self.country_menu.addItem("País")
        self.config_layout.addWidget(self.country_menu)

        # Menú de géneros
        self.gender_menu = QComboBox()
        self.gender_menu.addItem("Género")
        self.config_layout.addWidget(self.gender_menu)

        # Menú de estilos
        self.style_menu = QComboBox()
        self.style_menu.addItem("Estilo")
        self.config_layout.addWidget(self.style_menu)

        # Menú de voces
        self.voice_menu = QComboBox()
        self.voice_menu.addItem("Voces")
        self.config_layout.addWidget(self.voice_menu)

        # Añadir el layout de menús al layout principal
        self.layout_principal.addLayout(self.config_layout)

    def action_widgets(self):
        # Crear un layout para los menús de configuración
        config_layout = QHBoxLayout()

        # Menú para seleccionar el idioma (QComboBox en lugar de OptionMenu)
        self.language_menu = QComboBox(self)
        self.language_menu.addItems(self.idiomas)  # Utilizar la lista de idiomas importada
        self.language_menu.setCurrentText("Idioma")  # Establecer el valor por defecto
        config_layout.addWidget(self.language_menu)

        # Menú para seleccionar el país
        self.country_menu = QComboBox(self)
        self.country_menu.addItem("País")
        config_layout.addWidget(self.country_menu)

        # Menú para seleccionar el género
        self.gender_menu = QComboBox(self)
        self.gender_menu.addItem("Género")
        config_layout.addWidget(self.gender_menu)

        # Menú para seleccionar el estilo
        self.style_menu = QComboBox(self)
        self.style_menu.addItem("Estilo")
        config_layout.addWidget(self.style_menu)

        # Menú para seleccionar las voces
        self.voice_menu = QComboBox(self)
        self.voice_menu.addItem("Voces")
        config_layout.addWidget(self.voice_menu)

        # Añadir el layout de configuración al layout principal
        layout_principal().addLayout(config_layout)

        # Vincular los widgets al configurador (se utiliza .currentText() para obtener el valor seleccionado)
        self.audio_config.language_var = self.language_menu.currentText()
        self.audio_config.country_var = self.country_menu.currentText()
        self.audio_config.gender_var = self.gender_menu.currentText()
        self.audio_config.style_var = self.style_menu.currentText()
        self.audio_config.voice_var = self.voice_menu.currentText()

        # Vincular los menús al configurador (puedes llamar a tu método bind_widgets si es necesario)
        self.audio_config.bind_widgets(
            self.language_menu,
            self.country_menu,
            self.gender_menu,
            self.style_menu,
            self.voice_menu
        )

    def init_audio_controls(self):
        # Crear un QWidget para contener los botones de audio
        audio_controls_widget = QWidget(self)

        # Crear layout para los botones de audio
        self.audio_button_layout = QHBoxLayout(audio_controls_widget)

        # Botones para validar, convertir, reproducir y guardar audio
        self.verify_button = QPushButton("Validar Configuración")
        self.verify_button.clicked.connect(self.write_file_configuration)
        self.audio_button_layout.addWidget(self.verify_button)

        self.convert_button = QPushButton("Convertir a MP3")
        self.convert_button.clicked.connect(self.convert_text)
        self.convert_button.setEnabled(False)  # Deshabilitado por defecto
        self.audio_button_layout.addWidget(self.convert_button)

        self.play_button = QPushButton("Reproducir Audio")
        self.play_button.clicked.connect(self.play_audio)
        self.play_button.setEnabled(False)  # Deshabilitado por defecto
        self.audio_button_layout.addWidget(self.play_button)

        self.save_button = QPushButton("Guardar Audio")
        self.save_button.clicked.connect(self.save_audio)
        self.save_button.setEnabled(False)  # Deshabilitado por defecto
        self.audio_button_layout.addWidget(self.save_button)

        # Retornar el widget que contiene el layout
        return audio_controls_widget

    def write_file_configuration(self):
        from app.modules.audio.write_file_configuration import write_file_configuration

        # Deshabilitar el botón de verificación
        self.verify_button.setEnabled(False)

        try:
            # Llama a la función write_file_configuration del módulo
            write_file_configuration(self.audio_config, self.text_entry.toPlainText(),
                                     self.speed_scale.value(), self.pitch_scale.value(),
                                     self.status_label)
        except Exception as e:
            # Mostrar el error en un cuadro de diálogo
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText(str(e))
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
        finally:
            # Habilitar el botón de conversión y verificar
            self.convert_button.setEnabled(True)
            self.verify_button.setEnabled(True)
            show_status_message(self.status_label, "El archivo ha sido verificado exitosamente", "success")

    def convert_text(self):
        # Deshabilitar el botón de conversión
        self.convert_button.setEnabled(False)
        self.status_label.setText("Convirtiendo texto a audio...")

        try:
            # Llamar al método convert_text de AudioConfig
            self.status_label.setText("Convirtiendo texto a audio...")
            temp_file_path, error_message = self.audio_config.convert_text()

            if error_message:
                raise Exception(error_message)

            # Actualizar la ruta del archivo temporal y habilitar los botones de reproducción y guardado
            self.temp_file_path = temp_file_path
            self.play_button.setEnabled(True)
            self.save_button.setEnabled(True)
            self.status_label.setText("Conversión completada con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al convertir el texto a audio: {str(e)}")
        finally:
            # Habilitar el botón de conversión nuevamente, haya o no error
            self.convert_button.setEnabled(True)

    def play_audio(self):
        """Reproduce el archivo de audio temporal generado."""
        if self.temp_file_path:
            # Aquí puedes usar GStreamer para reproducir el audio
            self.player = Gst.ElementFactory.make("playbin", "player")
            self.player.set_property("uri", "file://" + self.temp_file_path)

            self.player.set_state(Gst.State.PLAYING)

            # Manejar el final de la reproducción
            bus = self.player.get_bus()
            bus.add_signal_watch()
            bus.connect("message", self.on_message)
        else:
            QMessageBox.critical(self, "Error", "No se encontró el archivo de audio.")

    def on_message(self, bus, message):
        """Maneja los mensajes del bus de GStreamer."""
        if message.type == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)

    def save_audio(self):
        """Función para guardar el archivo de audio."""
        if self.temp_file_path:
            try:
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo de audio", "",
                                                           "MP3 files (*.mp3);;All Files (*)", options=options)
                if file_name:
                    # Lógica para guardar el archivo, asumiendo que `save_file` está definida
                    save_file(self.temp_file_path, file_name)
                    self.status_label.setText("Archivo guardado exitosamente.")
                else:
                    self.status_label.setText("Operación de guardado cancelada.")
            except Exception as e:
                self.status_label.setText(f"Error al guardar el archivo: {str(e)}")
        else:
            QMessageBox.critical(self, "Error", "No hay ningún archivo de audio para guardar.")

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec_())
"""
# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
"""
