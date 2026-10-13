import os

# ----------------------------------------------------------------------
# Constantes
# ----------------------------------------------------------------------

CITIES = {
    "Paris": (48.8566, 2.3522),
    "Marseille": (43.2965, 5.3698),
    "Lyon": (45.7640, 4.8357),
    "Toulouse": (43.6047, 1.4442),
    "Bordeaux": (44.8378, -0.5792),
    "Lille": (50.6292, 3.0573),
    "Nantes": (47.2184, -1.5536),
    "Strasbourg": (48.5734, 7.7521),
    "Rennes": (48.1173, -1.6778),
    "Grenoble": (45.1885, 5.7245),
}

WIDTH = 400
HEIGHT = 500
URL_API = "https://api.open-meteo.com/v1/forecast"

# Chemin absolu : l'appli doit trouver ses images même si on la lance depuis un autre dossier
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Nombre de jours affichés dans l'écran des prévisions
FORECAST_DAYS = 7

# Limites mesurées sur l'API : au-delà de J+15 elle refuse la requête,
# avant J-70 elle renvoie des températures vides (None)
MAX_FUTURE_DAYS = 15
MAX_PAST_DAYS = 70

# Heures (heure locale) entre lesquelles on considère qu'il fait jour
DAY_START_HOUR = 7
NIGHT_START_HOUR = 20
