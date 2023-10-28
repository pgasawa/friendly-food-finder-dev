"""The feed page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev import styles

import reflex as rx


@template(route="/feed", title="Feed")
def feed() -> rx.Component:
    """The feed page.

    Returns:
        The UI for the feed page.
    """
    return rx.vstack(
        rx.center(
            rx.box(
                rx.heading("Feed", font_size="3em"),
                rx.text("Welcome to Feed!"),
                **styles.template_content_style,
            ),
        ),
        rx.text("Testing what happens rn"),
    )