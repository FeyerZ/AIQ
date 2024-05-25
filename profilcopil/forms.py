from django import forms


class InputForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    age_number = forms.IntegerField()
    interest_points = forms.CharField(max_length=1000)
    personality = forms.CharField(max_length=1000)