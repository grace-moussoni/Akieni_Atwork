/* =================================================================================
   PARTIE A — INSERT, UPDATE, DELETE (Manipulation de données)
   ================================================================================= */

-- ---------------------------------------------------------------------------------
-- Exercice 1 — Insérer des données manuellement
-- ---------------------------------------------------------------------------------
INSERT INTO customers (
    customer_id, 
    customer_unique_id, 
    customer_zip_code_prefix, -- Nom de colonne standard Olist (parfois juste zip_code_prefix)
    customer_city,            -- Nom de colonne standard Olist (parfois juste city)
    customer_state            -- Nom de colonne standard Olist (parfois juste state)
) 
VALUES 
    ('cust_test_001', 'unique_001', '20040', 'Rio de Janeiro-Test', 'RJ'),
    ('cust_test_002', 'unique_002', '01310', 'Sao Paulo-Test', 'SP'),
    ('cust_test_003', 'unique_003', '30130', 'Belo Horizonte-Test', 'MG');


-- ---------------------------------------------------------------------------------
-- Exercice 2 — INSERT avec SELECT
-- ---------------------------------------------------------------------------------
-- Insertion dans la table d'audit des commandes annulées.
INSERT INTO order_audit (order_id, action_type, action_date)
SELECT 
    order_id, 
    'FLAGGED_CANCEL',
    GETDATE() -- Date et heure de l'action
FROM orders 
WHERE order_status = 'canceled';


-- ---------------------------------------------------------------------------------
-- Exercice 3 — UPDATE — Corriger des données
-- ---------------------------------------------------------------------------------
-- a) Correction du bug de mars 2018 (commandes expédiées mais en réalité livrées)
UPDATE orders 
SET order_status = 'delivered'
WHERE order_status = 'shipped'
  AND order_purchase_timestamp >= '2018-03-01' 
  AND order_purchase_timestamp < '2018-04-01'
  AND order_delivered_customer_date IS NOT NULL; -- Sécurité pour confirmer la livraison

-- b) Désactiver les produits jamais commandés
UPDATE products 
SET is_active = 0 
WHERE product_id NOT IN (
    SELECT DISTINCT product_id 
    FROM order_items
);


-- ---------------------------------------------------------------------------------
-- Exercice 4 — DELETE — Nettoyage
-- ---------------------------------------------------------------------------------
-- a) Suppression des 3 clients fictifs
DELETE FROM customers 
WHERE customer_id LIKE 'cust_test_%';

-- b) Suppression des avis 5 étoiles vides
-- ETAPE 1 : Toujours faire un SELECT COUNT avant de supprimer (à exécuter seul d'abord)
/* 
SELECT COUNT(*) 
FROM order_reviews 
WHERE review_comment_message IS NULL 
  AND review_score = 5; 
*/

-- ETAPE 2 : La requête de suppression
DELETE FROM order_reviews 
WHERE review_comment_message IS NULL 
  AND review_score = 5;


/* =================================================================================
   PARTIE B — SELECT : Requêtes exploratoires
   ================================================================================= */

-- ---------------------------------------------------------------------------------
-- Exercice 5 — Explorer la volumétrie
-- ---------------------------------------------------------------------------------
-- a) Combien de clients distincts ?
SELECT COUNT(DISTINCT customer_unique_id) AS nb_clients_distincts 
FROM customers;

-- b) Combien de commandes au total ?
SELECT COUNT(order_id) AS nb_commandes_total 
FROM orders;

-- c) Combien de produits distincts vendus au moins une fois ?
SELECT COUNT(DISTINCT product_id) AS nb_produits_vendus 
FROM order_items;

-- d) Combien de vendeurs enregistrés ?
SELECT COUNT(seller_id) AS nb_vendeurs 
FROM sellers;


-- ---------------------------------------------------------------------------------
-- Exercice 6 — Filtrage avec WHERE
-- ---------------------------------------------------------------------------------
-- a) [SAV] Listez les commandes annulées
SELECT 
    order_id, 
    customer_id, 
    order_purchase_timestamp 
FROM orders 
WHERE order_status = 'canceled';

-- b) [Logistique] Produits hors gabarit standard (> 10kg)
SELECT 
    product_id, 
    product_category_name, 
    product_weight_g 
FROM products 
WHERE product_weight_g > 10000;

-- c) [Direction] Commandes passées au 1er semestre 2018
SELECT COUNT(*) AS total_commandes_S1_2018 
FROM orders 
WHERE order_purchase_timestamp >= '2018-01-01' 
  AND order_purchase_timestamp < '2018-07-01';


-- ---------------------------------------------------------------------------------
-- Exercice 7 — Tri et limitation
-- ---------------------------------------------------------------------------------
-- a) Les 10 produits les plus chers vendus
SELECT TOP 10 
    order_id, 
    product_id, 
    price 
FROM order_items 
ORDER BY price DESC;

-- b) Les 15 dernières commandes passées
SELECT TOP 15 
    order_id, 
    order_purchase_timestamp, 
    order_status 
FROM orders 
ORDER BY order_purchase_timestamp DESC;


-- ---------------------------------------------------------------------------------
-- Exercice 8 — Agrégation avec GROUP BY
-- ---------------------------------------------------------------------------------
-- a) Nombre de commandes par statut
SELECT 
    order_status, 
    COUNT(*) AS nb_commandes 
FROM orders 
GROUP BY order_status 
ORDER BY nb_commandes DESC;

-- b) Top 5 des états brésiliens les plus représentés par les clients
SELECT TOP 5 
    customer_state, 
    COUNT(*) AS nb_clients 
FROM customers 
GROUP BY customer_state 
ORDER BY nb_clients DESC;

-- c) Profil premium : Analyse des prix par vendeur (min 20 ventes)
SELECT 
    seller_id, 
    AVG(price) AS prix_moyen, 
    MIN(price) AS prix_min, 
    MAX(price) AS prix_max 
FROM order_items 
GROUP BY seller_id 
HAVING COUNT(*) > 20;


-- ---------------------------------------------------------------------------------
-- Exercice 9 — Fonctions de date
-- ---------------------------------------------------------------------------------
-- a) Les 20 livraisons les plus lentes (Délai en jours)
SELECT TOP 20 
    order_id, 
    DATEDIFF(day, order_purchase_timestamp, order_delivered_customer_date) AS delai_jours 
FROM orders 
WHERE order_delivered_customer_date IS NOT NULL 
ORDER BY delai_jours DESC;

-- b) Nombre de commandes par mois (Mois le plus actif)
SELECT 
    FORMAT(order_purchase_timestamp, 'yyyy-MM') AS mois, 
    COUNT(*) AS nb_commandes 
FROM orders 
GROUP BY FORMAT(order_purchase_timestamp, 'yyyy-MM') 
ORDER BY nb_commandes DESC;


-- ---------------------------------------------------------------------------------
-- Exercice 10 — Analyse de paiement
-- ---------------------------------------------------------------------------------
-- a) Statistiques par type de paiement
SELECT 
    payment_type, 
    COUNT(*) AS nb_transactions, 
    SUM(payment_value) AS total_encaisse, 
    AVG(payment_value) AS montant_moyen 
FROM order_payments 
GROUP BY payment_type;

-- b) Commandes réglées avec plus d'un mode de paiement
SELECT COUNT(DISTINCT order_id) AS nb_commandes_paiement_multiple 
FROM order_payments 
WHERE payment_sequential > 1;

-- c) Valeur totale des commandes par mois (évolution CA)
SELECT 
    FORMAT(o.order_purchase_timestamp, 'yyyy-MM') AS mois, 
    SUM(p.payment_value) AS chiffre_affaires 
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id 
GROUP BY FORMAT(o.order_purchase_timestamp, 'yyyy-MM') 
ORDER BY mois ASC;