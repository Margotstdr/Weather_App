import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date

from constants import *
from weather import *
from weather_queries import *
from plot import *

# ----------------------------------------------------------------------
# Variables globales
# ----------------------------------------------------------------------
# Ville actuelle
city = "Paris"
# city = "Bordeaux"

# ImageTk : ces variables globales permettent d'éviter que le garbage collector ne les efface
image_background = None
weather_icon = None
zone_graphique = None

# ----------------------------------------------------------------------
# Canvas
# ----------------------------------------------------------------------

def load_background(canvas):
    """Charge "assets/blue_sky.jpg", la redimensionne et la place sur le canvas."""
    global image_background

    image = Image.open("assets/blue_sky.jpg").convert("RGBA")
    image = image.resize((WIDTH, HEIGHT))
    image_background = ImageTk.PhotoImage(image)

    canvas.create_image(0, 0, image = image_background, anchor = "nw")


def erase_screen(canvas):
    """Supprime tout ce qui a le tag 'ecran'."""
    canvas.delete("ecran")


# ----------------------------------------------------------------------
# Ecrans
# ----------------------------------------------------------------------

def draw_welcome_screen(window, canvas):
    """Écran 1 : Icône de la météo, température actuelle, températures min et max du jour."""
    global weather_icon

    erase_screen(canvas)
    temperature, code, t_min, t_max = get_current_weather(city)

    # Nom de la ville
    canvas.create_text(WIDTH / 2, 60, text = city,
                       font = ("Helvetica", 24, "bold"), fill = "white", tags = "ecran")

    # Icône météo
    icon_name = icon_of_code(code)
    if icon_name == "unknown":
        icon_name = "cloudy"
    image = Image.open(f"assets/icons/{icon_name}.png").convert("RGBA")
    image = image.resize((120, 120))
    weather_icon = ImageTk.PhotoImage(image)
    canvas.create_image(WIDTH / 2, 170, image = weather_icon, tags = "ecran")

    # Température actuelle
    canvas.create_text(WIDTH / 2, 290, text = f"{round(temperature)} °C",
                       font = ("Helvetica", 40, "bold"), fill = "white", tags = "ecran")

    # Min / Max
    canvas.create_text(WIDTH / 2, 350,
                       text = f"Min : {round(t_min)} °C     Max : {round(t_max)} °C",
                       font = ("Helvetica", 12), fill = "white", tags = "ecran")

    # Bouton vers les prévisions
    button = tk.Button(window, text = "Prévisions 7 jours",
                       command = lambda : draw_forecast(window, canvas))
    canvas.create_window(WIDTH / 2, 440, window = button, tags = "ecran")


def draw_forecast(window, canvas):
    """Écran 2 : graphique des températures sur 7 jours"""
    global zone_graphique

    erase_screen(canvas)
    start_day = date.today()
    dates, t_mins, t_maxs = get_forecast(city, start_day)

    # Titre + période
    canvas.create_text(WIDTH / 2, 30, text = f"Prévisions sur 7 jours - {city}",
                       font = ("Helvetica", 16, "bold"), fill = "white", tags = "ecran")
    canvas.create_text(WIDTH / 2, 55, text = f"Du {dates[0]} au {dates[-1]}",
                       font = ("Helvetica", 10), fill = "white", tags = "ecran")

    # Graphique Matplotlib
    figure = create_plot(dates, t_mins, t_maxs)
    zone_graphique = FigureCanvasTkAgg(figure, master = window)
    canvas.create_window(WIDTH / 2, 230, window = zone_graphique.get_tk_widget(), tags = "ecran")

    # Bouton retour à l'accueil
    button = tk.Button(window, text = "Accueil",
                       command = lambda : draw_welcome_screen(window, canvas))
    canvas.create_window(WIDTH / 2, 450, window = button, tags = "ecran")
