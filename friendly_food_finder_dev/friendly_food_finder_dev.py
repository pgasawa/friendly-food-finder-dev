"""Welcome to Reflex!."""

from friendly_food_finder_dev import styles

# Import all the pages.
from friendly_food_finder_dev.pages import *
from friendly_food_finder_dev.routes import *

import reflex as rx

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.api.add_api_route('/user/create', user_create)
app.api.add_api_route('/user/signin', user_signin)
app.api.add_api_route('/user/setdietaryprefs', user_setdietaryprefs)
app.api.add_api_route('/user/setcuisineprefs', user_setcuisineprefs)
app.api.add_api_route('/user/addfriend', user_addfriend)
app.api.add_api_route('/user/showallfriends', user_showallfriends)
app.api.add_api_route('/user/showavailablefriends', user_showavailablefriends)
app.api.add_api_route('/hangout/getfriendclusters', hangout_getfriendclusters)
app.api.add_api_route('/hangout/getrestaurants', hangout_getrestaurants)
app.api.add_api_route('/hangout/invitecreate', hangout_invitecreate)
app.api.add_api_route('/hangout/inviteaccept', hangout_inviteaccept)
app.api.add_api_route('/hangout/invitedecline', hangout_invitedecline)
app.api.add_api_route('/feed/show', feed_show)
app.api.add_api_route('/history/show', history_show)

app.compile()
