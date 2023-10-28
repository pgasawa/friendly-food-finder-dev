import reflex as rx
from typing import List

class User(rx.Model, table=True):
    name: str
    email: str
    password: str
    dietary_prefs: List[str]
    cuisine_prefs: List[str]
    budget: float
    location_longitude: float
    location_latitude: float

class Restaurant(rx.Model, table=True):
    name: str
    description: str
    cuisine: str
    dietary_prefs: List[str]
    price: float
    location_longitude: float
    location_latitude: float

class Friend(rx.Model, table=True):
    requester: str
    requestee: str
    timestamp: int

class Hangout(rx.Model, table=True):
    user_ids: List[str]
    restaurant: str
    timestamp: int
