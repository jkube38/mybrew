from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from itertools import chain
from decouple import config
from my_brew_app.models import MyBrewUser, Breweries
from my_brew_app.forms import SignUpForm, LoginForm, StateSearchForm
from my_brew_app.forms import UserUpdateForm
from my_brew_app.api_helpers import state_search
import requests


# Create your views here.
def signup_view(request):
    context = {}

# runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

# Creates a new user
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data['state'])
            MyBrewUser.objects.create(
                username=data['username'],
                email=data['email'],
                state=data['state'],
                city=data['city'],
                favorite_beer=data['favorite_beer'],
            )
            new_user = MyBrewUser.objects.get(username=data['username'])
            print(new_user, 'pass:', data['password'])
            new_user.set_password(data['password'])
            new_user.save()
            print(data)
            return redirect(reverse('login'))
        else:
            print()
    state_form = StateSearchForm()
    form = SignUpForm()
    context.update({
        'form': form,
        'state_form': state_form
    })
    return render(request, 'signup.html', context)


def login_view(request):
    context = {}

# runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            brew_user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            if brew_user:
                login(request, brew_user)
                return redirect('home')
    state_form = StateSearchForm()
    form = LoginForm()
    context.update({
        'form': form,
        'state_form': state_form
    })
    return render(request, 'login.html', context)


def home_view(request):
    context = {}
    favorite_list = []
    brew_response = []
    local_brews = []
    fave_list_ids = []
    local_brews_response = request.session.get('brew_response')
# runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'stateresults/{state_breweries[0]["state"]}/')

# if user is authenticated and brewery is in user favorites voting
# feature will be available
    brew_user = request.user
    if brew_user.is_anonymous is False:
        favorite_list = list((brew_user.favorites.all()))
        db_breweries = Breweries.objects.all()
        for brewery in favorite_list:
            fave_list_ids.append(brewery.id)


# Get Local Breweries By User State
        if not local_brews_response:
            url = "https://brianiswu-open-brewery-db-v1.p.rapidapi.com/breweries"
            querystring = {"by_state": request.user.state}
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
            brew_response = response.json()
            request.session['brew_response'] = (brew_response)

# Filters state search by users city
            local_brews = []
            for brew in brew_response:
                if request.user.city == brew['city']:
                    local_brews.append(brew)

# If brewery has been rated it will display the rating
            for brewery in db_breweries:
                for local in local_brews:
                    if brewery.id == local['id']:
                        local['rating'] = brewery.rating
        else:
            # Filters state search by users city
            local_brews = []
            for brew in local_brews_response:
                if request.user.city == brew['city']:
                    local_brews.append(brew)

# If brewery has been rated it will display the rating
            for brewery in db_breweries:
                for local in local_brews:
                    if brewery.id == local['id']:
                        local['rating'] = brewery.rating

    state_form = StateSearchForm()
    user_initials = request.user.username[0:2]
    context.update({
        'user_initials': user_initials,
        'brew_response': brew_response,
        'local_brews': local_brews,
        'fave_list_ids': fave_list_ids,
        'state_form': state_form
    })
    return render(request, 'home.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def favorite_brewery_view(request, brew_id):
    local_brews_response = request.session.get('brew_response')
    state_search_results = request.session.get('state_search_results')
    if local_brews_response and state_search_results:
        all_sessions = list(chain(local_brews_response, state_search_results))
    elif local_brews_response and not state_search_results:
        all_sessions = local_brews_response

# creates a list of brewery ids in our db
    db_breweries = Breweries.objects.all()
    db_brew_ids = []
    for brewery in db_breweries:
        db_brew_ids.append(brewery.id)

    for brewery in all_sessions:
        if brew_id == brewery['id'] and brew_id not in db_brew_ids:
            Breweries.objects.create(
                id=brewery['id'],
                name=brewery['name'],
                brewer_type=brewery['brewery_type'],
                street=brewery['street'],
                city=brewery['city'],
                state=brewery['state'],
                postal_code=brewery['postal_code'],
                country=brewery['country'],
                longitude=brewery['longitude'],
                latitude=brewery['latitude'],
                phone=brewery['phone'],
                website_url=brewery['website_url']
            )

    add_to_favorites = Breweries.objects.get(id=brew_id)
    request.user.favorites.add(add_to_favorites)
    request.user.save()
    if add_to_favorites.city == request.user.city:
        return redirect(reverse('home'))
    else:
        return redirect(f'/stateresults/{ add_to_favorites.state }/')


def rating_view(request, rated, brewery_id):
    update_brewery = Breweries.objects.get(id=brewery_id)
    new_rating_total = update_brewery.rating_total + rated
    new_num_votes = update_brewery.num_votes + 1
    new_rating = new_rating_total / new_num_votes

    update_brewery.rating_total = new_rating_total
    update_brewery.num_votes = new_num_votes
    update_brewery.rating = new_rating
    update_brewery.save()

    print(update_brewery.rating)

    if update_brewery.city == request.user.city:
        return redirect(reverse('home'))
    else:
        return redirect(f'/stateresults/{ update_brewery.state }/')


def state_view(request, state):
    context = {}
    state_search_results = request.session.get('state_search_results')
    db_breweries = Breweries.objects.all()

    fave_list_ids = []
    brew_user = request.user
    if brew_user.is_anonymous is False:
        favorite_list = list((brew_user.favorites.all()))
        for brewery in favorite_list:
            fave_list_ids.append(brewery.id)

        # saving this incase i put a city filter on the state search
        # state_brews = []
        # for brew in state_search_results:
        #     if request.user.city == brew['city']:
        #         state_brews.append(brew)

    # runs search bar in header
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

    for brewery in db_breweries:
        for state in state_search_results:
            if brewery.id == state['id']:
                state['rating'] = brewery.rating

    state_form = StateSearchForm()
    state = state_search_results[0]['state']
    context.update({
        'state_form': state_form,
        'search_results': state_search_results,
        'state': state,
        # 'state_brews': state_brews,
        'fave_list_ids': fave_list_ids
    })
    return render(request, 'state_results.html', context)


def update_user_view(request, user_id):

    context = {}

    # runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

    if request.method == 'POST':
        profile_form = UserUpdateForm(
            request.POST, request.FILES, instance=request.user
        )
        if profile_form.is_valid():
            profile_form.cleaned_data
            profile_form.save()
            return redirect(reverse('home'))
    else:
        profile_form = UserUpdateForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'state': request.user.state,
            'city': request.user.city,
            'favorite_beer': request.user.favorite_beer,
            'profile_pic': request.user.profile_pic
        })

    state_form = StateSearchForm()
    context.update({
        'profile_form': profile_form,
        'state_form': state_form
    })
    return render(request, 'update_user.html', context)


# Link to google maps https://maps.google.com/?q=<lat>,<lng>
# Try it in a modal

def error_404(request, exception):
    # runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

    return render(request, "404.html")


def error_500(request):
    # runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

    return render(request, "500.html")
