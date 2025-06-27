from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Document

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Enter your phone number'})

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 9:
            raise forms.ValidationError('Password must be at least 9 characters long.')
        return password1

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'link', 'title', 'description', 'subject', 'subsubject', 'tags', 'type']

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        link = cleaned_data.get('link')
        if not file and not link:
            raise forms.ValidationError('You must provide either a file or a link.')
        if file and link:
            raise forms.ValidationError('Please provide only a file or a link, not both.')
        return cleaned_data 