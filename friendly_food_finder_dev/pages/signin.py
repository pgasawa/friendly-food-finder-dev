"""The signin page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.state import State

import reflex as rx


@template(route="/signin", title="signin")
def signin() -> rx.Component:
    """The signin page.

    Returns:
        The UI for the signin page.
    """
    return rx.vstack(
        rx.heading("Sign In", font_size="3em"),
        rx.input(on_change=State.set_user_signin_email, placeholder="Email", type_="email"),
        rx.input(on_change=State.set_user_signin_password, placeholder="Password", type_="password"),
        rx.button("Sign In", on_click=State.user_signin)
    )
