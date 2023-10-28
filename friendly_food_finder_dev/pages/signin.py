"""The signin page."""
from friendly_food_finder_dev.templates import template

import reflex as rx


@template(route="/signin", title="signin")
def signin() -> rx.Component:
    """The signin page.

    Returns:
        The UI for the signin page.
    """
    return rx.vstack(
        rx.heading("signin", font_size="3em"),
        rx.text("Welcome to signin!")
    )
