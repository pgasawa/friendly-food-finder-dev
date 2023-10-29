"""Welcome to Reflex!."""

from friendly_food_finder_dev import styles

# Import all the pages.
from friendly_food_finder_dev.pages import *

import reflex as rx

# Create the app and compile it.
app = rx.App(
    style=styles.base_style,
    stylesheets=[
        "fonts/futura.css"
    ]
)
app.compile()
