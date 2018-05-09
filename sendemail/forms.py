from django import forms


# define form fields and specify what data types to expect
class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    organisation = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    type = forms.CharField(widget=forms.HiddenInput(), required=True)

    # check if filled form data is valid
    def is_valid(self):
        valid = super(ContactForm, self).is_valid()

        if not valid:
            return False

        # ensure that form data that's emailed is from one of the two forms
        if self.cleaned_data['type'] not in ['Press', 'Service']:
            return False

        return True
