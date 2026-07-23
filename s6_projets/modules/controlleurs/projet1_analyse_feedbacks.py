import random


# 1. GÉNÉRATION AUTOMATISÉE DES DONNÉES
def generer_feedbacks(n):
    motifs_possibles = ["Qualité réseau", "Prix internet", "Prix appel", "Prix sms", "Service client"]
    data = []
    for i in range(1, n + 1):
        # Génération aléatoire : ID, Score (0-10), Motif aléatoire
        data.append((i, random.randint(0, 10), random.choice(motifs_possibles)))
    return data


# 2. LOGIQUE DE CALCUL (PROJET 1)
def calculer_nps(data):
    try:
        scores = {"Détracteurs": 0, "Passifs": 0, "Promoteurs": 0}
        motifs_plaintes = {}

        for _, note, motif in data:
            if note <= 6:
                scores["Détracteurs"] += 1
                motifs_plaintes[motif] = motifs_plaintes.get(motif, 0) + 1
            elif note <= 8:
                scores["Passifs"] += 1
            else:
                scores["Promoteurs"] += 1

        nps = ((scores["Promoteurs"] - scores["Détracteurs"]) / len(data)) * 100
        return nps, scores, motifs_plaintes
    except ZeroDivisionError:
        return 0, {}, {}
    except Exception as e:
        print(f"Erreur lors du calcul : {e}")
        return None