"""The feed page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.utils import prettydate

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
        rx.text("See what your friends have been up to!"),
        *eventCards,
    )

def eventCard(event) -> rx.Component:
    attendees = event[0]
    restaurant = event[1]
    time = event[2]
    description = event[3]
    picture = event[4]
    formatted_date = prettydate(datetime.datetime.fromisoformat(time).replace(tzinfo=None))

    attendant_docs = [
        firestore_client.read_from_document("user", attendant)
        for attendant in attendees
    ]

    avatars = [
        rx.image(src=attendant['picture'],
                 width="80px", height="auto", border_radius="50%",
                 padding_right="20px", padding_bottom="20px")
        for attendant in attendant_docs
    ]

    names = [
        attendant['name']
        for attendant in attendant_docs
    ]

    return rx.card(
        rx.vstack(
            rx.heading(f"Lunch at {restaurant}", size="md", width='100%', text_align='left'),
            rx.spacer(),
            rx.spacer(),
            rx.text('🕒  ' + formatted_date, font_size='14px', width='100%', text_align='left', as_="b"),
            rx.text('👥  ' + ', '.join(names), font_size='14px', width='100%', text_align='left'),
            rx.text(description, font_size='14px', width='100%', text_align='left'),
            rx.spacer(),
            rx.spacer(),
            rx.center(
                rx.hstack(*avatars),
            ),
            rx.center(
                rx.image(src=picture, width="200px", height="auto")
            ),
        ),
        width='500px'
    )

def fetch_events():
    docs = firestore_client.get_all_documents_from_collection("event-logs")
    events = []
    for doc in docs:
        doc["time"] = doc["time"].isoformat()
        events.append([doc["attendees"], doc["restaurant"], doc["time"], doc["description"], doc["picture"]])
    return events