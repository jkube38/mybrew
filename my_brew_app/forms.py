from django import forms
from django.contrib.auth import authenticate
from my_brew_app.models import MyBrewUser
from my_brew_app.state_choice import STATE_CHOICES


class SignUpForm(forms.Form):

    username = forms.CharField(
        max_length=180,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Username'
        })
    )

    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '*Email'
        })
    )

    state = forms.ChoiceField(
        label='',
        required=True,
        choices=STATE_CHOICES
    )

    city = forms.CharField(
        max_length=60,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'City'
        })
    )

    favorite_beer = forms.CharField(
        max_length=180,
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Favorite Beer'
        })
    )

    password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '*password'
        }))


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=180,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
        })
    )

    password = forms.CharField(
        max_length=180,
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password'
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        brew_user = authenticate(username=username, password=password)
        if not brew_user:
            print('in clean')
            raise forms.ValidationError(
                '''Sorry, that login did not match our records,
                Please try again.''')
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        brew_user = authenticate(username=username, password=password)
        return brew_user


class StateSearchForm(forms.Form):
    state_search = forms.CharField(
        max_length=180,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search By State'
        })
    )


class UserUpdateForm(forms.ModelForm):

    username = forms.CharField(
        max_length=18,
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
        })
    )

    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        })
    )

    state = forms.ChoiceField(
        label='',
        required=True,
        choices=STATE_CHOICES
    )

    city = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'City'
        })
    )

    favorite_beer = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Favorite Beer'
        })
    )

    profile_pic = forms.FileField(label='')

    class Meta:
        model = MyBrewUser
        fields = [
            'username',
            'email',
            'state',
            'city',
            'favorite_beer',
            'profile_pic'
        ]
