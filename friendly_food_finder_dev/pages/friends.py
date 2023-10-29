"""The friends page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.state import State
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.firebase import firestore_client
import reflex as rx

@template(route="/friends", title="Friends")
@require_google_login
def friends() -> rx.Component:
    """The friends page.

    Returns:
        The UI for the friends page.
    """

    return rx.vstack(
        rx.heading("Your Friends", font_size="3em"),
        rx.spacer(),
        rx.hstack(
            rx.input(on_change=State.set_user_add_friend_email, placeholder="Add Friend", type_="email"),
            rx.button("Add", on_click=State.user_add_friend, bg="lightblue", color="black"),
        ),
        rx.spacer(),
        rx.spacer(),
        rx.spacer(),
        rx.foreach(State.all_friends, friendComponent),
        rx.spacer()
    )

def friendComponent(friend):
    options = ["Hella tight", "Kinda close", "Lowkey chill"]

    return rx.hstack(
        rx.image(
            src=friend['picture'], width="100px", height="auto", border_radius="50%",
            padding_right="20px", padding_bottom="20px"
        ),
        rx.vstack(
            rx.text(friend['name'], font_size="18px", font_weight="bold"),
            rx.select(
                options,
                on_change=lambda value: State.update_friend_closeness(
                    value, friend["email"]
                ),
            ),
            padding_bottom="20px"
        ),
        rx.spacer()
    )
