"""The signup page."""
from friendly_food_finder_dev.templates import template

import reflex as rx


@template(route="/signup", title="signup")
def signup() -> rx.Component:
    """The signup page.

    Returns:
        The UI for the signup page.
    """
    return rx.vstack(
        rx.heading("signup", font_size="3em"),
        rx.text("Welcome to signup!")
    )
