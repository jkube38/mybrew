"""my_brew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_brew_app import views
from my_brew_brewery import views as b_views
from my_brew_posts import views as p_views
from my_brew_notifications import views as n_views
from my_brew_app.helpers import username_search
from my_brew import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.home_view, name='home'),
    path(
        'profile/<str:username>/followingVine/',
        views.user_profile_view,
        name='user_profile'),
    path(
        'profile/<str:username>/myVine/',
        views.user_profile_view,
        name='user_profile_my_vine'
    ),
    path(
        'brewerypage/<str:brewery_name>/',
        b_views.brewery_profile,
        name='brewery_profile'
    ),
    path(
        'profile/<str:username>/exploreVine/',
        views.user_profile_view,
        name='user_profile_explore_vine'
    ),
    path('stateresults/<str:state>/', views.state_view, name='state'),
    path(
        'usernamesearch/<str:user_input>/',
        username_search,
        name='user_search'
    ),
    path('logout/', views.logout_view, name='logout'),
    path('usersignup/', views.signup_view, name='signup'),
    path(
        'favorite/<str:brew_name>/',
        views.favorite_brewery_view,
        name='favorite'
    ),

    path(
        'rate/<int:rated>/<int:id>/',
        b_views.rating_view,
        name='rating'
    ),
    path('userpostsubmission/', p_views.user_post_view, name='userpost'),
    path(
        'userpostdelete/<int:post_id>/',
        p_views.delete_post_view,
        name='post_delete'
    ),
    path(
        'usercommentdelete/<int:comment_id>/',
        p_views.delete_comment_view,
        name='delete_comment'
    ),
    path(
        'userpostupdate/<int:post_id>/',
        p_views.update_post_view,
        name='update_post'
    ),
    path(
        'postupdateformfill/<int:post_id>/',
        p_views.update_post_data,
        name='update_post_data'
    ),
    path(
        'updateuser/<int:user_id>/',
        views.update_user_view,
        name='update_user'
    ),
    path('postlike/<str:username>/<int:post_id>/', p_views.post_like_view),
    path(
        'notificationviewed/<str:notification_id>/',
        n_views.notification_viewed_view,
        name='viewed'
    ),
    path(
        'postcommentdata/<str:post_commenter>/<int:post_id>/<str:post_creator>/',
        p_views.post_comment_data_view,
        name='post_comment_data'
    ),
    path(
        'postcommentsubmission/',
        p_views.post_comment_view,
        name='post_comment'
    ),
    path(
        'notificationdelete/<str:notification_id>/',
        n_views.notification_delete_view,
        name='delete_notification'
    ),
    path('resetrequest/', views.reset_request_view, name='request_reset'),
    path('passwordreset/<str:username>/<str:snippet>/',
         views.password_reset_view, name='password_reset'),
    path('follow/<str:username>/', views.follow_user_view, name='follow'),
    path('unfollow/<str:username>/', views.unfollow_view, name='unfollow'),
    path('tempusers/', views.temp_all_users, name='temp'),
    path(
        'registerbrewery/',
        b_views.register_brewery_view,
        name='register_brewery'
    ),
    path('deleteuser/', views.remove_user, name='remove_user'),
    path('admin/', admin.site.urls),
]

# added handler varables for views.py
handler404 = 'my_brew_app.views.error_404'
handler500 = 'my_brew_app.views.error_500'

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
