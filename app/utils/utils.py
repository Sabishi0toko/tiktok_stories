# app/utils/utils.py
import os
import sys
import shutil
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

def get_project_root() -> Path:
    """
    Obtiene la ruta del directorio raíz del proyecto.
    Si es un ejecutable (.exe), ajusta la ruta apropiadamente.
    """
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)  # PyInstaller usa _MEIPASS como el directorio temporal del ejecutable
    else:
        return Path(__file__).resolve().parents[2]

def get_data_dir() -> Path:
    """
    Retorna la ruta del directorio 'data/' dentro del proyecto.
    """
    project_root = get_project_root()
    data_dir = project_root / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_projects_dir() -> Path:
    """
    Retorna la ruta del directorio 'data/' dentro del proyecto.
    """
    project_root = get_project_root()
    projects_dir = project_root / 'Proyectos'
    projects_dir.mkdir(parents=True, exist_ok=True)
    return projects_dir

def get_tmp_dir() -> Path:
    """
    Retorna la ruta del directorio 'tmp/' dentro del proyecto.
    Crea el directorio si no existe.
    """
    project_root = get_project_root()
    tmp_dir = project_root / 'tmp'
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir

def get_save_dir() -> Path:
    """
    Retorna la ruta del directorio 'tmp/' dentro del proyecto.
    Crea el directorio si no existe.
    """
    project_root = get_project_root()
    save_dir = project_root / 'Proyectos'
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir

def save_file(temp_file_name, dest_dir, file_types=[("Todos los archivos", "*.*")], default_extension=""):
    """
    Función genérica para guardar un archivo en una ubicación seleccionada por el usuario.

    Args:
    - temp_file_name (str): El nombre del archivo temporal a guardar.
    - dest_dir (Path): Directorio destino donde se guardará el archivo.
    - file_types (list): Tipos de archivos permitidos para guardar. Ej: [("MP3 files", "*.mp3"), ("Text files", "*.txt")].
    - default_extension (str): Extensión predeterminada para el archivo guardado, ej: ".mp3", ".txt".
    
    Returns:
    - str: Mensaje de éxito si el archivo se guarda correctamente.
    """
    temp_file_path = get_tmp_dir() / temp_file_name

    if not temp_file_path.exists():
        raise Exception(f"No hay ningún archivo temporal '{temp_file_name}' para guardar.")

    # Mostrar el diálogo para seleccionar la ubicación de guardado
    file_path = filedialog.asksaveasfilename(initialdir=dest_dir, defaultextension=default_extension, filetypes=file_types)
    
    if file_path:
        try:
            shutil.copy(temp_file_path, file_path)
            QMessageBox.Information(None, "Guardado", f"Archivo guardado en {file_path}")
            return f"Archivo guardado en {file_path}"
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al guardar el archivo: {e}")
            raise e
    return None


def play(file_name=None, is_audio=True):
    """
    Reproduce un archivo de audio o video.

    Args:
    - file_name (str or None): El nombre del archivo a reproducir. Si es None, se pedirá seleccionar un archivo de video.
    - is_audio (bool): Indica si se está reproduciendo un archivo de audio (True) o video (False).

    """
    if is_audio:
        # Reproducir el archivo de audio desde la carpeta temporal
        temp_audio_path = get_tmp_dir() / 'final_audio.mp3'
        
        if temp_audio_path.exists():
            try:
                # Crear un pipeline de GStreamer
                pipeline = Gst.parse_launch(f"playbin uri=file://{str(temp_audio_path)}")
                pipeline.set_state(Gst.State.PLAYING)
                print("Reproduciendo audio...")
            except Exception as e:
                print(f"Error al intentar reproducir el audio: {e}")
                messagebox.showerror("Error", f"Error al intentar reproducir el archivo de audio: {e}")
        else:
            print("No se encontró el archivo de audio.")

def play(file_name=None, is_audio=True):
    """
    Reproduce un archivo de audio o video usando GStreamer.

    Args:
    - file_name (str or None): El nombre del archivo a reproducir. Si es None, se pedirá seleccionar un archivo.
    - is_audio (bool): Indica si se está reproduciendo un archivo de audio (True) o video (False).
    """
    if is_audio:
        # Reproducir el archivo de audio desde la carpeta temporal
        temp_audio_path = get_tmp_dir() / 'final_audio.mp3'
        
        if temp_audio_path.exists():
            try:
                # Crear un pipeline de GStreamer
                pipeline = Gst.parse_launch(f"playbin uri=file://{str(temp_audio_path)}")
                pipeline.set_state(Gst.State.PLAYING)
                print("Reproduciendo audio...")
            except Exception as e:
                print(f"Error al intentar reproducir el audio: {e}")
                QMessageBox.critical(None, "Error", f"Error al intentar reproducir el archivo de audio: {e}")
        else:
            print("No se encontró el archivo de audio.")
            QMessageBox.critical(None, "Error", "No se encontró el archivo de audio temporal.")
    else:
        if not file_name:
            # Seleccionar un archivo de video
            file_name, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo de video", "", "Video files (*.mp4 *.avi *.mov *.mkv)")

        if file_name:
            try:
                # Crear un pipeline de GStreamer para video
                pipeline = Gst.parse_launch(f"playbin uri=file://{str(file_name)}")
                pipeline.set_state(Gst.State.PLAYING)
                print("Reproduciendo video...")
            except Exception as e:
                print(f"Error al intentar reproducir el video: {e}")
                QMessageBox.critical(None, "Error", f"Error al intentar reproducir el archivo de video: {e}")
        else:
            print("No se seleccionó ningún archivo de video.")
            QMessageBox.critical(None, "Error", "No se seleccionó ningún archivo de video.")

def write(file_name, data):
    """
    Guarda datos en un archivo en el directorio 'data/'.
    """
    try:
        # Obtener el directorio 'data/' dentro del proyecto
        data_dir = get_data_dir()

        # Definir la ruta completa del archivo en el directorio 'data/'
        file_path = data_dir / file_name

        # Escribir los datos en el archivo
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)
        
        print(f"Archivo '{file_name}' creado/actualizado exitosamente en {file_path}")

    except Exception as e:
        print(f"Error al guardar el archivo '{file_name}': {e}")

