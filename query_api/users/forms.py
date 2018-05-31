from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

# Add styling to forms as needed.
# Currently, the same styling is being applied to all forms
form_attributes = {
                'class':'form-control',
            }

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=form_attributes))
    password = forms.CharField(widget=forms.PasswordInput(attrs=form_attributes))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            
            try: 
                User.objects.get(username=username)
                user = authenticate(username=username, password=password)
                if not user:
                    raise forms.ValidationError('Incorrect password')
            
            except User.DoesNotExist:
                raise forms.ValidationError(f'User "{username}" does not exist')
            
        return super(UserLoginForm, self).clean()


class UserRegisterForm(forms.ModelForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs=form_attributes))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs=form_attributes))
    email_confirmation = forms.EmailField(label='Confirm Email', widget=forms.TextInput(attrs=form_attributes))
    password = forms.CharField(widget=forms.PasswordInput(attrs=form_attributes))

    class Meta:
        model = User
        fields = ['username', 
                'email',
                'email_confirmation',
                'password'
        ]

    def clean_email_confirmation(self):
        email = self.cleaned_data.get('email')
        email_confirmation = self.cleaned_data.get('email_confirmation')
        if email != email_confirmation:
            raise forms.ValidationError('Email values do not match')

        return email