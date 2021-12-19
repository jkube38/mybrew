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
from my_brew import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.home_view, name='home'),
    path('stateresults/<str:state>/', views.state_view, name='state'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path(
        'favorite/<str:brew_name>/',
        views.favorite_brewery_view,
        name='favorite'
    ),
    path(
        'rate/<int:rated>/<str:brewery_address>/',
        views.rating_view,
        name='rating'
    ),
    path(
        'updateuser/<int:user_id>/',
        views.update_user_view,
        name='update_user'
    ),
    path('resetrequest/', views.reset_request_view, name='request_reset'),
    path('passwordreset/<str:username>/<str:snippet>/',
         views.password_reset_view, name='password_reset'),
    # path('registerbrewery/', views.register_brewery, name='register_brewery'),
    path('admin/', admin.site.urls),
]

# added handler varables for views.py
handler404 = 'my_brew_app.views.error_404'
handler500 = 'my_brew_app.views.error_500'

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
