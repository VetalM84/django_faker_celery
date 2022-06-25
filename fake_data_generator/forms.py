from django import forms


class FakeDataForm(forms.Form):
    total = forms.IntegerField(
        label="Total rows to create",
        min_value=10,
        max_value=100000,
        initial=10,
        widget=forms.NumberInput(),
    )
