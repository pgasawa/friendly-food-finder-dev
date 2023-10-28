"""The eatNow page."""
from friendly_food_finder_dev.GoogleAPI import does_user_have_conflict
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.state import State
from friendly_food_finder_dev.firebase import firestore_client

import math
import reflex as rx
import random
import requests
import os

from dotenv import load_dotenv

load_dotenv()

@template(route="/eatNow", title="Eat Now")
@require_google_login
def eatNow() -> rx.Component:
    """The eatNow page.

    Returns:
        The UI for the eatNow page.
    """
    return rx.vstack(
        rx.heading("Eat Now!", font_size="3em"),
        rx.text("Time to spontaneously eat!"),
        # rx.checkbox_group(
        #     rx.checkbox("$", color_scheme="blue", size="md", onChange=State.lowToggle),
        #     rx.checkbox("$$", color_scheme="blue", size="md", onChange=State.midToggle),
        #     rx.checkbox("$$$", color_scheme="blue", size="md", onChange=State.highToggle),
        #     space="2em",
        # ),
        # rx.checkbox_group(
        #     rx.checkbox("Close", color_scheme="blue", size="md", onChange=State.closeToggle),
        #     rx.checkbox("Medium", color_scheme="blue", size="md", onChange=State.midToggle),
        #     rx.checkbox("Far", color_scheme="blue", size="md", onChange=State.farToggle),
        #     space="2em",
        # ),
        rx.spacer(),
        rx.hstack(
            *[
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.link(
                                rx.text(meal[1].get("name")),
                                href=meal[1].get("url"),
                                color="rgb(2,133,194)",
                            ),
                            rx.text(meal[1].get("price")),
                        ),
                        rx.hstack(
                            rx.image(src=meal[1].get("image_url"), width="300px", height="300px"),
                        )
                    ),
                    header=rx.heading(meal[0]),
                )
                for meal in possible_meals()
            ]
        )
    )

def haversine(lat1, lon1, lat2, lon2):
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

def get_free_friends():
    friend_emails = [list(x.keys())[0] for x in firestore_client.read_from_document('user', 'ayushibatwara@gmail.com').get('friends')]
    friends = [firestore_client.read_from_document('user', friend_email) for friend_email in friend_emails]
    friends = [friend for friend in friends if not does_user_have_conflict(friend['email'], 0, 1)]
    friends = [friend for friend in friends if haversine(37.86531319642755, -122.2695501637612, friend['latitude'], friend['longitude']) < 1000]
    return friends

def possible_meals():
    friends = get_free_friends()
    
    radius = 600
    
    # TODO need user doc
    # user = firestore_client.read_from_document('user', State.tokeninfo['email'])
    user = firestore_client.read_from_document('user', 'ayushibatwara@gmail.com')
    viable_list = get_nearby_restaurants(user, radius)
    # price_set = []
    # if State.lowChecked:
    #     price_set.append("$")
    # if State.midChecked:
    #     price_set.append("$$")
    # if State.highChecked:
    #     price_set.append("$$$")
    price_set = ['$', '$$']
    # print(viable_list)
    viable_list = [x for x in viable_list if x.get("price") in price_set]
    possible_meals = {}

    for friend in friends:
        intersection = [dict1 for dict1 in viable_list for dict2 in get_nearby_restaurants(friend) if dict1.get("name") == dict2.get("name")]
        if intersection:
            possible_meals[friend.get('name')] = intersection
    print("TIGER", list(possible_meals.keys()))
    print("HELLO", possible_meals)
    keys = list(possible_meals.keys())
    random.shuffle(keys)

    selected_suggestions = []

    for key in keys[:3]:
        items = possible_meals[key]
        selected_item = random.choice(items)
        selected_suggestions.append((key, selected_item))

    return selected_suggestions

def get_nearby_restaurants(user, radius=600):
    api_key = os.environ.get('YELP_API_KEY')

    # TODO: get lat long by username
    latitude, longitude = 37.86531319642755, -122.2695501637612

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
