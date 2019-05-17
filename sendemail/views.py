from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm


# check if form data is valid
def contactview(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            organisation = form.cleaned_data['organisation']
            type = form.cleaned_data['type']

            # collate and send filled form data in one email
            message_from = 'Name: ' + name + '\n' + 'From: ' + organisation
            message_details = 'Email: ' + email + '\n' + 'Message: ' + message
            email_message = message_from + '\n' + message_details
            email_subject = type + ' Enquiry from ' + name

            # specify where form data is sent, depending on the type of enquiry
            if type == 'Service':
                recepients = settings.SERVICE_EMAIL_RECEPIENTS
            else:
                recepients = settings.PRESS_EMAIL_RECEPIENTS

            # flatten recepients list:
            # (('name1', 'email1'), ...) -> ('email1', ...)
            recepients = map(lambda recepient: recepient[1], recepients)

            # all form data will originate from the same email address
            try:
                send_mail(
                    email_subject, email_message,
                    settings.CONTACT_EMAIL_SENDER, recepients)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            # pop up message once form data has been sent successfully
            messages.info(
                request,
                'Thank you for your message. ' +
                'Someone from Open Knowledge Foundation' +
                ' will be in touch soon.')

    # reload the contact page after form data has been sent successfully
    return render(request, "cms_contact.html", {'form': form})
