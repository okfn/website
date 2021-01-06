from django import forms


# define form fields and specify what data types to expect
class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    name.widget.attrs = {'class': "form-control input-lg"}

    organisation = forms.CharField(required=True)
    organisation.widget.attrs = {'class': "form-control input-lg"}

    email = forms.EmailField(required=True, label='Email address')
    email.widget.attrs = {'class': "form-control input-lg"}

    message = forms.CharField(widget=forms.Textarea, required=True, label='How can we help?')
    message.widget.attrs = {'class': "form-control input-lg", 'rows': 10}

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
