import os
import sys
import argparse
import subprocess
import shutil
import shutil
import gnupg
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint
import questionary
from questionary import Style

custom_style = Style([
    ('qmark', 'fg:yellow bold'),        # Token in front of the question
    ('question', 'bold'),               # Question text
    ('answer', 'fg:#f44336 bold'),      # Submitted answer text behind the question
    ('pointer', 'fg:yellow bold'),      # Pointer used in select and checkbox prompts
    ('highlighted', 'fg:yellow bold'),  # Pointed-at choice in select and checkbox prompts
    ('selected', 'fg:yellow'),          # Style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # Separator in lists
    ('instruction', ''),                # User instructions for select, rawselect, checkbox
    ('text', ''),                       # Plain text
    ('disabled', 'fg:#858585 italic'),  # Disabled choices for select and checkbox prompts
    # Autocomplete menu specific styles - Force bg:default to remove grey background
    ('completion-menu.completion', 'fg:white bg:default'),
    ('completion-menu.completion.current', 'fg:yellow bold bg:default'),
    ('completion-menu.meta.completion', 'fg:gray bg:default'),
    ('completion-menu.meta.completion.current', 'fg:yellow bold bg:default'),
])

console = Console()

# Configuration
GPG_KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skyline_key.pub")
FINGERPRINT = "2F678007F08254265530095FB5B68F8BCE0CB069"

def check_dependencies():
    """Checks if 'sops' and 'gpg' are installed."""
    missing = []
    if shutil.which("sops") is None:
        missing.append("sops")
    if shutil.which("gpg") is None:
        missing.append("gpg")
    
    if missing:
        rprint(f"[bold red]Erreur : Dépendances manquantes : {', '.join(missing)}[/bold red]")
        rprint("Veuillez les installer avant de lancer ce script.")
        rprint("  - SOPS: https://github.com/getsops/sops")
        rprint("  - GPG:  https://gnupg.org/")
        sys.exit(1)

def import_gpg_key():
    """Imports the public key into the SYSTEM gpg keyring (same one sops uses)."""
    if not os.path.exists(GPG_KEY_PATH):
        rprint(f"[bold red]Erreur : Clé publique introuvable ici : {GPG_KEY_PATH}[/bold red]")
        sys.exit(1)

    # Check if key is already in system keyring
    try:
        result = subprocess.run(
            ["gpg", "--list-keys", FINGERPRINT],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return  # Key already imported
    except Exception:
        pass

    # Import into system gpg keyring (the one sops uses)
    try:
        result = subprocess.run(
            ["gpg", "--import", GPG_KEY_PATH],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            rprint(f"[green]✔ Clé publique importée dans le trousseau GPG système.[/green]")
        else:
            rprint(f"[red]Erreur lors de l'import de la clé : {result.stderr}[/red]")
            sys.exit(1)
    except Exception as e:
        rprint(f"[red]Erreur lors de l'import GPG : {e}[/red]")
        sys.exit(1)

def encrypt_config(file_path):
    """Encrypts a YAML/JSON configuration file using SOPS."""
    if not os.path.exists(file_path):
        rprint(f"[red]Erreur : Fichier {file_path} introuvable.[/red]")
        return

    # Check if already encrypted to avoid SOPS error
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if "sops:" in content and "mac:" in content:
                 rprint(f"[green]✔ Déjà chiffré (Métadonnées SOPS détectées).[/green]")
                 return
    except Exception:
        pass

    rprint(f"[dim]Chiffrement de '{file_path}' avec SOPS...[/dim]")
    cmd = ["sops", "--encrypt", "--in-place", file_path]
    try:
        subprocess.run(cmd, check=True)
        rprint(f"[green]Succès : {file_path} chiffré (in-place).[/green]")
    except subprocess.CalledProcessError as e:
        rprint(f"[red]Échec du chiffrement : {e}[/red]")

def decrypt_config(file_path):
    """Decrypts a YAML/JSON configuration file using SOPS."""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    print(f"Decrypting config file '{file_path}' with SOPS...")
    cmd = ["sops", "--decrypt", "--in-place", file_path]
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully decrypted {file_path} (in-place).")
    except subprocess.CalledProcessError as e:
        print(f"Decryption failed: {e}")

def encrypt_source(folder_path):
    """Zips and GPG-encrypts a source folder."""
    if not os.path.isdir(folder_path):
        print(f"Error: Folder {folder_path} not found.")
        return

    folder_path = os.path.normpath(folder_path)
    base_name = os.path.basename(folder_path)
    parent_dir = os.path.dirname(folder_path)
    
    # 1. Create Zip (Preserving 'src' folder structure)
    # This ensures that unzipping creates a 'src/' folder, matching Dockerfile COPY src/...
    zip_path = shutil.make_archive(base_name, 'zip', root_dir=parent_dir, base_dir=base_name)
    # shutil.make_archive creates in current dir, let's move it next to source if needed
    # But usually creating "src.zip" next to "src/" is fine.
    
    final_zip_path = os.path.join(parent_dir, f"{base_name}.zip")
    if zip_path != final_zip_path:
        shutil.move(zip_path, final_zip_path)
        
    print(f"Created zip archive: {final_zip_path}")
    
    # 2. Encrypt Zip with GPG
    gpg = gnupg.GPG()
    output_path = f"{final_zip_path}.gpg"
    
    with open(final_zip_path, 'rb') as f:
        status = gpg.encrypt_file(
            f, 
            recipients=[FINGERPRINT],
            output=output_path,
            always_trust=True
        )
        
    if status.ok:
        print(f"Successfully encrypted source code: {output_path}")
        os.remove(final_zip_path) # Remove the unencrypted zip
        print("Removed temporary zip file.")
        
        # Optional: Remove source folder? 
        # Usually devs want to keep source. This script is for preparing for commit.
        print("NOTE: You can now commit the .zip.gpg file. The original source folder is untouched.")
    else:
        print(f"Encryption failed: {status.status}")
        print(status.stderr)

def main():
    parser = argparse.ArgumentParser(description="SkylineCTF Secret Management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Config (SOPS)
    p_encrypt_conf = subparsers.add_parser("encrypt-config", help="Encrypt a YAML/JSON config file (SOPS)")
    p_encrypt_conf.add_argument("file", help="Path to the file to encrypt")

    p_decrypt_conf = subparsers.add_parser("decrypt-config", help="Decrypt a YAML/JSON config file (SOPS)")
    p_decrypt_conf.add_argument("file", help="Path to the file to decrypt")

    # Source (GPG Zip)
    p_encrypt_src = subparsers.add_parser("encrypt-source", help="Zip and encrypt a source folder (GPG)")
    p_encrypt_src.add_argument("folder", help="Path to the folder to encrypt")

    # Wizard
    p_wizard = subparsers.add_parser("secure", help="🧙‍♂️ Interactive Wizard to secure a challenge")
    p_wizard.add_argument("folder", help="Path to the challenge folder (e.g. Web/MyChall)")

    # Check if any args were passed
    if len(sys.argv) == 1:
        # No args -> Launch TUI
        try:
            run_tui()
        except KeyboardInterrupt:
            rprint("\n[yellow]👋 Bye![/yellow]")
            sys.exit(0)
    else:
        # Args passed -> Use argparse
        args = parser.parse_args()
        
        check_dependencies()
        import_gpg_key()

        if args.command == "encrypt-config":
            encrypt_config(args.file)
        elif args.command == "decrypt-config":
            decrypt_config(args.file)
        elif args.command == "encrypt-source":
            encrypt_source(args.folder)
        elif args.command == "secure":
            run_wizard(args.folder)

def run_tui():
    """Launches the beautiful interactive Text User Interface."""
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]SkylineCTF - Assistant de Sécurité[/bold cyan]\n"
        "[dim]Sécurisez vos challenges facilement![/dim]",
        border_style="cyan"
    ))
    
    check_dependencies()
    import_gpg_key()

    # WARNING (Moved to startup)
    rprint("\n[bold red blink]⚠️  ATTENTION AVANT DE CONTINUER ⚠️[/]")
    rprint("[bold white]Dû à la nature publique de ce dépôt, tout le monde peut contribuer.[/bold white]")
    rprint("[bold white]Pour empêcher la lecture des flags, le chiffrement est irréversible pour vous.[/bold white]")
    rprint("[bold white]Seul l'administrateur possède la clé privée pour déchiffrer ces fichiers.[/bold white]")
    rprint("[yellow]Assurez-vous d'avoir une copie de sauvegarde (backup en dehors de ce repo) de votre challenge ![/yellow]\n")
    
    if not questionary.confirm("J'ai une sauvegarde et je veux procéder au chiffrement", default=False, style=custom_style).ask():
        rprint("[red]Opération annulée.[/red]")
        return

    # Direct Wizard Launch
    dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and not d.startswith('__') and d != "Others"]
    dirs.sort()
    
    if not dirs:
        rprint("[yellow]Aucun dossier de challenge trouvé dans le répertoire courant.[/yellow]")
        return

    target = questionary.select(
        "Sélectionnez le dossier du challenge :",
        choices=dirs,
        style=custom_style,
        use_indicator=True,
        instruction="(Utilisez les flèches)"
    ).ask()
    
    if target:
        run_wizard(target)
        rprint("\n[dim]Terminé.[/dim]")


def encrypt_standalone_file(file_path):
    """Encrypts a single file using GPG and removes the original."""
    if not os.path.exists(file_path):
        return

    rprint(f"[dim]Chiffrement de '{file_path}' avec GPG...[/dim]")
    gpg = gnupg.GPG()
    output_path = f"{file_path}.gpg"
    
    with open(file_path, 'rb') as f:
        status = gpg.encrypt_file(
            f, 
            recipients=[FINGERPRINT],
            output=output_path,
            always_trust=True
        )

    if status.ok:
        rprint(f"[green]Succès : {output_path}[/green]")
        os.remove(file_path)
        rprint("[dim]Fichier original supprimé.[/dim]")
    else:
        rprint(f"[red]Échec du chiffrement : {status.status}[/red]")
    rprint(status.stderr)

def run_wizard(target_folder):
    """Interactive wizard to secure a challenge folder."""
    if not os.path.isdir(target_folder):
        rprint(f"[bold red]Erreur :[/bold red] Le dossier '{target_folder}' n'existe pas.")
        return

    rprint(f"\n[bold cyan]🧙‍♂️  Skyline Security Wizard[/bold cyan] pour : [bold yellow]{target_folder}[/bold yellow]")
    rprint("[cyan]" + "-" * 50 + "[/cyan]")

    rprint(f"\n[bold cyan]🧙‍♂️  Skyline Security Wizard[/bold cyan] pour : [bold yellow]{target_folder}[/bold yellow]")
    rprint("[cyan]" + "-" * 50 + "[/cyan]")

    # 1. Check Challenge.yaml
    yaml_path = os.path.join(target_folder, "Challenge.yaml")
    if os.path.exists(yaml_path):
        rprint(f"\n[bold blue][1/3] Fichier de Configuration[/bold blue] ({yaml_path})")
        rprint("   [green]✔ Trouvé[/green]")
        rprint("   [yellow]Chiffrement automatique (Obligatoire)...[/yellow]")
        encrypt_config(yaml_path)
    else:
        rprint(f"\n[bold blue][1/3] Fichier de Configuration[/bold blue]: [bold red]❌ MANQUANT[/bold red] ({yaml_path})")
        rprint("   [bold red]Erreur :[/bold red] Un challenge DOIT avoir un fichier Challenge.yaml.")
        sys.exit(1)

    # 2. Check WALKTHROUGH.md
    walkthrough_path = os.path.join(target_folder, "WALKTHROUGH.md")
    if os.path.exists(walkthrough_path):
        rprint(f"\n[bold blue][2/3] Walkthrough (Solution)[/bold blue] ({walkthrough_path})")
        rprint("   [green]✔ Trouvé[/green]")
        rprint("   [yellow]Chiffrement automatique (Obligatoire)...[/yellow]")
        encrypt_standalone_file(walkthrough_path)
    else:
         rprint(f"\n[bold blue][2/3] Walkthrough (Solution)[/bold blue]: [dim]Non trouvé (Ignoré)[/dim]")

    # 3. Check src/ folder
    src_path = os.path.join(target_folder, "src")
    if os.path.isdir(src_path):
        rprint(f"\n[bold blue][3/3] Code Source[/bold blue] ({src_path})")
        rprint("   [green]✔ Trouvé[/green]")
        
        do_zip = questionary.confirm("Chiffrer le code source (dossier 'src') ?", default=True, style=custom_style).ask()
        
        if do_zip:
            encrypt_source(src_path)
        else:
            rprint("   [dim]Chiffrement du source ignoré.[/dim]")
    else:
         rprint(f"\n[bold blue][3/3] Code Source[/bold blue]: [dim]Pas de dossier 'src' (Ignoré)[/dim]")

    rprint("[cyan]" + "-" * 50 + "[/cyan]")
    rprint("[bold green]✅  Sécurisation terminée.[/bold green]")

if __name__ == "__main__":
    main()
