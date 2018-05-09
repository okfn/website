from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm

# check if form data is valid
def contactView(request):
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
            email_message = 'From: ' + email + '\n' + 'Name: ' + name + '\n' + 'Organisation: ' + organisation + '\n' + 'Message: ' + message +'\n'
            email_subject = type + ' Enquiry from ' + name

            # specify where form data is sent, depending on the type of enquiry
            if type == 'Service':
                recepients = ['oks@okfn.org']
            else:
                recepients = ['press@okfn.org']

            # as it currently stands, all messages sent through the from will originate from the same email address
            try:
                send_mail(email_subject, email_message, "info@okfn.org", recepients)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            # pop up message at the top of the page once form data has been sent in an email successfully
            messages.info(request, 'Thank you for your message. Someone from Open Knowledge International will be in touch soon.')

    # reload the contact page after form data has been sent successfully
    return render(request, "cms_contact.html", {'form': form})
