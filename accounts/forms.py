from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    

    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    

    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password' ]


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget. attrs['Placeholder'] = 'Enter first Name'
        self.fields['last_name'].widget. attrs['Placeholder'] = 'Enter Last name'
        self.fields['phone_number'].widget. attrs['Placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget. attrs['Placeholder'] = 'Enter Email'
        self.fields['password'].widget. attrs['Placeholder'] = 'Enter Password'
        self.fields['confirm_password'].widget. attrs['Placeholder'] = 'Enter Confirm Password'

        for field in self.fields:
            self.fields[field].widget. attrs['class'] = 'form-control'

    # match password and confirm password functions

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )