"""Base state for the app."""

import uuid
from typing import List
import reflex as rx
from friendly_food_finder_dev.firebase import firestore_client
from google.cloud.firestore import ArrayUnion, ArrayRemove
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
        user_doc_name = self.tokeninfo["email"]
        user_docref = firestore_client.db.collection("user").document(user_doc_name)
        user_docref.update({"friends": ArrayUnion([{self.user_add_friend_email: []}])})

    @rx.var
    def all_friends(self) -> List[dict[str, str]]:
        friend_docs = firestore_client.query_by_condition('friend', 'requester', '==', self.tokeninfo.get('email'))
        user_docs = []
        for friend_doc in friend_docs:
            user_doc = firestore_client.read_from_document('user', friend_doc['requestee'])
            user_docs.append(user_doc)
        return user_docs

    def update_friend_closeness(self, option, friend_email):
        user_doc_name = self.tokeninfo["email"]
        friend_data = firestore_client.read_from_document("user", user_doc_name)["friends"]
        print("HELLO IM FREAKING HERE",friend_email, friend_data)
        for friend in friend_data:
            if f
        if len(friend_data[friend_email]) > 1:
            friend_data[friend_email][0] = [option]
        else:
            friend_data[friend_email].append(option)
        user_docref = firestore_client.db.collection("user").document(user_doc_name)
        user_docref.update({"friends": ArrayRemove([friend_email])})
        firestore_client.write_data_to_collection("user", user_doc_name, friend_data)

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

    def get_google_token(self):
        return self.id_token_json

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
            if user_doc is None:
                firestore_client.write_data_to_collection('user', result['email'], {
                    'name': result['name'],
                    'email': result['email'],
                    'picture': result['picture'],
                    'friends': []
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

    @rx.cached_var
    def protected_content(self) -> str:
        if self.token_is_valid:
            return f"This content can only be viewed by a logged in User. Nice to see you {self.tokeninfo['name']}"
        return "Not logged in."
    
   