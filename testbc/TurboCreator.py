import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import threading

# Variables globales pour la langue
LANGUAGE = "english"  # Par défaut en anglais

def set_language(lang):
    global LANGUAGE
    LANGUAGE = lang
    update_ui_text()

def update_ui_text():
    if LANGUAGE == "english":
        button_download.config(text="Download the 2 essential scripts")
        button_node.config(text="Test locally")
        button_teleport.config(text="Teleportation to essential scripts")
        button_default_project.config(text="Default Project Teleporter")
        button_sound_effects.config(text="Teleport to Sound Effects")
        settings_button.config(text="Settings")
    else:
        button_download.config(text="Télécharger les 2 scripts essentiels")
        button_node.config(text="Tester en local")
        button_teleport.config(text="Téléportation vers les scripts essentiels")
        button_default_project.config(text="Téléportation vers le projet par défaut")
        button_sound_effects.config(text="Téléportation vers les effets de sons")
        settings_button.config(text="Paramètres")

def execute_script():
    response = messagebox.askyesno("Confirmation", "Are you sure you want to continue?" if LANGUAGE == "english" else "Êtes-vous sûr de vouloir continuer ?")
    
    if response:
        progress_bar['value'] = 0
        progress_label.config(text="0%")
        progress_bar.grid()  # Afficher la barre de progression
        root.update_idletasks()
        threading.Thread(target=run_tasks).start()

def run_tasks():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        
        os.chdir(target_directory)
        
        subprocess.run(["git", "clone", "https://github.com/TurboWarp/scratch-gui.git"], shell=True)
        update_progress(25)
        
        subprocess.run(["git", "clone", "https://github.com/TurboWarp/scratch-vm.git"], shell=True)
        update_progress(50)
        
        messagebox.showinfo("Success", f"The repositories have been successfully cloned into {target_directory}!" if LANGUAGE == "english" else f"Les dépôts ont été clonés avec succès dans {target_directory} !")
        update_progress(100)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}" if LANGUAGE == "english" else f"Une erreur s'est produite : {e}")
    finally:
        progress_bar.grid_remove()  # Masquer la barre de progression

def execute_node_commands():
    try:
        subprocess.run(["npm", "-v"], shell=True, check=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "npm is not installed or not in the PATH." if LANGUAGE == "english" else "npm n'est pas installé ou n'est pas dans le PATH.")
        return
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred while running npm." if LANGUAGE == "english" else "Une erreur s'est produite lors de l'exécution de npm.")
        return

    try:
        progress_bar['value'] = 0
        progress_label.config(text="0%")
        progress_bar.grid()  # Afficher la barre de progression
        root.update_idletasks()
        threading.Thread(target=run_node_tasks).start()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}" if LANGUAGE == "english" else f"Une erreur s'est produite : {e}")

def run_node_tasks():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        vm_directory = os.path.join(target_directory, "scratch-vm")
        os.chdir(vm_directory)
        
        subprocess.run(["npm", "install"], shell=True, check=True)
        update_progress(25)
        
        subprocess.run(["npm", "link"], shell=True, check=True)
        update_progress(50)
        
        gui_directory = os.path.join(target_directory, "scratch-gui")
        os.chdir(gui_directory)
        
        subprocess.run(["npm", "install"], shell=True, check=True)
        update_progress(75)
        
        subprocess.run(["npm", "link", "scratch-vm"], shell=True, check=True)
        update_progress(90)
        
        subprocess.run(["npm", "start"], shell=True, check=True)
        update_progress(100)
        
        subprocess.run(["start", "http://localhost:8601/"], shell=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}" if LANGUAGE == "english" else f"Une erreur s'est produite : {e}")
    finally:
        progress_bar.grid_remove()  # Masquer la barre de progression

def teleport_to_scripts():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        libraries_directory = os.path.join(target_directory, "scratch-gui", "src", "lib", "libraries")
        
        if os.path.exists(libraries_directory):
            # Ouvrir le dossier dans l'explorateur de fichiers
            if os.name == "nt":  # Pour Windows
                os.startfile(libraries_directory)
            elif os.name == "posix":  # Pour macOS et Linux
                subprocess.run(["open", libraries_directory] if os.name == "darwin" else ["xdg-open", libraries_directory])
        else:
            messagebox.showerror("Error", "The directory does not exist." if LANGUAGE == "english" else "Le répertoire n'existe pas.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}" if LANGUAGE == "english" else f"Une erreur s'est produite : {e}")

def teleport_to_default_project():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        default_project_directory = os.path.join(target_directory, "scratch-gui", "src", "lib", "default-project")
        
        if os.path.exists(default_project_directory):
            # Ouvrir le dossier dans l'explorateur de fichiers
            if os.name == "nt":  # Pour Windows
                os.startfile(default_project_directory)
            elif os.name == "posix":  # Pour macOS et Linux
                subprocess.run(["open", default_project_directory] if os.name == "darwin" else ["xdg-open", default_project_directory])
        else:
            messagebox.showerror("Error", "The directory does not exist." if LANGUAGE == "english" else "Le répertoire n'existe pas.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}" if LANGUAGE == "english" else f"Une erreur s'est produite : {e}")

def teleport_to_sound_effects():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        sound_effects_directory = os.path.join(target_directory, "scratch-gui", "src", "lib", "audio", "effects")
        
        if os.path.exists(sound_effects_directory):
            # Ouvrir le dossier dans l'explorateur de fichiers
            if os.name == "nt":  # Pour Windows
                os.startfile(sound_effects_directory)
            elif os.name == "posix":  # Pour macOS et Linux
                subprocess.run(["open", sound_effects_directory] if os.name == "darwin" else ["xdg-open", sound_effects_directory])
        else:
            messagebox.showerror("Error", "The directory does not exist." if LANGUAGE == "english" else "Le répertoire n'existe pas.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}" if LANGUAGE == "english" else f"Une erreur s'est produite : {e}")

def update_progress(value):
    progress_bar['value'] = value
    progress_label.config(text=f"{value}%")
    root.update_idletasks()

# Créer la fenêtre principale
root = tk.Tk()
root.title("TurboCreator")

# Définir la taille de la fenêtre
root.geometry("400x450")  # Augmenter la hauteur pour le nouveau bouton

# Créer un bouton pour télécharger les scripts
button_download = tk.Button(root, text="Download the 2 essential scripts", command=execute_script, font=("Arial", 16))
button_download.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

# Créer un bouton pour exécuter les commandes Node.js
button_node = tk.Button(root, text="Test locally", command=execute_node_commands, font=("Arial", 16))
button_node.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

# Créer un bouton pour la téléportation vers les scripts essentiels
button_teleport = tk.Button(root, text="Teleportation to essential scripts", command=teleport_to_scripts, font=("Arial", 16))
button_teleport.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# Créer un bouton pour la téléportation vers le projet par défaut
button_default_project = tk.Button(root, text="Default Project Teleporter", command=teleport_to_default_project, font=("Arial", 16))
button_default_project.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# Créer un bouton pour la téléportation vers les effets de sons
button_sound_effects = tk.Button(root, text="Teleport to Sound Effects", command=teleport_to_sound_effects, font=("Arial", 16))
button_sound_effects.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Créer une barre de progression
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
progress_bar.grid_remove()  # Masquer la barre de progression initialement

# Créer un label pour afficher le pourcentage
progress_label = tk.Label(root, text="0%")
progress_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# Créer un bouton de paramètres
settings_button = tk.Button(root, text="Settings", command=lambda: settings_window(), font=("Arial", 12))
settings_button.place(relx=0.9, rely=0.1, anchor=tk.CENTER)

def settings_window():
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("200x100")
    
    lang_label = tk.Label(settings_win, text="Choose language:")
    lang_label.pack(pady=10)
    
    lang_frame = tk.Frame(settings_win)
    lang_frame.pack()
    
    english_button = tk.Button(lang_frame, text="English", command=lambda: set_language("english"))
    english_button.pack(side=tk.LEFT, padx=5)
    
    french_button = tk.Button(lang_frame, text="Français", command=lambda: set_language("french"))
    french_button.pack(side=tk.RIGHT, padx=5)

# Démarrer la boucle principale de l'interface
root.mainloop()