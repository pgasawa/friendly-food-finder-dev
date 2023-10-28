import reflex as rx

config = rx.Config(
    app_name="friendly_food_finder_dev",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)