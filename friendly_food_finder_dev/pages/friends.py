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
        rx.heading("Friends", font_size="3em"),
        rx.input(on_change=State.set_user_add_friend_email, placeholder="Friend Email", type_="email"),
        rx.spacer(),
        rx.button("Add Friend", on_click=State.user_add_friend),
        rx.spacer(),
        rx.heading("Your Friends", font_size="2em"),
        rx.foreach(State.all_friends, friendComponent)
    )

def friendComponent(friend):
    print(friend)
    options = ["Hella tight", "Kinda close", "Lowkey chill"]

    return rx.hstack(
        rx.image(
            src=friend['picture'], width="100px", height="auto"
        ),
        rx.vstack(
            rx.text(friend['name']),
            rx.select(
                options,
                on_change=lambda value: State.update_friend_closeness(
                    value, friend["email"]
                ),
            ),
        )
        
    )


