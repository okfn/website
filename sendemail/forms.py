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


# define form fields and specify what data types to expect
class ContactForm(forms.Form):
    name = forms.CharField(required=True, label='Name/Last name')
    name.widget.attrs = {'class': "form-control input-lg"}

    organisation = forms.CharField(required=True, label='Organization')
    organisation.widget.attrs = {'class': "form-control input-lg"}

    website = forms.URLField(required=False, label='Website')
    website.widget.attrs = {'class': "form-control input-lg"}

    email = forms.EmailField(required=True, label='Email address')
    email.widget.attrs = {'class': "form-control input-lg"}

    how_can_we_help = forms.ChoiceField(required=True, label='How can we help?', choices=HELP_CHOICES)
    how_can_we_help.widget.attrs = {'class': "form-control input-lg"}

    message = forms.CharField(widget=forms.Textarea, required=True, label='Tell us more about your needs')
    message.widget.attrs = {'class': "form-control input-lg", 'rows': 10}

    telephone = forms.CharField(required=False, label='Telephone')
    telephone.widget.attrs = {'class': "form-control input-lg"}

    type = forms.CharField(widget=forms.HiddenInput(), required=True)

    # check if filled form data is valid
    def is_valid(self):
        valid = super().is_valid()

        if not valid:
            return False

        # ensure that form data that's emailed is from one of the two forms
        if self.cleaned_data['type'] not in ['Press', 'Service']:
            return False

        return True
