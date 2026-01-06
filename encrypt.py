
try:
    import gnupg
except ImportError:
    print("Erreur : La librairie 'python-gnupg' est requise.")
    print("Veuillez l'installer avec : pip install python-gnupg")
    sys.exit(1)
import sys
import os
import base64

# Files/Dirs to exclude from encryption/listing
EXCLUDES = {'.git', '__pycache__', '.DS_Store', "Others", ".github", ".gitignore", "README.md"}

def encrypt_file(file_path):
    gpg = gnupg.GPG()
    
    # Path to the public key (assumed to be in the same dir as script)
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skyline_key.pub")

    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier d'entrée '{file_path}' est introuvable.")
        return
    
    if not os.path.exists(key_path):
        print(f"Erreur : La clé publique '{key_path}' est introuvable.")
        return

    # Import the key
    with open(key_path, "r") as key_file:
        key_data = key_file.read()
        import_result = gpg.import_keys(key_data)
        
    if not import_result.count:
        print("Erreur : Échec de l'importation de la clé publique.")
        return

    # Get the fingerprint
    fingerprint = import_result.fingerprints[0]

    with open(file_path, "rb") as f:
        status = gpg.encrypt_file(
            f, 
            recipients=[fingerprint],
            output=f"{file_path}.encrypted",
            always_trust=True 
        )

    if status.ok:
        print(f"Fichier chiffré avec succès : {file_path}.encrypted")
        try:
            os.remove(file_path)
            print(f"Fichier original '{file_path}' supprimé.")
        except OSError as e:
            print(f"Erreur lors de la suppression du fichier original : {e}")
    else:
        print(f"Échec du chiffrement : {status.status}")
        print(status.stderr)

def interactive_explorer():
    import questionary
    current_path = "."
    selected_files = set() # Stores absolute paths of selected files

    while True:
        # Clear screen for cleaner UI
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get absolute path for reliable comparison
        abs_current = os.path.abspath(current_path)
        
        choices = []
        
        # Option to go up
        if abs_current != os.path.abspath("."):
            choices.append(questionary.Choice(title=".. (Dossier Parent)", value=".."))

        try:
            items = sorted(os.listdir(current_path))
        except OSError as e:
            print(f"Erreur d'accès à {current_path} : {e}")
            items = []

        dirs_list = []
        files_list = []

        for item in items:
            if item in EXCLUDES:
                continue
            if item == "encrypt.py" or item == "skyline_key.pub":
                continue
            if item.endswith(".encrypted"):
                continue
            
            full_path = os.path.join(current_path, item)
            if os.path.isdir(full_path):
                dirs_list.append(item)
            else:
                files_list.append(item)

        # Add Directories
        for d in dirs_list:
            choices.append(questionary.Choice(title=f"📂 {d}/", value=f"DIR:{d}"))

        # Add Files with selection state
        for f in files_list:
            full_path = os.path.abspath(os.path.join(current_path, f))
            prefix = "[x]" if full_path in selected_files else "[ ]"
            choices.append(questionary.Choice(title=f"{prefix} {f}", value=f"FILE:{f}"))

        # Add Done option
        file_count = len(selected_files)
        choices.append(questionary.Separator())
        choices.append(questionary.Choice(title=f"✅ Terminé (Chiffrer {file_count} fichiers)", value="DONE"))
        choices.append(questionary.Choice(title="❌ Annuler", value="CANCEL"))

        # Show menu
        # We use select() because we want to trigger an action (toggle/nav) immediately
        action = questionary.select(
            f"Dossier actuel : {os.path.relpath(abs_current, start=os.path.abspath('.'))}\nSélectionnez un fichier à examiner ou basculez la sélection :",
            choices=choices,
            use_indicator=True
        ).ask()

        if action is None:
            sys.exit(0)

        if action == "CANCEL":
            sys.exit(0)
        elif action == "DONE":
            if not selected_files:
                print("Aucun fichier sélectionné.")
                sys.exit(0)
            return list(selected_files)
        elif action == "..":
            current_path = os.path.dirname(current_path)
        elif action.startswith("DIR:"):
            dirname = action.split(":", 1)[1]
            current_path = os.path.join(current_path, dirname)
        elif action.startswith("FILE:"):
            filename = action.split(":", 1)[1]
            full_path = os.path.abspath(os.path.join(current_path, filename))
            if full_path in selected_files:
                selected_files.remove(full_path)
            else:
                selected_files.add(full_path)

def encrypt_string(text):
    gpg = gnupg.GPG()
    
    # Path to the public key (assumed to be in the same dir as script)
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skyline_key.pub")
    
    if not os.path.exists(key_path):
        print(f"Erreur : La clé publique '{key_path}' est introuvable.")
        return

    with open(key_path, "r") as key_file:
        key_data = key_file.read()
        import_result = gpg.import_keys(key_data)
        
    if not import_result.count:
        print("Erreur : Échec de l'importation de la clé publique.")
        return

    fingerprint = import_result.fingerprints[0]

    encrypted_data_gpg = gpg.encrypt(
        text, 
        recipients=[fingerprint],
        always_trust=True,
        armor=True
    )
    encrypted_data = base64.b64encode(str(encrypted_data_gpg).encode()).decode('utf-8')

    if encrypted_data_gpg.ok:
        print("\n----- Flag Chiffré (GPG encodé en base64) -----")
        print(encrypted_data)
        print("------------------------\n")
    else:
        print(f"Échec du chiffrement : {encrypted_data_gpg.status}")
        print(encrypted_data_gpg.stderr)

def main_menu():
    import questionary
    os.system('cls' if os.name == 'nt' else 'clear')
    
    action = questionary.select(
        "Que souhaitez-vous chiffrer ?",
        choices=[
            questionary.Choice("📂 Chiffrer un fichier", value="FILE"),
            questionary.Choice("🚩 Chiffrer un flag", value="FLAG"),
            questionary.Choice("❌ Quitter", value="EXIT")
        ]
    ).ask()

    return action if action is not None else "EXIT"

if __name__ == "__main__":
    # Startup Warning
    print("\n⚠️  ATTENTION : Le fichier original sera supprimé après chiffrement !")
    print("Seul le fichier chiffré (.encrypted) restera.")
    print("Seul l'administrateur pourra restaurer le fichier original.")
    print("Assurez vous de faire un backup local du fichier original avant de le chiffrer.")
    
    confirm = input("Êtes-vous sûr de vouloir continuer ? (o/N) : ").strip().lower()
    if confirm not in ['o', 'oui', 'y', 'yes']:
        print("Opération annulée.")
        sys.exit(0)
    print("") # Newline for spacing

    if len(sys.argv) == 2:
        target_path = sys.argv[1]
        if os.path.isdir(target_path):
            print(f"Erreur : '{target_path}' est un dossier. Le chiffrement de dossier n'est pas supporté.")
        else:
            print(f"Vous allez chiffrer le fichier : {target_path}")
            response = input("Êtes-vous sûr de vouloir continuer ? (o/N) : ").strip().lower()
            if response in ['o', 'oui', 'y', 'yes']:
                encrypt_file(target_path)
            else:
                print("Opération annulée.")
    else:
        try:
            import questionary
        except ImportError:
            print("Erreur : La librairie 'questionary' est requise pour le mode interactif.")
            print("Veuillez l'installer avec : pip install questionary")
            sys.exit(1)

        try:
            while True:
                mode = main_menu()
                
                if mode == "EXIT":
                    sys.exit(0)
                
                elif mode == "FILE":
                    files_to_encrypt = interactive_explorer()
                    if files_to_encrypt:
                        print("\nVous allez chiffrer les fichiers suivants :")
                        for f in files_to_encrypt:
                            print(f" - {f}")
                        
                        confirm = questionary.confirm("Êtes-vous sûr de vouloir continuer ?", default=False).ask()
                        
                        if confirm:
                            for file_path in files_to_encrypt:
                                encrypt_file(file_path)
                        else:
                            print("Opération annulée.")
                            
                        input("\nAppuyez sur Entrée pour continuer...")
                    
                elif mode == "FLAG":
                    flag = questionary.text("Entrez le flag/chaîne à chiffrer :").ask()
                    
                    if flag is None:
                        continue

                    if flag:
                        encrypt_string(flag)
                        input("Appuyez sur Entrée pour continuer...")
        except KeyboardInterrupt:
            print("\n\nProgramme interrompu par l'utilisateur. Au revoir :) !")
            sys.exit(0)

