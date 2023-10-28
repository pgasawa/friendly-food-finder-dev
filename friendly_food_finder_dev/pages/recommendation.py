
friend_template = """Friend: {}
Cuisine Preferences: {}
Dietary Preferences: {}
Budget: {}"""

restaurant_template = """Restaurant Name: {}
Yelp Categories: {}
Price Level: {}
Rating: {}"""

prompt = """I have a few restaurants that I am considering to eat at with my friends. Below are my friends with their dietary preferences, as well as some restaurants of interest along with some relevant attributes for each restaurant.

Select the top {} restaurants that you think my friends would most enjoy eating at. Choose restaurants that match my friends' dietary/cuisine preferences and budgets the most.

---
Friends:
{}

---
Restaurants:
{}

"""

def recommend_restaurants(users, restaurants):
    raise NotImplementedError
