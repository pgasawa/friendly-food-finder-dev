"""Base state for the app."""

from typing import List
import reflex as rx
from friendly_food_finder_dev.firebase import firestore_client


class State(rx.State):
    """Base state for the app.

    The base state is used to store general vars used throughout the app.
    """
    curr_name: str
    curr_email: str

    user_create_name: str
    user_create_email: str
    user_create_password: str
    user_create_budget: float

    user_signin_email: str
    user_signin_password: str

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
            self.curr_name = self.user_create_name
            self.curr_email = self.user_create_email
            return rx.window_alert('You signed up!')

    def user_signin(self):
        with rx.session() as session:
            doc_data = firestore_client.read_from_document('user', self.user_signin_email)
            if doc_data is None:
                return rx.window_alert('The email does not exist')
            if doc_data['password'] != self.user_signin_password:
                return rx.window_alert('The password is incorrect')
            self.curr_email = self.user_signin_email
            self.curr_name = doc_data['name']
            return rx.window_alert(f'You signed in, {self.curr_name}!')

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

