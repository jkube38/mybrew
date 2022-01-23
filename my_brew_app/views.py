from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from itertools import chain
from decouple import config
from my_brew_app.models import MyBrewUser, TemporaryUrl
from my_brew_brewery.models import MyBrewBrewery
from my_brew_app.forms import SignUpForm, LoginForm, StateSearchForm
from my_brew_app.forms import ResetRequest, ResetPasswordForm
from my_brew_app.forms import UserUpdateForm, UserSearchForm
from my_brew_posts.forms import UserPostForm, PostCommentForm, EditPostForm
from my_brew_app.helpers import state_search
from my_brew_app.helpers import string_generator
from my_brew_notifications.views import header_notifications_view
from my_brew_posts.post_helpers import sort_posts, all_current_posts
from my_brew_posts.post_helpers import current_user_posts
from my_brew_posts.views import user_post_view
import requests


# Create your views here.
def signup_view(request):
    '''Provides form for user to register'''
    if request.is_ajax():
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                MyBrewUser.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    username=data['usernameSU'],
                    email=data['email'],
                    state=data['state'].capitalize(),
                    city=data['city'].capitalize(),
                    favorite_beer=data['favorite_beer'],
                )

                new_user = MyBrewUser.objects.get(username=data['usernameSU'])
                new_user.set_password(data['passwordSU'])
                new_user.save()
                return HttpResponse('success')

            except IntegrityError as e:
                error = str(e.__cause__)
                error_type = error.split('.')[-1]
                if error_type == 'email':
                    return HttpResponse(error_type)
                elif error_type == 'username':
                    return HttpResponse(error_type)
    return HttpResponse('oops')


def home_view(request):
    '''Determines user and directs accordingling to landing page
        or homepage with breweries in the users city. Allows for
        state search, login, forgot password link, signup link'''

    context = {}
    login_form = LoginForm()
    favorite_list = []
    local_brews = []
    fave_list_id = []
    local_brews_response = request.session.get('brew_response')
    notifications = header_notifications_view(request)
# runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

# if user is authenticated and brewery is in user followed breweries voting
# feature will be available
    brew_user = request.user
    endpoint = 'https://brianiswu-open-brewery-db-v1.p.rapidapi.com/breweries'
    if brew_user.is_anonymous is False:
        favorite_list = list((brew_user.followed_brewery.all()))
        db_breweries = MyBrewBrewery.objects.all()
        for brewery in favorite_list:
            fave_list_id.append(brewery.id)

# Get Local Breweries By User State
        if not local_brews_response:
            url = endpoint
            querystring = {"by_state": request.user.state}
            headers = {
                'x-rapidapi-key': config('MY_BREW_API_KEY'),
                'x-rapidapi-host':
                "brianiswu-open-brewery-db-v1.p.rapidapi.com"
            }
            response = requests.request(
                "GET",
                url,
                headers=headers,
                params=querystring
            )
            brew_response = response.json()

            request.session['brew_response'] = (brew_response)
# Filters state search by users city if using api response
            local_brews = []
            for brew in brew_response:
                if request.user.city == brew['city']:
                    local_brews.append(brew)

# if brewery is in our db, id of response is changed to match our db
# also adds the brewery rating to the response
            for brewery in db_breweries:
                for local in local_brews:
                    if brewery.brewery_name == local['name']:
                        local['id'] = brewery.id
                        local['rating'] = brewery.brewery_rating

# Filters state search by users city if using session
        else:
            local_brews = []
            for brew in local_brews_response:
                if request.user.city == brew['city']:
                    local_brews.append(brew)
# if brewery is in our db, id of response is changed to match our db
# also adds the brewery rating to the response
            for brewery in db_breweries:
                for local in local_brews:
                    if brewery.brewery_name == local['name']:
                        local['id'] = brewery.id
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

    signup_form = SignUpForm()
    login_form = LoginForm()
    state_form = StateSearchForm()
    user_initials = request.user.username[0:2]
    user_search_form = UserSearchForm()
    print(favorite_list)
    context.update({
        'user_initials': user_initials,
        'local_brews': local_brews,
        'fave_list_id': fave_list_id,
        'state_form': state_form,
        'login_form': login_form,
        'favorite_list': favorite_list,
        'login_form_errors': login_form_errors,
        'notifications': notifications,
        'signup_form': signup_form,
        'user_search_form': user_search_form
    })
    return render(request, 'home.html', context)


@login_required(login_url='/')
def user_profile_view(request, username):
    '''Displays all of a users information'''
    context = {}

    user = MyBrewUser.objects.get(username=username)

    notifications = header_notifications_view(request)

    relevant_posts = []

    post_list_selector = request.path.split('/')[3]
    if post_list_selector == 'followingVine':
        relevant_posts = sort_posts(request, username)
    elif post_list_selector == 'myVine':
        relevant_posts = current_user_posts(request)
    elif post_list_selector == 'exploreVine':
        relevant_posts = all_current_posts()

# runs the post, comment submit form
    post_form = user_post_view(request)

# runs the header search bar
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

    following_users = user.followed_user.all()
    following_usernames = [
        follow.username for follow in request.user.followed_user.all()]
    following_breweries = user.followed_brewery.all()
    initials = user.username[:2]

    state_form = StateSearchForm()
    user_search_form = UserSearchForm()
    post_form = UserPostForm()
    edit_post_form = EditPostForm()
    comment_form = PostCommentForm()
    context.update({
        'state_form': state_form,
        'user': user,
        'initials': initials,
        'following_users': following_users,
        'following_breweries': following_breweries,
        'post_form': post_form,
        'relevant_posts': relevant_posts,
        'following_usernames': following_usernames,
        'notifications': notifications,
        'comment_form': comment_form,
        'user_search_form': user_search_form,
        'edit_post_form': edit_post_form
    })
    return render(request, 'user_profile.html', context)


def logout_view(request):
    '''User Logout'''
    logout(request)
    return redirect(reverse('home'))


def favorite_brewery_view(request, brew_name):
    '''allows users to add a brewery to their followed breweries and if
        the brewery is not already in our db it adds it.'''

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

    add_to_followed_brewery = MyBrewBrewery.objects.get(brewery_name=brew_name)

    request.user.followed_brewery.add(add_to_followed_brewery)
    request.user.save()
    if add_to_followed_brewery.brewery_city == request.user.city:
        return redirect(reverse('home'))
    else:
        print(add_to_followed_brewery)
        return redirect(
            f'/stateresults/{add_to_followed_brewery.brewery_state }/')


def state_view(request, state):
    '''Returns the state search results from the header search bar'''
    context = {}
    notifications = header_notifications_view(request)
# runs search bar in header
    state_breweries = state_search(request)
    if state_breweries:
        request.session['state_search_results'] = state_breweries
        return redirect(f'/stateresults/{state_breweries[0]["state"]}/')

    state_search_results = request.session.get('state_search_results')
    db_breweries = MyBrewBrewery.objects.all()

# if the user is signed in, creates a list of their followed brewery id's
    fave_list_ids = []
    brew_user = request.user
    if brew_user.is_anonymous is False:
        favorite_list = list((brew_user.followed_brewery.all()))
        for brewery in favorite_list:
            fave_list_ids.append(brewery.id)

# saving this incase i put a city filter on the state search
        # state_brews = []
        # for brew in state_search_results:
        #     if request.user.city == brew['city']:
        #         state_brews.append(brew)

# if brewery is in our db, id of response is changed to match our db
# also adds the brewery rating to the response
    for brewery in db_breweries:
        for state in state_search_results:
            if brewery.brewery_name == state['name']:
                state['id'] = brewery.id
                state['brewery_rating'] = brewery.brewery_rating
    user_initials = request.user.username[0:2]
    state_form = StateSearchForm()
    state = state_search_results[0]['state']
    context.update({
        'state_form': state_form,
        'search_results': state_search_results,
        'state': state,
        # 'state_brews': state_brews,
        'fave_list_ids': fave_list_ids,
        'notifications': notifications,
        'user_initials': user_initials
    })
    return render(request, 'state_results.html', context)


@login_required(login_url='/')
def update_user_view(request, user_id):
    '''Allows the user to update profile info and add profile pic'''
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
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
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
    '''Allows the user to request a unique one time use url sent to
        their email allowing them to reset their password'''
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
                request_user = user.username
                random_string = string_generator()

                TemporaryUrl.objects.create(
                    snippet=random_string,
                    user=request_user
                )

                random_snippet = TemporaryUrl.objects.get(
                    snippet=random_string)

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
    '''Allows the user to reset their password only accessible via the
        one time use link sent to their email at their request'''
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
                    return redirect(reverse('home'))
                else:
                    match_error = 'Passwords did not match try again!'

        state_form = StateSearchForm()
        context.update({
            'form': form,
            'state_form': state_form,
            'match_error': match_error
        })

        return render(request, 'password_reset.html', context)


@login_required(login_url='/')
def follow_user_view(request, username):
    '''Allow users to follow each other for activity feed
        and socializing'''

    follow_user = MyBrewUser.objects.get(username=username)
    user = request.user
    user.followed_user.add(follow_user)
    user.save()
    return HttpResponse()


@login_required(login_url='/')
def unfollow_view(request, username):
    '''Allows users to unfollow each other'''

    unfollow_user = MyBrewUser.objects.get(username=username)
    user = request.user
    user.followed_user.remove(unfollow_user)
    user.save()
    return HttpResponse()


@login_required(login_url='/')
def temp_all_users(request):
    context = {}

    # user = MyBrewUser.objects.get(username=request.user)
    following = MyBrewUser.objects.all()

    context.update({
        'following': following
    })
    return render(request, 'temp.html', context)
