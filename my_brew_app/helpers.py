import requests
from decouple import config
import string
import random
from my_brew_app.forms import StateSearchForm


def state_search(request):
    if request.method == 'POST':
        form = StateSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Get Local Breweries By User State
            url = "https://brianiswu-open-brewery-db-v1.p.rapidapi.com/breweries"
            querystring = {"by_state": data['state_search']}
            headers = {
                'x-rapidapi-key': config('MY_BREW_API_KEY'),
                'x-rapidapi-host': "brianiswu-open-brewery-db-v1.p.rapidapi.com"
            }
            response = requests.request(
                "GET",
                url,
                headers=headers,
                params=querystring
            )
            state_brew_response = response.json()
            return state_brew_response


def string_generator():
    length = 16
    letters = string.ascii_lowercase
    numbers = string.digits
    url_snippet = ''.join(
        random.choice(letters + numbers) for i in range(length))
    return url_snippet
