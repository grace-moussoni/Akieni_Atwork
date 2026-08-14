# 📊 Olist Commerce - Dashboard & Data Management API

Application de bureau (GUI) développée en **Python** avec **CustomTkinter**, couplée à une base de données **SQL Server**. Elle permet l'administration, la correction, l'analyse (via **Pandas**) et l'importation massive de données issues de la marketplace **Olist**.

---

## 📑 Sommaire

- [1. Note sur la méthode d'importation des CSV](#-1-note-sur-la-méthode-dimportation-des-csv)
- [2. Prérequis & Prise en main](#-2-prérequis--prise-en-main)
- [3. Lancement de l'application](#️-3-lancement-de-lapplication)
- [4. Exécution des Tests Unitaires et de Services](#-4-exécution-des-tests-unitaires-et-de-services)
- [5. Structure du projet](#-5-structure-du-projet)
- [6. Stack technique](#️-6-stack-technique)
- [7. Licence](#-7-licence)

---

## 📌 1. Note sur la méthode d'importation des CSV

L'un des défis majeurs de ce projet concerne l'importation de fichiers CSV volumineux vers SQL Server. Plutôt que de lire et d'insérer les lignes une par une (ce qui serait extrêmement lent), nous avons opté pour une approche optimisée combinant **Pandas** et **SQLAlchemy** :

1. **Extraction (Read)** : le fichier CSV est lu en mémoire via `pandas.read_csv()`. Cela permet de profiter de la rapidité de Pandas pour parser les données et déduire automatiquement les types.
2. **Transformation (Clean)** : si nécessaire, Pandas permet de nettoyer les données (gestion des dates, des valeurs nulles) avant l'envoi.
3. **Chargement (Load)** : le DataFrame Pandas est envoyé massivement vers SQL Server grâce à la méthode `df.to_sql()` de Pandas interfacée avec le moteur **SQLAlchemy**.
4. **Avantage technique** : cette méthode utilise les optimisations d'insertion par lots (*batch insert*), ce qui réduit drastiquement les allers-retours avec le serveur de base de données par rapport à de simples requêtes `INSERT INTO`.

---

## 🚀 2. Prérequis & Prise en main

### A. Prérequis système

- **Python 3.10** ou supérieur.
- **SQL Server** installé et en cours d'exécution.
- Driver ODBC pour SQL Server installé sur la machine (ex : *ODBC Driver 17 for SQL Server*).

### B. Installation

1. **Cloner ou extraire le projet** dans le dossier de votre choix.
2. **Ouvrir un terminal** à la racine du projet.
3. **Créer un environnement virtuel** (recommandé) :

   ```bash
   python -m venv venv
   ```

4. **Activer l'environnement virtuel** :

   - Sur Windows :
     ```bash
     venv\Scripts\activate
     ```
   - Sur Mac/Linux :
     ```bash
     source venv/bin/activate
     ```

5. **Installer les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

### C. Configuration de la base de données

1. Créez un fichier `.env` à la racine du projet (au même niveau que `requirements.txt`).
2. Renseignez-y vos identifiants de connexion SQL Server. Par exemple :

   ```env
   DB_SERVER=localhost\SQLEXPRESS
   DB_NAME=Olist_Commerce
   DB_USER=votre_utilisateur
   DB_PASSWORD=votre_mot_de_passe
   ```

> ⚠️ Le fichier `.env` contient des informations sensibles : pensez à l'ajouter à votre `.gitignore` afin de ne jamais le versionner.

---

## ▶️ 3. Lancement de l'application

Pour démarrer l'interface graphique (Dashboard), exécutez le script principal depuis la racine du projet :

```bash
python main.py
```

---

## 🧪 4. Exécution des Tests Unitaires et de Services

Pour s'assurer du bon fonctionnement des différentes logiques métier (sans forcément passer par l'interface graphique), plusieurs scripts de test ont été mis en place dans le dossier `tests/`.

Ils sont conçus pour être exécutés individuellement depuis le terminal en utilisant le module Python (`-m`). Assurez-vous d'être à la racine du projet et d'avoir activé votre environnement virtuel.

### 👤 Test d'ajout de client

Teste la logique d'insertion manuelle d'un nouveau client dans la base.

```bash
python -m tests.test_add_customer
```

### 📊 Test du Dashboard (KPIs)

Vérifie la bonne récupération des métriques globales (total commandes, clients, vendeurs, CA).

```bash
python -m tests.test_dashboard_service
```

### 🚫 Test de nettoyage du catalogue (Produits inactifs)

Teste la requête `UPDATE` avec `NOT EXISTS` qui passe le statut `is_active` à `0` pour les produits n'ayant jamais été commandés.

```bash
python -m tests.test_deactivate_products
```

### 🔧 Test de correction du Bug (Mars 2018)

Exécute la logique de correction modifiant le statut des commandes bloquées sur `"shipped"` vers `"delivered"` pour le mois de mars 2018, à condition qu'une date de livraison client existe.

```bash
python -m tests.test_fix_orders
```

### 📁 Test d'importation CSV

Valide le fonctionnement de la pipeline d'importation (Pandas → SQLAlchemy → SQL Server) sur un fichier de test.

```bash
python -m tests.test_import
```

---

## 📂 5. Structure du projet

```
olist-commerce/
├── main.py                     # Point d'entrée de l'application (GUI)
├── requirements.txt             # Dépendances du projet
├── .env                         # Variables d'environnement (non versionné)
├── tests/                       # Scripts de test unitaires et de services
│   ├── test_add_customer.py
│   ├── test_dashboard_service.py
│   ├── test_deactivate_products.py
│   ├── test_fix_orders.py
│   └── test_import.py
└── README.md                    # Ce fichier
```

> ℹ️ Adaptez cette arborescence si votre projet comporte d'autres dossiers (ex : `services/`, `models/`, `ui/`, `data/`).

---

## 🛠️ 6. Stack technique

| Composant         | Technologie                     |
|--------------------|----------------------------------|
| Langage            | Python 3.10+                    |
| Interface graphique| CustomTkinter                   |
| Base de données    | SQL Server                      |
| ORM / Connexion DB | SQLAlchemy                      |
| Traitement de données | Pandas                       |
| Driver             | ODBC Driver 17 for SQL Server   |

---

## 📄 7. Licence

Projet réalisé dans le cadre de l'évaluation **Data Analyse / Architecture Logicielle**.