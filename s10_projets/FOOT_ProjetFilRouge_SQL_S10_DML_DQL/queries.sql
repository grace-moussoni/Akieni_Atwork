-- ==============================================================================
-- EXERCICE 1 — Insérer les 8 équipes
-- ==============================================================================
INSERT INTO T_EQUIPE (nom_equipe, qartier_equipe, nom_entraineur, annee_creation) 
VALUES 
    ('AS Poto-Poto', 'Poto-Poto', 'Jean Ibara', 1950),
    ('Diables Noirs', 'Bacongo', 'Paul Moukila', 1950),
    ('Etoile du Congo', 'Poto-Poto', 'Gaston Tchiangana', 1926),
    ('CARA Brazzaville', 'Ouenze', 'Jacques Ndoumbé', 1935),
    ('Inter Club', 'Makélékélé', 'Pierre Mvouama', 1967),
    ('Patronage Sainte-Anne', 'Moungali', 'Luc Kossa', 1933),
    ('AS Kondzo', 'Talangaï', 'Marc Makosso', 1999),
    ('JST', 'Talangaï', 'Eric Ndinga', 1980);

-- ==============================================================================
-- EXERCICE 2 — Insérer 3 stades et quelques joueurs
-- ==============================================================================
-- a) Insérer 3 stades
INSERT INTO T_STADE (nom_stade, quartier_stade, nombre_place) 
VALUES 
    ('Stade Alphonse Massamba-Débat', 'Makélékélé', 33037),
    ('Stade Municipal', 'Poto-Poto', 5000),
    ('Stade annexe', 'Ouenze', 2000);

-- b) Insérer au moins 3 joueurs par équipe (24 joueurs)
-- Note : J'utilise des sous-requêtes comme demandé pour cibler dynamiquement l'id_equipe.
INSERT INTO T_JOUER (nom_joueur, prenom, id_equipe, poste, numero_maillot, date_naissance) 
VALUES 
    -- AS Poto-Poto
    ('Bintsene', 'Kevin', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Poto-Poto'), 'Gardien', 1, '1998-05-12'),
    ('Okemba', 'Junior', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Poto-Poto'), 'Défenseur', 4, '2000-11-23'),
    ('Ngouabi', 'Tresor', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Poto-Poto'), 'Attaquant', 9, '1999-08-15'),
    
    -- Diables Noirs
    ('Kibamba', 'Guy', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Diables Noirs'), 'Gardien', 16, '1995-02-10'),
    ('Ndong', 'Arthur', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Diables Noirs'), 'Milieu', 8, '1997-07-21'),
    ('Moussa', 'Ali', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Diables Noirs'), 'Attaquant', 10, '1996-12-05'),
    
    -- Etoile du Congo
    ('Itoua', 'Bercy', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Etoile du Congo'), 'Défenseur', 5, '1994-09-30'),
    ('Mvouo', 'Prince', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Etoile du Congo'), 'Milieu', 6, '2001-04-14'),
    ('Ondo', 'Gael', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Etoile du Congo'), 'Attaquant', 11, '1998-01-18'),
    
    -- CARA Brazzaville
    ('Nsilou', 'Emile', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'CARA Brazzaville'), 'Gardien', 1, '1992-06-25'),
    ('Bale', 'Cyrille', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'CARA Brazzaville'), 'Défenseur', 3, '1999-03-08'),
    ('Kaya', 'Davy', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'CARA Brazzaville'), 'Milieu', 14, '2002-10-10'),
    
    -- Inter Club
    ('Babela', 'Yann', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Inter Club'), 'Défenseur', 2, '1996-05-05'),
    ('Mokono', 'Juslain', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Inter Club'), 'Milieu', 7, '1997-09-17'),
    ('Tchibinda', 'Franck', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Inter Club'), 'Attaquant', 19, '2000-01-22'),
    
    -- Patronage Sainte-Anne
    ('Kouassi', 'Ange', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Patronage Sainte-Anne'), 'Gardien', 30, '1998-11-11'),
    ('Dzabana', 'Chris', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Patronage Sainte-Anne'), 'Défenseur', 15, '1995-08-08'),
    ('Samba', 'David', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Patronage Sainte-Anne'), 'Attaquant', 20, '2001-12-12'),
    
    -- AS Kondzo
    ('Loko', 'Steve', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Kondzo'), 'Défenseur', 12, '1993-07-07'),
    ('Biyoko', 'Marc', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Kondzo'), 'Milieu', 18, '1998-02-14'),
    ('Makoumbou', 'Luc', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Kondzo'), 'Attaquant', 22, '1999-06-20'),
    
    -- JST
    ('Ibouanga', 'Yves', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'JST'), 'Gardien', 1, '1996-03-03'),
    ('Ngoma', 'Serge', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'JST'), 'Défenseur', 13, '1997-05-25'),
    ('Moutsita', 'Paul', (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'JST'), 'Attaquant', 10, '2000-10-30');

-- ==============================================================================
-- EXERCICE 3 — Insérer 6 matchs de la 1ère journée
-- ==============================================================================
-- Note : Avec 8 équipes qui ne jouent qu'une fois, on ne peut mathématiquement 
-- faire que 4 matchs. Pour respecter votre consigne de 6 matchs, je crée 4 matchs 
-- pour la journée 1, et j'anticipe 2 matchs de la journée 2.
INSERT INTO T_MATCH (id_equipe_domicile, id_equipe_exterieur, id_stade, date_match, score_domicile, score_exterieur, diff_buts)
VALUES 
    -- 4 matchs de la 1ère journée
    ((SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Poto-Poto'), (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Diables Noirs'), (SELECT id_stade FROM T_STADE WHERE nom_stade = 'Stade Alphonse Massamba-Débat'), '2026-08-15', 0, 0, 0),
    ((SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Etoile du Congo'), (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'CARA Brazzaville'), (SELECT id_stade FROM T_STADE WHERE nom_stade = 'Stade Municipal'), '2026-08-15', 0, 0, 0),
    ((SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Inter Club'), (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Patronage Sainte-Anne'), (SELECT id_stade FROM T_STADE WHERE nom_stade = 'Stade annexe'), '2026-08-15', 0, 0, 0),
    ((SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Kondzo'), (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'JST'), (SELECT id_stade FROM T_STADE WHERE nom_stade = 'Stade Municipal'), '2026-08-15', 0, 0, 0),
    
    -- 2 matchs supplémentaires pour atteindre les 6 demandés
    ((SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Diables Noirs'), (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'Etoile du Congo'), (SELECT id_stade FROM T_STADE WHERE nom_stade = 'Stade Alphonse Massamba-Débat'), '2026-08-22', 0, 0, 0),
    ((SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'CARA Brazzaville'), (SELECT id_equipe FROM T_EQUIPE WHERE nom_equipe = 'AS Poto-Poto'), (SELECT id_stade FROM T_STADE WHERE nom_stade = 'Stade Municipal'), '2026-08-22', 0, 0, 0);

-- ==============================================================================
-- EXERCICE 4 — UPDATE — Enregistrer les résultats
-- ==============================================================================
-- a) Mise à jour des scores
-- (J'utilise les ID 1 à 6 en supposant qu'ils sont auto-incrémentés dans l'ordre)
UPDATE T_MATCH SET score_domicile = 2, score_exterieur = 1, diff_buts = 1 WHERE id_match = 1; -- 2-1
UPDATE T_MATCH SET score_domicile = 0, score_exterieur = 0, diff_buts = 0 WHERE id_match = 2; -- 0-0
UPDATE T_MATCH SET score_domicile = 3, score_exterieur = 2, diff_buts = 1 WHERE id_match = 3; -- 3-2
UPDATE T_MATCH SET score_domicile = 1, score_exterieur = 1, diff_buts = 0 WHERE id_match = 4; -- 1-1
UPDATE T_MATCH SET score_domicile = 4, score_exterieur = 0, diff_buts = 4 WHERE id_match = 5; -- 4-0
UPDATE T_MATCH SET score_domicile = 0, score_exterieur = 1, diff_buts = -1 WHERE id_match = 6; -- 0-1

-- b) Correction du stade
UPDATE T_MATCH 
SET id_stade = (SELECT id_stade FROM T_STADE WHERE nom_stade = 'Stade Alphonse Massamba-Débat') 
WHERE id_match = 4;

-- ==============================================================================
-- EXERCICE 5 — INSERT — Enregistrer les buteurs
-- ==============================================================================
-- Match 1 (AS Poto-Poto 2 - 1 Diables Noirs) : 3 buts
INSERT INTO T_BUT (id_match, id_joueur, minute_but) VALUES 
    (1, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Ngouabi' AND prenom = 'Tresor'), 12),
    (1, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Ngouabi' AND prenom = 'Tresor'), 45),
    (1, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Moussa' AND prenom = 'Ali'), 78);

-- Match 3 (Inter Club 3 - 2 Patronage) : 5 buts
INSERT INTO T_BUT (id_match, id_joueur, minute_but) VALUES 
    (3, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Tchibinda' AND prenom = 'Franck'), 5),
    (3, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Tchibinda' AND prenom = 'Franck'), 22),
    (3, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Mokono' AND prenom = 'Juslain'), 89),
    (3, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Samba' AND prenom = 'David'), 30),
    (3, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Samba' AND prenom = 'David'), 60);

-- Match 4 (AS Kondzo 1 - 1 JST) : 2 buts
INSERT INTO T_BUT (id_match, id_joueur, minute_but) VALUES 
    (4, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Makoumbou' AND prenom = 'Luc'), 15),
    (4, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Moutsita' AND prenom = 'Paul'), 82);

-- Match 5 (Diables Noirs 4 - 0 Etoile) : 4 buts
INSERT INTO T_BUT (id_match, id_joueur, minute_but) VALUES 
    (5, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Moussa' AND prenom = 'Ali'), 10),
    (5, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Moussa' AND prenom = 'Ali'), 25),
    (5, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Ndong' AND prenom = 'Arthur'), 50),
    (5, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Ndong' AND prenom = 'Arthur'), 88);

-- Match 6 (CARA 0 - 1 Poto-Poto) : 1 but
INSERT INTO T_BUT (id_match, id_joueur, minute_but) VALUES 
    (6, (SELECT id_joueur FROM T_JOUER WHERE nom_joueur = 'Ngouabi' AND prenom = 'Tresor'), 90);

-- ==============================================================================
-- EXERCICE 6 — DELETE — Corriger une erreur de saisie
-- ==============================================================================
-- Insertion volontaire d'un doublon pour l'exercice
INSERT INTO T_JOUER (nom_joueur, prenom, id_equipe, poste, numero_maillot, date_naissance) 
VALUES ('Ngouabi', 'Tresor', 1, 'Attaquant', 9, '1999-08-15');

-- Étape 1 : Vérifier avec un SELECT combien de lignes correspondent
/*
SELECT COUNT(*) 
FROM T_JOUER 
WHERE nom_joueur = 'Ngouabi' AND prenom = 'Tresor';
*/

-- Étape 2 : Supprimer le doublon (en gardant l'ID le plus ancien par exemple)
DELETE FROM T_JOUER 
WHERE id_joueur = (
    SELECT MAX(id_joueur) 
    FROM T_JOUER 
    WHERE nom_joueur = 'Ngouabi' AND prenom = 'Tresor'
);

-- ==============================================================================
-- EXERCICE 7 — Explorer les données
-- ==============================================================================
-- a) Combien d'équipes sont enregistrées ?
SELECT COUNT(*) AS total_equipes 
FROM T_EQUIPE;

-- b) Combien de joueurs au total ? Combien par équipe ?
-- Total des joueurs
SELECT COUNT(*) AS total_joueurs 
FROM T_JOUER;

-- Par équipe (avec le nom de l'équipe pour plus de clarté)
SELECT e.nom_equipe, COUNT(j.id_joueur) AS nombre_joueurs
FROM T_EQUIPE e
LEFT JOIN T_JOUER j ON e.id_equipe = j.id_equipe
GROUP BY e.nom_equipe;

-- c) Combien de buts ont été marqués au total sur la journée ?
SELECT COUNT(*) AS total_buts 
FROM T_BUT;

-- ==============================================================================
-- EXERCICE 8 — Filtrage, tri et agrégation
-- ==============================================================================
-- a) Listez tous les joueurs qui jouent au poste "Attaquant"
SELECT nom_joueur, prenom, id_equipe 
FROM T_JOUER 
WHERE poste = 'Attaquant';

-- b) Listez les matchs où plus de 3 buts ont été marqués au total
SELECT * 
FROM T_MATCH 
WHERE (score_domicile + score_exterieur) > 3;

-- c) Pour chaque équipe, comptez son nombre de joueurs (Tri décroissant)
SELECT id_equipe, COUNT(*) AS effectif 
FROM T_JOUER 
GROUP BY id_equipe 
ORDER BY effectif DESC;

-- d) Score total de chaque match trié du plus spectaculaire au moins spectaculaire
SELECT 
    id_match, 
    (score_domicile + score_exterieur) AS score_total 
FROM T_MATCH 
ORDER BY score_total DESC;