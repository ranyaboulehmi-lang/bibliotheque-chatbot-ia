import os
import sys
import re

# Configuration Django
sys.path.append('C:/Users/DELL_2025/bibliotheque')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque.settings')

import django
django.setup()

from livres.models import Livre

# Nouvelle API Google Gemini (mise à jour)
# Documentation: https://ai.google.dev/gemini-api/docs/api-key
from google import genai
from google.genai import types

API_KEY = "AIzaSyBrXwUzbNazUOCxFFLbXPMGJ9MUhFdAYLc"

class BibliothequeChatbot:
    def __init__(self):
        # Initialiser le client Gemini (nouvelle API)
        try:
            self.client = genai.Client(api_key=API_KEY)
            # Modèles disponibles actuellement
            self.modeles_disponibles = [
                'gemini-2.0-flash',
                'gemini-2.0-flash-lite',
                'gemini-1.5-flash',
                'gemini-1.5-pro'
            ]
            self.gemini_ok = True
            self.modele_actif = 'gemini-2.0-flash'
            print("✅ Gemini connecté avec succès (nouvelle API)")
        except Exception as e:
            print(f"⚠️ Erreur Gemini: {e}")
            print("✅ Mode hors ligne activé")
            self.gemini_ok = False
    
    def get_all_books(self):
        """Récupérer tous les livres via Django ORM"""
        return Livre.objects.all().order_by('id')
    
    def get_available_books(self):
        """Récupérer les livres disponibles"""
        return Livre.objects.filter(statut='disponible').order_by('titre')
    
    def search_by_title(self, title):
        """Rechercher par titre"""
        return Livre.objects.filter(titre__icontains=title).order_by('titre')
    
    def search_by_author(self, author):
        """Rechercher par auteur"""
        return Livre.objects.filter(auteur__icontains=author).order_by('titre')
    
    def get_book_by_id(self, book_id):
        """Rechercher par ID"""
        try:
            return Livre.objects.get(id=book_id)
        except Livre.DoesNotExist:
            return None
    
    def get_books_by_category(self, category):
        """Rechercher par catégorie"""
        return Livre.objects.filter(categorie__icontains=category).order_by('titre')
    
    def get_catalogue_summary(self):
        """Obtenir un résumé du catalogue formaté"""
        books = self.get_all_books()
        if not books:
            return "📚 La bibliothèque est vide pour le moment."
        
        summary = "=" * 50 + "\n"
        summary += "📚 CATALOGUE COMPLET DE LA BIBLIOTHÈQUE 📚\n"
        summary += "=" * 50 + "\n\n"
        
        for book in books:
            if book.statut == 'disponible':
                status_icon = "✅"
                status_text = "Disponible"
            elif book.statut == 'emprunte':
                status_icon = "📖"
                status_text = "Emprunté"
            else:
                status_icon = "⏳"
                status_text = "Réservé"
            
            summary += f"{status_icon} **ID {book.id}**\n"
            summary += f"   📖 Titre : {book.titre}\n"
            summary += f"   ✍️ Auteur : {book.auteur}\n"
            summary += f"   🏷️ Catégorie : {book.categorie}\n"
            summary += f"   📅 Année : {book.annee_publication}\n"
            summary += f"   📊 {book.quantite_disponible} exemplaire(s)\n"
            summary += f"   ✅ Statut : {status_text}\n\n"
        
        summary += "=" * 50 + "\n"
        summary += f"📊 Total : {books.count()} livre(s) dans la bibliothèque\n"
        summary += "=" * 50
        
        return summary
    
    def get_books_by_author_text(self, author_name):
        """Récupérer les livres d'un auteur spécifique"""
        livres = Livre.objects.filter(auteur__icontains=author_name)
        if not livres.exists():
            return None
        
        result = f"📚 **Livres de {author_name} :**\n\n"
        for livre in livres:
            status_icon = "✅" if livre.statut == "disponible" else "📖" if livre.statut == "emprunte" else "⏳"
            status_text = "Disponible" if livre.statut == "disponible" else "Emprunté" if livre.statut == "emprunte" else "Réservé"
            result += f"{status_icon} **{livre.titre}**\n"
            result += f"   📅 {livre.annee_publication} | 🏷️ {livre.categorie}\n"
            result += f"   📚 {livre.quantite_disponible} exemplaire(s) - {status_text}\n\n"
        return result
    
    def recommend_books(self, user_query):
        """Recommander des livres selon les préférences de l'utilisateur"""
        query = user_query.lower()
        
        # Dictionnaire des catégories
        categories = {
            'roman': ['roman', 'romantique', 'amour', 'sentimental'],
            'science-fiction': ['science-fiction', 'sf', 'science', 'futur', 'scifi'],
            'aventure': ['aventure', 'aventures', 'voyage', 'exploration'],
            'fantaisie': ['fantaisie', 'fantasy', 'magique', 'magie', 'sorcier'],
            'policier': ['policier', 'polar', 'mystère', 'enquête', 'crime'],
            'philosophique': ['philosophique', 'philosophie', 'réflexion', 'conte philosophique'],
            'conte': ['conte', 'fable', 'histoire']
        }
        
        # Vérifier la catégorie demandée
        for categorie, mots in categories.items():
            if any(mot in query for mot in mots):
                livres = Livre.objects.filter(categorie__icontains=categorie, statut='disponible')
                if livres.exists():
                    result = f"📚 **Recommandations de {categorie} :**\n\n"
                    for livre in livres[:3]:
                        result += f"📖 **{livre.titre}** - {livre.auteur}\n"
                        result += f"   📅 {livre.annee_publication}\n"
                        result += f"   ✅ {livre.quantite_disponible} exemplaire(s)\n\n"
                    return result
        
        # Recommandations générales (livres disponibles)
        livres_dispo = Livre.objects.filter(statut='disponible')
        if livres_dispo.exists():
            result = "📚 **Nos recommandations générales :**\n\n"
            for livre in livres_dispo[:5]:
                result += f"📖 **{livre.titre}** - {livre.auteur}\n"
                result += f"   🏷️ {livre.categorie} | 📅 {livre.annee_publication}\n\n"
            return result
        
        return "📚 Désolé, aucun livre disponible pour le moment."
    
    def ask_gemini(self, question):
        """Poser une question à Gemini avec le contexte de la bibliothèque (nouvelle API)"""
        if not self.gemini_ok:
            return self.ask_simple(question)
        
        # Récupérer le catalogue formaté
        books = self.get_all_books()
        catalogue_text = ""
        for book in books:
            status_text = "disponible" if book.statut == "disponible" else "emprunté" if book.statut == "emprunte" else "réservé"
            catalogue_text += f"- ID:{book.id} : {book.titre} par {book.auteur} ({book.categorie}, {book.annee_publication}) - {book.quantite_disponible} exemplaire(s) - {status_text}\n"
        
        # Construire le prompt
        prompt = f"""Tu es un bibliothécaire amical et professionnel.

Voici le catalogue complet de notre bibliothèque :

{catalogue_text}

L'utilisateur te demande : "{question}"

Règles importantes :
1. Réponds UNIQUEMENT en utilisant les informations du catalogue ci-dessus
2. Si l'utilisateur demande un livre qui n'existe pas, dis-le poliment
3. Si l'utilisateur demande une recommandation, propose des livres du catalogue
4. Si l'utilisateur demande les livres d'un auteur, liste-les
5. Sois chaleureux, utile et concis
6. Réponds en français
7. N'invente jamais d'informations qui ne sont pas dans le catalogue

Réponse :"""
        
        try:
            # Utilisation de la nouvelle API
            response = self.client.models.generate_content(
                model=self.modele_actif,
                contents=prompt
            )
            return response.text
        except Exception as e:
            # Fallback vers le mode simple
            return f"⚠️ Erreur API: {str(e)}\n\n{self.ask_simple(question)}"
    
    def ask_simple(self, question):
        """Mode hors ligne - répond avec les données réelles de la base"""
        q = question.lower()
        
        # === RECHERCHE PAR AUTEUR (PRIORITAIRE) ===
        noms_auteurs = {
            'hugo': 'Victor Hugo',
            'victor hugo': 'Victor Hugo',
            'orwell': 'George Orwell',
            'george orwell': 'George Orwell',
            'camus': 'Albert Camus',
            'albert camus': 'Albert Camus',
            'dumas': 'Alexandre Dumas',
            'alexandre dumas': 'Alexandre Dumas',
            'saint-exupéry': 'Antoine de Saint-Exupéry',
            'antoine de saint-exupéry': 'Antoine de Saint-Exupéry',
            'rowling': 'J.K. Rowling',
            'herbert': 'Frank Herbert',
            'frank herbert': 'Frank Herbert',
            'verne': 'Jules Verne',
            'jules verne': 'Jules Verne',
            'flaubert': 'Gustave Flaubert',
            'zola': 'Émile Zola'
        }
        
        for nom_key, nom_complet in noms_auteurs.items():
            if nom_key in q:
                result = self.get_books_by_author_text(nom_complet)
                if result:
                    return result
        
        # === RECOMMANDATIONS ===
        mots_reco = ['recommande', 'conseille', 'suggère', 'propose', 'proposer', 
                     'veux', 'cherche', 'idee', 'idée', 'suggestion', 'besoin',
                     'un bon livre', 'livre sympa', 'que me conseilles']
        if any(mot in q for mot in mots_reco):
            return self.recommend_books(question)
        
        # === CATALOGUE ===
        if any(mot in q for mot in ['catalogue', 'tous les livres', 'liste des livres', 'affiche tout', 'affiche tous']):
            return self.get_catalogue_summary()
        
        # === LIVRES DISPONIBLES ===
        if any(mot in q for mot in ['disponible', 'disponibles', 'emprunter', 'que peut-on prendre']):
            dispo = self.get_available_books()
            if dispo:
                result = "✅ **Livres actuellement disponibles :**\n\n"
                for livre in dispo:
                    result += f"📖 **{livre.titre}** - {livre.auteur}\n"
                    result += f"   🏷️ {livre.categorie} | 📅 {livre.annee_publication}\n"
                    result += f"   📚 {livre.quantite_disponible} exemplaire(s)\n\n"
                result += f"📊 Total : {dispo.count()} livre(s) disponible(s)"
                return result
            return "❌ Aucun livre n'est actuellement disponible."
        
        # === RECHERCHE PAR ID ===
        ids = re.findall(r'\d+', q)
        if ids and ('id' in q or 'ID' in question):
            livre = self.get_book_by_id(int(ids[0]))
            if livre:
                status = "✅ Disponible" if livre.statut == "disponible" else "📖 Emprunté" if livre.statut == "emprunte" else "⏳ Réservé"
                return f"""📖 **Livre trouvé (ID {livre.id}) !**

• **Titre :** {livre.titre}
• **Auteur :** {livre.auteur}
• **Catégorie :** {livre.categorie}
• **Année :** {livre.annee_publication}
• **Statut :** {status}
• **Exemplaires :** {livre.quantite_disponible}"""
            else:
                return f"❌ Aucun livre avec l'ID {ids[0]} n'existe."
        
        # === RECHERCHE PAR TITRE ===
        mots_cles = [m for m in q.split() if len(m) > 2 and m not in ['le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'que', 'qui', 'dans', 'pour', 'avec', 'par']]
        for mot in mots_cles:
            livres = self.search_by_title(mot)
            if livres.exists():
                result = f"🔍 **Livres contenant '{mot}' :**\n\n"
                for livre in livres[:5]:
                    statut_icon = "✅" if livre.statut == "disponible" else "📖"
                    result += f"{statut_icon} **{livre.titre}** - {livre.auteur} ({livre.annee_publication})\n"
                return result
        
        # === RECHERCHE PAR CATÉGORIE ===
        categories = ['roman', 'science-fiction', 'aventure', 'fantaisie', 'policier', 'philosophique', 'conte']
        for cat in categories:
            if cat in q:
                livres = self.get_books_by_category(cat)
                if livres.exists():
                    result = f"🔍 **Livres de {cat} :**\n\n"
                    for livre in livres:
                        statut_icon = "✅" if livre.statut == "disponible" else "📖"
                        result += f"{statut_icon} **{livre.titre}** - {livre.auteur} ({livre.annee_publication})\n"
                    return result
        
        # === RÉPONSE PAR DÉFAUT ===
        return """🤖 **Assistant Bibliothèque**

📝 **Exemples de questions :**

• 📚 "Livres de Victor Hugo" - Recherche par auteur
• 🎁 "Recommande-moi un livre" - Suggestions personnalisées
• 📖 "Affiche tous les livres" - Catalogue complet
• ✅ "Livres disponibles" - Voir disponibilités
• 🔍 "Le Petit Prince" - Rechercher un titre
• 🆔 "Livre avec ID 1" - Rechercher par ID
• 🏷️ "Livres de science-fiction" - Par catégorie

💬 **Posez votre question en français !**"""
    
    def chat(self, question, use_gemini=True):
        """Fonction principale de chat"""
        if use_gemini and self.gemini_ok:
            return self.ask_gemini(question)
        else:
            return self.ask_simple(question)

# Point d'entrée
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 CHATBOT BIBLIOTHÈQUE")
    print("=" * 60)
    
    bot = BibliothequeChatbot()
    
    if bot.gemini_ok:
        print(f"✅ Mode GEMINI activé - Réponses intelligentes")
    else:
        print(f"✅ Mode HORS LIGNE activé - Recherche dans la base de données")
    
    print("\n" + "=" * 60)
    print("Questions à tester :")
    print("  • Livres de Victor Hugo")
    print("  • Recommande-moi un livre")
    print("  • Affiche tous les livres")
    print("  • Livres disponibles")
    print("  • Le Petit Prince")
    print("=" * 60)
    
    while True:
        try:
            question = input("\n👤 Vous: ")
            if question.lower() in ['quit', 'q', 'exit', 'fin']:
                print("\n👋 Au revoir !")
                break
            
            if question.lower() == 'gemini on':
                bot.gemini_ok = True
                print("✅ Gemini activé")
                continue
            elif question.lower() == 'gemini off':
                bot.gemini_ok = False
                print("⚠️ Gemini désactivé (mode hors ligne)")
                continue
            
            response = bot.chat(question, use_gemini=bot.gemini_ok)
            print(f"\n🤖 Bot: {response}")
            print("-" * 40)
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {e}")