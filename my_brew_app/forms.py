from django import forms
from my_brew_app.models import MyBrewUser


class SignUpForm(forms.Form):
    STATE_CHOICES = (
        ('Alabama', 'Alabama'),
        ('Alaska', 'Alaska'),
        ('Arizona', 'Arizona'),
        ('Arkansas', 'Arkansas'),
        ('California', 'California'),
        ('Colorado', 'Colorado'),
        ('Connecticut', 'Connecticut'),
        ('Delaware', 'Connecticut'),
        ('Florida', 'Florida'),
        ('Georgia', 'Georgia'),
        ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'),
        ('Illinois', 'Illinois'),
        ('Indiana', 'Illinois'),
        ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'),
        ('Kentucky', 'Kentucky'),
        ('Louisiana', 'Louisiana'),
        ('Maine', 'Maine'),
        ('Maryland', 'Maryland'),
        ('Massachusetts', 'Massachusetts'),
        ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'),
        ('Mississippi', 'Mississippi'),
        ('Missouri', 'Missouri'),
        ('Montana', 'Montana'),
        ('Nebraska', 'Nebraska'),
        ('Nevada', 'Nevada'),
        ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'),
        ('New Mexico', 'New Mexico'),
        ('New York', 'New York'),
        ('North Carolina', 'North Carolina'),
        ('North Dakota', 'North Dakota'),
        ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'),
        ('Oregon', 'Oregon'),
        ('Pennsylvania', 'Pennsylvania'),
        ('Rhode Island', 'Rhode Island'),
        ('South Carolina', 'South Carolina'),
        ('South Dakota', 'South Dakota'),
        ('Tennessee', 'Tennessee'),
        ('Texas', 'Texas'),
        ('Utah', 'Utah'),
        ('Vermont', 'Vermont'),
        ('Virginia', 'Virginia'),
        ('Washington', 'Washington'),
        ('West Virginia', 'West Virginia'),
        ('Wisconsin', 'Wisconsin'),
        ('Wyoming', 'Wyoming')
    )
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
            'placeholder': '*Username'
        })
    )

    password = forms.CharField(
        max_length=180,
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': '*Password'
        })
    )


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
    STATE_CHOICES = (
        ('Alabama', 'Alabama'),
        ('Alaska', 'Alaska'),
        ('Arizona', 'Arizona'),
        ('Arkansas', 'Arkansas'),
        ('California', 'California'),
        ('Colorado', 'Colorado'),
        ('Connecticut', 'Connecticut'),
        ('Delaware', 'Connecticut'),
        ('Florida', 'Florida'),
        ('Georgia', 'Georgia'),
        ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'),
        ('Illinois', 'Illinois'),
        ('Indiana', 'Illinois'),
        ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'),
        ('Kentucky', 'Kentucky'),
        ('Louisiana', 'Louisiana'),
        ('Maine', 'Maine'),
        ('Maryland', 'Maryland'),
        ('Massachusetts', 'Massachusetts'),
        ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'),
        ('Mississippi', 'Mississippi'),
        ('Missouri', 'Missouri'),
        ('Montana', 'Montana'),
        ('Nebraska', 'Nebraska'),
        ('Nevada', 'Nevada'),
        ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'),
        ('New Mexico', 'New Mexico'),
        ('New York', 'New York'),
        ('North Carolina', 'North Carolina'),
        ('North Dakota', 'North Dakota'),
        ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'),
        ('Oregon', 'Oregon'),
        ('Pennsylvania', 'Pennsylvania'),
        ('Rhode Island', 'Rhode Island'),
        ('South Carolina', 'South Carolina'),
        ('South Dakota', 'South Dakota'),
        ('Tennessee', 'Tennessee'),
        ('Texas', 'Texas'),
        ('Utah', 'Utah'),
        ('Vermont', 'Vermont'),
        ('Virginia', 'Virginia'),
        ('Washington', 'Washington'),
        ('West Virginia', 'West Virginia'),
        ('Wisconsin', 'Wisconsin'),
        ('Wyoming', 'Wyoming')
    )

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
