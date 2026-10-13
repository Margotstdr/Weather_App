from datetime import datetime

from constants import *

# ----------------------------------------------------------------------
# Météo
# ----------------------------------------------------------------------

# Seules ces icônes montrent un soleil : les autres (pluie, neige...) conviennent aussi la nuit
NIGHT_ICONS = {
    "sunny": "night",
    "partly_cloudy_day": "partly_cloudy_night",
}


def icon_of_code(code):
    """Obtient le nom d'icône correspondant au code météo (WMO) d'Open-Meteo."""
    if code == 0:
        return "sunny"
    if code in (1, 2):
        return "partly_cloudy_day"
    if code == 3:
        return "cloudy"
    if code in (45, 48):
        return "fog"
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "rain"
    if code in (71, 73, 75, 77, 85, 86):
        return "snow"
    if code in (95, 96, 99):
        return "storm"
    return "unknown"


def time_of_day(hour=None):
    """Renvoie "day" ou "night" en fonction de l'heure de la journée"""
    if hour is None:
        hour = datetime.now().hour
    if DAY_START_HOUR <= hour < NIGHT_START_HOUR:
        return "day"
    return "night"


def choose_icon(code, is_night=False):
    """Renvoie le nom du fichier d'icône à afficher pour un code météo, en version nuit si besoin."""
    icon_name = icon_of_code(code)
    # Il n'y a pas d'icône "unknown" dans assets/icons
    if icon_name == "unknown":
        icon_name = "cloudy"
    if is_night:
        icon_name = NIGHT_ICONS.get(icon_name, icon_name)
    return icon_name
