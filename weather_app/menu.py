import os
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date, timedelta

from constants import *
from weather import *
from weather_queries import *
from plot import *

# ----------------------------------------------------------------------
# Variables globales
# ----------------------------------------------------------------------
# Ville actuelle
city = "Paris"
# Premier jour affiché dans l'écran des prévisions (déplacé par les flèches)
forecast_start = date.today()

# ImageTk : ces variables globales permettent d'éviter que le garbage collector ne les efface
image_background = None
weather_icon = None
zone_graphique = None
# Même raison : si la StringVar est effacée, le menu déroulant s'affiche vide
city_variable = None

# canvas.delete() retire les widgets du canvas sans les détruire :
# on les garde ici pour pouvoir les détruire à chaque changement d'écran
screen_widgets = []

# ----------------------------------------------------------------------
# Canvas
# ----------------------------------------------------------------------


def load_image(file_name, size):
    """Ouvre une image du dossier assets et la redimensionne."""
    image = Image.open(os.path.join(ASSETS_DIR, file_name)).convert("RGBA")
    return image.resize(size)


def load_background(canvas):
    """Place sur le canvas le fond de jour (blue_sky) ou de nuit (night_sky) selon l'heure."""
    global image_background

    file_name = "night_sky.jpg" if time_of_day() == "night" else "blue_sky.jpg"
    image_background = ImageTk.PhotoImage(load_image(file_name, (WIDTH, HEIGHT)))

    canvas.create_image(0, 0, image=image_background, anchor="nw")


def add_widget(canvas, widget, x, y):
    """Place un widget Tk sur le canvas et le mémorise pour qu'erase_screen le détruise."""
    screen_widgets.append(widget)
    canvas.create_window(x, y, window=widget, tags="ecran")


def erase_screen(canvas):
    """Supprime tout ce qui a le tag 'ecran' et détruit les widgets de l'écran précédent."""
    canvas.delete("ecran")
    for widget in screen_widgets:
        widget.destroy()
    screen_widgets.clear()


def show_error(window, canvas, message, retry_command):
    """Affiche un message d'erreur et un bouton pour réessayer, à la place de faire planter l'appli."""
    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2,
        text=message,
        justify="center",
        width=WIDTH - 40,
        font=("Helvetica", 13, "bold"),
        fill="white",
        tags="ecran",
    )
    button = tk.Button(window, text="Réessayer", command=retry_command)
    add_widget(canvas, button, WIDTH / 2, HEIGHT / 2 + 70)


# ----------------------------------------------------------------------
# Ecran 1 : accueil
# ----------------------------------------------------------------------


def draw_welcome_screen(window, canvas):
    """Écran 1 : Icône de la météo, température actuelle, températures min et max du jour."""
    erase_screen(canvas)
    draw_city_menu(window, canvas)

    try:
        temperature, code, t_min, t_max = get_current_weather(city)
    except WeatherAPIError as error:
        show_error(
            window, canvas, str(error), lambda: draw_welcome_screen(window, canvas)
        )
        return

    draw_weather_icon(canvas, code)

    # Température actuelle
    canvas.create_text(
        WIDTH / 2,
        290,
        text=f"{round(temperature)} °C",
        font=("Helvetica", 40, "bold"),
        fill="white",
        tags="ecran",
    )

    # Min / Max
    canvas.create_text(
        WIDTH / 2,
        350,
        text=f"Min : {round(t_min)} °C     Max : {round(t_max)} °C",
        font=("Helvetica", 12),
        fill="white",
        tags="ecran",
    )

    # Bouton vers les prévisions
    button = tk.Button(
        window, text="Prévisions 7 jours", command=lambda: open_forecast(window, canvas)
    )
    add_widget(canvas, button, WIDTH / 2, 440)


def draw_city_menu(window, canvas):
    """Menu déroulant affichant la ville actuelle et permettant d'en choisir une autre."""
    global city_variable

    city_variable = tk.StringVar(window, value=city)
    city_menu = tk.OptionMenu(
        window,
        city_variable,
        *CITIES,
        command=lambda chosen_city: change_city(window, canvas, chosen_city),
    )
    city_menu.config(font=("Helvetica", 20, "bold"))
    add_widget(canvas, city_menu, WIDTH / 2, 60)


def change_city(window, canvas, chosen_city):
    """Change la ville actuelle puis redessine l'accueil avec sa météo."""
    global city

    city = chosen_city
    draw_welcome_screen(window, canvas)


def draw_weather_icon(canvas, code):
    """Affiche l'icône du temps actuel, en version nuit si le soleil est couché."""
    global weather_icon

    is_night = time_of_day() == "night"
    icon_name = choose_icon(code, is_night)
    weather_icon = ImageTk.PhotoImage(load_image(f"icons/{icon_name}.png", (120, 120)))
    canvas.create_image(WIDTH / 2, 170, image=weather_icon, tags="ecran")


# ----------------------------------------------------------------------
# Ecran 2 : prévisions
# ----------------------------------------------------------------------


def open_forecast(window, canvas):
    """Ouvre les prévisions en repartant toujours d'aujourd'hui."""
    global forecast_start

    forecast_start = date.today()
    draw_forecast(window, canvas)


def shift_forecast(window, canvas, days):
    """Décale la période affichée de `days` jours (négatif = vers le passé)."""
    global forecast_start

    forecast_start = forecast_start + timedelta(days=days)
    draw_forecast(window, canvas)


def draw_forecast(window, canvas):
    """Écran 2 : graphique des températures sur 7 jours"""
    global zone_graphique

    erase_screen(canvas)
    draw_forecast_buttons(window, canvas)

    try:
        dates, t_mins, t_maxs, codes = get_forecast(city, forecast_start)
    except WeatherAPIError as error:
        show_error(window, canvas, str(error), lambda: draw_forecast(window, canvas))
        return

    # Titre + période
    canvas.create_text(
        WIDTH / 2,
        30,
        text=f"Prévisions sur 7 jours - {city}",
        font=("Helvetica", 16, "bold"),
        fill="white",
        tags="ecran",
    )
    canvas.create_text(
        WIDTH / 2,
        55,
        text=f"Du {dates[0]} au {dates[-1]}",
        font=("Helvetica", 10),
        fill="white",
        tags="ecran",
    )

    # Graphique Matplotlib, avec l'icône météo de chaque jour
    day_icons = [
        load_image(f"icons/{choose_icon(code)}.png", (30, 30)) for code in codes
    ]
    figure = create_plot(dates, t_mins, t_maxs, day_icons)
    zone_graphique = FigureCanvasTkAgg(figure, master=window)
    add_widget(canvas, zone_graphique.get_tk_widget(), WIDTH / 2, 245)


def draw_forecast_buttons(window, canvas):
    """Boutons ◄ Accueil ► ; les flèches sont grisées aux limites de ce que l'API fournit."""
    today = date.today()
    can_go_back = forecast_start - timedelta(days=FORECAST_DAYS) >= today - timedelta(
        days=MAX_PAST_DAYS
    )
    last_day_after_next = forecast_start + timedelta(days=2 * FORECAST_DAYS - 1)
    can_go_forward = last_day_after_next <= today + timedelta(days=MAX_FUTURE_DAYS)

    previous_button = tk.Button(
        window,
        text="◄",
        state="normal" if can_go_back else "disabled",
        command=lambda: shift_forecast(window, canvas, -FORECAST_DAYS),
    )
    home_button = tk.Button(
        window, text="Accueil", command=lambda: draw_welcome_screen(window, canvas)
    )
    next_button = tk.Button(
        window,
        text="►",
        state="normal" if can_go_forward else "disabled",
        command=lambda: shift_forecast(window, canvas, FORECAST_DAYS),
    )

    add_widget(canvas, previous_button, WIDTH / 2 - 110, 455)
    add_widget(canvas, home_button, WIDTH / 2, 455)
    add_widget(canvas, next_button, WIDTH / 2 + 110, 455)
