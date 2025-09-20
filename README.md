# 🚗 Gestion du Stock de Pièces Automobiles

![App Screenshot](lien_vers_screenshot.png)

Une application web développée avec **Django** pour la gestion complète du stock de pièces automobiles. Elle permet de centraliser, suivre et analyser les pièces en stock, les transactions, ainsi que l’import/export de données via fichiers Excel. L’interface est intuitive et interactive pour faciliter le travail des ateliers et services de gestion de stocks.

---

## 🔎 Vue d'ensemble du projet

Cette application permet à l’utilisateur de :  

- Ajouter, modifier et supprimer des pièces
- Suivre les transactions d’entrée et de sortie
- Importer et exporter des fichiers Excel
- Filtrer et rechercher les pièces rapidement
- Visualiser les alertes de stock (seuils minimums)

L’application est conçue pour être **responsive, rapide et facile à utiliser**.

---

## 🚀 Fonctionnalités principales

- 📦 Gestion complète des pièces et du stock  
- 🔄 Suivi des transactions entrantes et sortantes  
- 📥 Importation de fichiers Excel  
- 📤 Exportation des résultats filtrés  
- 🔍 Recherche et filtres dynamiques  
- ⚠️ Alertes de stock faible  
- 🖥️ Interface moderne et responsive  

---

## 🧰 Technologies utilisées

- Python 3 & Django  
- HTML5, CSS3, Bootstrap 5  
- JavaScript & jQuery  
- SweetAlert2 (confirmations et alertes)  
- DataTables (tableaux dynamiques)  
- SQLite (ou toute autre base de données Django)

---

## 🧠 Architecture & Solution

- Les données des pièces sont centralisées dans un modèle Django `Piece`  
- Les transactions sont liées aux pièces pour suivre les entrées et sorties  
- Les imports Excel sont normalisés et validés avant insertion  
- Les exports peuvent être complets ou filtrés selon la recherche  
- Les alertes et confirmations sont gérées côté front avec **SweetAlert2**  

---

## 🖼️ Structure du projet
![App Scructure](lien_vers_screenshot.png)


---

## 🌐 Démo en ligne

Lien vers la démo : [Votre lien ici](#)

---

## ⚙️ Installation

1. Cloner le repository :  
```bash
git clone https://github.com/tonusername/gestion-pieces-auto.git
cd gestion-pieces-auto
```

2. Créer un environnement virtuel
```bash
python -m venv venv
```

3. Activer l’environnement virtuel
Sur macOS/Linux :
```bash
source venv/bin/activate
```

Sur Windows :
```bash
venv\Scripts\activate
```

4. Installer les dépendances
```bash
pip install -r requirements.txt
```

5. Lancer le serveur Django
```bash
python manage.py runserver
```

##👤 Auteur

Alfran Essone


##📄 Licence

Ce projet est sous licence MIT. Vous pouvez réutiliser, modifier et partager avec attribution.
