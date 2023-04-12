from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class ReminderForm(forms.Form):
    email = forms.EmailField()
    reminding_text = forms.CharField(max_length=200, widget=forms.Textarea)
    reminding_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def clean_reminding_datetime(self):
        now = timezone.now()
        plus_two_days = now + timedelta(days=2)
        reminding_datetime = self.cleaned_data['reminding_datetime']
        if reminding_datetime < now or reminding_datetime > plus_two_days:
            raise ValidationError('Please select a date and time within the next 2 days.')
        return reminding_datetime
