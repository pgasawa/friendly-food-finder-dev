"""The eatNow page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login

import reflex as rx


@template(route="/eatNow", title="Eat Now")
@require_google_login
def eatNow() -> rx.Component:
    """The eatNow page.

    Returns:
        The UI for the eatNow page.
    """
    return rx.vstack(
        rx.heading("Eat Now!", font_size="3em"),
        rx.text("Time to spontaneously eat!")
    )
