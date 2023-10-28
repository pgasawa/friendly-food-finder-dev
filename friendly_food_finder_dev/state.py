"""Base state for the app."""

import uuid
from typing import List
import reflex as rx
from friendly_food_finder_dev.firebase import firestore_client

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
    curr_name: str
    curr_email: str

    user_signin_email: str
    user_signin_password: str

    user_addfriend_email: str
    
    def user_signin(self):
        doc_data = firestore_client.read_from_document('user', self.user_signin_email)
        if doc_data is None:
            return rx.window_alert('The email does not exist')
        if doc_data['password'] != self.user_signin_password:
            return rx.window_alert('The password is incorrect')
        self.curr_email = self.user_signin_email
        self.curr_name = doc_data['name']
        return rx.window_alert(f'You signed in, {self.curr_name}!')

    def user_addfriend(self):
        if not self.curr_email or len(self.curr_email) == 0:
            return rx.window_alert('You are not signed in!')
        friend_doc = firestore_client.read_from_document('user', self.user_addfriend_email)
        if friend_doc is None:
            return rx.window_alert('No user exists with this email!')
        firestore_client.write_data_to_collection('friend', str(uuid.uuid1()), {
            'requester': self.curr_email,
            'requestee': self.user_addfriend_email,
        })
        friend_name = friend_doc['name']
        return rx.window_alert(f'You are now friends with {friend_name}!')

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

