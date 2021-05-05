from django import forms


class Dependencies(forms.Form):
    CHOICES = (('a', 'a'),
               ('b', 'b'),
               ('c', 'c'),
               ('d', 'd'),)
    picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())