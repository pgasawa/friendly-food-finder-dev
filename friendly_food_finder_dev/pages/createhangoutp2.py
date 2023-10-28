"""The createhangoutp2 page."""
from friendly_food_finder_dev.templates import template

import reflex as rx


@template(route="/createhangoutp2", title="createhangoutp2")
def createhangoutp2() -> rx.Component:
    """The createhangoutp2 page.

    Returns:
        The UI for the createhangoutp2 page.
    """
    return rx.vstack(
        rx.heading("createhangoutp2", font_size="3em"),
        rx.text("Welcome to createhangoutp2!")
    )
