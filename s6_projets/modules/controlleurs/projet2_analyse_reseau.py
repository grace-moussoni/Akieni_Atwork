import random


# 1. GÉNÉRATION AUTOMATISÉE DES DONNÉES DE RÉSEAU
def generer_donnees_reseau(n):
    zones = ["Brazzaville_Nord", "Brazzaville_Sud", "Pointe-Noire_Centre", "Dolisie_Est", "Ouesso_Ville"]
    donnees = {}
    for _ in range(n):
        zone = random.choice(zones)
        trafic = random.randint(100, 5000)  # Go
        utilisateurs = random.randint(50, 1500)
        # On stocke dans un dictionnaire avec le nom de la zone comme clé
        donnees[zone] = {"trafic": trafic, "utilisateurs": utilisateurs}
    return donnees


# 2. LOGIQUE DE CALCUL (PROJET 2)
def analyser_trafic(data):
    try:
        if not data:
            raise ValueError("Aucune donnée disponible.")

        resultats_analyse = []
        for zone, stats in data.items():
            # Calcul du ratio Go par utilisateur
            ratio = stats["trafic"] / stats["utilisateurs"]
            resultats_analyse.append((zone, round(ratio, 2)))

        # Tri des zones les plus saturées (ratio le plus élevé)
        resultats_analyse.sort(key=lambda x: x[1], reverse=True)
        return resultats_analyse
    except Exception as e:
        print(f"Erreur de calcul : {e}")
        return []