"""The feed page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login

import reflex as rx
import calendar
import datetime
from friendly_food_finder_dev.firebase import firestore_client
from friendly_food_finder_dev.state import State

@template(route="/feed", title="Feed")
@require_google_login
def feed() -> rx.Component:
    """The feed page.

    Returns:
        The UI for the feed page.
    """

    events = fetch_events()
    eventCards = [eventCard(event) for event in events]

    return rx.vstack(
        rx.heading("Feed", font_size="3em"),
        rx.text("Welcome to Feed!"),
        rx.text("Testing what happens rn"),
        *eventCards,
    )

def eventCard(event) -> rx.Component:
    attendees = event[0]
    restaurant = event[1]
    time = event[2]
    formatted_date = f"{calendar.month_name[int(time[5:7])]} {time[8:10]}, {time[0:4]} at {time[11:19]}"
    avatars = [rx.avatar(name=attendant, size="md") for attendant in attendees]

    return rx.card(
        rx.vstack(
            rx.center(
            rx.hstack(*avatars),
        ),
        rx.center(
            rx.image( src="https://media.photographycourse.net/wp-content/uploads/2022/04/08152906/food-photographer-ideas.jpg", width="200px", height="auto")
        ),
    ),
    header=rx.heading(f"Lunch at {restaurant}", size="lg"),
    footer=rx.heading(formatted_date, size="sm"),
)

def fetch_events():
    docs = firestore_client.get_all_documents_from_collection("event-logs")
    events = []
    for doc in docs:
        doc["time"] = doc["time"].isoformat()
        events.append([doc["attendees"], doc["restaurant"], doc["time"]])
    return events
