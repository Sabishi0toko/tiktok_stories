# app/modules/video/audio_duration.py

import os  
import subprocess
from app.utils.utils import get_tmp_dir

def get_audio_duration_ffmpeg(audio_path=None):
    """
    Obtiene la duración del archivo de audio usando ffmpeg en milisegundos.

    Args:
    - audio_path (str or None): Ruta del archivo de audio. Si no se proporciona, 
                                se usará el archivo 'final_audio.mp3' en el directorio temporal.

    Returns:
    - int: Duración del archivo de audio en milisegundos.
    """
    if audio_path is None:
        audio_path = get_tmp_dir() / 'final_audio.mp3'  # Archivo de audio predeterminado

    if not audio_path.exists():
        print("El archivo de audio no existe.")
        return -1

    try:
        # Ejecutar el comando de ffmpeg para obtener la duración en milisegundos
        result = subprocess.run(
            ["ffmpeg", "-i", str(audio_path), "-hide_banner"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Buscar la línea que contiene "Duration"
        for line in result.stdout.splitlines():
            if "Duration" in line:
                duration_str = line.split(",")[0].split("Duration: ")[1].strip()
                h, m, s = map(float, duration_str.split(":"))
                # Convertir a milisegundos
                duration_ms = int((h * 3600 + m * 60 + s) * 1000)
                return duration_ms

    except Exception as e:
        print(f"Error al obtener la duración del audio: {e}")
        return -1



