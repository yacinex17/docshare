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
    has_correction = forms.BooleanField(required=False, label="Has Correction?")
    corrected_file = forms.FileField(required=False, label="Corrected File")
    corrected_link = forms.URLField(required=False, label="Corrected Link")

    class Meta:
        model = Document
        fields = ['file', 'link', 'title', 'description', 'subject', 'classroom', 'subsubject', 'tags', 'type', 'has_correction', 'corrected_file', 'corrected_link']

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        link = cleaned_data.get('link')
        has_correction = cleaned_data.get('has_correction')
        corrected_file = cleaned_data.get('corrected_file')
        corrected_link = cleaned_data.get('corrected_link')
        if not file and not link:
            raise forms.ValidationError('You must provide either a file or a link.')
        if file and link:
            raise forms.ValidationError('Please provide only a file or a link, not both.')
        if has_correction:
            if not corrected_file and not corrected_link:
                raise forms.ValidationError('If you checked Has Correction, you must provide either a corrected file or a corrected link.')
            if corrected_file and corrected_link:
                raise forms.ValidationError('Please provide only a corrected file or a corrected link, not both.')
        return cleaned_data 