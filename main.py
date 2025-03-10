import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AppPompiers:
    def __init__(self, root):
        self.root = root
        self.root.title("Urgences Pompiers - Signalement")
        self.root.geometry("1000x700")
        
        # Configuration du style
        self.setup_styles()
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Titre principal
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        title_label = ttk.Label(
            title_frame,
            text="CENTRE D'URGENCE POMPIERS",
            style='Title.TLabel'
        )
        title_label.pack()
        emergency_label = ttk.Label(
            title_frame,
            text="Numéro d'urgence : 18 ou 112",
            style='Emergency.TLabel'
        )
        emergency_label.pack()

        # Bouton d'urgence
        emergency_button = ttk.Button(
            main_frame,
            text=" SIGNALER UNE URGENCE ",
            style='Emergency.TButton',
            command=self.nouvelle_urgence
        )
        emergency_button.pack(pady=(0, 20), ipadx=20, ipady=10)

        # Création des onglets
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill='both')

        # Onglets principaux
        self.tab_urgences = ttk.Frame(self.notebook)
        self.tab_historique = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_urgences, text='Signalement')
        self.notebook.add(self.tab_historique, text='Historique')

        self.setup_urgences_tab()
        self.setup_historique_tab()

    def setup_styles(self):
        style = ttk.Style()
        
        # Style du titre
        style.configure(
            'Title.TLabel',
            font=('Helvetica', 24, 'bold'),
            foreground='#FF0000',
            padding=10
        )
        
        # Style du numéro d'urgence
        style.configure(
            'Emergency.TLabel',
            font=('Helvetica', 16),
            foreground='#FF0000',
            padding=5
        )
        
        # Style du bouton d'urgence
        style.configure(
            'Emergency.TButton',
            font=('Helvetica', 14, 'bold'),
            background='#FF0000',
            foreground='white'
        )

    def setup_urgences_tab(self):
        # Formulaire d'urgence
        form_frame = ttk.LabelFrame(
            self.tab_urgences,
            text="Détails de l'urgence",
            padding="20"
        )
        form_frame.pack(fill='x', padx=20, pady=10)

        # Type d'urgence
        ttk.Label(form_frame, text="Type d'urgence:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.type_urgence = ttk.Combobox(
            form_frame,
            values=[
                " Incendie",
                " Accident de la route",
                " Urgence médicale",
                " Incident domestique",
                " Incident naturel",
                " Autre urgence"
            ],
            width=30
        )
        self.type_urgence.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Localisation
        ttk.Label(form_frame, text="Adresse précise:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.adresse_entry = ttk.Entry(form_frame, width=50)
        self.adresse_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Description
        ttk.Label(form_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.description_text = tk.Text(form_frame, height=4, width=50)
        self.description_text.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Nombre de personnes concernées
        ttk.Label(form_frame, text="Personnes concernées:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.nb_personnes = ttk.Spinbox(form_frame, from_=1, to=100, width=5)
        self.nb_personnes.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Bouton de soumission
        submit_frame = ttk.Frame(form_frame)
        submit_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            submit_frame,
            text="Envoyer le signalement",
            command=self.envoyer_signalement
        ).pack(pady=10)

    def setup_historique_tab(self):
        # Liste des signalements
        self.tree_historique = ttk.Treeview(
            self.tab_historique,
            columns=('Date', 'Type', 'Adresse', 'Personnes', 'Statut'),
            show='headings'
        )
        
        # Configuration des colonnes
        self.tree_historique.heading('Date', text='Date et Heure')
        self.tree_historique.heading('Type', text="Type d'urgence")
        self.tree_historique.heading('Adresse', text='Adresse')
        self.tree_historique.heading('Personnes', text='Personnes')
        self.tree_historique.heading('Statut', text='Statut')
        
        # Ajustement des colonnes
        self.tree_historique.column('Date', width=150)
        self.tree_historique.column('Type', width=150)
        self.tree_historique.column('Adresse', width=250)
        self.tree_historique.column('Personnes', width=100)
        self.tree_historique.column('Statut', width=100)
        
        self.tree_historique.pack(fill='both', expand=True, padx=20, pady=10)

    def nouvelle_urgence(self):
        self.notebook.select(0)  # Aller à l'onglet de signalement
        self.type_urgence.focus()

    def envoyer_signalement(self):
        type_urg = self.type_urgence.get()
        adresse = self.adresse_entry.get()
        description = self.description_text.get("1.0", tk.END).strip()
        nb_pers = self.nb_personnes.get()

        if not all([type_urg, adresse, description, nb_pers]):
            messagebox.showerror(
                "Erreur",
                "Veuillez remplir tous les champs du formulaire"
            )
            return

        # Ajouter à l'historique
        date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.tree_historique.insert(
            '',
            'end',
            values=(date_actuelle, type_urg, adresse, nb_pers, "En cours")
        )

        # Confirmation
        messagebox.showinfo(
            "Signalement envoyé",
            "Votre signalement a été transmis aux équipes d'intervention.\nLes secours sont en route."
        )

        # Réinitialiser le formulaire
        self.type_urgence.set('')
        self.adresse_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
        self.nb_personnes.delete(0, tk.END)
        self.nb_personnes.insert(0, "1")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppPompiers(root)
    root.mainloop()
