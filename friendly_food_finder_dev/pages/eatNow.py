"""The eatNow page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login

import reflex as rx
import requests
import os

@template(route="/eatNow", title="Eat Now")
@require_google_login
def eatNow() -> rx.Component:
    """The eatNow page.

    Returns:
        The UI for the eatNow page.
    """
    nearby = get_nearby_restaurants(1)
    return rx.vstack(
        rx.heading("Eat Now!", font_size="3em"),
        rx.text("Time to spontaneously eat!"),
        rx.image(src=nearby[0].get('image_url'), height="7.5em"),
        rx.text(nearby),
    )

def get_free_friends():
    friends = []
    # TODO: filter friends by who is free for the next hour.

    # TODO: filter friends by who is within a certain distance.
    return friends

def possible_restaurants_by_loc(user, friends):
    viable_list = get_nearby_restaurants(user)

    for friend in friends:
        viable_list = [dict1 for dict1 in viable_list for dict2 in get_nearby_restaurants(friend) if dict1.get("name") == dict2.get("name")]
    return viable_list

def get_nearby_restaurants(username):
    api_key = os.environ['YELP_API_KEY']

    # TODO: get lat long by username
    latitude, longitude = 37.86531319642755, -122.2695501637612

    # Set the search parameters
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'categories': 'restaurants',
        'radius': 800,  # Search radius in meters
    }

    # Define the API endpoint URL
    url = 'https://api.yelp.com/v3/businesses/search'

    # Set the request headers to include your API Key
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    # Send the GET request to the Yelp API
    response = requests.get(url, headers=headers, params=params)

    restaurants = []
    # Check the response status code
    if response.status_code == 200:
        data = response.json()
        # Iterate through the results and print restaurant names
        for business in data.get('businesses', []):
            restaurants.append(business)
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return restaurants
