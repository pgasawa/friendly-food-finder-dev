"""The feed page."""
from friendly_food_finder_dev.templates import template

import reflex as rx


@template(route="/feed", title="Feed")
def feed() -> rx.Component:
    """The feed page.

    Returns:
        The UI for the feed page.
    """
    return rx.vstack(
        rx.heading("Feed", font_size="3em"),
        rx.text("Welcome to Feed!")
    )
