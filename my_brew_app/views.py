from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from itertools import chain
from decouple import config
from my_brew_app.models import MyBrewUser, TemporaryUrl
from my_brew_brewery.models import MyBrewBrewery
from my_brew_app.forms import SignUpForm, LoginForm, StateSearchForm
from my_brew_app.forms import ResetRequest, ResetPasswordForm
from my_brew_app.forms import UserUpdateForm
from my_brew_app.helpers import state_search, string_generator
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
            MyBrewUser.objects.create(
                username=data['username'],
                email=data['email'],
                state=data['state'].capitalize(),
                city=data['city'].capitalize(),
                favorite_beer=data['favorite_beer'],
            )
            new_user = MyBrewUser.objects.get(username=data['username'])
            new_user.set_password(data['password'])
            new_user.save()
            return redirect(reverse('login'))
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
    login_form = LoginForm()
    favorite_list = []
    brew_response = []
    local_brews = []
    fave_list_address = []
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
        db_breweries = MyBrewBrewery.objects.all()
        for brewery in favorite_list:
            fave_list_address.append(brewery.brewery_address)

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
                    if brewery.brewery_address == local['street']:
                        local['rating'] = brewery.brewery_rating

        else:
            # Filters state search by users city
            local_brews = []
            for brew in local_brews_response:
                if request.user.city == brew['city']:
                    local_brews.append(brew)

            for brewery in db_breweries:
                for local in local_brews:
                    if brewery.brewery_address == local['street']:
                        local['rating'] = brewery.brewery_rating

# Logs in a registered user
    login_form_errors = None
    login_form = LoginForm(request.POST or None)
    if request.method == "POST":
        if login_form.is_valid():
            brew_user = login_form.login(request)
            if brew_user:
                login(request, brew_user)
                return redirect('home')
        else:
            login_form_errors = login_form.non_field_errors

    login_form = LoginForm()
    state_form = StateSearchForm()
    user_initials = request.user.username[0:2]
    context.update({
        'user_initials': user_initials,
        'brew_response': brew_response,
        'local_brews': local_brews,
        'fave_list_address': fave_list_address,
        'state_form': state_form,
        'login_form': login_form,
        'favorite_list': favorite_list,
        'login_form_errors': login_form_errors
    })
    return render(request, 'home.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def favorite_brewery_view(request, brew_name):

    local_brews_response = request.session.get('brew_response')
    state_search_results = request.session.get('state_search_results')
    if local_brews_response and state_search_results:
        all_sessions = list(chain(local_brews_response, state_search_results))
    elif local_brews_response and not state_search_results:
        all_sessions = local_brews_response

# creates a list of brewery ids in our db
    db_breweries = MyBrewBrewery.objects.all()
    db_brew_names = []
    for brewery in db_breweries:
        db_brew_names.append(brewery.brewery_name)

    for brewery in all_sessions:
        if brew_name == brewery['name'] and brew_name not in db_brew_names:
            MyBrewBrewery.objects.create(
                brewery_name=brewery['name'],
                brewery_address=brewery['street'],
                brewery_city=brewery['city'].capitalize(),
                brewery_state=brewery['state'].capitalize(),
                brewery_zip=brewery['postal_code'][0:5],
                brewery_phone=brewery['phone'],
                brewery_website=brewery['website_url'],
            )
            break

    add_to_favorites = MyBrewBrewery.objects.get(brewery_name=brew_name)

    request.user.favorites.add(add_to_favorites)
    request.user.save()
    if add_to_favorites.brewery_city == request.user.city:
        return redirect(reverse('home'))
    else:
        print(add_to_favorites)
        return redirect(f'/stateresults/{ add_to_favorites.brewery_state }/')


def rating_view(request, rated, brewery_address):

    update_brewery = MyBrewBrewery.objects.get(brewery_address=brewery_address)

# updates and calculates the new rating values in brewery object
    new_rating_total = update_brewery.brewery_rating_total + rated
    new_num_votes = update_brewery.brewery_num_votes + 1
    new_rating = new_rating_total / new_num_votes

    update_brewery.brewery_rating_total = new_rating_total
    update_brewery.brewery_num_votes = new_num_votes
    update_brewery.brewery_rating = new_rating
    update_brewery.save()

    if update_brewery.brewery_city == request.user.city:
        return redirect(reverse('home'))
    else:
        return redirect(f'/stateresults/{ update_brewery.brewery_state }/')


def state_view(request, state):
    context = {}
    state_search_results = request.session.get('state_search_results')
    db_breweries = MyBrewBrewery.objects.all()

    fave_list_streets = []
# if the user is signed in creates a list of their favorites address
# gotta figure out how to use id's with id's coming back with response
    brew_user = request.user
    if brew_user.is_anonymous is False:
        favorite_list = list((brew_user.favorites.all()))
        for brewery in favorite_list:
            fave_list_streets.append(brewery.brewery_address)

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

# adds rating to the state search results json (dict)
    for brewery in db_breweries:
        for state in state_search_results:
            if brewery.brewery_address == state['street']:
                state['brewery_rating'] = brewery.brewery_rating

    state_form = StateSearchForm()
    state = state_search_results[0]['state']
    context.update({
        'state_form': state_form,
        'search_results': state_search_results,
        'state': state,
        # 'state_brews': state_brews,
        'fave_list_streets': fave_list_streets
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


def error_404(request, exception):
    context = {}
# runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')
    state_form = StateSearchForm()
    context.update({
        'state_form': state_form
    })
    return render(request, "404.html", context)


def error_500(request):
    context = {}
# runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')
    state_form = StateSearchForm()
    context.update({
        'state_form': state_form
    })
    return render(request, "500.html", context)


def reset_request_view(request):
    context = {}

# runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

# starts sending email process
    email = ''
    non_existent = False
    request_user = None
    form = ResetRequest()
    if request.method == 'POST':
        form = ResetRequest(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data['email']

            try:
                print('try: ', non_existent)
                user = MyBrewUser.objects.get(email=email)
            except MyBrewUser.DoesNotExist:
                non_existent = True
                print('except: ', non_existent)

            if non_existent is False:
                print('why am i in here', non_existent)
                request_user = user.username
                random_string = string_generator()

                TemporaryUrl.objects.create(
                    snippet=random_string,
                    user=request_user
                )

                random_snippet = TemporaryUrl.objects.get(snippet=random_string)

# Email Data
                subject = 'MyBrew Password Reset'
                from_email = None
                to = email
                text_content = 'Follow the link to reset your password'
                html_content = render_to_string('email.html', {
                    'request_user': request_user,
                    'random_snippet': random_snippet.snippet
                })

# Email Config
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

    state_form = StateSearchForm()
    context.update({
        'form': form,
        'email': email,
        'request_user': request_user,
        'state_form': state_form,
        'non_existent': non_existent
    })
    return render(request, 'reset_request.html', context)


def password_reset_view(request, username, snippet):

    # runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

    match_error = None

    temporary = TemporaryUrl.objects.get(snippet=snippet)
    if temporary:
        context = {}
        form = ResetPasswordForm()
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_password = data['password']
                retype = data['password2']

                if new_password == retype:
                    user = MyBrewUser.objects.get(username=username)
                    user.set_password(new_password)
                    user.save()
                    temporary.delete()
                    return redirect(reverse('login'))
                else:
                    match_error = 'Passwords did not match try again!'

        state_form = StateSearchForm()
        context.update({
            'form': form,
            'state_form': state_form,
            'match_error': match_error
        })

        return render(request, 'password_reset.html', context)
