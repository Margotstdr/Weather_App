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
    temperature, code, t_min, t_max = 0, 0, 0, 0 # TODO

    # TODO
    # canvas.create_text(...)

    # ...

def draw_forecast(window, canvas):
    """Écran 2 : graphique des températures sur 7 jours"""

    erase_screen(canvas)
    # start_day = ...

    dates = ['2026-10-06', '2026-10-07', '2026-10-08', '2026-10-09', '2026-10-10', '2026-10-11', '2026-10-12']
    t_mins = [18.0, 17.8, 12.6, 7.9, 12.3, 13.4, 13.1]
    t_maxs = [27.4, 20.6, 17.6, 18.7, 20.2, 20.0, 20.7]

    # Titre et période
    canvas.create_text(WIDTH / 2, 40, 
                    text = "Prévisions sur 7 jours - " + city,
                    font = ("Helvetica", 14, "bold"),
                    fill = "white", tags = "ecran")
    
    canvas.create_text(WIDTH / 2, 65,
                    text = "Du " + dates[0] + " au " + dates[-1],
                    font = ("Helvetica", 10),
                    fill = "white", tags = "ecran")

    figure = create_plot(dates, t_mins, t_maxs)
    zone_graphique = FigureCanvasTkAgg(figure, master = window)
    canvas.create_window(WIDTH / 2, HEIGHT / 2,
                        window = zone_graphique.get_tk_widget(),
                        tags = "ecran")

    button = tk.Button(window, text = "Accueil",
                    command = lambda : draw_welcome_screen(window, canvas))
    
    canvas.create_window(WIDTH / 2, HEIGHT - 60, window = button, tags = "ecran")

