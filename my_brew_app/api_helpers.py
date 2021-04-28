import requests
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
                'x-rapidapi-key': "1ddf0a8da3msh877010e622bf74dp10873cjsnd762a292965a",
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
