# app/config/credentials.py
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from app.utils.utils import get_project_root


class OAuthCredentialsConfig:
    def __init__(self):
        print("Inicializando OAuthCredentialsConfig...")
        self.root_path = os.path.join(get_project_root(), 'credentials')
        self.ensure_credentials_dir()

        self.credentials_path = None
        self.token_path = os.path.join(self.root_path, 'token.json')
        self.creds = None
        self.scopes = ['https://www.googleapis.com/auth/cloud-platform']

        # Verificar y cargar credenciales/token
        self.check_token_and_auth()

    def ensure_credentials_dir(self):
        """Crea el directorio de credenciales si no existe."""
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
            print(f"Directorio de credenciales creado: {self.root_path}")

    def check_token_and_auth(self):
        """Verifica si existe un token válido, si no, inicia el flujo OAuth."""
        if os.path.exists(self.token_path):
            print("Token existente encontrado, cargándolo...")
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)

            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("El token ha expirado, intentando refrescarlo...")
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"Error al refrescar el token: {e}")
            elif not self.creds or not self.creds.valid:
                print("El token no es válido, iniciando flujo OAuth.")
                self.auth_flow()
        else:
            print("No se encontró un token, iniciando flujo OAuth.")
            self.auth_flow()

        # Guardar token si se generó
        if self.creds:
            self.save_token()

    def auth_flow(self):
        """Inicia el flujo OAuth 2.0 para obtener nuevas credenciales."""
        if not self.credentials_path or not os.path.exists(self.credentials_path):
            print("No se encontró archivo de credenciales, solicitando selección.")
            self.credentials_path = self.ask_for_credentials()

        flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.scopes)
        self.creds = flow.run_local_server(port=0)

    def ask_for_credentials(self):
        """Solicita al usuario seleccionar el archivo de credenciales de OAuth."""
        options = QFileDialog.Options()
        credentials_file, _ = QFileDialog.getOpenFileName(None, "Seleccione el archivo de credenciales de OAuth", "",
                                                          "JSON Files (*.json);;All Files (*)", options=options)
        if not credentials_file:
            QMessageBox.critical(None, "Error", "No se seleccionó un archivo de credenciales.")
            return None
        return credentials_file

    def save_token(self):
        """Guarda el token OAuth en el directorio de credenciales."""
        if self.creds:
            try:
                with open(self.token_path, 'w') as token_file:
                    token_data = {
                        'token': self.creds.token,
                        'refresh_token': self.creds.refresh_token,
                        'token_uri': self.creds.token_uri,
                        'client_id': self.creds.client_id,
                        'client_secret': self.creds.client_secret,
                        'scopes': self.creds.scopes
                    }
                    json.dump(token_data, token_file)
                    print(f"Token guardado en {self.token_path}")
            except Exception as e:
                print(f"Error al guardar el token: {e}")

