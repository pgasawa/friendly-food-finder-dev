# """The auth page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.state import State

import functools
import os
import time
from ..state import State

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token

import reflex as rx

from ..react_oauth_google import GoogleOAuthProvider, GoogleLogin

CLIENT_ID = "419615612188-fupdhp748n09ba2ibt0qi9633lk1pkhp.apps.googleusercontent.com"

def user_info(tokeninfo: dict) -> rx.Component:
    return rx.hstack(
        rx.avatar(
            name=tokeninfo["name"],
            src=tokeninfo["picture"],
            size="lg",
        ),
        rx.vstack(
            rx.heading(tokeninfo["name"], size="md"),
            rx.text(tokeninfo["email"]),
            align_items="flex-start",
        ),
        rx.button("Logout", on_click=State.logout),
        padding="10px",
    )


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

@template(route="/auth", title="Auth")
@require_google_login
def auth() -> rx.Component:
    """The auth page.

    Returns:
        The UI for the auth page.
    """
    return rx.vstack(
        rx.heading("Auth", font_size="3em"),
        rx.text(f"Welcome to auth, {State.tokeninfo['name']}!"),
        rx.button("Logout", on_click=State.logout)
    ) 
