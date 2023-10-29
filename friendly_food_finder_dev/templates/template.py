"""Common templates used between pages in the app."""

from __future__ import annotations

from friendly_food_finder_dev import styles
from friendly_food_finder_dev.components.footer import footer
from typing import Callable

import reflex as rx

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]


def menu_button() -> rx.Component:
    """The menu button on the top right of the page.

    Returns:
        The menu button component.
    """
    from reflex.page import get_decorated_pages

    return rx.box(
        rx.menu(
            rx.menu_button(
                rx.icon(
                    tag="hamburger",
                    size="4em",
                    color=styles.text_color,
                ),
            ),
            rx.menu_list(
                *[
                    rx.menu_item(
                        rx.link(
                            page["title"],
                            href=page["route"],
                            width="100%",
                        )
                    )
                    for page in get_decorated_pages() if 
                    page.get("title", page["route"].strip("/").capitalize()) not in ["Home", "Eat Now", "Feed", "Friends", "Schedule Eat", "Auth", "Notifications"]
                ]
            ),
        ),
        position="fixed",
        right="1.5em",
        top="1.5em",
        z_index="500",
    )

def logo() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(
                src="/omnom_loading.gif",
                width="64px",
                height="auto"
            ),
            rx.heading(
                "OmNom",
                font_family="Futura Extra Bold",
                color="#b0d644",
                font_size="1.5em"
            )
        ),
        box_shadow="md",
        border_radius="20px",
        padding="0.25em 1em",
        position="fixed",
        left="1.5em",
        top="1.5em",
        z_index="500",
    )


def template(
    route: str | None = None,
    title: str | None = None,
    image: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventHandler | list[rx.event.EventHandler] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app.

    Args:
        route: The route to reach the page.
        title: The title of the page.
        image: The favicon of the page.
        description: The description of the page.
        meta: Additionnal meta to add to the page.
        on_load: The event handler(s) called when the page load.
        script_tags: Scripts to attach to the page.

    Returns:
        The template with the page content.
    """

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        """The template for each page of the app.

        Args:
            page_content: The content of the page.

        Returns:
            The template with the page content.
        """
        # Get the meta tags for the page.
        all_meta = [*default_meta, *(meta or [])]

        @rx.page(
            route=route,
            title=title,
            image=image,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def templated_page():
            return rx.vstack(
                rx.hstack(
                    rx.box(
                        page_content(),
                        **styles.template_page_style,
                    ),
                    rx.spacer(),
                    menu_button(),
                    logo(),
                    align_items="flex-start",
                    transition="left 0.5s, width 0.5s",
                    position="sticky",
                ),
                footer(),
                padding_bottom="5em",
            ) 

        return templated_page

    return decorator
