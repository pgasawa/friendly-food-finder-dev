"""Base state for the app."""

from typing import List
import reflex as rx
from friendly_food_finder_dev.firebase import firestore_client


class State(rx.State):
    """Base state for the app.

    The base state is used to store general vars used throughout the app.
    """
    user_create_name: str
    user_create_email: str
    user_create_password: str
    user_create_budget: float

    def user_create(self):
        with rx.session() as session:
            firestore_client.write_data_to_collection('user', self.user_create_email, {
                'name': self.user_create_name,
                'email': self.user_create_email,
                'password': self.user_create_password,
                'budget': self.user_create_budget,
                'dietary_prefs': ['Vegan'],
                'cuisine_prefs': ['Your mom'],
                'location_longitude': 37.784161,
                'location_latitude': -122.403549
            })
            return rx.window_alert('You signed up!')

    def user_signin():
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

