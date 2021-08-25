import pytz

from django import forms

sorted_country_list = sorted(pytz.country_names.items(), key=lambda item: item[1])


class AdvancedSearchForm(forms.Form):
    country = forms.ChoiceField(choices=sorted_country_list)
    city = forms.CharField(max_length=128)
