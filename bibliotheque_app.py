# Configuration Django AVANT d'importer les modèles
import os
import sys

# Ajouter le chemin du projet
sys.path.append('C:/Users/DELL_2025/bibliotheque')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliotheque.settings')

# Initialiser Django
import django
django.setup()

# Maintenant on peut importer les modèles Django
from livres.models import Livre

# Import CustomTkinter
import customtkinter as ctk
from tkinter import messagebox, ttk

# Configuration du thème moderne
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BibliothequeApp:
    def __init__(self):
        # Fenêtre principale
        self.window = ctk.CTk()
        self.window.title("📚 Bibliothèque Numérique - Django + CustomTkinter")
        self.window.geometry("1300x750")
        self.window.minsize(1100, 650)
        
        # Centrer la fenêtre
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1300 // 2)
        y = (self.window.winfo_screenheight() // 2) - (750 // 2)
        self.window.geometry(f'1300x750+{x}+{y}')
        
        # Interface
        self.setup_ui()
        
        # Charger les livres
        self.load_books()
    
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        
        # Frame principale
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # HEADER
        self.header = ctk.CTkFrame(self.main_frame, height=100, corner_radius=15)
        self.header.pack(fill="x", padx=10, pady=(0, 20))
        self.header.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.header, 
            text="📚 Bibliothèque Numérique - Django + CustomTkinter", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", padx=30, pady=20)
        
        self.stats_label = ctk.CTkLabel(
            self.header,
            text="📊 0 livre(s)",
            font=ctk.CTkFont(size=16)
        )
        self.stats_label.pack(side="right", padx=30)
        
        # PANEL DE CONTRÔLE
        self.control_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.control_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        # Boutons
        self.btn_add = ctk.CTkButton(
            self.control_frame,
            text="➕ Ajouter",
            command=self.open_add_dialog,
            height=40,
            width=120,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.btn_add.pack(side="left", padx=10, pady=15)
        
        self.btn_edit = ctk.CTkButton(
            self.control_frame,
            text="✏️ Modifier",
            command=self.open_edit_dialog,
            height=40,
            width=120,
            font=ctk.CTkFont(size=14),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.btn_edit.pack(side="left", padx=10, pady=15)
        
        self.btn_delete = ctk.CTkButton(
            self.control_frame,
            text="🗑️ Supprimer",
            command=self.delete_book,
            height=40,
            width=120,
            font=ctk.CTkFont(size=14),
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.btn_delete.pack(side="left", padx=10, pady=15)
        
        self.btn_refresh = ctk.CTkButton(
            self.control_frame,
            text="🔄 Actualiser",
            command=self.load_books,
            height=40,
            width=120,
            font=ctk.CTkFont(size=14),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.btn_refresh.pack(side="left", padx=10, pady=15)
        
        self.btn_chatbot = ctk.CTkButton(
            self.control_frame,
            text="🤖 Chatbot IA",
            command=self.open_chatbot,
            height=40,
            width=120,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        self.btn_chatbot.pack(side="left", padx=10, pady=15)
        
        # Barre de recherche
        self.search_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.search_frame.pack(side="right", padx=10, pady=15)
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Rechercher par titre ou auteur...",
            width=300,
            height=40
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_books())
        
        self.btn_search = ctk.CTkButton(
            self.search_frame,
            text="Rechercher",
            command=self.search_books,
            height=40,
            width=100
        )
        self.btn_search.pack(side="left", padx=5)
        
        # TABLEAU
        self.table_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=35,
                       fieldbackground="#2b2b2b")
        style.configure("Treeview.Heading", 
                       background="#1e1e1e",
                       foreground="white",
                       font=('Segoe UI', 11, 'bold'))
        
        scrollbar_y = ttk.Scrollbar(self.table_frame)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(self.table_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        
        columns = ("ID", "Titre", "Auteur", "Catégorie", "Année", "Quantité", "Statut")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            height=20
        )
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Titre", text="📖 Titre")
        self.tree.heading("Auteur", text="✍️ Auteur")
        self.tree.heading("Catégorie", text="🏷️ Catégorie")
        self.tree.heading("Année", text="📅 Année")
        self.tree.heading("Quantité", text="📚 Qté")
        self.tree.heading("Statut", text="✅ Statut")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Titre", width=280)
        self.tree.column("Auteur", width=200)
        self.tree.column("Catégorie", width=150)
        self.tree.column("Année", width=80, anchor="center")
        self.tree.column("Quantité", width=80, anchor="center")
        self.tree.column("Statut", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Double-clic pour modifier
        self.tree.bind("<Double-1>", lambda e: self.open_edit_dialog())
    
    def load_books(self, search_term=None):
        """Charger tous les livres via Django ORM"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if search_term:
                livres = Livre.objects.filter(
                    models.Q(titre__icontains=search_term) | 
                    models.Q(auteur__icontains=search_term)
                ).order_by('id')
            else:
                livres = Livre.objects.all().order_by('id')
            
            for livre in livres:
                status_display = ""
                if livre.statut == 'disponible':
                    status_display = "✅ Disponible"
                elif livre.statut == 'emprunte':
                    status_display = "📖 Emprunté"
                else:
                    status_display = "⏳ Réservé"
                
                self.tree.insert("", "end", values=(
                    livre.id, livre.titre, livre.auteur, 
                    livre.categorie, livre.annee_publication, 
                    livre.quantite_disponible, status_display
                ))
            
            count = Livre.objects.count()
            self.stats_label.configure(text=f"📊 {count} livre(s)")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur chargement: {str(e)}")
    
    def search_books(self):
        """Rechercher"""
        search_term = self.search_entry.get()
        self.load_books(search_term if search_term else None)
    
    def open_add_dialog(self):
        """Ajouter un livre via Django ORM"""
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("➕ Ajouter un livre")
        dialog.geometry("600x700")
        dialog.grab_set()
        dialog.transient(self.window)
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f'600x700+{x}+{y}')
        
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(main_frame, text="➕ Nouveau livre", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 30))
        
        # Champs
        ctk.CTkLabel(main_frame, text="📖 Titre:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_titre = ctk.CTkEntry(main_frame, placeholder_text="Ex: Le Petit Prince", height=40)
        entry_titre.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="✍️ Auteur:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_auteur = ctk.CTkEntry(main_frame, placeholder_text="Ex: Antoine de Saint-Exupéry", height=40)
        entry_auteur.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="🏷️ Catégorie:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_categorie = ctk.CTkEntry(main_frame, placeholder_text="Ex: Roman, Science-fiction...", height=40)
        entry_categorie.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="📅 Année:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_annee = ctk.CTkEntry(main_frame, placeholder_text="Ex: 1943", height=40)
        entry_annee.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="📚 Quantité:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_quantite = ctk.CTkEntry(main_frame, placeholder_text="Ex: 3", height=40)
        entry_quantite.insert(0, "1")
        entry_quantite.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="✅ Statut:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        combo_statut = ctk.CTkComboBox(main_frame, values=["disponible", "emprunte", "reserve"], height=40)
        combo_statut.pack(fill="x", pady=(0, 30))
        combo_statut.set("disponible")
        
        def save():
            try:
                titre = entry_titre.get().strip()
                auteur = entry_auteur.get().strip()
                categorie = entry_categorie.get().strip()
                annee = int(entry_annee.get())
                quantite = int(entry_quantite.get())
                statut = combo_statut.get()
                
                if not titre or not auteur:
                    messagebox.showerror("Erreur", "Le titre et l'auteur sont obligatoires")
                    return
                
                # Utilisation de Django ORM
                Livre.objects.create(
                    titre=titre,
                    auteur=auteur,
                    categorie=categorie,
                    annee_publication=annee,
                    quantite_disponible=quantite,
                    statut=statut
                )
                
                messagebox.showinfo("Succès", "✅ Livre ajouté avec succès !")
                dialog.destroy()
                self.load_books()
            except ValueError:
                messagebox.showerror("Erreur", "❌ L'année et la quantité doivent être des nombres")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(btn_frame, text="✅ Ajouter", command=save, height=45, fg_color="#2ecc71").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(btn_frame, text="❌ Annuler", command=dialog.destroy, height=45, fg_color="#7f8c8d").pack(side="right", fill="x", expand=True, padx=(10, 0))
    
    def open_edit_dialog(self):
        """Modifier un livre via Django ORM"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre")
            return
        
        item = self.tree.item(selection[0])
        book_id = item['values'][0]
        
        # Utilisation de Django ORM
        livre = Livre.objects.get(id=book_id)
        
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("✏️ Modifier le livre")
        dialog.geometry("600x700")
        dialog.grab_set()
        dialog.transient(self.window)
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f'600x700+{x}+{y}')
        
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(main_frame, text="✏️ Modifier le livre", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 30))
        
        ctk.CTkLabel(main_frame, text="📖 Titre:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_titre = ctk.CTkEntry(main_frame, height=40)
        entry_titre.insert(0, livre.titre)
        entry_titre.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="✍️ Auteur:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_auteur = ctk.CTkEntry(main_frame, height=40)
        entry_auteur.insert(0, livre.auteur)
        entry_auteur.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="🏷️ Catégorie:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_categorie = ctk.CTkEntry(main_frame, height=40)
        entry_categorie.insert(0, livre.categorie)
        entry_categorie.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="📅 Année:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_annee = ctk.CTkEntry(main_frame, height=40)
        entry_annee.insert(0, str(livre.annee_publication))
        entry_annee.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="📚 Quantité:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        entry_quantite = ctk.CTkEntry(main_frame, height=40)
        entry_quantite.insert(0, str(livre.quantite_disponible))
        entry_quantite.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(main_frame, text="✅ Statut:", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        combo_statut = ctk.CTkComboBox(main_frame, values=["disponible", "emprunte", "reserve"], height=40)
        combo_statut.set(livre.statut)
        combo_statut.pack(fill="x", pady=(0, 30))
        
        def update():
            try:
                # Utilisation de Django ORM
                livre.titre = entry_titre.get().strip()
                livre.auteur = entry_auteur.get().strip()
                livre.categorie = entry_categorie.get().strip()
                livre.annee_publication = int(entry_annee.get())
                livre.quantite_disponible = int(entry_quantite.get())
                livre.statut = combo_statut.get()
                livre.save()
                
                messagebox.showinfo("Succès", "✅ Livre modifié avec succès !")
                dialog.destroy()
                self.load_books()
            except ValueError:
                messagebox.showerror("Erreur", "❌ L'année et la quantité doivent être des nombres")
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(btn_frame, text="💾 Enregistrer", command=update, height=45, fg_color="#3498db").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(btn_frame, text="❌ Annuler", command=dialog.destroy, height=45, fg_color="#7f8c8d").pack(side="right", fill="x", expand=True, padx=(10, 0))
    
    def delete_book(self):
        """Supprimer un livre via Django ORM"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre")
            return
        
        item = self.tree.item(selection[0])
        book_id = item['values'][0]
        book_title = item['values'][1]
        
        if messagebox.askyesno("Confirmation", f"Supprimer '{book_title}' ?"):
            try:
                # Utilisation de Django ORM
                Livre.objects.get(id=book_id).delete()
                self.load_books()
                messagebox.showinfo("Succès", "✅ Livre supprimé")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
    
    def open_chatbot(self):
        """Ouvrir la fenêtre du chatbot avec Gemini"""
        try:
            # Importer le chatbot
            import sys
            sys.path.append('C:/Users/DELL_2025/bibliotheque')
            from chatbot import BibliothequeChatbot
            chatbot = BibliothequeChatbot()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur chatbot: {str(e)}")
            return
        
        chat_window = ctk.CTkToplevel(self.window)
        chat_window.title("🤖 Assistant Bibliothèque IA - Gemini")
        chat_window.geometry("650x700")
        chat_window.grab_set()
        chat_window.transient(self.window)
        
        chat_window.update_idletasks()
        x = (chat_window.winfo_screenwidth() // 2) - (650 // 2)
        y = (chat_window.winfo_screenheight() // 2) - (700 // 2)
        chat_window.geometry(f'650x700+{x}+{y}')
        
        # Header
        header = ctk.CTkFrame(chat_window, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="🤖 Assistant Bibliothèque IA", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)
        ctk.CTkLabel(header, text="Propulsé par Google Gemini", font=ctk.CTkFont(size=12), text_color="#9b59b6").pack()
        
        # Zone de chat
        chat_frame = ctk.CTkFrame(chat_window)
        chat_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        messages_text = ctk.CTkTextbox(chat_frame, height=400, font=ctk.CTkFont(size=13))
        messages_text.pack(fill="both", expand=True, pady=(0, 10))
        messages_text.configure(state="disabled")
        
        # Message de bienvenue
        messages_text.configure(state="normal")
        welcome = """🤖 **Bienvenue sur l'assistant bibliothèque IA !**

Je suis votre bibliothécaire virtuel propulsé par Google Gemini.

✨ **Ce que je peux faire :**
• 🔍 Rechercher des livres par titre, auteur ou ID
• 📊 Afficher le catalogue complet
• ✅ Vérifier la disponibilité des livres
• 📚 Vous recommander des livres

💬 **Exemples :**
• "Affiche tous les livres"
• "Livres disponibles"
• "Trouve Le Petit Prince"
• "Livres de Victor Hugo"

Posez votre question ci-dessous !
"""
        messages_text.insert("end", welcome)
        messages_text.configure(state="disabled")
        
        # Zone de saisie
        input_frame = ctk.CTkFrame(chat_window)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        entry_question = ctk.CTkEntry(input_frame, placeholder_text="Écrivez votre question...", height=45)
        entry_question.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        use_gemini = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(input_frame, text="Gemini AI", variable=use_gemini).pack(side="right", padx=(0, 10))
        
        def send():
            question = entry_question.get().strip()
            if not question:
                return
            
            messages_text.configure(state="normal")
            messages_text.insert("end", f"\n👤 Vous: {question}\n\n")
            entry_question.delete(0, "end")
            
            try:
                response = chatbot.chat(question, use_gemini=use_gemini.get())
                messages_text.insert("end", f"🤖 Assistant: {response}\n\n")
                messages_text.insert("end", "-" * 50 + "\n\n")
            except Exception as e:
                messages_text.insert("end", f"❌ Erreur: {str(e)}\n\n")
            
            messages_text.configure(state="disabled")
            messages_text.see("end")
        
        ctk.CTkButton(input_frame, text="📤 Envoyer", command=send, height=45, width=100, fg_color="#9b59b6").pack(side="right")
        entry_question.bind("<Return>", lambda e: send())
    
    def run(self):
        self.window.mainloop()

# Import pour la recherche
from django.db import models

# Lancer l'application
if __name__ == "__main__":
    app = BibliothequeApp()
    app.run()