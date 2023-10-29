"""The eatNow page."""
from friendly_food_finder_dev.GoogleAPI import does_user_have_conflict
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.state import State
from friendly_food_finder_dev.firebase import firestore_client

import reflex as rx

from dotenv import load_dotenv

load_dotenv()

@template(route="/eatNow", title="Eat Now")
@require_google_login
def eatNow() -> rx.Component:
    """The eatNow page.

    Returns:
        The UI for the eatNow page.
    """
    
    return rx.vstack(
        rx.heading("Eat Now!", font_size="3em"),
        rx.text("Time to spontaneously eat!"),
        rx.spacer(),
        rx.hstack(
            rx.foreach(State.possible_meals,
                lambda meal: rx.card(
                    rx.vstack(
                        rx.heading(meal[0]),
                        rx.hstack(
                            rx.link(
                                rx.text(meal[1]),
                                href=meal[2],
                                color="rgb(2,133,194)",
                            ),
                            rx.text(meal[3]),
                        ),
                        rx.text(meal[5] + " minutes away"),
                        rx.button("Invite!", on_click=lambda: State.invite(0, 0, 0)),
                        rx.text("Schedule for " + meal[7] + " to " + meal[8]),
                        rx.image(src=meal[4], width="300px", height="250px"),
                    ),
            ))
        )
    )


