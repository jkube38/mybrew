from django import forms


class RegisterBreweryForm(forms.Form):
    brewery_name = forms.CharField(
        max_length=180,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Brewery Name'
        })
    )
    brewery_logo = forms.ImageField(
        widget=forms.ClearableFileInput()
    )
    brewery_hero_image = forms.ImageField(
        widget=forms.ClearableFileInput()
    )
    brewery_intro = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Brewery Introduction'
        })
    )
    brewery_address = forms.CharField(
        max_length=180,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Brewery Address'
        })
    )
    brewery_city = forms.CharField(
        max_length=180,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Brewery City'
        })
    )
    brewery_state = forms.CharField(
        max_length=180,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Brewery State'
        })
    )
    brewery_zip_code = forms.CharField(
        max_length=180,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Brewery Zip Code'
        })
    )
    brewery_phone = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Brewery Phone'
        })
    )
    brewery_website = forms.URLField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Brewery Website'
        })
    )
