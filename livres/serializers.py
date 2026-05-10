from rest_framework import serializers
from .models import Livre

class LivreSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle Livre
    Convertit les objets Livre en JSON et vice-versa
    """
    
    # Affichage lisible du statut
    statut_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Livre
        fields = ['id', 'titre', 'auteur', 'categorie', 'annee_publication', 
                  'quantite_disponible', 'statut', 'statut_display']
    
    def get_statut_display(self, obj):
        """Retourne le statut en français lisible"""
        statuts = {
            'disponible': '✅ Disponible',
            'emprunte': '📖 Emprunté',
            'reserve': '⏳ Réservé'
        }
        return statuts.get(obj.statut, obj.statut)