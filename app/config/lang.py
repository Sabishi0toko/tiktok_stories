# app/config/lang.py
import os

class Language:
    def __init__(self, lang):
        self.lang = lang
        
    def get_lang(self):
        # Obtener la ruta absoluta del directorio de la aplicación
        lang_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Ruta del directorio de idiomas
        lang_path = os.path.join(lang_dir, self.lang)
        
        # Comprobar si el directorio existe
        if not os.path.exists(lang_path):
            raise FileNotFoundError(f"El directorio de idiomas no se encontró en la ruta {lang_path}")

        try:
            # Obtener la lista de elementos en el directorio de idiomas
            elementos = os.listdir(lang_path)
            
            # Filtrar solo los archivos .py, excluyendo aquellos que contienen __ en ambos extremos
            files_py = [
                archivo[:-3] for archivo in elementos  # Quitamos el ".py" del nombre
                if archivo.endswith('.py') and
                not archivo.startswith('__') and
                not ('__' in archivo and archivo.endswith('.py'))
            ]
            
            return files_py
        except PermissionError:
            return f"No tienes permiso para acceder al directorio '{lang_path}'."

import os

def generate_languages_file():
    lang_instance = Language('lang')
    lang_list = lang_instance.get_lang()
    
    # Ruta del archivo a crear
    # Obtener la ruta del directorio 'text2speech/data'
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
    
    # Ruta del archivo a crear en 'text2speech/data'
    file_path = os.path.join(data_dir, 'languages.py')
    
    try:
        with open(file_path, 'w') as file:
            file.write("LANGUAGES = [\n")
            for lang in lang_list:
                file.write(f"    '{lang}',  # Comentario para {lang}\n")
            file.write("]\n\n")
            
            # Agregar la función languages_get al final del archivo
            file.write("def languages_get():\n")
            file.write("    return LANGUAGES\n")
            
        print(f"Archivo 'languages.py' creado exitosamente en {file_path}")
    except Exception as e:
        print(f"Error al crear el archivo 'languages.py': {e}")
