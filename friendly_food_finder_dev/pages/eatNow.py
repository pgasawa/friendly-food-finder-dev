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
                        rx.text(meal[5] + " minute(s) away"),
                        rx.button(rx.cond(meal[12], "Invited! ✔️", "Invite"), 
                                  is_disabled=rx.cond(meal[12], True, False),
                                  on_click=lambda: State.invite(meal[1], meal[0], meal[10], meal[6], meal[8], meal[9], meal[11], meal[4], meal[5], meal[3], meal[2], meal[13])
                                ), # Xd
                        
                        rx.text("Schedule for " + meal[8] + " to " + meal[9]),
                        # rx.image(src=folium.Marker([meal[1].get('coordinates').get('latitude'), meal[1].get('coordinates').get('longitude')], tooltip=meal[1].get("mame")).add_to(folium.Map(location=[meal[1].get('coordinates').get('latitude'), meal[1].get('coordinates').get('longitude')], zoom_start=15)).get_root().render(), width="300px", height="300px"),
                        rx.image(src=meal[4], width="300px", height="250px"),
                    ),
            ))
        )
    )


