from datetime import time, timedelta

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
        if reminding_datetime < now or time > plus_two_days:
            raise ValidationError('reminding_datetime error')
        return reminding_datetime
