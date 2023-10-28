"""The createhangoutp1 page."""
from friendly_food_finder_dev.templates import template

import reflex as rx


@template(route="/createhangoutp1", title="createhangoutp1")
def createhangoutp1() -> rx.Component:
    """The createhangoutp1 page.

    Returns:
        The UI for the createhangoutp1 page.
    """
    return rx.vstack(
        rx.heading("createhangoutp1", font_size="3em"),
        rx.text("Welcome to createhangoutp1!")
    )
