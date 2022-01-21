from django import forms
from django.contrib.auth import authenticate
from my_brew_app.models import MyBrewUser
from my_brew_app.state_choice import STATE_CHOICES


class SignUpForm(forms.Form):

    first_name = forms.CharField(
        max_length=18,
        label='First Name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        max_length=18,
        label='Last Name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name'
        })
    )

    usernameSU = forms.CharField(
        max_length=180,
        label='Username',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
        })
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        })
    )

    state = forms.ChoiceField(
        label='State',
        required=True,
        choices=STATE_CHOICES
    )

    city = forms.CharField(
        max_length=60,
        label='City',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'City'
        })
    )

    favorite_beer = forms.CharField(
        max_length=180,
        label='Favorite Beer',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Favorite Beer'
        })
    )

    passwordSU = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password'
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
        label='State Search',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search By State'
        })
    )


class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=18,
        label='First Name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        max_length=18,
        label='Last Name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name'
        })
    )

    username = forms.CharField(
        max_length=18,
        label='Username',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
        })
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        })
    )

    state = forms.ChoiceField(
        label='State',
        required=True,
        choices=STATE_CHOICES
    )

    city = forms.CharField(
        label='City',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'City'
        })
    )

    favorite_beer = forms.CharField(
        label='Favorite Beer',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Favorite Beer'
        })
    )

    profile_pic = forms.FileField(label='Profile Picture')

    class Meta:
        model = MyBrewUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'state',
            'city',
            'favorite_beer',
            'profile_pic'
        ]


class ResetRequest(forms.Form):
    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email'
        })
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New Password'
        })
    )

    password2 = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Re-Type Password'
        })
    )


class UserSearchForm(forms.Form):
    username_search = forms.CharField(
        label='Search Users',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search Users'
        })
    )
