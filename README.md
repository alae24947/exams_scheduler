# exams_scheduler

Application web pour générer automatiquement les emplois du temps d'examens universitaires.

##  Contexte

Projet réalisé dans le cadre du cours de Bases de Données. L'objectif est de résoudre le problème de planification des examens dans une faculté de 13,000 étudiants répartis sur 7 départements et 20 formations.

**Problèmes identifiés:**
- Étudiants avec plusieurs examens le même jour
- Professeurs surchargés (trop de surveillances)
- Mauvaise utilisation des salles
- Génération manuelle = beaucoup d'erreurs et de temps perdu

##  Objectifs

- Créer une base de données relationnelle pour gérer les examens
- Développer un algorithme qui génère les plannings automatiquement
- Éviter tous les conflits d'horaires
- Interface web simple et fonctionnelle

##  Technologies

**Backend:**
- Python 3.11
- MySQL (base de données)
- PyMySQL (connexion DB)
- Pandas (analyse de données)

**Frontend:**
- Streamlit
- CSS personnalisé

**Déploiement:**
- Railway (hébergement cloud)
- Nixpacks (configuration déploiement)

## Structure du Projet

```
exams_scheduler/
├── app.py                  # Application principale
├── backend/
│   ├── auth.py            # Authentification
│   ├── db.py              # Connexion MySQL
│   ├── scheduler.py       # Algorithme de génération
│   └── analytics.py       # Statistiques et conflits
├── database/
│   ├── schema.sql         # Structure de la base
│   └── data.sql           # Données de test
├── frontend/
│   └── styles.css         # Design
├── requirements.txt       # Dépendances Python
├── nixpacks.toml         # Config Railway
└── runtime.txt           # Version Python
```

##  Base de Données

**Tables principales:**
- `departements` - Les 7 départements (Info, Maths, Bio, Anglais, Français, Chimie, Physique)
- `formations` - 20 programmes (Licence Info, Master IA, etc.)
- `etudiants` - Informations étudiants
- `professeurs` - Corps enseignant
- `modules` - Matières à examiner
- `salles` - Salles disponibles avec capacités
- `examens` - Planning généré
- `users` - Comptes utilisateurs

##  Installation Locale

1. **Clone le projet**
```bash
git clone https://github.com/votre-username/exams_scheduler.git
cd exams_scheduler
```

2. **Installe les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configure les variables d'environnement**
```bash
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=ton_password
MYSQLDATABASE=exam_scheduler
MYSQLPORT=3306
```

4. **Crée la base de données**
```sql
-- Exécute dans MySQL:
source database/schema.sql
source database/data.sql
```

5. **Lance l'application**
```bash
streamlit run app.py
```

## Comptes de Test

- **Admin**: `admin` / `admin123` (peut tout faire)
- **Doyen**: `doyen` / `doyen123` (vue globale)
- **Chef**: `chef_info` / `chef123` (chef de département)

##  Fonctionnalités

### 1. Planning des Examens
Affiche tous les examens planifiés avec:
- Module
- Date et heure
- Salle assignée

### 2. Statistiques
- Total étudiants, examens, professeurs, salles
- Utilisation des salles
- Charge de surveillance par professeur (graphique)

### 3. Détection des Conflits
- Étudiants avec plusieurs examens le même jour
- Professeurs avec plus de 3 surveillances/jour

### 4. Génération Automatique (Admin)
Bouton "Gérer emplois du temps" qui crée automatiquement le planning.

## Contraintes Implémentées

**Étudiants:**
-  Maximum 1 examen par jour par étudiant (RÈGLE PRIORITAIRE)
-  Tous les modules de la formation planifiés

**Professeurs:**
-  Maximum 3 surveillances par jour
- Répartition équitable

**Salles:**
- Capacité respectée
- Pas de double réservation

**Créneaux horaires:** 9h00, 11h00, 14h00, 16h00

## Algorithme

Pour chaque module à planifier:

1. Vérifie si les étudiants ont déjà un examen ce jour → si oui, passe au jour suivant
2. Trouve un prof disponible (< 3 examens ce jour + créneau libre)
3. Trouve une salle avec assez de place et disponible
4. Crée l'examen
5. Marque tous les étudiants comme occupés pour cette date

## Déploiement sur Railway

Railway est une plateforme cloud qui permet de déployer facilement des applications et des bases de données sans configuration complexe. Elle se connecte à un dépôt GitHub, installe automatiquement les dépendances via un fichier requirements.txt, et démarre l’application avec un fichier Procfile. Railway gère aussi les bases de données (MySQL, PostgreSQL ext..) et fournit des variables d’environnement (env vars) pour connecter l’application à la base de données. Les déploiements sont affichés dans l’onglet Deployments, où l’on peut consulter les logs et corriger les erreurs. En résumé, Railway simplifie l’hébergement et l’exécution d’un projet web en automatisant le build, le déploiement et la connexion à la base de données.
. **Configuré** les variables d'environnement dans Railway:
   - MYSQLHOST
   - MYSQLUSER
   - MYSQLPASSWORD
   - MYSQLDATABASE
   - MYSQLPORT

**App en ligne:** [(https://web-production-c2d8.up.railway.app)]
