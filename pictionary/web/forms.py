from django import forms

class PlayerDetailsForm(forms.Form):
    age = forms.IntegerField(label='What is your age?', required=True)
    hand = forms.ChoiceField(choices=(('left', 'Left'), ('right', 'Right')), required=True, label='Are you left handed or right handed?', widget=forms.Select())
    gender = forms.ChoiceField(choices=(('male', 'Male'), ('female', 'Female')), required=True, label='Are you a male or a female?', widget=forms.Select())