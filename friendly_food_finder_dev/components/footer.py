"""Sidebar component for the app."""

from friendly_food_finder_dev import styles
from friendly_food_finder_dev.state import State

import reflex as rx

def footer_item(text: str, icon: str, url: str) -> rx.Component:
    """Sidebar item.

    Args:
        text: The text of the item.
        icon: The icon of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The sidebar item component.
    """
    # Whether the item is active.
    active = (State.router.page.path.lower() == f"/{text.replace(' ', '').lower()}") | (
        (State.router.page.path == "/") & text == "Home"
    )

    return rx.link(
        rx.center(
            rx.image(
                src=icon,
                height="2.5em",
                padding="0.5em",
            ),
            bg=rx.cond(
                active,
                styles.accent_color,
                "#D2F0FC",
            ),
            color=rx.cond(
                active,
                styles.accent_text_color,
                styles.text_color,
            ),
            border_radius=styles.border_radius,
            box_shadow=styles.box_shadow,
            width="100%",
            padding_x="1em",
        ),
        href=url,
        width="100%",
    )


def footer() -> rx.Component:
    """The footer.

    Returns:
        The footer component.
    """
    # Get all the decorated pages and add them to the footer.
    from reflex.page import get_decorated_pages

    images = {
        '/eatNow': '/eat_now.png',
        '/feed': '/feed.png',
        '/friends': '/friends.png',
        '/scheduleEat': '/calendar-solid.svg',
        '/settings': '/settings.png',
        '/notifications': '/bell.png',
    }

    decorated_pages = []
    for pageTitle in ["Feed - OmNom", "Friends - OmNom", "Eat Now - OmNom", "Schedule Eat - OmNom", "Notifications - OmNom"]:
        for page in get_decorated_pages():
            if page.get("title") == pageTitle:
                decorated_pages.append(page)
                break

    return rx.box(
        rx.hstack(
            *[
                footer_item(
                    text=page.get("title", page["route"].strip("/").capitalize()),
                    icon=page.get("image", images[page["route"]]),
                    url=page["route"],
                )
                for page in decorated_pages if page.get("title", page["route"].strip("/").capitalize()) not in ["Auth - OmNom", "Home - OmNom", "Settings - OmNom"]
            ],
            width="100%",
            overflow_x="auto",
            align_items="flex-start",
            padding="1em",
        ),
        rx.spacer(),
        display=["none", "none", "block"],
        min_width=styles.sidebar_width,
        width="100%",
        height="5em",
        position="fixed",
        bottom="0px",
        border_top=styles.border,
        background_color="#cdedfa",
    )
