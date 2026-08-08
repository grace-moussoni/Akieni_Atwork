/*
===============================================================
				Semaine 9 — SQL Fondamentaux 1
===============================================================
*/

/* Resolution des Exercices - PARTIE 0

Exercice 0.1 : Schéma relationnel (MLD)
----------------------------------------
- EQUIPE (#id_equipe, nom_equipe, quartier_equipe, nom_entraineur, annee_creation)
- STADE (#id_stade, nom_stade, quartier_stade, nombre_place)
- JOUEUR (#id_joueur, prenom, nom_joueur, poste, numero_maillot, date_naissance, id_equipe*)
- MATCH (#id_match, date_match, score_domicile, score_exterieur, id_equipe_domicile*, id_equipe_exterieur*, id_stade*)
- BUT (#id_but, minute_but, id_match*, id_joueur*)

Exercice 0.2 : Associations et cardinalités
-------------------------------------------
- Une ÉQUIPE (1,n) est composée de plusieurs JOUEURS ; un JOUEUR (1,1) appartient à une seule ÉQUIPE.
- Une ÉQUIPE (0,n) peut être hôte dans plusieurs MATCHS ; un MATCH (1,1) contient une seule ÉQUIPE hôte.
- Une ÉQUIPE (0,n) peut être invitée dans plusieurs MATCHS ; un MATCH (1,1) contient une seule ÉQUIPE invitée.
- Un STADE (0,n) peut accueillir plusieurs MATCHS ; un MATCH (1,1) est joué dans un seul STADE.
- Un JOUEUR (0,n) peut marquer plusieurs BUTS ; un BUT (1,1) est marqué par un seul JOUEUR.
- Un MATCH (0,n) peut enregistrer plusieurs BUTS ; un BUT (1,1) est inscrit lors d'un seul MATCH.
*/


--		Exercice 1 :

CREATE DATABASE LigueFootball;

--		Exercice 2 :

USE LigueFootball;

CREATE TABLE T_EQUIPE (
	id_equipe INT IDENTITY(1,1) NOT NULL,
	nom_equipe VARCHAR(50) NOT NULL,
	qartier_equipe VARCHAR(50) NOT NULL,
	nom_entraineur VARCHAR(50),
	annee_creation DATE,

	CONSTRAINT pk_equipe PRIMARY KEY CLUSTERED (id_equipe)
);

CREATE TABLE T_STADE (
	id_stade INT IDENTITY(1,1) NOT NULL,
	nom_stade VARCHAR(50) NOT NULL,
	quartier_stade VARCHAR(50),
	nombre_place INT,

	CONSTRAINT pk_stade PRIMARY KEY CLUSTERED (id_stade)
);

--		Exercice 3 :

CREATE TABLE T_JOUER (
	id_joueur INT IDENTITY(1,1) NOT NULL,
	nom_joueur VARCHAR(50) NOT NULL,
	prenom VARCHAR(50),
	id_equipe INT NOT NULL,
	poste VARCHAR(50),
	numero_maillot INT,
	date_naissance DATE,

	CONSTRAINT pk_joueur PRIMARY KEY CLUSTERED (id_joueur),

	CONSTRAINT fk_equipe_joueur FOREIGN KEY (id_equipe) 
        REFERENCES T_EQUIPE (id_equipe)
);

CREATE TABLE T_MATCH (
	id_match INT IDENTITY(1,1) NOT NULL,
	id_equipe_domicile INT NOT NULL,
	id_equipe_exterieur INT NOT NULL,
	id_stade INT NOT NULL,
	date_match DATE NOT NULL,
	score_domicile INT DEFAULT 0,
	score_exterieur INT DEFAULT 0,

	CONSTRAINT pk_match PRIMARY KEY CLUSTERED (id_match),

	CONSTRAINT fk_equipe_domicile_match FOREIGN KEY (id_equipe_domicile) 
        REFERENCES T_EQUIPE (id_equipe),

	CONSTRAINT fk_equipe_exterieur_match FOREIGN KEY (id_equipe_exterieur) 
        REFERENCES T_EQUIPE (id_equipe),

	CONSTRAINT fk_stade_match FOREIGN KEY (id_stade) 
        REFERENCES T_STADE (id_stade),
);

CREATE TABLE T_BUT (
	id_but INT IDENTITY(1,1) NOT NULL,
	id_match INT NOT NULL,
	id_joueur INT NOT NULL,
	minute_but INT,

	CONSTRAINT pk_but PRIMARY KEY CLUSTERED (id_but),

	CONSTRAINT fk_match_but FOREIGN KEY (id_match) 
        REFERENCES T_MATCH (id_match),

	CONSTRAINT fk_joueur_but FOREIGN KEY (id_joueur) 
        REFERENCES T_JOUER (id_joueur),
);

--		Exercice 4 :

ALTER TABLE T_JOUER
ADD CONSTRAINT CHK_Poste_Joueur CHECK (poste IN ('Gardien', 'Défenseur', 'Milieu', 'Attaquant'));

--		Exercice 5 :

ALTER TABLE T_MATCH
ADD diff_buts AS (score_domicile - score_exterieur);

--		Exercice 6 :

ALTER TABLE T_JOUER
ADD capitaine BIT DEFAULT 0,
    telephone VARCHAR(20);

--		Exercice 7 :

-- a-/
CREATE TABLE test_saison (
    id INT,
    nom_test VARCHAR(50),
    date_test DATE
);

-- b-/
EXEC sp_rename 'test_saison', 'test_saison_v2';

-- c-/
DROP TABLE test_saison_v2;

--		Exercice 8 :

-- a-/
CREATE NONCLUSTERED INDEX idx_matchs_date
ON T_MATCH(date_match);

-- b-/
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_CATALOG = 'LigueFootball'
ORDER BY TABLE_NAME, ORDINAL_POSITION;