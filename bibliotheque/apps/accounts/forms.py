from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta:
        model  = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role  = 'lecteur'
        if commit:
            user.save()
        return user


class ProfilForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ('first_name', 'last_name', 'email', 'avatar', 'bio',
                  'date_naissance', 'langue_preferee', 'notif_email')
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'bio':            forms.Textarea(attrs={'rows': 4}),
        }