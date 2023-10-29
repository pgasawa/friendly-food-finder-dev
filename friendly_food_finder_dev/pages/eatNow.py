"""The eatNow page."""
from friendly_food_finder_dev.GoogleAPI import does_user_have_conflict
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.state import State
from friendly_food_finder_dev.firebase import firestore_client

import math
import reflex as rx
import random
import requests
import json
# import folium
import os

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
        # rx.checkbox_group(
        #     rx.checkbox("$", color_scheme="blue", size="md", onChange=State.lowToggle),
        #     rx.checkbox("$$", color_scheme="blue", size="md", onChange=State.midToggle),
        #     rx.checkbox("$$$", color_scheme="blue", size="md", onChange=State.highToggle),
        #     space="2em",
        # ),
        # rx.checkbox_group(
        #     rx.checkbox("Close", color_scheme="blue", size="md", onChange=State.closeToggle),
        #     rx.checkbox("Medium", color_scheme="blue", size="md", onChange=State.midToggle),
        #     rx.checkbox("Far", color_scheme="blue", size="md", onChange=State.farToggle),
        #     space="2em",
        # ),
        rx.spacer(),
        rx.hstack(
            rx.foreach(State.possible_meals,
                lambda meal: rx.card(
                    rx.vstack(
                        rx.heading(meal[0]),
                        rx.button("Invite!", on_click=lambda: State.invite(0, 0, 0)),
                        rx.hstack(
                            rx.link(
                                rx.text(meal[1]),
                                href=meal[2],
                                color="rgb(2,133,194)",
                            ),
                            rx.text(meal[3]),
                        ),
                        # rx.image(src=folium.Marker([meal[1].get('coordinates').get('latitude'), meal[1].get('coordinates').get('longitude')], tooltip=meal[1].get("mame")).add_to(folium.Map(location=[meal[1].get('coordinates').get('latitude'), meal[1].get('coordinates').get('longitude')], zoom_start=15)).get_root().render(), width="300px", height="300px"),
                        rx.image(src=meal[4], width="300px", height="250px"),
                    ),
            ))
                # rx.card(
                #     rx.vstack(
                #         rx.heading(meal[0]),
                #         rx.button("Invite!", on_click=lambda: State.invite(0, 0, 0)),
                #         rx.hstack(
                #             rx.link(
                #                 rx.text(meal[1].get("name")),
                #                 href=meal[1].get("url"),
                #                 color="rgb(2,133,194)",
                #             ),
                #             rx.text(meal[1].get("price")),
                #         ),
                #         # rx.image(src=folium.Marker([meal[1].get('coordinates').get('latitude'), meal[1].get('coordinates').get('longitude')], tooltip=meal[1].get("mame")).add_to(folium.Map(location=[meal[1].get('coordinates').get('latitude'), meal[1].get('coordinates').get('longitude')], zoom_start=15)).get_root().render(), width="300px", height="300px"),
                #         rx.image(src=meal[1].get("image_url"), width="300px", height="250px"),
                #     ),
                # )
                # for meal in State.possible_meals
        )
    )


