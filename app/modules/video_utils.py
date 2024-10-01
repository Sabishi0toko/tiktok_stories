# app/modules/audio_utils.py
import os
import time
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from app.utils.utils import get_tmp_dir, get_project_root, get_data_dir, get_projects_dir, write
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

""" Inicia GStreamer"""
Gst.init(None)

# Definir variables globales
player = None
current_video_path = None
current_audio_path = None

def initialize_player():
    """Inicializa el reproductor de GStreamer."""
    global player
    if player is None:
        player = Gst.ElementFactory.make("playbin", "player")
        if not player:
            raise Exception("No se pudo crear el reproductor.")


def load_audio():
    """Carga el archivo de audio."""
    global current_audio_path

    current_audio_path = get_tmp_dir() / 'final_audio.mp3'

    if os.path.exists(current_audio_path):
        print("Audio asociado al reproductor")
    else:
        print("Archivo de audio no encontrado.")


def load_video(video_frame):
    """Carga un archivo de video y muestra el primer fotograma."""
    global current_video_path

    project_root = get_project_root()
    video_dir = os.path.join(project_root, 'videos')

    video_path, _ = QFileDialog.getOpenFileName(None, "Seleccionar archivo de video", video_dir,
                                                "Video Files (*.mp4 *.avi *.mkv *.mov)")

    if video_path:
        current_video_path = video_path
        initialize_player()

        # Configurar la URI del video
        player.set_property("uri", "file://" + current_video_path)
        print(f"Video cargado: {video_path}")


def play_video_audio():
    """Reproduce el video y el audio simultáneamente."""
    global player

    if not current_video_path:
        QMessageBox.critical(None, "Error", "No se ha cargado ningún video.")
        return

    if not os.path.exists(get_tmp_dir() / 'final_audio.mp3'):
        QMessageBox.critical(None, "Error", "No se ha encontrado el archivo de audio temporal.")
        return

    initialize_player()

    # Asignar el audio
    set_audio()

    # Reproducir video y audio simultáneamente
    player.set_state(Gst.State.PLAYING)
    print("Reproduciendo video y audio...")


def set_audio():
    """Asigna el archivo de audio al reproductor."""
    global current_audio_path

    current_audio_path = get_tmp_dir() / 'final_audio.mp3'

    if os.path.exists(current_audio_path):
        player.set_property("uri", "file://" + str(current_audio_path))
        print("Audio asociado al reproductor")
    else:
        print("Archivo de audio no encontrado.")


def stop_video_audio():
    """Detiene la reproducción de video y audio."""
    global player

    if player:
        player.set_state(Gst.State.NULL)
    print("Video y audio detenidos")


def save_media():
    """Guarda el video y audio combinados."""
    save_dir = get_projects_dir()
    save_path, _ = QFileDialog.getSaveFileName(None, "Guardar archivo", save_dir, "MP4 files (*.mp4);;All files (*)")

    if save_path:
        print(f"Archivo guardado: {save_path}")

"""
# Definir variables globales
instance = None
player = None
audio_instance = None
audio_player = None
current_video_path = None
current_audio_path = None
media_player = vlc.MediaPlayer()

def initialize_player():
    #Inicializa los reproductores de VLC.
    global instance, player, audio_instance, audio_player
    if instance is None:
        instance = vlc.Instance()
    if player is None:
        player = instance.media_player_new()
    if audio_instance is None:
        audio_instance = vlc.Instance()
    if audio_player is None:
        audio_player = audio_instance.media_player_new()

def load_audio():
    Carga el archivo de audio y guarda la duración en 'audio_duration.txt'.
    global audio_player, audio_instance, current_audio_path

    # Obtener la duración del archivo de audio y guardarla
    import app.modules.video.audio_duration as audio_duration
    duration_ms = audio_duration.get_audio_duration_ffmpeg()
    
    if duration_ms != -1:
        write(get_data_dir() / 'audio_duration.txt', str(duration_ms))
        print(f"Duración del audio: {duration_ms} ms")
    else:
        print("No se pudo obtener la duración del audio.")
    
    # Asignar el archivo de audio al reproductor
    if audio_player is None:
        initialize_player()
    
    current_audio_path = get_tmp_dir() / 'final_audio.mp3'
    
    if os.path.exists(current_audio_path):
        audio_media = audio_instance.media_new(str(current_audio_path))
        audio_player.set_media(audio_media)
        print("Audio asociado al reproductor")
    else:
        print("Archivo de audio no encontrado.")

def load_video(video_frame):
    #Carga un archivo de video sin reproducir automáticamente y muestra el primer fotograma.
    global player, instance, current_video_path

    # Obtener la ruta del directorio del proyecto y apuntar al subdirectorio 'videos'
    project_root = get_project_root()
    video_dir = os.path.join(project_root, 'videos')

    # Seleccionar archivo de video (inicia en la carpeta 'video')
    video_path = filedialog.askopenfilename(initialdir=video_dir, filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov")])

    if video_path:
        current_video_path = video_path
        
        if player is None:
            initialize_player()
        
        # Crear la media y asignarla al media_player
        media = instance.media_new(current_video_path)
        player.set_media(media)
        
        # Configurar el área de visualización en el frame según el sistema operativo
        video_id = video_frame.winfo_id()
        if os.name == "nt":  # Para Windows
            player.set_hwnd(video_id)
        else:  # Para otros sistemas operativos
            player.set_xwindow(video_id)
        
        # Iniciar la reproducción para cargar el video
        player.play()
        
        # Esperar un poco para que el video se cargue
        time.sleep(1)
        
        try:
            # Intentar configurar la posición del video
            player.set_position(0.05)  # Configurar la posición al inicio del video (5% del video)
            print("Posición del video establecida en 5%")
        except Exception as e:
            print(f"Error al establecer la posición del video: {e}")

        # Pausar después de establecer la posición
        player.pause()
        print(f"Video cargado: {video_path}")

        # Verificar la duración del video
        duration = player.get_length() / 1000  # duración en segundos
        print(f"Duración del video: {duration} segundos")
        print(f"Posición actual: {player.get_position()}")  # Debe ser aproximadamente 0.05
def check_video_end():
    #Verifica si el video ha terminado y lo reinicia para reproducirlo en bucle.
    global player

    if player.get_state() == vlc.State.Ended:
        # Si el video ha terminado, reiniciarlo desde el principio
        player.set_position(0)
        player.play()
        print("Reiniciando video desde el inicio...")

    # Continuar revisando cada 500ms si el video ha terminado
    root.after(500, check_video_end)

def loop_video():
    #Reproduce el video en bucle acorde a la duración del audio.
    global player

    # Leer la duración del audio desde el archivo 'audio_duration.txt'
    duration_path = get_data_dir() / 'audio_duration.txt'
    if os.path.exists(duration_path):
        with open(duration_path, 'r') as f:
            duration_ms = int(f.read().strip())

        print(f"Reiniciando video en bucle durante {duration_ms} ms...")

        # Comenzar a reproducir el video
        player.set_position(0)
        player.play()

        # Iniciar la verificación continua del final del video
        check_video_end()
    else:
        print("No se encontró el archivo 'audio_duration.txt'.")

def play_video_audio():
    #Reproduce el video y el audio, y mantiene el video en bucle acorde a la duración del audio.
    global player, audio_player

    if not current_video_path:
        messagebox.showerror("Error", "No se ha cargado ningún video.")
        return

    if not os.path.exists(get_tmp_dir() / 'final_audio.mp3'):
        messagebox.showerror("Error", "No se ha encontrado el archivo de audio temporal.")
        return

    # Inicializar reproductores si no están inicializados
    initialize_player()

    # Asignar el audio
    set_audio()

    # Reproducir video y audio simultáneamente
    player.play()
    audio_player.play()

    print("Reproduciendo video y audio...")
    
    # Iniciar el bucle del video acorde a la duración del audio
    loop_video()

def set_audio():
    #Asigna el archivo de audio al reproductor.
    global audio_player, audio_instance, current_audio_path

    current_audio_path = get_tmp_dir() / 'final_audio.mp3'
    
    if os.path.exists(current_audio_path):
        audio_media = audio_instance.media_new(str(current_audio_path))
        audio_player.set_media(audio_media)
        print("Audio asociado al reproductor")
    else:
        print("Archivo de audio no encontrado.")

def stop_video_audio():
    #Detiene la reproducción de video y audio.
    global player, audio_player
    
    if player:
        player.stop()
    if audio_player:
        audio_player.stop()
    print("Video y audio detenidos")

def save_media():
    #Guarda el video y audio combinados.
    # Usar 'get_projects_dir' para iniciar el diálogo de guardado en la carpeta de proyectos
    save_dir = get_projects_dir()
    save_path = filedialog.asksaveasfilename(initialdir=save_dir, defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    
    if save_path:
        print(f"Archivo guardado: {save_path}")
"""
