"""The feed page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login

import reflex as rx


@template(route="/feed", title="Feed")
@require_google_login
def feed() -> rx.Component:
    """The feed page.

    Returns:
        The UI for the feed page.
    """
    # return rx.vstack(
    #     eventComponent(),
    #     rx.center(
    #         rx.box(
    #             rx.heading("Feed", font_size="3em"),
    #             rx.text("Welcome to Feed!"),
    #             **styles.template_content_style,
    #         ),
    #     ),
    #     rx.text("Testing what happens rn"),
    # )
    return rx.vstack(
        rx.heading("Feed", font_size="3em"),
        rx.text("Welcome to Feed!"),
        rx.text("Testing what happens rn"),
    )

# def eventComponent() -> rx.Component:
#     firestore_client = Firebase.get_firestore_client()
#     events = firestore_client.get_all_documents_from_collection()
#     for event in events:
#         print(event)
#     return rx.card(
#     rx.text("Body of the Card Component"),
#     header=rx.heading("Header", size="lg"),
#     footer=rx.heading("Footer", size="sm"),
# )
