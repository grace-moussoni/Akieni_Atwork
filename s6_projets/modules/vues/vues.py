#AFFICHAGE GÉNÉRIQUE (*args)
def afficher_resultat(type_analyse="scores", *args):
    """
    args[0] = nps/valeur_principale
    args[1] = dictionnaire_repartition
    args[2] = dictionnaire_motifs
    """
    try:
        if type_analyse == "scores":
            nps, repartitions, motifs = args
            print(f"--- RAPPORT NPS MTN CONGO ---")
            print(f"Score NPS global : {nps:.1f}")
            print(f"Détail : {repartitions}")
            print("\n--- Top des motifs de mécontentement ---")
            for m, c in sorted(motifs.items(), key=lambda x: x[1], reverse=True):
                print(f"- {m} : {c} mentions")

        elif type_analyse == "trafic":
            analyse = args[0]  # On reçoit la liste de tuples (zone, ratio)
            print("\n--- RAPPORT OPTIMISATION RÉSEAU : MTN CONGO ---")
            print(f"{'ZONE':<20} | {'RATIO (Go/User)':<15} | {'ÉTAT'}")
            print("-" * 50)
            for zone, ratio in analyse:
                etat = "CRITIQUE" if ratio > 3.5 else "OK"
                print(f"{zone:<20} | {ratio:<15} | {etat}")

    except IndexError:
        print("Erreur : Arguments manquants pour l'affichage.")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'affichage : {e}")