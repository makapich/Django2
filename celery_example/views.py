from datetime import timedelta

from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ReminderForm
from .tasks import send_mail as celery_send_mail


def reminder(request):
    error_msg = ""
    if request.method == 'POST':
        form = ReminderForm(request.POST)

        if form.is_valid():
            to_email = form.cleaned_data['email']
            message = form.cleaned_data['reminding_text']
            reminding_datetime = form.cleaned_data['reminding_datetime']
            now = timezone.now()

            if reminding_datetime - now > timedelta(days=2):
                error_msg = "Please select a date and time within the next 2 days."
            else:
                subject = 'Reminder'
                from_email = 'from@example.com'
                celery_send_mail.apply_async((subject, message, from_email, [to_email, ]), eta=reminding_datetime)
                return redirect('celery_example:success-page')

    else:
        form = ReminderForm()
    context = {'form': form, 'error_msg': error_msg}
    return render(request, 'celery_example/reminder.html', context)


def success_page(request):
    return render(request, 'celery_example/success_page.html')
