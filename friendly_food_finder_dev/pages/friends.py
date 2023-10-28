"""The friends page."""
from friendly_food_finder_dev.templates import template

import reflex as rx


@template(route="/friends", title="friends")
def friends() -> rx.Component:
    """The friends page.

    Returns:
        The UI for the friends page.
    """
    return rx.vstack(
        rx.heading("Friends", font_size="3em"),
        rx.text("Welcome to friends!"),
        rx.text("You have no friends and you never will <3"),
    )
