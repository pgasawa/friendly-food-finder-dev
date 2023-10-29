"""Base state for the app."""

import uuid
from typing import List
import reflex as rx
from friendly_food_finder_dev.firebase import firestore_client
from google.cloud.firestore import ArrayUnion, ArrayRemove
import os
import os.path
import json
import time
import math
import random
import requests

from friendly_food_finder_dev.GoogleAPI import does_user_have_conflict

from google.auth.transport import requests as googlerequests
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
    update_budget: str = '$'

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
                'italian': False,
                'budget': '$',
                'friends': []
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
        self.set_update_budget(user_doc['budget'])

        return user_doc

    # lowChecked: bool = False
    # midChecked: bool = False
    # highChecked: bool = False

    # @rx.var
    # def getLowToggle(self):
    #     return self.lowChecked

    # def lowToggle(self):
    #     self.lowChecked = not self.lowChecked

    # def midToggle(self):
    #     self.midChecked = not self.midChecked

    # def highToggle(self):
    #     self.highChecked = not self.highChecked

    # @rx.var
    # def getPriceSet(self) -> List[str]:
    #     price_set = []
    #     if self.lowChecked:
    #         price_set.append("$")
    #     if self.midChecked:
    #         price_set.append("$$")
    #     if self.highChecked:
    #         price_set.append("$$$")
    #     return price_set

    # closeChecked: bool = False
    # midChecked: bool = False
    # farChecked: bool = False

    # def closeToggle(self):
    #     self.closeChecked = not self.closeChecked

    # def midToggle(self):
    #     self.midChecked = not self.midChecked

    # def farToggle(self):
    #     self.farChecked = not self.farChecked

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

    def invite(self, recipient, startTime, endTime, ):
        print(self.tokeninfo)
        pass

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
        user_docref.update({"friends": ArrayUnion([{self.user_add_friend_email: {'closeness': "Hella tight"}}])})

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
            'italian': prefs['italian'],
            'budget': prefs['budget']
        }
        firestore_client.update_data_in_collection('user', self.tokeninfo['email'], new_doc)


    def update_friend_closeness(self, option, friend_email):
        user_doc_name = self.tokeninfo["email"]
        friend_data = firestore_client.read_from_document("user", user_doc_name)["friends"]
        for i in range(len(friend_data)):
            if friend_email in friend_data[i]:
                friend_data[i][friend_email] = {"closeness": option}
        user_docref = firestore_client.db.collection("user").document(user_doc_name)
        user_docref.update({"friends": friend_data})

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
                googlerequests.Request(),
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

    @rx.cached_var
    def protected_content(self) -> str:
        if self.token_is_valid:
            return f"This content can only be viewed by a logged in User. Nice to see you {self.tokeninfo['name']}"
        return "Not logged in."
    
    ### eatNow Logic ###

    def haversine(self, lat1, lon1, lat2, lon2):
        # Radius of the Earth in meters
        earth_radius = 6371000

        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c

        return distance

    def get_free_friends(self):
        if 'email' not in self.tokeninfo:
            return []
        print("SLEEP", self.id_token_json)
        print("SELF", self.tokeninfo)
        friend_emails = [list(x.keys())[0] for x in firestore_client.read_from_document('user', self.tokeninfo["email"]).get('friends')]
        friends = [firestore_client.read_from_document('user', friend_email) for friend_email in friend_emails]
        friends = [friend for friend in friends if not does_user_have_conflict(friend['email'], 0, 1)]
        friends = [friend for friend in friends if self.haversine(37.7845607111444, -122.40337703253672, friend['latitude'], friend['longitude']) < 1000]
        return friends

    @rx.var
    def possible_meals(self) -> List[tuple[str, str, str]]:
        if 'email' not in self.tokeninfo:
            return []
        if self.id_token_json == "":
            return []
        friends = self.get_free_friends()
        
        radius = 600
        
        # TODO need user doc
        user = firestore_client.read_from_document('user', self.tokeninfo["email"])
        # viable_list = self.get_nearby_restaurants(user, radius)
        viable_list = json.load(open('restaurant_pre_list.json', 'r'))['data']
        # get_nearby_restaurants(user, radius)

        price_set = ["$", "$$", "$$$", "$$$$"]
        print("HFIUWEHFIU", price_set)

        viable_list = [x for x in viable_list if x.get("price") in price_set]
        possible_meals = {}

        for friend in friends:
            intersection = [dict1 for dict1 in viable_list for dict2 in viable_list if dict1.get("name") == dict2.get("name")]
            if intersection:
                possible_meals[friend.get('name')] = intersection

        for friend in friends:
            possible_meals[friend.get('name')] = viable_list

        keys = list(possible_meals.keys())
        random.shuffle(keys)

        selected_suggestions = []

        for key in keys[:3]:
            items = possible_meals[key]
            if len(items) == 0:
                return []
            selected_item = random.choice(items)
            selected_suggestions.append((key, selected_item.get('name'), selected_item.get('url'), selected_item.get('price'), selected_item.get('image_url')))

        print(selected_suggestions)
        return selected_suggestions

    def get_nearby_restaurants(self, user, radius=600):
        api_key = os.environ.get('YELP_API_KEY')

        # TODO: get lat long by username
        latitude, longitude = 37.7845607111444, -122.40337703253672

        # Set the search parameters
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'categories': 'restaurants',
            'radius': radius,  # Search radius in meters
        }

        url = 'https://api.yelp.com/v3/businesses/search'

        headers = {
            'Authorization': f'Bearer {api_key}',
        }

        response = requests.get(url, headers=headers, params=params)

        is_vegetarian = user.get('vegetarian')
        is_vegan = user.get('vegan')

        restaurants = []
        if response.status_code == 200:
            data = response.json()
            for business in data.get('businesses', []):
                if is_vegetarian or is_vegan:
                    if is_vegan:
                        if business.get('attributes') and business['attributes'].get('liked_by_vegans'):
                            restaurants.append(business)
                    else:
                        if business.get('attributes') and business['attributes'].get('liked_by_vegetarians'):
                            restaurants.append(business)
                else:
                    restaurants.append(business)
                restaurants.append(business)
        else:
            print(f"Error: {response.status_code} - {response.text}")

        return restaurants