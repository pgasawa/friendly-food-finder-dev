"""The signup page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.state import State

import reflex as rx


@template(route="/signup", title="signup")
def signup() -> rx.Component:
    """The signup page.

    Returns:
        The UI for the signup page.
    """
    return rx.vstack(
        rx.heading("Sign Up", font_size="3em"),
        rx.input(on_change=State.set_user_create_name, placeholder="Name"),
        rx.input(on_change=State.set_user_create_email, placeholder="Email", type_="email"),
        rx.input(on_change=State.set_user_create_password, placeholder="Password", type_="password"),
        rx.number_input(on_change=State.set_user_create_budget, placeholder="Budget"),
        rx.button("Sign Up", on_click=State.user_create)
    )
