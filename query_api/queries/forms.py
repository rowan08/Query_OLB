from django import forms

def validate(form_input):
    '''
    Set all form input to at least be alphanumeric
    '''
    check_list = form_input.replace('-','').split(',')
    for value in check_list:
        if not value.strip().isalnum():
            raise forms.ValidationError("Identifiers should consist of only letters and digits")

class OLBooksAPIForm(forms.Form):
    
    ISBN = forms.CharField(required=False, label="ISBN:", widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'e.g. 0201558025',}))
    OCLC = forms.CharField(required=False, label="OCLC", widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'e.g. 297222669'}))
    LCCN = forms.CharField(required=False, label="LCCN", widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'e.g. 93005405'}))
    OLID = forms.CharField(required=False, label="OLID", widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'e.g. OL123M'}))

    show_raw = forms.BooleanField(required=False, label="Show raw output", widget=forms.CheckboxInput())

    def clean(self):
        ISBN = self.cleaned_data.get('ISBN')
        OCLC = self.cleaned_data.get('OCLC')
        LCCN = self.cleaned_data.get('LCCN')
        OLID = self.cleaned_data.get('OLID')

        if not (ISBN or OCLC or LCCN or OLID):
            raise forms.ValidationError("Please specify at least one field to search")

        for form_data in (ISBN, OCLC, LCCN, OLID):
            if form_data:
                validate(form_data)

        return super(OLBooksAPIForm, self).clean()