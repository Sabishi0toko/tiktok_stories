+--------------------------------------+
|                                      |
|                tittle_story()       |  (25% sobre menu_options)
|                                      |
+--------------------------------------+
|                                      |
|               menu_options()        |  (10% sobre action_buttons)
|                                      |
+--------------------------------------+
|                                      |
|               action_buttons()       |  (10% sobre messages_bg)
|                                      |
+--------------------------------------+
|                                      |
|               messages_bg()          |  (3% de la parte inferior)
|                                      |
+--------------------------------------+
|                                      |
|               right_buttons()        |  (20% del lado derecho)
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
|                                      |
|               window_widget()        |  (Resto de la pantalla)
|                                      |
+--------------------------------------+




    def init_video_controls(self, layout_principal):
        """
        Configurar los controles de video y añadirlos al layout principal.
        """
        # Crear layout para los botones de video
        self.video_button_layout = QHBoxLayout()

        self.load_video_button = QPushButton("Cargar Video")
        self.load_video_button.clicked.connect(self.load_video)
        self.video_button_layout.addWidget(self.load_video_button)

        self.load_audio_button = QPushButton("Cargar Audio")
        self.load_audio_button.clicked.connect(self.load_audio)
        self.video_button_layout.addWidget(self.load_audio_button)

        self.play_video_audio_button = QPushButton("Reproducir")
        self.play_video_audio_button.clicked.connect(self.play_video_audio)
        self.video_button_layout.addWidget(self.play_video_audio_button)

        self.stop_video_audio_button = QPushButton("Detener")
        self.stop_video_audio_button.clicked.connect(self.stop_video_audio)
        self.video_button_layout.addWidget(self.stop_video_audio_button)

        # Botón para agregar subtítulos
        self.add_subtitles_button = QPushButton("Agregar Subtítulos")
        self.add_subtitles_button.clicked.connect(self.add_subtitles)
        self.video_button_layout.addWidget(self.add_subtitles_button)

        # Añadir los controles de video al layout principal
        layout_principal.addLayout(self.video_button_layout)


    def init_video_controls(self, layout_principal):
        # Crear layout para botones de video
        self.video_button_layout = QHBoxLayout()

        # Botones para cargar y reproducir video
        self.load_video_button = QPushButton("Cargar Video")
        self.load_video_button.clicked.connect(self.load_video)
        self.video_button_layout.addWidget(self.load_video_button)

        self.load_audio_button = QPushButton("Cargar Audio")
        self.load_audio_button.clicked.connect(self.load_audio)
        self.video_button_layout.addWidget(self.load_audio_button)

        self.play_video_audio_button = QPushButton("Reproducir")
        self.play_video_audio_button.clicked.connect(self.play_video_audio)
        self.video_button_layout.addWidget(self.play_video_audio_button)

        self.stop_video_audio_button = QPushButton("Detener")
        self.stop_video_audio_button.clicked.connect(self.stop_video_audio)
        self.video_button_layout.addWidget(self.stop_video_audio_button)

        # Botón para agregar subtítulos
        self.add_subtitles_button = QPushButton("Agregar Subtítulos")
        self.add_subtitles_button.clicked.connect(self.add_subtitles)
        self.video_button_layout.addWidget(self.add_subtitles_button)

        # Agregar los botones al layout principal
        layout_principal.addLayout(self.video_button_layout)
    """

        # Crear el marco para el video
        self.setup_video_frame()

        # Configurar la interfaz gráfica
        self.setup_grid()
        self.window_widget()
        self.message_bg()
        self.action_widgets()
        self.button_action()
        self.action_scale()
        self.button_action_videos()
        self.hide_video_buttons()

    def center_window(self):
        # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular posición para centrar
        x_coordinate = int((screen_width / 2) - (800 / 2))
        y_coordinate = int((screen_height / 2) - (600 / 2))

        # Posicionar la ventana
        self.root.geometry(f"800x600+{x_coordinate}+{y_coordinate}")

    def setup_grid(self):
        # Configurar filas
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0, minsize=50)
        self.root.grid_rowconfigure(2, minsize=50)
        self.root.grid_rowconfigure(3, minsize=50)
        self.root.grid_rowconfigure(4, minsize=50)

        # Configurar columnas
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0, minsize=50)  # Marco de botones derecha

        # Crear el marco para los menús de configuración (solo ubicación)
        self.config_frame = tk.Frame(self.root)
        self.config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Crear el marco para los botones (solo la ubicación)
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Crear el marco para los ajustes (solo la ubicación)
        self.adjustment_frame = tk.Frame(self.root)
        self.adjustment_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.adjustment_frame.grid_rowconfigure(0, weight=1)
        self.adjustment_frame.grid_columnconfigure(0, weight=1)
        self.adjustment_frame.grid_columnconfigure(1, weight=1)  # Para la escala de pitch

        # Crear un marco para los botones al lado derecho del campo de texto
        self.right_button_frame = tk.Frame(self.root)
        self.right_button_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=5, sticky="ns")

        # Asegurarse de que las columnas del config_frame se expandan uniformemente
        for i in range(5):
            self.config_frame.grid_columnconfigure(i, weight=1)

    def hide_audio_buttons(self):
        self.language_menu.grid_forget()
        self.country_menu.grid_forget()
        self.gender_menu.grid_forget()
        self.style_menu.grid_forget()
        self.voice_menu.grid_forget()
        self.speed_scale.grid_forget()
        self.pitch_scale.grid_forget()
        self.verify_button.grid_forget()
        self.convert_button.grid_forget()
        self.play_button.grid_forget()
        self.save_button.grid_forget()
        self.phoneme_button.grid_forget()
        self.say_as_button.grid_forget()
        self.sub_alias_button.grid_forget()
        self.emphasis_button.grid_forget()
        self.audio_button.grid_forget()
        self.voice_button.grid_forget()
        self.text_frame.grid_forget() 

    def show_audio_buttons(self):
        self.hide_video_buttons()
        self.text_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew") 
        self.language_menu.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.country_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.gender_menu.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.style_menu.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.voice_menu.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        self.speed_scale.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.pitch_scale.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.verify_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.convert_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.play_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.save_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.phoneme_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.say_as_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.sub_alias_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.emphasis_button.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.audio_button.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.voice_button.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

    def hide_video_buttons(self):
        self.load_video_button.grid_forget()
        self.load_audio_button.grid_forget()
        self.play_video_audio_button.grid_forget()
        self.stop_video_audio_button.grid_forget()
        self.save_media_button.grid_forget()

    def show_video_buttons(self):
        self.hide_audio_buttons()
        self.load_video_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.load_audio_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.play_video_audio_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.stop_video_audio_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.save_media_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        self.add_subtitles_button.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
    """


    """
    def action_widgets(self):
        # Menú para seleccionar el idioma
        self.language_var = tk.StringVar(value='Idioma')
        self.language_menu = tk.OptionMenu(
                self.config_frame,
                self.language_var,
                *self.idiomas  # Utilizar la lista de idiomas importada
                )
        self.language_menu.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Menú para seleccionar el país
        self.country_var = tk.StringVar(value='País')
        self.country_menu = tk.OptionMenu(
                self.config_frame,
                self.country_var,
                "País"
                )
        self.country_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Menú para seleccionar el género
        self.gender_var = tk.StringVar(value='Género')
        self.gender_menu = tk.OptionMenu(
                self.config_frame,
                self.gender_var,
                "Género"
                )
        self.gender_menu.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Menú para seleccionar el estilo
        self.style_var = tk.StringVar(value='Estilo')
        self.style_menu = tk.OptionMenu(
                self.config_frame,
                self.style_var,
                "Estilo"
                )
        self.style_menu.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Menú para seleccionar las voces
        self.voice_var = tk.StringVar(value='Voces')
        self.voice_menu = tk.OptionMenu(
                self.config_frame,
                self.voice_var,
                "Voces"
                )
        self.voice_menu.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Vincular los widgets al configurador
        self.audio_config.language_var = self.language_var
        self.audio_config.country_var = self.country_var
        self.audio_config.gender_var = self.gender_var
        self.audio_config.style_var = self.style_var
        self.audio_config.voice_var = self.voice_var

        # Vincular los menús al configurador
        self.audio_config.bind_widgets(
                self.language_menu, 
                self.country_menu, 
                self.gender_menu, 
                self.style_menu, 
                self.voice_menu
                )
    """

    def action_scale(self):
        # Crear un layout para los sliders de velocidad y tono
        adjustment_layout = QHBoxLayout()

        # Escala para ajustar la velocidad del habla (QSlider en lugar de tk.Scale)
        self.speed_label = QLabel("Velocidad de Voz")
        adjustment_layout.addWidget(self.speed_label)

        self.speed_scale = QSlider(Qt.Horizontal, self)
        self.speed_scale.setRange(25, 200)  # Mapeamos el rango de 0.25 a 2.0 en valores enteros (25 a 200)
        self.speed_scale.setSingleStep(5)  # Equivalente a resolución 0.05
        self.speed_scale.setValue(100)  # Valor predeterminado (velocidad normal, equivalente a 1.0)
        adjustment_layout.addWidget(self.speed_scale)

        # Escala para ajustar el pitch (tono) del habla
        self.pitch_label = QLabel("Tono de Voz")
        adjustment_layout.addWidget(self.pitch_label)

        self.pitch_scale = QSlider(Qt.Horizontal, self)
        self.pitch_scale.setRange(-500, 500)  # Rango de -500 a 500 Hz
        self.pitch_scale.setSingleStep(10)  # Incremento de 10 Hz
        self.pitch_scale.setValue(0)  # Valor predeterminado (tono normal)
        adjustment_layout.addWidget(self.pitch_scale)

        # Añadir el layout de ajuste al layout principal
        self.layout().addLayout(adjustment_layout)

    """
    def action_scale(self):
        # Escala para ajustar la velocidad del habla
        self.speed_scale = tk.Scale(
                self.adjustment_frame,
                from_=0.25,  # Velocidad mínima
                to=2.0,      # Velocidad máxima
                resolution=0.05,  # Incremento de velocidad
                orient=tk.HORIZONTAL,
                label="Velocidad de Voz"
                )

        self.speed_scale.set(1.0)  # Valor predeterminado (velocidad normal)
        self.speed_scale.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Escala para ajustar el pitch (tono) del habla
        self.pitch_scale = tk.Scale(
                self.adjustment_frame,
                from_=-500,  # Tono mínimo en Hz
                to=500,      # Tono máximo en Hz
                resolution=10,  # Incremento de tono en Hz
                orient=tk.HORIZONTAL,
                label="Tono de Voz"
        )

        self.pitch_scale.set(0)  # Valor predeterminado (tono normal)
        self.pitch_scale.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    """

    def button_action(self):
        # Layout para los botones de acción de audio
        self.button_layout = QGridLayout()

        # Botón para validar la configuración
        self.verify_button = QPushButton("Validar Configuración", self)
        self.verify_button.clicked.connect(self.write_file_configuration)  # Conectar el evento
        self.button_layout.addWidget(self.verify_button, 0, 0)

        # Botón para convertir el texto a MP3
        self.convert_button = QPushButton("Convertir a MP3", self)
        self.convert_button.setEnabled(False)  # Deshabilitado por defecto
        self.convert_button.clicked.connect(self.convert_text)
        self.button_layout.addWidget(self.convert_button, 0, 1)

        # Botón para reproducir el audio
        self.play_button = QPushButton("Reproducir Audio", self)
        self.play_button.setEnabled(False)  # Deshabilitado por defecto
        self.play_button.clicked.connect(self.play_audio)
        self.button_layout.addWidget(self.play_button, 0, 2)

        # Botón para guardar el audio
        self.save_button = QPushButton("Guardar Audio", self)
        self.save_button.setEnabled(False)  # Deshabilitado por defecto
        self.save_button.clicked.connect(self.save_audio)
        self.button_layout.addWidget(self.save_button, 0, 3)

        # Agregar el layout de botones al layout principal
        self.layout().addLayout(self.button_layout)

        # Layout para el marco derecho de botones
        self.right_button_layout = QVBoxLayout()

        # Botón para la acción <phoneme>
        self.phoneme_button = QPushButton("<phoneme>", self)
        self.phoneme_button.clicked.connect(self.phoneme_action)
        self.right_button_layout.addWidget(self.phoneme_button)

        # Botón para la acción <say-as>
        self.say_as_button = QPushButton("<say-as>", self)
        self.say_as_button.clicked.connect(self.say_as_action)
        self.right_button_layout.addWidget(self.say_as_button)

        # Botón para la acción <sub alias>
        self.sub_alias_button = QPushButton("<sub alias>", self)
        self.sub_alias_button.clicked.connect(self.sub_alias_action)
        self.right_button_layout.addWidget(self.sub_alias_button)

        # Botón para la acción <emphasis>
        self.emphasis_button = QPushButton("<emphasis>", self)
        self.emphasis_button.clicked.connect(self.emphasis_action)
        self.right_button_layout.addWidget(self.emphasis_button)

        # Botón para la acción <audio>
        self.audio_button = QPushButton("<audio>", self)
        self.audio_button.clicked.connect(self.audio_action)
        self.right_button_layout.addWidget(self.audio_button)

        # Botón para la acción <voice>
        self.voice_button = QPushButton("<voice>", self)
        self.voice_button.clicked.connect(self.voice_action)
        self.right_button_layout.addWidget(self.voice_button)

        # Botón para cambiar a la vista de video
        self.show_video_button = QPushButton("<VIDEO>", self)
        self.show_video_button.clicked.connect(self.show_video_buttons)
        self.right_button_layout.addWidget(self.show_video_button)

        # Botón para cambiar a la vista de audio
        self.show_audio_button = QPushButton("<AUDIO>", self)
        self.show_audio_button.clicked.connect(self.show_audio_buttons)
        self.right_button_layout.addWidget(self.show_audio_button)

        # Añadir el layout de botones de la derecha al layout principal
        self.layout().addLayout(self.right_button_layout)

    """
    def button_action(self):
    # Botones de accion de audio

        # Botón para validar la configuración
        self.verify_button = tk.Button(
                self.button_frame,
                text="Validar Configuración",
                command=self.write_file_configuration
                )
        self.verify_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Botón para convertir el texto a MP3
        self.convert_button = tk.Button(
                self.button_frame,
                text="Convertir a MP3",
                command=self.convert_text,
                state=tk.DISABLED
                )
        self.convert_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botón para reproducir el audio
        self.play_button = tk.Button(
                self.button_frame,
                text="Reproducir Audio",
                command=self.play_audio,
                state=tk.DISABLED
                )
        self.play_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Botón para guardar el audio
        self.save_button = tk.Button(
                self.button_frame,
                text="Guardar Audio",
                command=self.save_audio,  # Llamar a la función save_audio
                state=tk.DISABLED
                )
        self.save_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Configurar las columnas del marco de botones para que se expandan uniformemente
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

        # Agregar botones al marco derecho con sus funcionalidades específicas
        self.phoneme_button = tk.Button(
                self.right_button_frame, 
                text="<phoneme>", 
                command=self.phoneme_action
                )
        self.phoneme_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.say_as_button = tk.Button(
                self.right_button_frame, 
                text="<say-as>", 
                command=self.say_as_action
                )
        self.say_as_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.sub_alias_button = tk.Button(
                self.right_button_frame, 
                text="<sub alias>", 
                command=self.sub_alias_action
                )
        self.sub_alias_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.emphasis_button = tk.Button(
                self.right_button_frame, 
                text="<emphasis>", 
                command=self.emphasis_action
                )
        self.emphasis_button.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.audio_button = tk.Button(
                self.right_button_frame, 
                text="<audio>", 
                command=self.audio_action
                )
        self.audio_button.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        self.voice_button = tk.Button(
                self.right_button_frame, 
                text="<voice>", 
                command=self.voice_action
                )
        self.voice_button.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.show_video_button = tk.Button(
                self.right_button_frame, 
                text="<VIDEO>", 
                command=self.show_video_buttons
                )
        self.show_video_button.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        self.show_audio_button = tk.Button(
                self.right_button_frame, 
                text="<AUDIO>", 
                command=self.show_audio_buttons
                )
        self.show_audio_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    """

    def button_action_videos(self):
        # Crear un layout para los botones de acción de video
        self.video_button_layout = QGridLayout()

        # Botón para cargar video
        self.load_video_button = QPushButton("Cargar Video", self)
        self.load_video_button.clicked.connect(self.load_video)
        self.video_button_layout.addWidget(self.load_video_button, 0, 0)

        # Botón para cargar audio
        self.load_audio_button = QPushButton("Cargar Audio", self)
        self.load_audio_button.clicked.connect(self.load_audio)
        self.video_button_layout.addWidget(self.load_audio_button, 0, 1)

        # Botón para reproducir video/audio
        self.play_video_audio_button = QPushButton("Reproducir", self)
        self.play_video_audio_button.clicked.connect(self.play_video_audio)
        self.video_button_layout.addWidget(self.play_video_audio_button, 0, 2)

        # Botón para detener reproducción de video/audio
        self.stop_video_audio_button = QPushButton("Detener", self)
        self.stop_video_audio_button.clicked.connect(self.stop_video_audio)
        self.video_button_layout.addWidget(self.stop_video_audio_button, 0, 3)

        # Botón para guardar video/audio
        self.save_media_button = QPushButton("Guardar", self)
        self.save_media_button.clicked.connect(self.save_media)
        self.video_button_layout.addWidget(self.save_media_button, 0, 4)

        # Botón para agregar subtítulos
        self.add_subtitles_button = QPushButton("Agregar Subtítulos", self)
        self.add_subtitles_button.clicked.connect(self.add_subtitles)
        self.video_button_layout.addWidget(self.add_subtitles_button, 0, 5)

        # Añadir el layout de los botones de video al layout principal
        self.layout().addLayout(self.video_button_layout)

    """
    def button_action_videos(self):
    #Botones de acción de video

        # Botón para cargar video
        self.load_video_button = ttk.Button(
                self.button_frame,
                text="Cargar Video",
                command=self.load_video
                )
        self.load_video_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Botón para cargar el audio
        self.load_audio_button = ttk.Button(
                self.button_frame,
                text="Cargar Audio",
                command=self.load_audio
                )
        self.load_audio_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botón para reproducir video
        self.play_video_audio_button = ttk.Button(
                self.button_frame,
                text="Reproducir",
                command=self.play_video_audio
                )
        self.play_video_audio_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Botón para detener reproducción
        self.stop_video_audio_button = ttk.Button(
                self.button_frame,
                text="Detener",
                command=self.stop_video_audio
                )
        self.stop_video_audio_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Botón para guardar video
        self.save_media_button = ttk.Button(
                self.button_frame,
                text="Guardar",
                command=self.save_media
                )
        self.save_media_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        
        # Botón para agregar subtitulos
        self.add_subtitles_button = tk.Button(
                self.button_frame, 
                text="Agregar Subtítulos", 
                command=self.add_subtitles
        )
        self.add_subtitles_button.grid(row=0, column=5, padx=5, pady=5, sticky="ew")
    """

    def setup_video_frame(self):
        # Crear un QWidget para el marco del video
        self.video_frame = QWidget(self)
        self.video_frame.setFixedSize(640, 360)  # Ajustar las dimensiones
        self.video_frame.setStyleSheet("background-color: black;")  # Establecer el color de fondo

        # Crear un layout para el frame de video (opcional si deseas agregar más elementos)
        video_layout = QVBoxLayout()
        self.video_frame.setLayout(video_layout)

        # Añadir el video frame al layout principal
        self.layout().addWidget(self.video_frame)

        # Obtener el identificador del contenedor de video (winId() es equivalente a winfo_id() en Tkinter)
        self.video_panel_id = self.video_frame.winId()

    """
    def setup_video_frame(self):
        #Configura un frame para reproducir el video

        self.video_frame = tk.Frame(self.root, width=640, height=360, bg='black')  # Ajusta las dimensiones
        self.video_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Obtener el identificador del contenedor de video
        self.video_panel_id = self.video_frame.winfo_id()
    """
    def load_video(self):
        video_module.load_video(self.video_frame)

    def load_audio(self):
        video_module.load_audio()

    def play_video_audio(self):
        video_module.play_video_audio()

    def stop_video_audio(self):
        video_module.stop_video_audio()

    def save_media(self):
        video_module.save_media()

    def phoneme_action(self):
        # Acción para el botón <phoneme>
        phoneme = "<phoneme> - Aquí puedes ingresar el texto o formato de phoneme"
        self.text_entry.insertPlainText(phoneme)

    """
    # Métodos para las nuevas funcionalidades
    def phoneme_action(self):
        # Acción para el botón <phoneme>
        phoneme = "<phoneme> - Aquí puedes ingresar el texto o formato de phoneme"
        self.text_entry.insert(tk.END, phoneme)
    """

    def say_as_action(self):
        from .modules.audio.say_as import get_say_as_options, get_currency_options, get_unit_options

        # Obtener la selección del texto
        selected_text = self.text_entry.textCursor().selectedText()

        # Mostrar opciones de <say-as> al usuario
        options = get_say_as_options()
        option_labels = [opt[0] for opt in options]

        # Crear un cuadro de diálogo para seleccionar la opción de <say-as>
        selected_option, ok = QInputDialog.getItem(self,
                                                   "Selecciona el tipo de <say-as>",
                                                   "Opciones disponibles:",
                                                   option_labels, 0, False)

        if ok and selected_option:
            say_as_tag = next((opt[1] for opt in options if opt[0] == selected_option), None)
            additional_options = ""

            # Si la opción seleccionada requiere más subopciones, las mostramos
            if say_as_tag == "currency":
                currency_options = get_currency_options()
                currency_labels = [cur[0] for cur in currency_options]
                selected_currency, ok_currency = QInputDialog.getItem(self,
                                                                      "Selecciona una moneda",
                                                                      "Opciones disponibles:",
                                                                      currency_labels, 0, False)
                if ok_currency and selected_currency:
                    additional_options = f' interpret-as="{say_as_tag}" currency="{selected_currency}"'
                else:
                    return  # Salir si no se selecciona una opción válida

            elif say_as_tag == "unit":
                unit_options = get_unit_options()
                unit_labels = [unit[0] for unit in unit_options]
                selected_unit, ok_unit = QInputDialog.getItem(self,
                                                              "Selecciona una unidad",
                                                              "Opciones disponibles:",
                                                              unit_labels, 0, False)
                if ok_unit and selected_unit:
                    additional_options = f' interpret-as="{say_as_tag}" unit="{selected_unit}"'
                else:
                    return  # Salir si no se selecciona una opción válida
            else:
                additional_options = f' interpret-as="{say_as_tag}"'

            # Insertar la etiqueta <say-as> en el texto seleccionado
            say_as_tagged = f'<say-as{additional_options}>{selected_text}</say-as>'
            cursor = self.text_entry.textCursor()
            cursor.removeSelectedText()  # Borrar el texto seleccionado
            cursor.insertText(say_as_tagged)  # Insertar la etiqueta <say-as>
        else:
            QMessageBox.critical(self, "Error", "Opción no válida seleccionada.")

    """
    def say_as_action(self):
        from app.modules.audio.say_as import get_say_as_options, get_currency_options, get_unit_options
        # Obtener la selección del texto
        selected_text = self.text_entry.selection_get()

        # Mostrar opciones de <say-as> al usuario
        options = get_say_as_options()
        option_labels = [opt[0] for opt in options]

        # Crear un cuadro de diálogo para seleccionar la opción de <say-as>
        selected_option = simpledialog.askstring("Selecciona el tipo de <say-as>", 
                                                 "Opciones disponibles:\n" + "\n".join(option_labels))

        # Buscar la opción seleccionada
        say_as_tag = next((opt[1] for opt in options if opt[0] == selected_option), None)

        if say_as_tag:
            additional_options = ""

            # Si la opción seleccionada requiere más subopciones, las mostramos
            if say_as_tag == "currency":
                currency_options = get_currency_options()
                currency_labels = [cur[0] for cur in currency_options]
                selected_currency = simpledialog.askstring("Monedas", "Selecciona una moneda:\n" + "\n".join(currency_labels))
                additional_options = f' interpret-as="{say_as_tag}" currency="{selected_currency}"'

            elif say_as_tag == "unit":
                unit_options = get_unit_options()
                unit_labels = [unit[0] for unit in unit_options]
                selected_unit = simpledialog.askstring("Unidades", "Selecciona una unidad:\n" + "\n".join(unit_labels))
                additional_options = f' interpret-as="{say_as_tag}" unit="{selected_unit}"'

            else:
                additional_options = f' interpret-as="{say_as_tag}"'

            # Insertar la etiqueta <say-as> en el texto seleccionado
            say_as_tagged = f'<say-as{additional_options}>{selected_text}</say-as>'
            self.text_entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_entry.insert(tk.INSERT, say_as_tagged)
        else:
            tk.messagebox.showerror("Error", "Opción no válida seleccionada.")
    """

    def sub_alias_action(self):
        # Acción para el botón <sub alias>
        sub_alias = "<sub alias> - Aquí puedes ingresar el texto o formato de sub alias"
        self.text_entry.insertPlainText(sub_alias)

    """
    def sub_alias_action(self):
        # Acción para el botón <sub alias>
        sub_alias = "<sub alias> - Aquí puedes ingresar el texto o formato de sub alias"

        self.text_entry.insert(tk.END, sub_alias)
    """

    def emphasis_action(self):
        # Acción para el botón <emphasis>
        emphasis = "<emphasis> - Aquí puedes ingresar el texto o formato de emphasis"
        self.text_entry.insertPlainText(emphasis)

    """
    def emphasis_action(self):
        # Acción para el botón <emphasis>
        emphasis = "<emphasis> - Aquí puedes ingresar el texto o formato de emphasis"
        self.text_entry.insert(tk.END, emphasis)
    """

    def audio_action(self):
        # Acción para el botón <sub alias>
        audio = "<audio> - Aquí puedes ingresar el texto o formato de audio"
        self.text_entry.insertPlainText(audio)

    """
    def audio_action(self):
        # Acción para el botón <audio>
        audio = "<audio> - Aquí puedes ingresar el texto o formato de audio"
        self.text_entry.insert(tk.END, audio)
    """

    def voice_action(self):
        # Acción para el botón <sub alias>
        voice = "<voice> - Aquí puedes ingresar el texto o formato de voice"
        self.text_entry.insertPlainText(voice)

    """
    def voice_action(self):
        # Acción para el botón <voice>
        voice = "<voice> - Aquí puedes ingresar el texto o formato de voice"
        self.text_entry.insert(tk.END, voice)
    """

    def add_subtitles(self):
        from app.modules.subtitles import process_subtitles
        result = process_subtitles()

        # Mostrar el resultado usando QMessageBox en lugar de messagebox.showinfo
        QMessageBox.information(self, "Resultado", result)

    """
    def add_subtitles(self):
        from app.modules.subtitles import process_subtitles
        result = process_subtitles()
        messagebox.showinfo("Resultado", result)
    """

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

    """
    def write_file_configuration(self):
        from app.modules.audio.write_file_configuration import write_file_configuration

        # Deshabilitar el botón de verificación
        self.verify_button.config(state=tk.DISABLED)

        try:
            # Llama a la función write_file_configuration del módulo
            write_file_configuration(self.audio_config, self.text_entry, self.speed_scale, self.pitch_scale, self.status_label)
        except Exception as e:
            # Mostrar el error en un cuadro de diálogo
            messagebox.showerror("Error", str(e))
        finally:
            self.convert_button.config(state=tk.NORMAL)
            self.verify_button.config(state=tk.NORMAL)
            show_status_message(self.status_label, "El archivo ha sido verificado exitosamente", "success")

    """

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
    """
    def convert_text(self):
        # Deshabilitar el botón de conversión
        self.convert_button.config(state=tk.DISABLED)
        show_status_message(self.status_label, "Convirtiendo texto a audio...", "info")

        try:
            # Llamar al método convert_text de AudioConfig
            show_status_message(self.status_label, "Convirtiendo texto a audio...", "info")
            temp_file_path, error_message = self.audio_config.convert_text()

            if error_message:
                raise Exception(error_message)

            # Actualizar la ruta del archivo temporal y habilitar los botones de reproducción y guardado
            self.temp_file_path = temp_file_path
            self.play_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            show_status_message(self.status_label, "Conversión completada con éxito.", "success")
        except Exception as e:
            messagebox.showerror("Error", f"Error al convertir el texto a audio: {str(e)}")
        finally:
            # Habilitar el botón de conversión nuevamente, haya o no error
            self.convert_button.config(state=tk.NORMAL)
    """

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

    """
    def play_audio(self):
        #Reproduce el archivo de audio temporal generado.
        if self.temp_file_path:
            play(self.temp_file_path)  # Usar la función genérica
        else:
            messagebox.showerror("Error", "No se encontró el archivo de audio.")
    """

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

    """
    def save_audio(self):
        #Función para guardar el archivo de audio.
        if self.temp_file_path:
            try:
                save_file(self.temp_file_path, get_save_dir(), file_types=[("MP3 files", "*.mp3")], default_extension=".mp3")
            except Exception as e:
                show_status_message(self.status_label, f"Error al guardar el archivo: {e}", "error")
        else:
            messagebox.showerror("Error", "No hay ningún archivo de audio para guardar.")
    """

    def save_text(self):
        """Función para guardar el archivo de texto."""
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo de texto", "",
                                                       "Text files (*.txt);;All Files (*)", options=options)
            if file_name:
                # Lógica para guardar el archivo, asumiendo que `save_file` está definida
                save_file(self.temp_file_path, file_name)
                self.status_label.setText("Archivo guardado exitosamente.")
            else:
                self.status_label.setText("Operación de guardado cancelada.")
        except Exception as e:
            self.status_label.setText(f"Error al guardar el archivo: {str(e)}")

    """
    def save_text(self):
        #Función para guardar el archivo de texto.
        try:
            save_file(self.temp_file_path, get_save_dir(), file_types=[("Text files", "*.txt")], default_extension=".txt")
        except Exception as e:
            show_status_message(self.status_label, f"Error al guardar el archivo: {e}", "error")
    """

    def save_video(self):
        """Función para guardar el archivo de video."""
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Guardar archivo de video", "",
                                                       "Video files (*.mp4);;All Files (*)", options=options)
            if file_name:
                # Lógica para guardar el archivo, asumiendo que `save_file` está definida
                save_file(self.temp_file_path, file_name)
                self.status_label.setText("Archivo guardado exitosamente.")
            else:
                self.status_label.setText("Operación de guardado cancelada.")
        except Exception as e:
            self.status_label.setText(f"Error al guardar el archivo: {str(e)}")

    """
    def save_video(self):
        #Función para guardar el archivo de video.
        try:
            save_file(self.temp_file_path, get_save_dir(), file_types=[("Video files", "*.mp4")], default_extension=".mp4")
        except Exception as e:
            show_status_message(self.status_label, f"Error al guardar el archivo: {e}", "error")
    """


