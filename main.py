# main.py

from PyQt5.QtWidgets import QApplication
from start import MainApp

if __name__ == "__main__":
    # Crear una instancia de la aplicación PyQt
    app = QApplication([])
    
    # Inicializar la interfaz principal
    window = MainApp()
    window.show()
    
    # Iniciar el bucle de la aplicación
    app.exec_()
