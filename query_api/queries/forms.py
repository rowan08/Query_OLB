from django import forms

# Add styling to forms as needed.
# Currently, the same styling is being applied to all forms
form_attributes = {
                'class':'form-control',
            }

class OLBooksAPIForm(forms.Form):
    
    ISBN = forms.CharField(required=False, label="ISBN", widget=forms.TextInput(attrs=form_attributes))
    OCLC = forms.CharField(required=False, label="OCLC", widget=forms.TextInput(attrs=form_attributes))
    LCCN = forms.CharField(required=False, label="LCCN", widget=forms.TextInput(attrs=form_attributes))
    OLID = forms.CharField(required=False, label="OLID", widget=forms.TextInput(attrs=form_attributes))

    show_raw = forms.BooleanField(required=False, label="Show raw output", widget=forms.CheckboxInput())

    def clean(self):
        ISBN = self.cleaned_data.get('ISBN')
        OCLC = self.cleaned_data.get('OCLC')
        LCCN = self.cleaned_data.get('LCCN')
        OLID = self.cleaned_data.get('OLID')

        if not (ISBN or OCLC or LCCN or OLID):
            raise forms.ValidationError("Please specify at least one field to search")

        return super(OLBooksAPIForm, self).clean()