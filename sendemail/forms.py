from django import forms

HELP_CHOICES = [
    ('ckan', 'CKAN (data portals)'),
    ('tech-services', 'Tech Services'),
    ('open-data-strategy', 'Open Data Strategy'),
    ('consultancy', 'Consultancy'),
    ('training', 'Training'),
    ('partnerships', 'Partnerships / Alliances'),
    ('campaigns', 'Campaigns'),
    ('open-knowledge-network', 'Open Knowledge Network (local services)'),
]


class ContactForm(forms.Form):
    name = forms.CharField(label='Name/Last name *')
    name.widget.attrs = {'class': "form-control input-lg"}

    organisation = forms.CharField(required=False, label='Organization')
    organisation.widget.attrs = {'class': "form-control input-lg"}

    website = forms.URLField(required=False, label='Website')
    website.widget.attrs = {'class': "form-control input-lg"}

    email = forms.EmailField(label='Email address *')
    email.widget.attrs = {'class': "form-control input-lg"}

    how_can_we_help = forms.ChoiceField(label='How can we help?', choices=HELP_CHOICES)
    how_can_we_help.widget.attrs = {'class': "form-control input-lg"}

    message = forms.CharField(required=False, widget=forms.Textarea, label='Tell us more about your needs')
    message.widget.attrs = {'class': "form-control input-lg", 'rows': 10}

    telephone = forms.CharField(required=False, label='Telephone')
    telephone.widget.attrs = {'class': "form-control input-lg"}
