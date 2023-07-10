from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm


# check if form data is valid
def contactview(request):
    if request.method == 'GET':
        return render(request, "cms_contact.html", {'form': ContactForm()})

    form = ContactForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Required information is missing')
        return render(request, "cms_contact.html", {'form': form})

    how_can_we_help = form.cleaned_data['how_can_we_help']
    email_subject = 'New contact from OKFN website: ' + how_can_we_help

    email_message = f"""
Name: {form.cleaned_data['name']}
From: {form.cleaned_data['organisation']}
Email: {form.cleaned_data['email']}
Telephone: {form.cleaned_data['telephone']}
Message: {form.cleaned_data['message']}
    """

    # flatten recepients list:
    # (('name1', 'email1'), ...) -> ('email1', ...)
    recepients = settings.GENERAL_EMAIL_RECEPIENTS
    recepients = [recepient[1] for recepient in recepients]

    try:
        send_mail(
            email_subject, email_message,
            settings.CONTACT_EMAIL_SENDER, recepients)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    messages.info(
        request,
        'Thank you for your message. '
        + 'Someone from Open Knowledge Foundation'
        + ' will be in touch soon.')
    return render(request, "cms_contact.html", {'form': ContactForm()})
