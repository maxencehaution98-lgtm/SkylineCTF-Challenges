# SkylineCTF - Guide de Contribution 🏰

![](Others/skylinectf.png)

Bienvenue dans le dépôt des challenges SkylineCTF ! Ce guide vous expliquera comment créer, sécuriser et publier votre challenge sur la plateforme.

---

## 🚀 Comment ajouter un challenge ?

Suivez ces 4 étapes simples pour voir votre challenge en ligne.

### 1. Préparation 🛠️
Clonez ce dépôt.
```bash
git clone https://github.com/Sp00kySkelet0n/SkylineCTF-Challenges.git
cd SkylineCTF-Challenges
```

### 2. Création du Challenge 📝
Créez un dossier pour votre challenge (par exemple `Web/Mon-Challenge`).
Il doit contenir :
*   `Challenge.yaml` : La définition du challenge.
*   `Dockerfile` (si dockerisé).
*   `uploads/` (optionnel) : Fichiers associés au challenge à fournir aux joueurs.
*   `src/` (optionnel) : Code source (chiffré par le wizard).

---

## 📂 Structure du Challenge.yaml

### Type 1 : Challenge Docker (Web, Pwn...) 🐳
Utilise une image Docker et un port. Les points s'ajustent dynamiquement.

```yaml

apiVersion: skyline.local/v1 # Ne jamais modifier
kind: CTFChallenge # Ne jamais modifier
metadata:
  name: mon-challenge-unique # Doit correspondre au nom du dossier (lowercase, sans espaces)
  namespace: ctfd # Ne jamais modifier
spec:
  # Infos Générales
  name: "Titre du Challenge"
  description: "Trouvez le flag !"
  category: "Web"       # Web, Pwn, Crypto, Reverse...
  
  # Points Dynamiques (Recommandé)
  type: "dynamic"
  initial: 500          # Points de départ
  decay: 10             # Nombre de solutions pour baisse max
  minimum: 50           # Points minimum

  # Déploiement
  image: "ghcr.io/sp00kyskelet0n/chall:latest"
  port: 1337            # Port interne du conteneur
  instance: true        # Détermine si le challenge peut être déployé à la demande
  
  # Fichiers (si besoin de fournir un binaire/source)
  upload_files: true    # Upload tout le dossier 'uploads/' vers CTFd

  flag: "SKL{...}"    # À chiffrer avec wizard.sh !
```

### Type 2 : Challenge Statique (Forensic, Reverse) 📁
Pas de Docker, juste des fichiers à télécharger.

```yaml
apiVersion: skyline.local/v1
kind: CTFChallenge
metadata:
  name: mon-challenge-forensic # Doit correspondre au nom du dossier (lowercase, sans espaces)
  namespace: ctfd
spec:
  name: "Analyse Mystère"
  description: "Analysez ce fichier PCAP..."
  category: "Forensic"
  type: "standard"      # Ou dynamic
  points: 100
  
  upload_files: true    # Indispensable pour Forensic/Reverse !
  # Placez vos fichiers (PCAP, binaire...) (dans la limite de 50mb) dans le dossier 'uploads/' du challenge.
  
  flag: "SKL{...}"      # À chiffrer avec wizard.sh !
```

**Note sur la Connexion :** 
L'opérateur détecte automatiquement le protocole (`http://` ou `tcp://`) selon la catégorie et le port. Vous pouvez forcer via `connection_info: "..."`.

---

### 3. Sécurisation (Chiffrement) 🔐
**C'est l'étape la plus importante !** Protégez vos flags et votre code source avec notre assistant.

**Sur Linux / Mac :**
```bash
./wizard.sh
```

**Sur Windows :**
```cmd
wizard.bat
```

L'assistant va :
1.  Chiffrer le `Challenge.yaml` (les secrets).
2.  Chiffrer le `WALKTHROUGH.md` (writeup).
3.  Proposer de chiffrer le dossier `src/` (code source).

**C'est tout !** Vos fichiers `.encrypted` sont prêts.

### 4. Publication ✈️
Une fois vos fichiers sécurisés :

1.  Ajoutez vos fichiers (les versions chiffrées !) :
    ```bash
    git add Web/Mon-Challenge/Challenge.yaml
    git add Web/Mon-Challenge/src.zip.gpg
    git add Web/Mon-Challenge/Dockerfile
    ```
2.  Commitez et Pushez :
    ```bash
    git commit -m "feat: Ajout du challenge Mon-Super-Challenge"
    git push origin ma-branche
    ```
3.  Ouvrez une Pull Request. Une fois validée, Flux déploiera automatiquement votre challenge sur le cluster ! 🚀

---

## ℹ️ Fonctionnement Technique

### Infrastructure as Code (IoC)
SkylineCTF utilise une approche GitOps. Tout ce qui est sur la branche `main` est la vérité absolue du cluster.

### Déploiement Automatique
1.  **Flux** détecte les modifications.
2.  **SkylineOperator** lit votre `Challenge.yaml`.
3.  Le challenge est créé dans **CTFd** et déployé sur le cluster Kubernetes.

### Architecture
![](Others/challenge_creation_process.png)

*Pour les instances à la demande (Pods/VMs) :*
![](Others/instance_deployment_diagram.png)
