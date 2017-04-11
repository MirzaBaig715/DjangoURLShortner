from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class UrlForm(forms.Form):
    url = forms.URLField(required=True, label="Please Enter Url ", max_length=400)

    def clean_url(self):

        try:
            cleaned_url = self.cleaned_data['url']
            validate_url = URLValidator()
            validate_url(cleaned_url)
            return cleaned_url
        except ValidationError:
            raise "Validation Error !!!"


