# start.py
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from app.utils.utils import get_project_root  # Importar la función para obtener la raíz del proyecto
from app.config.credentials import OAuthCredentialsConfig
from PyQt5.QtWidgets import QMessageBox
# Deshabilitar el uso de MIT-SHM y forzar backend de software

os.environ["QT_X11_NO_MITSHM"] = "1"
os.environ["QT_QUICK_BACKEND"] = "software"

# Obtener la ruta raíz del proyecto
project_root = get_project_root()

# Combinar la ruta raíz con la ruta de la imagen
image_path = os.path.join(project_root, 'includes', 'images', 'fondo.jpg')

def start_credentials_flow():
    creds_config = OAuthCredentialsConfig()

    if os.path.exists(creds_config.token_path):
        use_token = QMessageBox.question(None, "Token existente",
                                         "Ya existe un token guardado. ¿Desea usar el token guardado?",
                                         QMessageBox.Yes | QMessageBox.No)
        if use_token == QMessageBox.Yes:
            print("Usando el token guardado...")
        else:
            print("Seleccionando nuevas credenciales...")
            creds_config.auth_flow()
    else:
        print("No se encontró token, seleccionando nuevas credenciales...")
        creds_config.auth_flow()

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")

        # Eliminar la barra de título
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Bloquear el tamaño de la ventana a 600x400
        self.setFixedSize(600, 400)

        # Centrar la ventana
        self.center_window()

        # Cargar la imagen y aplicarla como fondo
        self.load_background_image(image_path)

        # Crear botones directamente en la ventana principal
        self.create_buttons()

    def center_window(self):
        # Obtener las dimensiones de la pantalla
        screen_rect = self.frameGeometry()
        screen_center = QApplication.desktop().availableGeometry().center()
        screen_rect.moveCenter(screen_center)
        self.move(screen_rect.topLeft())

    def load_background_image(self, image_path):
        try:
            # Crear una etiqueta para la imagen de fondo
            self.background_label = QLabel(self)
            pixmap = QPixmap(image_path).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)
            
            # Ajustar la etiqueta para ocupar todo el espacio disponible
            self.background_label.setGeometry(self.rect())
            self.background_label.raise_()  # Asegura que la etiqueta esté detrás de otros widgets

        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")

    def create_buttons(self):
        # Crear un layout
        layout = QVBoxLayout(self)

        # Botón AUDIO
        self.button1 = QPushButton("AUDIO")
        self.button1.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: red; /* Color del texto */
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px; 
                font-weight: bold;
                font-family: Arial, sans-serif;
            }
            QPushButton:hover {
                background-color: #45a049;
                color: blue;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
                color: yellow;
            }
        """)
        self.button1.setFixedSize(200, 50)  # Ajustar tamaño del botón
        self.button1.setCursor(Qt.PointingHandCursor)  # Cambiar a mano al pasar el mouse
        self.button1.clicked.connect(self.button1_action)
        layout.addWidget(self.button1)

        # Alinear el layout al centro
        layout.setAlignment(Qt.AlignCenter)

        # Establecer el layout
        self.setLayout(layout)

    def button1_action(self):
        # Cerrar la ventana actual
        self.hide()

        # Importar y ejecutar la aplicación de gui.py
        from app.gui import TextToSpeechApp
        self.new_app = TextToSpeechApp()
        self.new_app.show()

if __name__ == "__main__":
    app = QApplication([])
    main_app = MainApp()
    main_app.show()
    app.exec_()
