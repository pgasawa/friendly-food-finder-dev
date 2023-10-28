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
    update_vegetarian: bool = False
    update_vegan: bool = False
    update_south_asian: bool = False
    update_east_asian: bool = False
    update_american: bool = False
    update_mexican: bool = False
    update_mediterranean: bool = False
    update_italian: bool = False

    @rx.var
    def user_doc(self) -> dict[str, bool]:
        if self.tokeninfo is None or len(self.tokeninfo.keys()) == 0:
            return {}
        user_doc = firestore_client.read_from_document('user', self.tokeninfo['email'])
        if user_doc is None:
            user_doc = {
                'name': self.tokeninfo['name'],
                'email': self.tokeninfo['email'],
                'picture': self.tokeninfo['picture'],
                'token': GoogleAPI.get_user_token(),
                'vegetarian': False,
                'vegan': False,
                'south_asian': False,
                'east_asian': False,
                'american': False,
                'mexican': False,
                'mediterranean': False,
                'italian': False
            }
            firestore_client.write_data_to_collection('user', self.tokeninfo['email'], user_doc)
        
        self.set_update_vegetarian(user_doc['vegetarian'])
        self.set_update_vegan(user_doc['vegan'])
        self.set_update_south_asian(user_doc['south_asian'])
        self.set_update_east_asian(user_doc['east_asian'])
        self.set_update_american(user_doc['american'])
        self.set_update_mexican(user_doc['mexican'])
        self.set_update_mediterranean(user_doc['mediterranean'])
        self.set_update_italian(user_doc['italian'])

        return user_doc

    lowChecked: bool = False
    midChecked: bool = False
    highChecked: bool = False

    @rx.var
    def getLowToggle(self):
        return self.lowChecked

    def lowToggle(self):
        self.lowChecked = not self.lowChecked

    def midToggle(self):
        self.midChecked = not self.midChecked

    def highToggle(self):
        self.highChecked = not self.highChecked

    # @rx.var
    # def getPriceSet(self) -> List[str]:
    #     price_set = []
    #     if State.lowChecked:
    #         price_set.append("$")
    #     if State.midChecked:
    #         price_set.append("$$")
    #     if State.highChecked:
    #         price_set.append("$$$")
    #     return price_set

    closeChecked: bool = False
    midChecked: bool = False
    farChecked: bool = False

    def closeToggle(self):
        self.closeChecked = not self.closeChecked

    def midToggle(self):
        self.midChecked = not self.midChecked

    def farToggle(self):
        self.farChecked = not self.farChecked

    # @rx.var
    # def getRadius(self) -> int:
    #     radius = 0
    #     if self.lowChecked:
    #         radius = 300
    #     if self.midChecked:
    #         radius = 650
    #     if self.farChecked:
    #         radius = 1000
    #     print("Test:", radius)
    #     return radius

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
        return user_docs
    
    def update_profile(self, prefs: dict[str, bool]):
        new_doc = {
            'vegetarian': prefs['vegetarian'],
            'vegan': prefs['vegan'],
            'south_asian': prefs['south_asian'],
            'east_asian': prefs['east_asian'],
            'american': prefs['american'],
            'mexican': prefs['mexican'],
            'mediterranean': prefs['mediterranean'],
            'italian': prefs['italian']
        }
        firestore_client.update_data_in_collection('user', self.tokeninfo['email'], new_doc)

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