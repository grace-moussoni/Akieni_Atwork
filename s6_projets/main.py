# from modules.controlleurs.projet1_analyse_feedbacks import *
# from modules.controlleurs.projet2_analyse_reseau import *
# from modules.vues.vues import *
#
# def main():
#     while True:
#         print("\n=== BIENVENUE DANS LE PROJET DE LA SEMAINE 6 ===")
#         print("1. Analyse des feedbacks")
#         print("2. Analyse du réseau")
#         choix = input("Faites votre choix (1 ou 2) : ")
#
#         if choix == "1":
#             n = 0
#             while n < 5:
#                 n = int(input("Combien d'utilisateurs (min 5) : "))
#             data = generer_feedbacks(n)
#             nps, rep, mot = calculer_nps(data)
#             afficher_resultat("scores", nps, rep, mot)
#
#         elif choix == "2":
#             n = 0
#             while n < 5:
#                 n = int(input("Combien de données réseau (min 5) : "))
#             data = generer_donnees_reseau(n)
#             analyse = analyser_trafic(data)
#             afficher_resultat("trafic", analyse)
#
#         quitter = input("\nSouhaitez-vous quitter le programme ? (oui/non) : ").lower()
#         if quitter == "oui":
#             print("Au revoir !")
#             break
#
#
# if __name__ == "__main__":
#     main()


import streamlit as st
import pandas as pd
import plotly.express as px

# Importation de tes contrôleurs (logique métier)
from modules.controlleurs.projet1_analyse_feedbacks import generer_feedbacks, calculer_nps
from modules.controlleurs.projet2_analyse_reseau import generer_donnees_reseau, analyser_trafic


def main():
    # Configuration de la page
    st.set_page_config(page_title="Dashboard MTN Congo", page_icon="📶", layout="wide")

    # Titre principal
    st.title("📶 Dashboard MTN Congo - Semaine 6")
    st.markdown("Bienvenue dans le tableau de bord interactif pour l'analyse des données de la semaine 6.")

    # Barre latérale pour la navigation
    st.sidebar.header("Menu de Navigation")
    choix = st.sidebar.radio(
        "Choisissez votre module :",
        ["1. Analyse des feedbacks (NPS)", "2. Analyse du réseau (Trafic)"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info("Projet réalisé dans le cadre de l'exercice d'école.")

    # ==========================================
    # MODULE 1 : ANALYSE DES FEEDBACKS
    # ==========================================
    if choix == "1. Analyse des feedbacks (NPS)":
        st.header("🗣️ Analyse de la Satisfaction Client")

        # Le st.number_input remplace ton `while n < 5` et `input()`
        n = st.number_input("Combien d'utilisateurs souhaitez-vous analyser ?", min_value=5, value=50, step=5)

        if st.button("Lancer l'analyse des feedbacks"):
            with st.spinner("Génération et calcul en cours..."):
                # 1. Récupération des données
                data = generer_feedbacks(n)
                nps, repartitions, motifs = calculer_nps(data)

                # 2. Affichage des KPIs (Indicateurs clés)
                st.subheader("Résultats du Net Promoter Score (NPS)")

                # Utilisation de colonnes pour un affichage structuré
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Score NPS", f"{nps:.1f}")
                col2.metric("Promoteurs 🟢", repartitions.get("Promoteurs", 0))
                col3.metric("Passifs 🟡", repartitions.get("Passifs", 0))
                col4.metric("Détracteurs 🔴", repartitions.get("Détracteurs", 0))

                # 3. Graphique Plotly pour les motifs
                st.subheader("Analyse des motifs de mécontentement")
                if motifs:
                    df_motifs = pd.DataFrame(list(motifs.items()), columns=["Motif", "Occurrences"])
                    df_motifs = df_motifs.sort_values(by="Occurrences", ascending=True)  # Tri pour le graphique

                    fig = px.bar(
                        df_motifs,
                        x="Occurrences",
                        y="Motif",
                        orientation='h',  # Barres horizontales
                        title="Répartition des plaintes (Détracteurs)",
                        color="Occurrences",
                        color_continuous_scale="Reds"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.success("Aucun détracteur, donc aucun motif de mécontentement !")

                # 4. Données brutes repliables
                with st.expander("Voir les données brutes générées"):
                    df_brut = pd.DataFrame(data, columns=["ID_Client", "Note", "Motif"])
                    st.dataframe(df_brut, use_container_width=True)

    # ==========================================
    # MODULE 2 : ANALYSE DU RÉSEAU
    # ==========================================
    elif choix == "2. Analyse du réseau (Trafic)":
        st.header("📡 Optimisation de la Couverture Réseau")

        n = st.number_input("Combien de données réseau (zones) souhaitez-vous générer ?", min_value=5, value=15, step=1)

        if st.button("Lancer l'analyse du trafic"):
            with st.spinner("Génération et calcul en cours..."):
                # 1. Récupération des données
                data = generer_donnees_reseau(n)
                analyse = analyser_trafic(data)

                # 2. Transformation pour affichage
                # analyse est censé être une liste de tuples : [(zone, ratio), ...]
                df_trafic = pd.DataFrame(analyse, columns=["Zone Géographique", "Ratio (Go/Utilisateur)"])

                # Ajout d'une colonne statut
                df_trafic["État"] = df_trafic["Ratio (Go/Utilisateur)"].apply(
                    lambda x: "CRITIQUE 🔴" if x > 3.5 else "OK 🟢")

                st.subheader("Rapport de saturation par zone")

                # 3. Graphique Plotly interactif
                fig2 = px.bar(
                    df_trafic,
                    x="Zone Géographique",
                    y="Ratio (Go/Utilisateur)",
                    color="Ratio (Go/Utilisateur)",
                    color_continuous_scale="Viridis",
                    title="Charge du réseau par zone"
                )
                # Ajout d'une ligne rouge pour le seuil critique
                fig2.add_hline(y=3.5, line_dash="dash", line_color="red", annotation_text="Seuil Critique (3.5)")
                st.plotly_chart(fig2, use_container_width=True)

                # 4. Tableau de données mis en forme
                st.dataframe(df_trafic, use_container_width=True)


if __name__ == "__main__":
    main()