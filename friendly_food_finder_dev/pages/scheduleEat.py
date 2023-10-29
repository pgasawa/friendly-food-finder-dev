"""The scheduleEat page."""
from friendly_food_finder_dev.templates import template
from friendly_food_finder_dev.pages.auth import require_google_login
from friendly_food_finder_dev.state import State

import reflex as rx
import random


@template(route="/scheduleEat", title="Schedule Eat - OmNom")
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
                        rx.text("Lunch at " + random.choice(["11:15am", "11:30am", "11:45am", "12:00pm", "12:15pm", "12:30pm", "12:45pm", "1:00pm", "1:15pm", "1:30pm"]), font_size="1em"),
                        rx.text("Location: " + random.choice(["Joyride Pizza - Yerba Buena Gardens", "The View Lounge", "Ippudo San Francisco", "Freshroll Vietnamese Rolls and Bowls", "Oren's Hummus", "Bodega", "Bimi Poke", "Fresca Garden", "The Harlequin"])),
                        rx.text("Who's going?"),
                        rx.hstack(
                            rx.foreach(State.populate_clusters[0:1], lambda cluster: 
                                rx.foreach(cluster, lambda person:
                                    rx.box(
                                        rx.tooltip(
                                            rx.image(
                                                src=person[2], width="40px", height="auto", border_radius="50%",
                                                padding_right="5px", padding_bottom="5px"
                                            ),
                                            # label=rx.text(person[1])),
                                            label=f"{person[1]}",
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        rx.button('Join event', color_scheme='whatsapp'),
                    ),
                ),
                # footer=rx.heading("Footer", size="sm"),
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
                    rx.vstack(
                        rx.text("Lunch at " + random.choice(["11:15am", "11:30am", "11:45am", "12:00pm", "12:15pm", "12:30pm", "12:45pm", "1:00pm", "1:15pm", "1:30pm"]), font_size="1em"),
                        rx.text("Location: " + random.choice(["Joyride Pizza - Yerba Buena Gardens", "The View Lounge", "Ippudo San Francisco", "Freshroll Vietnamese Rolls and Bowls", "Oren's Hummus", "Bodega", "Bimi Poke", "Fresca Garden", "The Harlequin"])),
                        rx.text("Who's going?"),
                        rx.hstack(
                            rx.foreach(State.populate_clusters[1:2], lambda cluster: 
                                rx.foreach(cluster, lambda person:
                                    rx.box(
                                        rx.tooltip(
                                            rx.image(
                                                src=person[2], width="40px", height="auto", border_radius="50%",
                                                padding_right="5px", padding_bottom="5px"
                                            ),
                                            # label=rx.text(person[1])),
                                            label=f"{person[1]}",
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        rx.button('Join event', color_scheme='whatsapp'),
                    ),
                ),
                # footer=rx.heading("Footer", size="sm"),
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
                    rx.vstack(
                        rx.text("Lunch at " + random.choice(["11:15am", "11:30am", "11:45am", "12:00pm", "12:15pm", "12:30pm", "12:45pm", "1:00pm", "1:15pm", "1:30pm"]), font_size="1em"),
                        rx.text("Location: " + random.choice(["Joyride Pizza - Yerba Buena Gardens", "The View Lounge", "Ippudo San Francisco", "Freshroll Vietnamese Rolls and Bowls", "Oren's Hummus", "Bodega", "Bimi Poke", "Fresca Garden", "The Harlequin"])),
                        rx.text("Who's going?"),
                        rx.hstack(
                            rx.foreach(State.populate_clusters[2:3], lambda cluster: 
                                rx.foreach(cluster, lambda person:
                                    rx.box(
                                        rx.tooltip(
                                            rx.image(
                                                src=person[2], width="40px", height="auto", border_radius="50%",
                                                padding_right="5px", padding_bottom="5px"
                                            ),
                                            # label=rx.text(person[1])),
                                            label=f"{person[1]}",
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        rx.button('Join event', color_scheme='whatsapp'),
                    ),
                ),
                # footer=rx.heading("Footer", size="sm"),
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
                    rx.vstack(
                        rx.text("Lunch at " + random.choice(["11:15am", "11:30am", "11:45am", "12:00pm", "12:15pm", "12:30pm", "12:45pm", "1:00pm", "1:15pm", "1:30pm"]), font_size="1em"),
                        rx.text("Location: " + random.choice(["Joyride Pizza - Yerba Buena Gardens", "The View Lounge", "Ippudo San Francisco", "Freshroll Vietnamese Rolls and Bowls", "Oren's Hummus", "Bodega", "Bimi Poke", "Fresca Garden", "The Harlequin"])),
                        rx.text("Who's going?"),
                        rx.hstack(
                            rx.foreach(State.populate_clusters[3:4], lambda cluster: 
                                rx.foreach(cluster, lambda person:
                                    rx.box(
                                        rx.tooltip(
                                            rx.image(
                                                src=person[2], width="40px", height="auto", border_radius="50%",
                                                padding_right="5px", padding_bottom="5px"
                                            ),
                                            # label=rx.text(person[1])),
                                            label=f"{person[1]}",
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        rx.button('Join event', color_scheme='whatsapp'),
                    ),
                ),
                # footer=rx.heading("Footer", size="sm"),
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
                    rx.vstack(
                        rx.text("Lunch at " + random.choice(["11:15am", "11:30am", "11:45am", "12:00pm", "12:15pm", "12:30pm", "12:45pm", "1:00pm", "1:15pm", "1:30pm"]), font_size="1em"),
                        rx.text("Location: " + random.choice(["Joyride Pizza - Yerba Buena Gardens", "The View Lounge", "Ippudo San Francisco", "Freshroll Vietnamese Rolls and Bowls", "Oren's Hummus", "Bodega", "Bimi Poke", "Fresca Garden", "The Harlequin"])),
                        rx.text("Who's going?"),
                        rx.hstack(
                            rx.foreach(State.populate_clusters[4:5], lambda cluster: 
                                rx.foreach(cluster, lambda person:
                                    rx.box(
                                        rx.tooltip(
                                            rx.image(
                                                src=person[2], width="40px", height="auto", border_radius="50%",
                                                padding_right="5px", padding_bottom="5px"
                                            ),
                                            # label=rx.text(person[1])),
                                            label=f"{person[1]}",
                                        ),
                                    ),
                                ),
                            ),
                        ),
                        rx.button('Join event', color_scheme='whatsapp'),
                    ),
                ),
                # footer=rx.heading("Footer", size="sm"),
                width="15em",
                height="32em",
            ),
        ),
    )