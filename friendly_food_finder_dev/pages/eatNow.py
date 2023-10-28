"""The eatNow page."""
from friendly_food_finder_dev.templates import template

import reflex as rx


@template(route="/eatNow", title="Eat Now")
def eatNow() -> rx.Component:
    """The eatNow page.

    Returns:
        The UI for the eatNow page.
    """
    return rx.vstack(
        rx.heading("Eat Now!", font_size="3em"),
        rx.text("Time to spontaneously eat!")
    )
