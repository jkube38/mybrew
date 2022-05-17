from django.shortcuts import render, redirect, reverse
from my_brew_brewery.models import MyBrewBrewery
from my_brew_brewery.brewery_forms import RegisterBreweryForm
from my_brew_app.forms import StateSearchForm, UserSearchForm


# Create your views here.
def rating_view(request, rated, id):
    '''Updates the breweries rating, num votes, num hops total, avg rating
        and returns the user to either home or back to the state they were on
        depending on the breweries city they voted on'''
    update_brewery = MyBrewBrewery.objects.get(id=id)

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


def register_brewery_view(request):
    context = {}
    user_search_form = UserSearchForm()
    state_form = StateSearchForm()
    register_form = RegisterBreweryForm()
    context.update({
        'register_form': register_form,
        'state_form': state_form,
        'user_search_form': user_search_form
    })
    return render(request, 'register_brewery.html', context)


def brewery_profile(request, brewery_name):
    context = {}
    brewery = MyBrewBrewery.objects.get(brewery_name=brewery_name)

    context.update({
        'brewery': brewery
    })
    return render(request, 'brewery_profile.html', context)
