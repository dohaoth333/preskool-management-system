# 🏫 PreSkool - Système de Gestion Scolaire

Projet développé dans le cadre du module **Développement Web Avancé - Back-end (Python / Django)**.

**Réalisé par :** Doha OUTAHAR & Ahlam ELHADI  
**Établissement :** FST Tanger (Encadré par Prof. Sara AHSAIN)

---

## 🎥 Démonstration Vidéo




https://github.com/user-attachments/assets/189cfb29-9d0e-48d2-a95f-066597b0dd92


---

## ✨ Fonctionnalités Principales

Ce système de gestion scolaire propose des interfaces adaptées à différents types d'utilisateurs :
* **Administration :** Gestion globale de l'établissement (création des départements, matières, utilisateurs).
* **Enseignants :** Consultation de l'emploi du temps et saisie des notes d'examens.
* **Étudiants :** Accès sécurisé à leur profil, consultation de leur emploi du temps et de leurs notes.
* **Gestion du temps :** Planification des emplois du temps et calendrier des jours fériés.

---

## 🛠️ Instructions d'installation

Suivez ces étapes pour exécuter le projet localement sur votre machine.

**1. Cloner le dépôt :**
```bash
git clone [https://github.com/dohaoth333/preskool-management-system.git](https://github.com/dohaoth333/preskool-management-system.git)
cd preskool-management-system
```

**2. Créer et activer un environnement virtuel :**
```bash
python -m venv monenv
# Pour l'activer sur Windows :
monenv\Scripts\activate
# Pour l'activer sur Mac/Linux :
source monenv/bin/activate
```

**3. Installer les dépendances du projet :**
```bash
pip install -r requirements.txt
```

**4. Créer la base de données locale :**
*Remarque : La base de données db.sqlite3 n'est pas incluse dans le dépôt pour garantir l'intégrité des données de chaque développeur.*
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Créer un compte Super Administrateur :**
Pour pouvoir accéder au panneau d'administration, lier les comptes et tester les fonctionnalités, vous devez créer un compte admin :
```bash
python manage.py createsuperuser
```
*(Suivez les instructions dans le terminal pour choisir un nom d'utilisateur et un mot de passe).*

**6. Lancer le serveur de développement :**
```bash
python manage.py runserver
```

**7. Accéder à l'application :**
* Site public / Connexion : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Panneau d'administration : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
