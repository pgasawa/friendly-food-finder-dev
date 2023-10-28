"""Base state for the app."""

import reflex as rx

import os
import json
import time

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token

CLIENT_ID = "419615612188-fupdhp748n09ba2ibt0qi9633lk1pkhp.apps.googleusercontent.com"

class State(rx.State):
    """Base state for the app.

    The base state is used to store general vars used throughout the app.
    """

    def user_create():
        raise NotImplementedError

    def user_signin():
        raise NotImplementedError

    def user_setdietaryprefs():
        raise NotImplementedError

    def user_setcuisineprefs():
        raise NotImplementedError

    def user_addfriend():
        raise NotImplementedError

    def user_showallfriends():
        raise NotImplementedError

    def user_showavailablefriends():
        raise NotImplementedError

    def hangout_getfriendclusters():
        raise NotImplementedError

    def hangout_getrestaurants():
        raise NotImplementedError

    def hangout_invitecreate():
        raise NotImplementedError

    def hangout_inviteaccept():
        raise NotImplementedError

    def hangout_invitedecline():
        raise NotImplementedError

    def feed_show():
        raise NotImplementedError

    def history_show():
        raise NotImplementedError
    
    id_token_json: str = rx.LocalStorage()

    def on_success(self, id_token: dict):
        self.id_token_json = json.dumps(id_token)

    def get_google_token(self):
        return self.id_token_json

    @rx.cached_var
    def tokeninfo(self) -> dict[str, str]:
        try:
            return verify_oauth2_token(
                json.loads(self.id_token_json)["credential"],
                requests.Request(),
                CLIENT_ID,
            )
        except Exception as exc:
            if self.id_token_json:
                print(f"Error verifying token: {exc}")
        return {}

    def logout(self):
        self.id_token_json = ""

    @rx.var
    def token_is_valid(self) -> bool:
        try:
            return bool(
                self.tokeninfo
                and int(self.tokeninfo.get("exp", 0)) > time.time()
            )
        except Exception:
            return False

    @rx.cached_var
    def protected_content(self) -> str:
        if self.token_is_valid:
            return f"This content can only be viewed by a logged in User. Nice to see you {self.tokeninfo['name']}"
        return "Not logged in."

