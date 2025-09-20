📦 Gestion des pièces auto

Application web Django pour la gestion complète du stock de pièces automobiles : centralisation, suivi, analyse, transactions, import/export Excel, interface intuitive et responsive.

🔎 Project Overview

Gestion des pièces auto permet :

La création et modification des pièces et transactions

La consultation et recherche de pièces (marque, nom, référence)

L’importation de fichiers Excel pour mettre à jour le stock

L’exportation des pièces ou résultats filtrés vers Excel

Le suivi des seuils de stock et des alertes

Une interface fluide et responsive pour desktop et mobile

🚀 Features

📦 Gestion complète du stock

🔍 Recherche dynamique et filtrage instantané

📥 Importation Excel (.xlsx) avec validation ligne par ligne

📤 Export des résultats filtrés vers Excel

⚠️ Alertes de stock faible

🧾 Historique des transactions et activités

🖥️ Interface web responsive

🧰 Technologies Used

Backend : Python 3 / Django 5

Frontend : HTML5, CSS3, JavaScript, jQuery, Bootstrap 5

Librairies : SweetAlert2, pandas, openpyxl

Base de données : SQLite (modifiable)

🧠 Approach & Solution

Les données sont stockées dans une base Django.

L’import Excel est traité côté serveur avec vérification et retour d’erreurs.

Les exports peuvent cibler tout le stock ou uniquement les résultats filtrés.

Actions critiques (ajout, import, transaction) validées via pop-ups de confirmation.

Architecture modulaire et extensible pour ajouter de nouvelles fonctionnalités facilement.

🖼️ Project Structure
📁 inventory/
   ├─ migrations/
   ├─ templates/
   │   └─ inventory/
   │       ├─ base.html
   │       ├─ pieces_list.html
   │       ├─ piece_form.html
   │       └─ import_stock.html
   ├─ static/
   │   ├─ css/
   │   ├─ js/
   │   └─ images/
   ├─ models.py
   ├─ views.py
   └─ urls.py
📄 manage.py
📄 db.sqlite3
📄 requirements.txt
📄 README.md

🌐 Live Demo

Voir le projet en ligne
 (ou ton URL de déploiement)

⚙️ Installation

Cloner le repository :

git clone https://github.com/tonusername/gestion-pieces-auto.git
cd gestion-pieces-auto


Installer les dépendances :

pip install -r requirements.txt


Appliquer les migrations :

python manage.py migrate


Créer un superutilisateur :

python manage.py createsuperuser


Lancer le serveur :

python manage.py runserver

👤 Author

Alfran Essone

📄 License

Ce projet est sous licence MIT. Libre d’utilisation, modification et partage avec attribution.
