"""The feed page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.utils import prettydate

import reflex as rx
from friendly_food_finder_dev.state import State

@template(route="/notifications", title="Notifications")
@require_google_login
def notifications() -> rx.Component:
    """The notifs page.

    Returns:
        The UI for the notifs page.
    """

    return rx.vstack(
        rx.heading("Notifications", font_size="3em"),
        rx.text("Some people are thinking about you :)!"),
        
        rx.vstack(
            rx.foreach(State.incoming_invites,
                lambda invite: rx.card(
                    rx.vstack(
                        rx.heading(invite[11]),
                        rx.hstack(
                            rx.link(
                                rx.text(invite[1]),
                                href=invite[2],
                                color="rgb(2,133,194)",
                            ),
                            rx.text(invite[3]),
                        ),
                        rx.text(invite[5] + " minute(s) away"),
                        rx.text("Schedule for " + invite[8] + " to " + invite[9]),
                        rx.image(src=invite[4], width="300px", height="250px"),
                    ),
            ))
        ),
    )