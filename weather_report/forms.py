import pytz

from django import forms


class AdvancedSearchForm(forms.Form):
    country = forms.ChoiceField(choices=pytz.country_names.items())
    city = forms.CharField(max_length=128)

