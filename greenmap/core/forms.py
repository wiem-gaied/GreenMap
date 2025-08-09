from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Citoyen
from django import forms
from .models import Reclamation
from .models import Agent, CodePostale


class ReclamationForm(forms.ModelForm):
    code_postale = forms.ModelChoiceField(
        queryset=CodePostale.objects.all().order_by('zip'),
        empty_label="Sélectionnez un code postal"
    )

    class Meta:
        model = Reclamation
        fields = ['type_reclamation', 'description', 'localisation', 'latitude', 'longitude', 'code_postale']
        labels = {
            'type_reclamation': 'Type de réclamation',
            'description': 'Description',
            'localisation': 'Adresse ou lieu concerné',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'image': 'Image (facultative)',
            'code_postale': 'Code postal'
        }


class CitoyenRegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    email = forms.EmailField(label="Adresse e-mail")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")
    nom = forms.CharField(max_length=80, label="Nom")
    prenom = forms.CharField(max_length=80, label="Prénom")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1']
        )
        citoyen = Citoyen.objects.create(
            user=user,
            nom=data['nom'],
            prenom=data['prenom']
        )
        return citoyen

class AgentRegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    email = forms.EmailField(label="Adresse e-mail")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")
    nom = forms.CharField(max_length=80, label="Nom")
    prenom = forms.CharField(max_length=80, label="Prénom")
    cin = forms.CharField(max_length=8, label="CIN")
    code_postale = forms.ModelChoiceField(
        queryset=CodePostale.objects.all(),
        label="Code postal",
        required=True
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_cin(self):
        cin = self.cleaned_data['cin']
        if not cin.isdigit() or len(cin) != 8:
            raise ValidationError("Le CIN doit contenir exactement 8 chiffres.")
        if Agent.objects.filter(cin=cin).exists():
            raise ValidationError("Ce numéro de CIN est déjà utilisé.")
        return cin

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1']
        )
        agent = Agent.objects.create(
            user=user,
            nom=data['nom'],
            prenom=data['prenom'],
            cin=data['cin'],
            code_postale=data['code_postale']
        )
        return agent