"""The scheduleEat page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login

import reflex as rx


@template(route="/scheduleEat", title="Schedule Eat")
@require_google_login
def scheduleEat() -> rx.Component:
    """The scheduleEat page.

    Returns:
        The UI for the scheduleEat page.
    """
    return rx.vstack(
        rx.heading("Schedule Ahead!", font_size="3em"),
        rx.text("Welcome to scheduling ahead ur eats!")
    )
