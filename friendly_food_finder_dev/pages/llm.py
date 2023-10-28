import requests

friend_template = """Friend: {}
Cuisine Preferences: {}
Dietary Preferences: {}
Budget: {}

"""

restaurant_template = """Restaurant Name: {}
Yelp Categories: {}
Price Level: {}
Rating: {}

"""

prompt = """Instruction:
I have a few restaurants that I am considering to eat at with my friends. Below are my friends with their dietary preferences, as well as some restaurants of interest along with some relevant attributes for each restaurant.

Select the top {} restaurants that you think my friends would most enjoy eating at as a semicolon-separated list. Choose restaurants that match my friends' dietary/cuisine preferences and budgets the most, and rank them from your best choice to worst choice. Format your answer like: Restaurant 1; Restaurant 2; Restaurant 3; etc. Do not include any other text beyond this restaurant list in your response!

---
Friends:

{}

---
Restaurants:

{}

---
Response:
"""

def call_together_ai(prompt: str) -> str:
    endpoint = 'https://api.together.xyz/inference'
    TOGETHER_API_KEY = 'a98fedd4c4e8d8fb4f41445322b8e766e0f22b96346cde3c56d8b88f8ea5e7ba'

    res = requests.post(endpoint, json={
        'model': 'togethercomputer/llama-2-13b-chat',
        'prompt': prompt
    }, headers={
        'Authorization': f'Bearer {TOGETHER_API_KEY}',
        'User-Agent': 'Calhacks23'
    })

    return res.json()['choices'][0]['text']

def recommend_restaurants(users, restaurants, top_k=3):
    # 1. Prompt engineering
    friends_template = ""
    for user in users:
        cuisine_prefs = []
        if user["south_asian"]:
            cuisine_prefs.append("South Asian")
        if user["east_asian"]:
            cuisine_prefs.append("East Asian")
        if user["american"]:
            cuisine_prefs.append("American")
        if user["mexican"]:
            cuisine_prefs.append("Mexican")
        if user["mediterranean"]:
            cuisine_prefs.append("Mediterranean")
        if user["italian"]:
            cuisine_prefs.append("Italian")

        dietary_prefs = []
        if user["vegetarian"]:
            dietary_prefs.append("Vegetarian")
        if user["vegan"]:
            dietary_prefs.append("Vegan")

        cuisine_prefs_str = 'Okay with anything' if len(cuisine_prefs) == 0 else ', '.join(cuisine_prefs)
        dietary_prefs_str = 'Okay with anything' if len(dietary_prefs) == 0 else ', '.join(dietary_prefs)
        friend_template.format(user['name'], cuisine_prefs_str, dietary_prefs_str, user['budget'])
        friends_template += friend_template
    
    restaurants_template = ""
    for restaurant in restaurants:
        categories = sum(restaurant['categories'], [])
        categories = [x['title'] for x in categories]
        categories_str = ', '.join(categories)
        restaurant_template.format(restaurant['name'], categories_str, restaurant['price'], restaurant['rating'])
        restaurants_template += restaurant_template

    formatted_prompt = prompt.format(str(top_k), friends_template, restaurants_template)
    
    # 2. Call together.ai endpoint
    restaurant_names_filtered = set(call_together_ai(formatted_prompt).split(';'))
    restaurants_filtered = [r for r in restaurants if r['name'] in restaurant_names_filtered]
    return restaurants_filtered
