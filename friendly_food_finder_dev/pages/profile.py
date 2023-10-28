"""The profile page."""
from typing import List
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.state import State
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.firebase import firestore_client

import functools
from ..state import State

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token

import reflex as rx

budget_options: List[str] = ['$', '$$', '$$$', '$$$$']

budget_options: List[str] = ['$', '$$', '$$$', '$$$$']

from ..react_oauth_google import GoogleOAuthProvider, GoogleLogin

CLIENT_ID = "419615612188-fupdhp748n09ba2ibt0qi9633lk1pkhp.apps.googleusercontent.com"


def login() -> rx.Component:
    return rx.vstack(
        GoogleLogin.create(on_success=State.on_success),
    )


def require_google_login(page) -> rx.Component:
    @functools.wraps(page)
    def _auth_wrapper() -> rx.Component:
        return GoogleOAuthProvider.create(
            rx.cond(
                State.is_hydrated,
                rx.cond(State.token_is_valid, page(), login()),
                rx.spinner(),
            ),
            client_id=CLIENT_ID
        )
    return _auth_wrapper

@template(route="/settings", title="Settings")
@require_google_login
def profile() -> rx.Component:
    """The profile page.

    Returns:
        The UI for the profile page.
    """

    return rx.vstack(
        rx.heading("Profile", font_size="3em"),
        rx.image(
            src=State.tokeninfo['picture'], width="100px", height="auto"
        ),
        rx.table_container(
            rx.table(
                rows=[
                    ("Name", State.tokeninfo['name']),
                    ("Email", State.tokeninfo['email']),
                    ("Dietary Preferences", rx.vstack(
                        rx.switch('Vegetarian', is_checked=State.update_vegetarian, on_change=State.set_update_vegetarian),
                        rx.switch('Vegan', is_checked=State.update_vegan, on_change=State.set_update_vegan),
                    )),
                    ("Cuisine Preferences", rx.vstack(
                        rx.switch('South Asian', is_checked=State.update_south_asian, on_change=State.set_update_south_asian),
                        rx.switch('East Asian', is_checked=State.update_east_asian, on_change=State.set_update_east_asian),
                        rx.switch('American', is_checked=State.update_american, on_change=State.set_update_american),
                        rx.switch('Mexican', is_checked=State.update_mexican, on_change=State.set_update_mexican),
                        rx.switch('Mediterranean', is_checked=State.update_mediterranean, on_change=State.set_update_mediterranean),
                        rx.switch('Italian', is_checked=State.update_italian, on_change=State.set_update_italian),
                    )),
                    ("Budget per meal", rx.select(
                        budget_options,
                        value=State.update_budget,
                        on_change=State.set_update_budget
                    ))
                ],
            )
        ),
        rx.button("Save Changes", on_click=lambda: State.update_profile({
            'vegetarian': State.update_vegetarian,
            'vegan': State.update_vegan,
            'south_asian': State.update_south_asian,
            'east_asian': State.update_east_asian,
            'american': State.update_american,
            'mexican': State.update_mexican,
            'mediterranean': State.update_mediterranean,
            'italian': State.update_italian,
            'budget': State.update_budget
        })),
        rx.button("Logout", on_click=State.logout),
    )
