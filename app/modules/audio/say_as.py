# app/modules/audio/say-as.py

def say_as_action(self):
    # Crear un nuevo menú emergente para seleccionar la opción de <say-as>
    say_as_menu = tk.Menu(self.root, tearoff=0)

    # Opciones principales de <say-as>
    say_as_menu.add_command(
            label="Número", 
            command=lambda: self.insert_say_as('number')
    )

    say_as_menu.add_command(
            label="Fecha", 
            command=lambda: self.insert_say_as('date')
    )

    say_as_menu.add_command(
            label="Hora", 
            command=lambda: self.insert_say_as('time')
    )
    
    # Crear un submenú para Moneda (currency)
    currency_menu = tk.Menu(say_as_menu, tearoff=0)
    currencies = self.audio_config.get_currency_options()  # Llamar la función para obtener monedas
    for currency in currencies:
        currency_menu.add_command(
            label=currency[0], 
            command=lambda c=currency[1]: self.insert_say_as('currency', c)
        )
    say_as_menu.add_cascade(label="Moneda", menu=currency_menu)

    say_as_menu.add_command(
            label="Porcentaje", 
            command=lambda: self.insert_say_as('percent')
    )

    say_as_menu.add_command(
            label="Teléfono", 
            command=lambda: self.insert_say_as('telephone')
    )
    
    # Crear un submenú para Unidad (unit)
    unit_menu = tk.Menu(say_as_menu, tearoff=0)
    units = self.audio_config.get_unit_options()  # Llamar la función para obtener unidades
    for unit in units:
        unit_menu.add_command(
            label=unit[0], 
            command=lambda u=unit[1]: self.insert_say_as('unit', u)
        )
    say_as_menu.add_cascade(label="Unidad", menu=unit_menu)

    # Mostrar el menú emergente
    try:
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        say_as_menu.tk_popup(x, y)
    finally:
        say_as_menu.grab_release()

def insert_say_as(self, interpret_as, value=None):
    # Crear la etiqueta <say-as> con las opciones seleccionadas
    if value:
        tag = f'<say-as interpret-as="{interpret_as}" {interpret_as}="{value}">'
    else:
        tag = f'<say-as interpret-as="{interpret_as}">'
    
    self.text_entry.insert(tk.INSERT, tag)
    self.text_entry.insert(tk.INSERT, '</say-as>')

def get_say_as_options():
    return [
        ("Número", "number"),
        ("Fecha", "date"),
        ("Hora", "time"),
        ("Moneda", "currency"),
        ("Porcentaje", "percent"),
        ("Teléfono", "telephone"),
        ("Unidad", "unit")
    ]

def get_currency_options():
    return [
        ("USD", "Dólar estadounidense"),
        ("EUR", "Euro"),
        ("GBP", "Libra esterlina"),
        ("JPY", "Yen japonés"),
        ("AUD", "Dólar australiano")
        # Puedes agregar más monedas aquí
    ]

def get_unit_options():
    return [
        ("Centímetros", "centimeter"),
        ("Metros", "meter"),
        ("Kilómetros", "kilometer"),
        ("Gramos", "gram"),
        ("Libras", "pound"),
        ("Kilogramos", "kilogram"),
        ("Toneladas", "ton"),
        ("Litros", "liter"),
        ("Galones", "gallon")
    ]

