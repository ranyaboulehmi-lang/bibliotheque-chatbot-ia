from django import forms
from .models import Livre

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'categorie', 'annee_publication', 'quantite_disponible', 'statut']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Le Petit Prince'}),
            'auteur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Victor Hugo'}),
            'categorie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Roman, Science-fiction, Aventure...'}),  # ← Champ texte
            'annee_publication': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1949'}),
            'quantite_disponible': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 3'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'titre': '📖 Titre du livre',
            'auteur': '✍️ Auteur',
            'categorie': '🏷️ Catégorie',
            'annee_publication': '📅 Année de publication',
            'quantite_disponible': '📚 Quantité disponible',
            'statut': '✅ Statut',
        }