import numpy as np
from matplotlib.figure import Figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# ----------------------------------------------------------------------
# Plot Matplotlib
# ----------------------------------------------------------------------


def create_plot(dates, temperatures_min, temperatures_max, icons=None):
    """Crée et retourne une Figure Matplotlib avec les courbes de températures min et max sur les dates fournies.

    icons : liste optionnelle d'images PIL (une par jour) affichées au-dessus du graphique.
    """
    figure = Figure(figsize=(3.8, 3.4))
    # Fond bleu clair : les icônes de nuages sont blanches et disparaîtraient sur du blanc
    figure.patch.set_facecolor("#cfe0f1")
    axes = figure.add_subplot(111)

    x = range(len(dates))

    axes.plot(x, temperatures_max, color="red", marker="o")
    axes.plot(x, temperatures_min, color="blue", marker="o")
    axes.fill_between(x, temperatures_min, temperatures_max, color="gray", alpha=0.15)

    # Le titre est remonté pour laisser la place à la rangée d'icônes
    axes.set_title("Températures (°C)", pad=32 if icons else 6)
    axes.grid(True)

    # Améliore la lisibilité
    axes.set_xticks(range(len(dates)))
    axes.set_xticklabels([d[5:] for d in dates], rotation=45)

    if icons:
        add_day_icons(axes, icons)

    figure.tight_layout()
    return figure


def add_day_icons(axes, icons):
    """Place une icône au-dessus de chaque jour, alignée sur l'abscisse de ce jour."""
    for day_index, icon in enumerate(icons):
        image_box = OffsetImage(np.asarray(icon), zoom=1)
        # x en coordonnées de données (le jour), y en fraction de la hauteur des axes (juste au-dessus)
        annotation = AnnotationBbox(
            image_box,
            (day_index, 1.0),
            xycoords=("data", "axes fraction"),
            box_alignment=(0.5, 0),
            frameon=False,
            annotation_clip=False,
        )
        axes.add_artist(annotation)
