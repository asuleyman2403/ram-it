from django import forms


class CreateAnswerForm(forms.Form):
    content = forms.CharField(min_length=4, max_length=200, required=True)

