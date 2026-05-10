from django.db import models

class Livre(models.Model):
    STATUT_CHOICES = [
        ('disponible', '✅ Disponible'),
        ('emprunte', '📖 Emprunté'),
        ('reserve', '⏳ Réservé'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name="Titre")
    auteur = models.CharField(max_length=100, verbose_name="Auteur")
    categorie = models.CharField(max_length=100, verbose_name="Catégorie")
    annee_publication = models.IntegerField(verbose_name="Année")
    quantite_disponible = models.IntegerField(default=1, verbose_name="Quantité")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')
    
    def __str__(self):
        return f"{self.titre} - {self.auteur}"
    
    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ['titre']