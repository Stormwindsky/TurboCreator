import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import threading
import re
from tkinter import font as tkfont

# --------------------------------------
# VARIABLES GLOBALES
# --------------------------------------
LANGUAGE = "english"

# Couleurs
BG_COLOR = "#2d2d2d"
BUTTON_COLOR = "#3a3a3a"
HOVER_COLOR = "#4a4a4a"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#4CAF50"
PROGRESS_COLOR = "#4CAF50"
SETTINGS_COLOR = "#3a3a3a"

# Repère : bouton « localhost »
localhost_button = None
localhost_visible = False

# --------------------------------------
# LANGUES
# --------------------------------------
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
        if localhost_button:
            localhost_button.config(text="Open in Browser (localhost)")
    else:
        button_download.config(text="Télécharger les 2 scripts essentiels")
        button_node.config(text="Tester en local")
        button_teleport.config(text="Téléportation vers les scripts essentiels")
        button_default_project.config(text="Téléportation vers le projet par défaut")
        button_sound_effects.config(text="Téléportation vers les effets de sons")
        settings_button.config(text="Paramètres")
        if localhost_button:
            localhost_button.config(text="Ouvrir dans le navigateur (localhost)")

# --------------------------------------
# ANIMATIONS BOUTONS
# --------------------------------------
def animate_button(button, color, hover_color):
    def on_enter(e):
        button.config(bg=hover_color, relief=tk.SUNKEN)
    def on_leave(e):
        button.config(bg=color, relief=tk.RAISED)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def create_modern_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground=HOVER_COLOR,
        activeforeground=TEXT_COLOR,
        relief=tk.RAISED,
        borderwidth=0,
        font=("Segoe UI", 12),
        padx=20,
        pady=10
    )
    animate_button(btn, BUTTON_COLOR, HOVER_COLOR)
    return btn

# --------------------------------------
# BARRE DE PROGRESSION
# --------------------------------------
def update_progress(value):
    progress_bar['value'] = value
    progress_label.config(text=f"{value}%")
    root.update_idletasks()

# --------------------------------------
# TÉLÉCHARGEMENT DES REPOS
# --------------------------------------
def execute_script():
    if not messagebox.askyesno("Confirmation",
                               "Are you sure you want to continue?" if LANGUAGE == "english"
                               else "Êtes-vous sûr de vouloir continuer ?"):
        return
    reset_localhost_button()
    progress_bar['value'] = 0
    progress_label.config(text="0%")
    progress_bar.pack()
    root.update_idletasks()
    threading.Thread(target=run_tasks).start()

def run_tasks():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        os.makedirs(target_directory, exist_ok=True)
        os.chdir(target_directory)

        subprocess.run(["git", "clone", "https://github.com/TurboWarp/scratch-gui.git"], shell=True)
        update_progress(50)

        subprocess.run(["git", "clone", "https://github.com/TurboWarp/scratch-vm.git"], shell=True)
        update_progress(100)

        messagebox.showinfo("Success",
                            f"The repositories have been successfully cloned into {target_directory}!"
                            if LANGUAGE == "english"
                            else f"Les dépôts ont été clonés avec succès dans {target_directory} !")
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred: {e}" if LANGUAGE == "english"
                             else f"Une erreur s'est produite : {e}")
    finally:
        progress_bar.pack_forget()

# --------------------------------------
# TEST LOCAL / SERVEUR
# --------------------------------------
def execute_node_commands():
    try:
        subprocess.run(["npm", "-v"], shell=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        msg = "npm is not installed or not in the PATH." if LANGUAGE == "english" \
              else "npm n'est pas installé ou n'est pas dans le PATH."
        messagebox.showerror("Error", msg)
        return

    reset_localhost_button()
    progress_bar['value'] = 0
    progress_label.config(text="0%")
    progress_bar.pack()
    root.update_idletasks()
    threading.Thread(target=run_node_tasks).start()

def run_node_tasks():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)

        vm_directory = os.path.join(target_directory, "scratch-vm")
        os.chdir(vm_directory)
        subprocess.run(["npm", "install"], shell=True, check=True)
        update_progress(20)

        subprocess.run(["npm", "link"], shell=True, check=True)
        update_progress(40)

        gui_directory = os.path.join(target_directory, "scratch-gui")
        os.chdir(gui_directory)
        subprocess.run(["npm", "install"], shell=True, check=True)
        update_progress(60)

        subprocess.run(["npm", "link", "scratch-vm"], shell=True, check=True)
        update_progress(80)

        # npm start + attente Compiled successfully
        proc = subprocess.Popen(["npm", "start"], shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True, bufsize=1)
        for line in iter(proc.stdout.readline, ''):
            if re.search(r"Compiled successfully", line):
                update_progress(100)
                show_localhost_button()
                break
        proc.stdout.close()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error",
                             f"An error occurred: {e}" if LANGUAGE == "english"
                             else f"Une erreur s'est produite : {e}")
    finally:
        progress_bar.pack_forget()

# --------------------------------------
# BOUTON LOCALHOST
# --------------------------------------
def show_localhost_button():
    global localhost_button, localhost_visible
    if localhost_button is None:
        localhost_button = create_modern_button(button_frame,
                                                "Open in Browser (localhost)" if LANGUAGE == "english"
                                                else "Ouvrir dans le navigateur (localhost)",
                                                open_localhost)
    localhost_button.pack(fill=tk.X, pady=5)
    localhost_visible = True

def reset_localhost_button():
    global localhost_visible
    if localhost_button and localhost_visible:
        localhost_button.pack_forget()
        localhost_visible = False

def open_localhost():
    url = "http://localhost:8601/"
    if os.name == "nt":
        os.startfile(url)
    elif os.name == "posix":
        subprocess.run(["open", url] if os.name == "darwin" else ["xdg-open", url])

# --------------------------------------
# TÉLÉPORTATIONS
# --------------------------------------
def teleport_to_scripts():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        libraries_directory = os.path.join(target_directory, "scratch-gui", "src", "lib", "libraries")
        if not os.path.exists(libraries_directory):
            raise FileNotFoundError
        opener = "open" if os.name == "darwin" else "xdg-open" if os.name == "posix" else "start"
        subprocess.run([opener, libraries_directory], shell=True)
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred: {e}" if LANGUAGE == "english"
                             else f"Une erreur s'est produite : {e}")

def teleport_to_default_project():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        default_project_directory = os.path.join(target_directory, "scratch-gui", "src", "lib", "default-project")
        if not os.path.exists(default_project_directory):
            raise FileNotFoundError
        opener = "open" if os.name == "darwin" else "xdg-open" if os.name == "posix" else "start"
        subprocess.run([opener, default_project_directory], shell=True)
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred: {e}" if LANGUAGE == "english"
                             else f"Une erreur s'est produite : {e}")

def teleport_to_sound_effects():
    try:
        downloads_directory = os.path.join(os.path.expanduser("~"), "Downloads")
        clone_directory = os.path.join(downloads_directory, "testbc")
        script_name = os.path.splitext(os.path.basename(__file__))[0]
        target_directory = os.path.join(clone_directory, script_name)
        sound_effects_directory = os.path.join(target_directory, "scratch-gui", "src", "lib", "audio", "effects")
        if not os.path.exists(sound_effects_directory):
            raise FileNotFoundError
        opener = "open" if os.name == "darwin" else "xdg-open" if os.name == "posix" else "start"
        subprocess.run([opener, sound_effects_directory], shell=True)
    except Exception as e:
        messagebox.showerror("Error",
                             f"An error occurred: {e}" if LANGUAGE == "english"
                             else f"Une erreur s'est produite : {e}")

# --------------------------------------
# FENÊTRE PRINCIPALE
# --------------------------------------
root = tk.Tk()
root.title("TurboCreator")
root.configure(bg=BG_COLOR)
root.geometry("500x600")

style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", thickness=20, troughcolor=BG_COLOR,
                bordercolor=BG_COLOR, lightcolor=PROGRESS_COLOR,
                darkcolor=PROGRESS_COLOR, background=PROGRESS_COLOR)

title_label = tk.Label(root, text="TurboCreator", font=("Segoe UI", 24, "bold"),
                       fg=ACCENT_COLOR, bg=BG_COLOR)
title_label.pack(pady=20)

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

button_download = create_modern_button(button_frame, "Download the 2 essential scripts", execute_script)
button_download.pack(fill=tk.X, pady=5)

button_node = create_modern_button(button_frame, "Test locally", execute_node_commands)
button_node.pack(fill=tk.X, pady=5)

localhost_button = None  # sera créé dynamiquement

button_teleport = create_modern_button(button_frame, "Teleportation to essential scripts", teleport_to_scripts)
button_teleport.pack(fill=tk.X, pady=5)

button_default_project = create_modern_button(button_frame, "Default Project Teleporter", teleport_to_default_project)
button_default_project.pack(fill=tk.X, pady=5)

button_sound_effects = create_modern_button(button_frame, "Teleport to Sound Effects", teleport_to_sound_effects)
button_sound_effects.pack(fill=tk.X, pady=5)

progress_frame = tk.Frame(root, bg=BG_COLOR)
progress_frame.pack(pady=20, padx=20, fill=tk.BOTH)

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(fill=tk.X)
progress_bar.pack_forget()

progress_label = tk.Label(progress_frame, text="0%", fg=TEXT_COLOR, bg=BG_COLOR, font=("Segoe UI", 12))
progress_label.pack()

settings_button = tk.Button(root, text="Settings", command=lambda: settings_window(),
                            bg=SETTINGS_COLOR, fg=TEXT_COLOR, activebackground=HOVER_COLOR,
                            activeforeground=TEXT_COLOR, borderwidth=0, font=("Segoe UI", 12))
settings_button.place(relx=0.95, rely=0.05, anchor=tk.NE)
animate_button(settings_button, SETTINGS_COLOR, HOVER_COLOR)

def settings_window():
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("300x150")
    settings_win.configure(bg=BG_COLOR)
    settings_win.resizable(False, False)
    title = tk.Label(settings_win, text="Language Settings", font=("Segoe UI", 14, "bold"),
                     fg=ACCENT_COLOR, bg=BG_COLOR)
    title.pack(pady=10)
    lang_frame = tk.Frame(settings_win, bg=BG_COLOR)
    lang_frame.pack(pady=10)
    english_button = create_modern_button(lang_frame, "English", lambda: set_language("english"))
    english_button.pack(side=tk.LEFT, padx=10)
    french_button = create_modern_button(lang_frame, "Français", lambda: set_language("french"))
    french_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()