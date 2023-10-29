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
from datetime import datetime, timedelta
import requests

from friendly_food_finder_dev.GoogleAPI import does_user_have_conflict
from friendly_food_finder_dev.pages.llm import recommend_restaurants, collect_cuisine_prefs, collect_dietary_prefs, call_together_ai

from google.auth.transport import requests as googlerequests
from google.oauth2.id_token import verify_oauth2_token

from . import GoogleAPI

CLIENT_ID = "419615612188-fupdhp748n09ba2ibt0qi9633lk1pkhp.apps.googleusercontent.com"

expected_last_hangout = {
    'Hella tight': 14,
    'Kinda close': 21,
    'Lowkey chill': 30
}

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
                'friends': [],
                'latitude': 37.7845607111444,
                'longitude': -122.40337703253672
            }
            firestore_client.write_data_to_collection('user', self.tokeninfo['email'], user_doc)
        elif "token" not in user_doc:
            user_doc = {
                'token': GoogleAPI.get_user_token(),
            }
            firestore_client.update_data_in_collection('user', self.tokeninfo['email'], user_doc)
        
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

    def friend_insight(self, user, friend):
        prompt = """Instruction:
I'm building a social networking app for friends to hangout together and get food. Here is the signed in user's preferences:
Cuisine Preferences - {}
Dietary Preferences - {}

And here is their friend's preferences (name: {}):
Cuisine Preferences - {}
Dietary Preferences - {}

Write a small message, less than 15 words, describing an insight about how they are similar. Address the signed in user as "you". Don't include anything in your response except the message itself. Add a food emoji at the beginning of the message that's relevant to the cuisine/dietary preferences being described. It must be no less than 15 words - this is very important!
---
Response:
"""

        formatted_prompt = prompt.format(
            collect_cuisine_prefs(user),
            collect_dietary_prefs(user),
            friend['name'].split(' ')[0],
            collect_cuisine_prefs(friend),
            collect_dietary_prefs(friend)
        )

        return call_together_ai(formatted_prompt)

    def user_add_friend(self):
        friend_doc = firestore_client.read_from_document('user', self.user_add_friend_email)
        if friend_doc is None:
            return rx.window_alert('No user exists with this email!')
        friend_name = friend_doc['name']
        user_doc_name = self.tokeninfo["email"]
        user_docref = firestore_client.db.collection("user").document(user_doc_name)
        user_docref.update({"friends": ArrayUnion([{self.user_add_friend_email: {
            'closeness': "Hella tight",
            'last_hangout': 0,
            'similarities': self.friend_insight(self.user_doc, friend_doc),
        }}])})
        firestore_client.write_data_to_collection('friend', str(uuid.uuid1()), {
            'requester': self.tokeninfo['email'],
            'requestee': self.user_add_friend_email,
        })
        print("Success!")

    @rx.var
    def all_friends(self) -> List[dict[str, str]]:
        if self.id_token_json == "":
            return []

        friend_docs = firestore_client.query_by_condition('friend', 'requester', '==', self.tokeninfo.get('email'))
        user_docs = []
        for friend_doc in friend_docs:
            user_doc = firestore_client.read_from_document('user', friend_doc['requestee'])
            
            friend_data = firestore_client.read_from_document("user", self.tokeninfo.get('email'))["friends"]
            for i in range(len(friend_data)):
                if user_doc['email'] in friend_data[i]:
                    user_doc["last_hangout"] = friend_data[i][user_doc['email']]["last_hangout"]
                    user_doc["closeness"] = friend_data[i][user_doc['email']]["closeness"]
                    user_doc["similarities"] = friend_data[i][user_doc['email']]["similarities"]
                    break

            if expected_last_hangout[user_doc["closeness"]] <= user_doc["last_hangout"]:
                friendship_insight = "💡 It's been a while since you both hung out, so we'll recommend a hangout with {} soon!".format(user_doc['name'].split(' ')[0])
            else:
                friendship_insight = ""
            user_doc['friendship_insight'] = friendship_insight
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
                friend_data[i][friend_email]['closeness'] = option
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
            self.id_token_json = ""
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
    
    def calculate_time(self, lat1, lon1, lat2, lon2, speed=1.352, round=1):
        """
        speed = m/s walk
        """
        meter_distance = self.haversine(lat1, lon1, lat2, lon2)
        print("Meter", meter_distance)
        time_needed = ((meter_distance / speed / 60) // round) * round + round
        return int(time_needed)

    def get_free_friends(self, user):
        if 'email' not in self.tokeninfo:
            return []
        
        friend_emails = [list(x.keys())[0] for x in user.get('friends')]
        friends = [firestore_client.read_from_document('user', friend_email) for friend_email in friend_emails]
        friends = [friend for friend in friends if not does_user_have_conflict(friend, 0, 1)]
        friends = [friend for friend in friends if self.haversine(37.7845607111444, -122.40337703253672, friend['latitude'], friend['longitude']) < 1000]
        return friends

    @rx.var
    def current_path(self):
        return self.get_current_page()
    
    def invite(self, location, friendName, friendEmail, friendDistance, startTime, endTime, selfName, locationImage, selfDistance, expensiveness, locationurl, startDateTime):
        # Make sure the sender doesn't have an active invite already.
        if self.id_token_json == "":
            return None
        
        docs = firestore_client.get_all_documents_from_collection("invites")
        for doc in docs:
            if doc.get("sender") == self.tokeninfo["email"]:
                return
        
        invite_info = {
            'sender': self.tokeninfo["email"],
            'senderName': selfName,
            'receiver': friendEmail,
            'receiverName': friendName,
            'location': location,
            'locationurl': locationurl,
            'locationImage': locationImage,
            'senderTimeDistance': selfDistance,
            'expensiveness': expensiveness,
            'recieverTimeDistance': friendDistance,
            'startTime': startTime,
            'endTime': endTime,
            'startDateTime': startDateTime,
        }
        firestore_client.write_data_to_collection('invites', self.tokeninfo['email'], invite_info)

    counter : int = 0

    @rx.cached_var
    def incoming_invites(self) -> List[tuple[str, str, str]]:
        if self.id_token_json == "":
            return []
        
        invites = []
        docs = firestore_client.get_all_documents_from_collection("invites")
        for doc in docs:
            if doc.get("receiver") == self.tokeninfo["email"]:
                invites.append((doc.get("receiverName"), doc.get("location"), doc.get("locationurl"), 
                            doc.get("expensiveness"), doc.get("locationImage"), 
                            doc.get("senderTimeDistance"), doc.get("recieverTimeDistance"), max(doc.get("senderTimeDistance"), doc.get("recieverTimeDistance")),
                            doc.get("startTime"), doc.get("endTime"), 
                            doc.get("receiver"), doc.get("senderName"), doc.get("sender"), False, False))
        print(invites, self.counter)
        return invites

    @rx.cached_var
    def number_of_incoming_invite(self):
        if self.id_token_json == "":
            return []
        
        count = 0
        docs = firestore_client.get_all_documents_from_collection("invites")
        for doc in docs:
            if doc.get("receiver") == self.tokeninfo["email"]:
                count += 1
        return count
    
    def decline_incoming_invite(self, senderEmail):
        if self.id_token_json == "":
            return None
        
        docs = firestore_client.get_all_documents_from_collection("invites")
        for doc in docs:
            if doc.get("sender") == senderEmail and doc.get("receiver") == self.tokeninfo["email"]:
                firestore_client.delete_data_from_collection("invites", senderEmail)
        self.counter += 1

    def accept_incoming_invite(self, senderEmail):
        if self.id_token_json == "":
            return None

        docs = firestore_client.get_all_documents_from_collection("invites")
        for doc in docs:
            if doc.get("sender") == senderEmail and doc.get("receiver") == self.tokeninfo["email"]:
                print("MAKE CAL", senderEmail, [self.tokeninfo["email"]], doc.get("startDateTime"), doc.get("location"))
                GoogleAPI.send_cal_invite(senderEmail, [self.tokeninfo["email"]], doc.get("startDateTime"), doc.get("location"))
                firestore_client.delete_data_from_collection("invites", senderEmail)
            elif doc.get("receiver") == self.tokeninfo["email"]:
                firestore_client.delete_data_from_collection("invites", doc.get("sender"))
        self.counter += 1

    @rx.cached_var
    def possible_meals(self) -> List[tuple[str, str, str]]:
        if self.current_path != "/eatNow":
            return []
        else:
            docs = firestore_client.get_all_documents_from_collection("invites")
            for doc in docs:
                if doc.get("sender") == self.tokeninfo["email"]:
                    return [(doc.get("receiverName"), doc.get("location"), doc.get("locationurl"), 
                            doc.get("expensiveness"), doc.get("locationImage"), 
                            doc.get("senderTimeDistance"), doc.get("recieverTimeDistance"), max(doc.get("senderTimeDistance"), doc.get("recieverTimeDistance")),
                            doc.get("startTime"), doc.get("endTime"), 
                            doc.get("reciever"), doc.get("senderName"), True)]

            if 'email' not in self.tokeninfo:
                return []
            if self.id_token_json == "":
                return []
            # TODO need user doc
            user = firestore_client.read_from_document('user', self.tokeninfo["email"])
            friends = self.get_free_friends(user)
            if self.id_token_json == "":
                return []            
            
            # radius = 600
            # viable_list = self.get_nearby_restaurants(user, radius)

            viable_list = json.load(open('restaurant_pre_list.json', 'r'))['data']
            # get_nearby_restaurants(user, radius)

            price_set = ["$", "$$", "$$$", "$$$$"]

            viable_list = [x for x in viable_list if x.get("price") in price_set]
            possible_meals = {}
            friend_info = {}

            for friend in friends:
                friend_info[friend.get('email')] = friend
                intersection = [dict1 for dict1 in viable_list for dict2 in viable_list if dict1.get("name") == dict2.get("name")]
                if intersection:
                    possible_meals[friend.get('email')] = intersection

            for friend in friends:
                possible_meals[friend.get('email')] = viable_list

            keys = list(possible_meals.keys())
            random.shuffle(keys)

            selected_suggestions = []

            for key in keys[:3]:
                items = possible_meals[key]
                if len(items) == 0:
                    return []
                # selected_item = random.choice(items)
                users = [user, firestore_client.read_from_document('user', key)]
                selected_item = recommend_restaurants(users, items, top_k=1)

                friend = friend_info[key]

                userLat, userLong = user.get("latitude"), user.get("longitude")
                friendLat, friendLong = friend.get("latitude"), friend.get("longitude")
                restLat, restLong = selected_item.get("coordinates").get("latitude"), selected_item.get("coordinates").get("longitude")
                
                yourDistance = self.calculate_time(userLat, userLong, restLat, restLong)
                friendDistance = self.calculate_time(friendLat, friendLong, restLat, restLong)

                print(datetime.now())
                print(datetime.now() + timedelta(minutes=max(yourDistance, friendDistance)))
                earliestDateTime = datetime.now() + timedelta(minutes=max(yourDistance, friendDistance))
                # addMinutes = (int(earliestDateTime.strftime("%M")) % 5 + 4) // 5 * 5 - int(earliestDateTime.strftime("%M"))
                addMinutes = 5 # RNG
                print(earliestDateTime)
                print(addMinutes)
                startDateTime = earliestDateTime + timedelta(minutes=addMinutes)
                endDateTime = startDateTime + timedelta(hours=1)

                print(startDateTime.strftime("%I:%M %p"))
                print(endDateTime.strftime("%I:%M %p"))

                selected_suggestions.append((friend.get("name"), selected_item.get('name'), selected_item.get('url'), 
                                             selected_item.get('price'), selected_item.get('image_url'), 
                                            str(yourDistance), str(friendDistance), str(max(yourDistance, friendDistance)),
                                            startDateTime.strftime("%I:%M %p"), endDateTime.strftime("%I:%M %p"), 
                                            key, user.get("name"), False, startDateTime))

            # print(selected_suggestions)
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