from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from my_brew_app.models import MyBrewUser, Breweries
from my_brew_app.forms import SignUpForm, LoginForm
import requests


# Create your views here.
def signup_view(request):
    context = {}
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

    form = SignUpForm()
    context.update({'form': form})
    return render(request, 'signup.html', context)


def login_view(request):
    context = {}
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
    form = LoginForm()
    context.update({
        'form': form
    })
    return render(request, 'login.html', context)


def home_view(request):
    context = {}

    brew_user = request.user
    favorite_list = list((brew_user.favorites.all()))
    fave_list_ids = []
    for brewery in favorite_list:
        fave_list_ids.append(brewery.id)

    # Get Local Breweries By User State
    url = "https://brianiswu-open-brewery-db-v1.p.rapidapi.com/breweries"
    querystring = {"by_state": request.user.state}
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
    brew_response = response.json()
    request.session['brew_response'] = (brew_response)

    local_brews = []
    for brew in brew_response:
        if request.user.city == brew['city']:
            local_brews.append(brew)

    user_initials = request.user.username[0:2]
    context.update({
        'user_initials': user_initials,
        'brew_response': brew_response,
        'local_brews': local_brews,
        'fave_list_ids': fave_list_ids
    })
    return render(request, 'home.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def favorite_brewery_view(request, brew_id):
    local_brews_response = request.session.get('brew_response')

    for brewery in local_brews_response:
        if brew_id == brewery['id']:
            Breweries.objects.create(
                id=brewery['id'],
                name=brewery['name'],
                brewer_type=brewery['brewery_type'],
                street=brewery['street'],
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
    return redirect('home')
