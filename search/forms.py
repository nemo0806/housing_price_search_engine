from django import forms


class SearchForm(forms.Form):
    search_name = forms.CharField(required=False)
    search_city = forms.CharField()
    search_location = forms.CharField(required=False)
    search_area = forms.FloatField()
    search_price = forms.FloatField()

class MixtureForm(forms.Form):
    search_anything = forms.CharField()