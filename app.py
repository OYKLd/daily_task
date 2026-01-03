import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
import customtkinter as ctk

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("Liste de Tâches Quotidiennes")
        self.geometry("800x600")
        ctk.set_appearance_mode("system")
        
        # Données
        self.tasks = []
        self.filename = "taches_quotidiennes.json"
        
        # Charger les tâches existantes
        self.load_tasks()
        
        # Configuration de la grille
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Création des widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Titre
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"Liste de Tâches - {datetime.now().strftime('%d/%m/%Y')}",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=10)
        
        # Zone de saisie
        self.task_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Ajouter une nouvelle tâche...",
            width=400
        )
        self.task_entry.pack(pady=10, padx=10, fill="x")
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Bouton Ajouter
        self.add_button = ctk.CTkButton(
            self.main_frame,
            text="Ajouter",
            command=self.add_task
        )
        self.add_button.pack(pady=5)
        
        # Liste des tâches
        self.tasks_frame = ctk.CTkScrollableFrame(self)
        self.tasks_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        # Charger les tâches existantes
        self.update_tasks_display()
        
        # Boutons en bas
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Effacer terminées",
            command=self.clear_completed,
            fg_color="#FF6B6B",
            hover_color="#FF5252"
        )
        self.clear_button.pack(side="left", padx=5)
        
        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="Enregistrer",
            command=self.save_tasks,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.save_button.pack(side="left", padx=5)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                "id": len(self.tasks) + 1,
                "text": task_text,
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.update_tasks_display()
    
    def toggle_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self.update_tasks_display()
    
    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.update_tasks_display()
    
    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task["completed"]]
        self.update_tasks_display()
    
    def update_tasks_display(self):
        # Effacer les tâches actuelles
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        # Trier les tâches (non complétées d'abord)
        sorted_tasks = sorted(self.tasks, key=lambda x: x["completed"])
        
        # Afficher les tâches
        for task in sorted_tasks:
            task_frame = ctk.CTkFrame(self.tasks_frame)
            task_frame.pack(fill="x", pady=2, padx=5)
            
            # Checkbox de complétion
            check_var = tk.BooleanVar(value=task["completed"])
            check = ctk.CTkCheckBox(
                task_frame,
                text="",
                variable=check_var,
                command=lambda t=task: self.toggle_task(t["id"])
            )
            check.pack(side="left", padx=5)
            
            # Texte de la tâche
            task_label = ctk.CTkLabel(
                task_frame,
                text=task["text"],
                font=("Arial", 12, "strike" if task["completed"] else "normal")
            )
            task_label.pack(side="left", fill="x", expand=True, padx=5)
            
            # Bouton Supprimer
            delete_btn = ctk.CTkButton(
                task_frame,
                text="×",
                width=30,
                height=30,
                fg_color="#FF6B6B",
                hover_color="#FF5252",
                command=lambda t=task: self.delete_task(t["id"])
            )
            delete_btn.pack(side="right", padx=5)
    
    def save_tasks(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=4)
            messagebox.showinfo("Succès", "Tâches enregistrées avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement: {str(e)}")
    
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
                self.tasks = []

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
