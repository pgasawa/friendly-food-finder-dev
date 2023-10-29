"""The scheduleEat page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.state import State

import reflex as rx


@template(route="/scheduleEat", title="Schedule Eat - BiteBuddy")
@require_google_login
def scheduleEat() -> rx.Component:
    """The scheduleEat page.

    Returns:
        The UI for the scheduleEat page.
    """

    return rx.vstack(
        rx.heading("Week of October 30th — November 3rd!", font_size="3em"),
        rx.text("Let's plan the week."),
        rx.hstack(
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.text("Mon", as_="b"),
                        rx.text("10/30/2023")
                    ),
                    rx.image(
                        src="/paneer.png",
                        height="7.5em",
                    ),
                    rx.vstack(
                        rx.foreach(State.populate_clusters, lambda cluster: rx.text(cluster)),
                    ),
                ),
                footer=rx.heading("Footer", size="sm"),
                width="15em",
                height="32em",
            ),
            rx.spacer(),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.text("Tu", as_="b"),
                        rx.text("10/31/2023")
                    ),
                    rx.image(
                        src="/padthai.png",
                        height="7.5em",
                    ),
                ),
                footer=rx.heading("Footer", size="sm"),
                width="15em",
                height="32em",
            ),
            rx.spacer(),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.text("Wed", as_="b"),
                        rx.text("11/01/2023")
                    ),
                    rx.image(
                        src="/tacos.png",
                        height="7.5em",
                    ),
                ),
                footer=rx.heading("Footer", size="sm"),
                width="15em",
                height="32em",
            ),
            rx.spacer(),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.text("Thu", as_="b"),
                        rx.text("11/02/2023")
                    ),
                    rx.image(
                        src="/sesame-tofu.png",
                        height="7.5em",
                    ),
                ),
                footer=rx.heading("Footer", size="sm"),
                width="15em",
                height="32em",
            ),
            rx.spacer(),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.text("Fri", as_="b"),
                        rx.text("11/03/2023")
                    ),
                    rx.image(
                        src="/pho.png",
                        height="7.5em",
                    ),
                ),
                footer=rx.heading("Footer", size="sm"),
                width="15em",
                height="32em",
            ),
        ),
    )
