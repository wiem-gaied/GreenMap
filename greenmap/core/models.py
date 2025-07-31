from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User


# --------------------
# Abstract User
# --------------------
class AbstractUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cin = models.CharField(max_length=20, unique=True)
    login = models.CharField(max_length=50, unique=True)
    mot_pass = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    derniere_connexion = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def se_connecter(self):
        return self.is_active

    def modifier_profil(self, nom, prenom):
        self.nom = nom
        self.prenom = prenom
        self.save()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# --------------------
# Citoyen
# --------------------
class Citoyen(AbstractUser):
    cin = models.CharField(max_length=8, unique=True)

    def creer_reclamation(self, **kwargs):
        return Reclamation.objects.create(citoyen=self, **kwargs)

    def consulter_reclamations(self):
        return self.reclamation_set.all()

# --------------------
# Agent
# --------------------
class Agent(AbstractUser):
    cin = models.CharField(max_length=8, unique=True)

    def accepter_reclamation(self, reclamation):
        reclamation.etat = "Acceptée"
        reclamation.save()

    def rejeter_reclamation(self, reclamation):
        reclamation.etat = "Rejetée"
        reclamation.save()

    def afficher_reclamations_en_attente(self):
        return Reclamation.objects.filter(etat="En attente")

# --------------------
# Code Postale
# --------------------
class CodePostale(models.Model):
    num = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def est_valide(self):
        return self.num.isdigit()

    def get_info_region(self):
        return f"{self.ville}, {self.region}"

# --------------------
# Réclamation
# --------------------
class Reclamation(models.Model):
    TYPE_CHOICES = [
        ('pollution', 'Pollution'),
        ('dechet', 'Déchets'),
        ('autre', 'Autre'),
    ]
    ETAT_CHOICES = [
        ('En attente', 'En attente'),
        ('Acceptée', 'Acceptée'),
        ('Rejetée', 'Rejetée'),
    ]

    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    type_reclamation = models.CharField(max_length=50, choices=TYPE_CHOICES)
    date_re = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='reclamations/', null=True, blank=True)
    localisation = models.CharField(max_length=255)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default="En attente")
    description = models.TextField()
    priorite = models.IntegerField(default=1)
    code_postale = models.ForeignKey(CodePostale, on_delete=models.SET_NULL, null=True)

    def get_details(self):
        return f"{self.type_reclamation} - {self.localisation} - {self.etat}"

    def modifier_etat(self, nv_etat):
        self.etat = nv_etat
        self.save()
