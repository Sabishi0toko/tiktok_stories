# app/modules/audio_utils.py

import os
import tempfile
import json
import shutil
import subprocess
from PyQt5.QtWidgets import QComboBox, QLabel, QMessageBox
#from app.utils.utils import get_tmp_dir

from app.config.credentials import Credentials
from google.cloud import texttospeech
from pydub import AudioSegment
import math
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

class AudioConfig:
    def __init__(self):
        # Reemplazamos StringVar por QComboBox o QLineEdit
        self.language_var = QComboBox()  # Lista desplegable
        self.country_var = QComboBox()
        self.gender_var = QComboBox()
        self.style_var = QComboBox()
        self.voice_var = QComboBox()

        self.country_map = {}
        self.gender_map = {}
        self.style_map = {}
        self.voices_map = {}

        # Configuración de las credenciales y cliente
        #self.credentials_config = Credentials()
    """"
        if not self.credentials_config.client:
            # Reemplazamos messagebox.showerror con QMessageBox
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("No se pudieron cargar las credenciales.")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()

            # Si hay una raíz o ventana, podemos cerrar la aplicación
            if hasattr(self, 'root'):
                self.root.close()  # PyQt usa close() para cerrar la ventana
            return

        self.client = self.credentials_config.client
    """
    def update_country_options(self):
        # Obtener el idioma seleccionado
        selected_language = self.language_var.currentText()  # En QComboBox usamos currentText() para obtener el valor

        # Importar dinámicamente el módulo del idioma seleccionado
        try:
            lang_module = __import__(f'lang.{selected_language}', fromlist=['country_map', 'gender_map', 'style_map', 'voices_map'])
        except ImportError:
            print(f"Error: No se pudo cargar el módulo para el idioma '{selected_language}'.")
            return

        # Actualizar los diccionarios con los datos del módulo importado
        self.country_map = lang_module.country_map
        self.gender_map = lang_module.gender_map
        self.style_map = lang_module.style_map
        self.voices_map = lang_module.voices_map

        # Actualizar el menú de países
        country_options = list(self.country_map.keys())
        self.country_var.clear()  # Limpiamos las opciones existentes en QComboBox

        for country in country_options:
            self.country_var.addItem(country)  # Agregamos los países al QComboBox

        # Mantener el texto predeterminado
        self.country_var.setCurrentText("País")
        self.update_gender_options()

    def update_gender_options(self):
        country = self.country_var.currentText()  # Usamos currentText() para obtener el valor seleccionado en el QComboBox
        gender_options = list(self.gender_map.keys())

        # Actualizar el menú de género
        self.gender_var.clear()  # Limpiar las opciones anteriores en QComboBox

        for gender in gender_options:
            self.gender_var.addItem(gender)  # Agregar las opciones de género al QComboBox

        # Mantener el texto Predeterminado
        self.gender_var.setCurrentText("Género")
        self.update_style_options()

    def update_style_options(self):
        """
        Actualiza las opciones de estilo de voz disponibles según el género seleccionado.
        """
        country = self.country_var.currentText()  # Obtener el país seleccionado
        gender = self.gender_var.currentText()     # Obtener el género seleccionado
        style_options = []

        if country and gender:
            style_options = list(self.voices_map[self.country_map[country]][self.gender_map[gender]].keys())

        # Actualizar el menú de opciones de estilo
        self.style_var.clear()  # Limpiar las opciones anteriores en QComboBox

        for style in style_options:
            self.style_var.addItem(style)  # Agregar las nuevas opciones de estilo al QComboBox

        # Mantener el texto predeterminado
        self.style_var.setCurrentText("Estilo")
        self.update_voice_options()

    def update_voice_options(self):
        """
        Actualiza las opciones de voz disponibles según el estilo de voz seleccionado.
        """
        country = self.country_var.currentText()  # Obtener el país seleccionado
        gender = self.gender_var.currentText()     # Obtener el género seleccionado
        style = self.style_var.currentText()       # Obtener el estilo seleccionado
        voice_options = []

        if country and gender and style:
            voice_options = list(self.voices_map[self.country_map[country]][self.gender_map[gender]][style].keys())

        # Actualizar el menú de opciones de voz
        self.voice_var.clear()  # Limpiar las opciones anteriores en QComboBox

        for voice in voice_options:
            self.voice_var.addItem(voice)  # Agregar las nuevas opciones de voz al QComboBox

        # Mantener el texto predeterminado
        self.voice_var.setCurrentText("Voces")

    def bind_widgets(self, language_menu, country_menu, gender_menu, style_menu, voice_menu):
        # Vincular widgets al configurador
        self.language_menu = language_menu
        self.country_menu = country_menu
        self.gender_menu = gender_menu
        self.style_menu = style_menu
        self.voice_menu = voice_menu

        # Conectar señales a las funciones de actualización
        self.language_menu.currentIndexChanged.connect(self.update_country_options)
        self.country_menu.currentIndexChanged.connect(self.update_gender_options)
        self.gender_menu.currentIndexChanged.connect(self.update_style_options)
        self.style_menu.currentIndexChanged.connect(self.update_voice_options)

    def get_voice_configuration(self):
        # Obtener la configuración seleccionada
        country_code = self.country_map.get(self.country_var.get(), 'es-ES')
        gender = self.gender_map.get(self.gender_var.get(), 'MALE')
        style = self.style_var.get()
        voice_key = self.voice_var.get()

        # Validar que todas las opciones estén seleccionadas
        if not all([country_code, gender, style, voice_key]):
            error_message = "Por favor, complete todas las opciones de configuración."
            return None, error_message

        try:
            # Obtener el directorio temporal donde se almacenarán los archivos temporales
            temp_dir = get_tmp_dir()

            # Configurar el nombre de la voz a partir de las opciones seleccionadas
            voice_config = self.voices_map[country_code][gender]
            voice_name = f"{country_code}-{style}{voice_config[style][voice_key]}"
            country_id = f"{country_code}"
            gender_mf = f"{gender}"

        except KeyError as e:
            # Manejar el caso en que una clave no se encuentra en el diccionario
            error_message = f"Error en la configuración de la voz: {e}"
            return None, error_message

        return voice_name, country_id, gender_mf, None

    def convert_text(self):
        # Definir el límite de caracteres por solicitud
        CHAR_LIMIT = 4500  # Un poco menos de 5000 para seguridad

        # Obtener el directorio del archivo actual (audio.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Subir dos niveles al directorio 'text2speech/'
        parent_dir = os.path.dirname(os.path.dirname(current_dir))

        # Definir las rutas de los archivos en 'data/'
        data_dir = os.path.join(parent_dir, 'data')
        text_file_path = os.path.join(data_dir, 'text_for_user.txt')
        voice_file_path = os.path.join(data_dir, 'voice_config.txt')
        country_id_file_path = os.path.join(data_dir, 'country_code.txt')
        gender_mf_file_path = os.path.join(data_dir, 'gender.txt')
        speed_file_path = os.path.join(data_dir, 'speed.txt')
        pitch_file_path = os.path.join(data_dir, 'pitch.txt')  # Archivo para el pitch

        try:
            # Obtener el directorio temporal donde se almacenarán los archivos temporales
            temp_dir = get_tmp_dir()  # <-- Aquí definimos temp_dir

            # Leer el texto
            with open(text_file_path, 'r', encoding='utf-8') as file:
                text = file.read().strip()

            # Leer la configuración de voz
            with open(voice_file_path, 'r', encoding='utf-8') as file:
                voice_name = file.read().strip()

            # Leer el código de país (idioma)
            with open(country_id_file_path, 'r', encoding='utf-8') as file:
                country_id = file.read().strip()

            # Leer el género
            with open(gender_mf_file_path, 'r', encoding='utf-8') as file:
                gender_mf = file.read().strip()

            with open(speed_file_path, 'r', encoding='utf-8') as file:
                self.speaking_rate = float(file.read().strip())

            # Leer el pitch (tono)
            with open(pitch_file_path, 'r', encoding='utf-8') as file:
                self.speaking_pitch = int(file.read().strip())  # El pitch lo obtenemos como entero

            # Validar que los archivos no estén vacíos
            if not text:
                raise ValueError("El archivo 'text_for_user.txt' está vacío.")

            if not voice_name:
                raise ValueError("El archivo 'voice_config.txt' está vacío.")

            # Configurar parámetros de voz
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=country_id,
                name=voice_name,
                ssml_gender=texttospeech.SsmlVoiceGender[gender_mf.upper()]  # Usar el género
            )

            # Configurar el audio, incluyendo el speaking_rate y el pitch
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=self.speaking_rate,  # Usar la velocidad obtenida
                pitch=self.speaking_pitch / 100.0  # Google TTS requiere un valor flotante (factor de ajuste)
            )

            # Dividir el texto en fragmentos
            text_chunks = self.split_text_into_chunks(text, CHAR_LIMIT)

            audio_segments = []

            for idx, chunk in enumerate(text_chunks):
                print(f"Sintetizando fragmento {idx + 1}/{len(text_chunks)}")

                # Crear una cadena SSML con la etiqueta <prosody> para ajustar tono y velocidad
                ssml_text = f'<speak><prosody rate="{self.speaking_rate}" pitch="{self.speaking_pitch}Hz">{chunk}</prosody></speak>'
                input_text = texttospeech.SynthesisInput(ssml=ssml_text)

                # Realizar la síntesis de voz
                response = self.client.synthesize_speech(input=input_text, voice=voice_params,
                                                         audio_config=audio_config)

                # Guardar cada fragmento en un archivo temporal en el directorio 'tmp/'
                temp_file_path = os.path.join(temp_dir, f"temp_audio_{idx}.mp3")
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(response.audio_content)
                    audio_segments.append(AudioSegment.from_file(temp_file_path, format='mp3'))
                    print(f"Fragmento {idx + 1} guardado en {temp_file_path}")

            # Combinar todos los fragmentos en un solo archivo de audio
            combined = AudioSegment.empty()
            for segment in audio_segments:
                combined += segment

            # Guardar el audio combinado en un archivo temporal final en el directorio 'tmp/'
            final_temp_file_path = os.path.join(temp_dir, "final_audio.mp3")
            combined.export(final_temp_file_path, format="mp3")

            print(f"Audio combinado guardado en {final_temp_file_path}")
            return final_temp_file_path, None

        except Exception as e:
            print(f"Error al convertir el texto: {e}")
            return None, str(e)

def split_text_into_chunks(self, text, max_length):
    """
    Divide el texto en fragmentos que no excedan max_length caracteres.
    Preferiblemente, divide por oraciones.
    """
    import re

    # Utilizar expresiones regulares para dividir el texto en oraciones
    sentence_endings = re.compile(r'([.!?])')
    sentences = sentence_endings.split(text)
    chunks = []
    current_chunk = ""

    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i].strip()
        ending = sentences[i + 1].strip()  # Agregar strip() aquí para limpiar espacios
        full_sentence = sentence + ending + " "

        if len(current_chunk) + len(full_sentence) > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = full_sentence
            else:
                # La oración es más larga que el límite, se divide a la mitad
                for j in range(0, len(full_sentence), max_length):
                    chunks.append(full_sentence[j:j + max_length])
        else:
            current_chunk += full_sentence

    # Añadir la última parte del texto
    if len(sentences) % 2 != 0:
        last_part = sentences[-1].strip()
        if last_part:
            if len(current_chunk) + len(last_part) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = last_part
                else:
                    for j in range(0, len(last_part), max_length):
                        chunks.append(last_part[j:j + max_length])
            else:
                current_chunk += last_part

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
