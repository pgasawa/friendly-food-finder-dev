"""Base state for the app."""

import uuid
from typing import List
import reflex as rx
from friendly_food_finder_dev.firebase import firestore_client

import os
import os.path
import json
import time

from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token

from . import GoogleAPI

CLIENT_ID = "419615612188-fupdhp748n09ba2ibt0qi9633lk1pkhp.apps.googleusercontent.com"

class State(rx.State):
    """Base state for the app.

    The base state is used to store general vars used throughout the app.
    """
    user_add_friend_email: str

    def user_add_friend(self):
        friend_doc = firestore_client.read_from_document('user', self.user_add_friend_email)
        if friend_doc is None:
            return rx.window_alert('No user exists with this email!')
        firestore_client.write_data_to_collection('friend', str(uuid.uuid1()), {
            'requester': self.tokeninfo['email'],
            'requestee': self.user_add_friend_email,
        })
        friend_name = friend_doc['name']

    @rx.var
    def all_friends(self) -> List[dict[str, str]]:
        friend_docs = firestore_client.query_by_condition('friend', 'requester', '==', self.tokeninfo.get('email'))
        user_docs = []
        for friend_doc in friend_docs:
            user_doc = firestore_client.read_from_document('user', friend_doc['requestee'])
            user_docs.append(user_doc)
        print(user_docs)
        return user_docs

    def user_show_available_friends():
        raise NotImplementedError

    def hangout_get_friend_clusters():
        raise NotImplementedError

    def hangout_get_restaurants():
        raise NotImplementedError

    def hangout_invite_create():
        raise NotImplementedError

    def hangout_invite_accept():
        raise NotImplementedError

    def hangout_invite_decline():
        raise NotImplementedError

    def feed_show():
        raise NotImplementedError

    def history_show():
        raise NotImplementedError
    
    id_token_json: str = rx.LocalStorage()

    def on_success(self, id_token: dict):
        self.id_token_json = json.dumps(id_token)

    @rx.cached_var
    def google_auth_token(self) -> dict[str, str]:
        try:
            return json.loads(self.id_token_json)
        except Exception as e:
            return {}

    @rx.cached_var
    def tokeninfo(self) -> dict[str, str]:
        try:
            result = verify_oauth2_token(
                json.loads(self.id_token_json)["credential"],
                requests.Request(),
                CLIENT_ID,
            )
            
            # Create user if it doesn't exist
            user_doc = firestore_client.read_from_document('user', result['email'])
            if user_doc is None or "token" not in user_doc:
                firestore_client.write_data_to_collection('user', result['email'], {
                    'name': result['name'],
                    'email': result['email'],
                    'picture': result['picture'],
                    'token': GoogleAPI.get_user_token()
                })

            return result
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