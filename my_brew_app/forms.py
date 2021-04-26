from django import forms


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
        required=False,
        choices=STATE_CHOICES
    )

    city = forms.CharField(
        max_length=60,
        label='',
        required=False,
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
