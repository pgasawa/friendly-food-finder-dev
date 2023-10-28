"""The friends page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.state import State
from friendly_food_finder_dev.pages.auth import require_google_login

import reflex as rx


@template(route="/friends", title="Friends")
@require_google_login
def friends() -> rx.Component:
    """The friends page.

    Returns:
        The UI for the friends page.
    """
    return rx.vstack(
        rx.heading("Friends", font_size="3em"),
        rx.input(on_change=State.set_user_add_friend_email, placeholder="Friend Email", type_="email"),
        rx.button("Add Friend", on_click=State.user_add_friend),
        rx.heading("Your Friends", font_size="2em"),
        rx.text("Coming Soon..."),
    )
