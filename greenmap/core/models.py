from django.db import models
from django.contrib.auth.models import User


# ----------------------------
# Code Postale
# ----------------------------
class CodePostale(models.Model):
    num = models.CharField(max_length=10, unique=True)


    def __str__(self):
        return self.num

class Citoyen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=80)
    prenom = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    # Méthode pour créer ou mettre à jour un citoyen lié à un utilisateur
    @classmethod
    def create_or_update(cls, user, nom, prenom):
        citoyen, created = cls.objects.update_or_create(
            user=user,
            defaults={'nom': nom, 'prenom': prenom}
        )
        return citoyen


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=110)
    prenom = models.CharField(max_length=110)  # Ajouté
    cin = models.CharField(max_length=8, unique=True)
    code_postale = models.ForeignKey(CodePostale, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.cin}"

# ----------------------------
# Réclamation
# ----------------------------
class Reclamation(models.Model):
    TYPE_CHOICES = [
        ('Trottoir dégradé ou impraticable', 'Trottoir dégradé ou impraticable'),
        ('Espaces verts non entretenus', 'Espaces verts non entretenus'),
        ('Éclairage insuffisant dans une zone', 'Éclairage insuffisant dans une zone'),
        ('Dégradation d’un bâtiment public', 'Dégradation d’un bâtiment public'),
        ('Clôture ou mur endommagé', 'Clôture ou mur endommagé'),
        ('autre', 'Autre'),
    ]
    ETAT_CHOICES = [
        ('En attente', 'En attente'),
        ('Acceptée', 'Acceptée'),
        ('Rejetée', 'Rejetée'),
    ]

    citoyen = models.ForeignKey(Citoyen, on_delete=models.CASCADE, related_name='reclamations')
    type_reclamation = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    localisation = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    date_re = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='reclamations/', null=True, blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default="En attente")
    code_postale = models.ForeignKey(CodePostale, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.type_reclamation} - {self.localisation} ({self.etat})"
