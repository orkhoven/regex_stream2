import streamlit as st
import pandas as pd
import re
import smtplib
from email.message import EmailMessage
import io

st.title("TP Webscraping & RegEx - Analyse manuelle des citations")

st.markdown("""
**Instructions :**

**Étape 1 :** Téléversez votre fichier `quotes.csv` après avoir fait le scraping sur [https://quotes.toscrape.com/](https://quotes.toscrape.com/)

➡️ **Colonnes attendues :** `quote`, `author`, `birth_date`, `birth_place`

**Étape 2 :** Répondez manuellement aux questions Regex suivantes, en vous basant sur le texte de la colonne `quote`.

**Étape 3 :** Téléchargez vos réponses au format CSV ou envoyez-les par email à l’enseignant.
""")

uploaded_file = st.file_uploader("Téléversez ici votre fichier CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Aperçu des données téléversées :", df.head())

    text = " ".join(df['quote'].astype(str))

    st.markdown("### Répondez aux questions Regex (manuellement) :")

    num_words = st.text_input("Nombre de mots dans le texte :", "")
    punctuation_count = st.text_input("Nombre de signes de ponctuation :", "")
    num_years = st.text_input("Nombre d’années (ex: 1999, 2024) :", "")
    num_emails = st.text_input("Nombre d’adresses e-mail :", "")
    num_proper_names = st.text_input("Nombre de noms propres (Prénom Nom) :", "")
    num_long_words = st.text_input("Nombre de mots de plus de 6 lettres :", "")
    life_count = st.text_input("Nombre d’occurrences du mot « life » (insensible à la casse) :", "")
    num_inner_quotes = st.text_input("Nombre de guillemets dans des guillemets :", "")
    num_lowercase_words = st.text_input("Nombre de mots en minuscules uniquement :", "")
    num_number_words = st.text_input("Nombres en toutes lettres (un à dix) :", "")
    num_ing_verbs = st.text_input("Nombre de mots finissant par -ing :", "")
    num_emotions = st.text_input("Nombre de mots exprimant des émotions (love, hate, fear, hope, joy, sadness) :", "")
    num_negations = st.text_input("Nombre de négations (not, never, no) :", "")
    num_repeated_words = st.text_input("Nombre de mots répétés consécutivement (exemple : very very) :", "")
    avg_word_length = st.text_input("Longueur moyenne des mots (arrondie à 2 décimales) :", "")

    if st.button("Télécharger mes réponses en CSV"):
        data = {
            "Tâche Regex": [
                "Nombre de mots",
                "Nombre de signes de ponctuation",
                "Nombre d’années",
                "Nombre d’adresses e-mail",
                "Nombre de noms propres (Prénom Nom)",
                "Nombre de mots de plus de 6 lettres",
                "Nombre d’occurrences du mot « life »",
                "Nombre de guillemets dans des guillemets",
                "Nombre de mots en minuscules uniquement",
                "Nombres en toutes lettres (un à dix)",
                "Nombre de mots finissant par -ing",
                "Nombre de mots exprimant des émotions",
                "Nombre de négations",
                "Nombre de mots répétés consécutivement",
                "Longueur moyenne des mots"
            ],
            "Réponse": [
                num_words, punctuation_count, num_years, num_emails, num_proper_names, num_long_words,
                life_count, num_inner_quotes, num_lowercase_words, num_number_words, num_ing_verbs,
                num_emotions, num_negations, num_repeated_words, avg_word_length
            ]
        }
        result_df = pd.DataFrame(data)
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("Télécharger le fichier CSV", csv, "reponses_regex.csv", "text/csv")

    st.markdown("---")
    st.markdown("### Envoyer vos réponses par email")

    email_address = st.text_input("Votre adresse email :", "")
    teacher_email = "selcuk_orkun@yahoo.com"  # DESTINATAIRE

    if st.button("Envoyer par email"):
        try:
            data = {
                "Tâche Regex": [
                    "Nombre de mots",
                    "Nombre de signes de ponctuation",
                    "Nombre d’années",
                    "Nombre d’adresses e-mail",
                    "Nombre de noms propres (Prénom Nom)",
                    "Nombre de mots de plus de 6 lettres",
                    "Nombre d’occurrences du mot « life »",
                    "Nombre de guillemets dans des guillemets",
                    "Nombre de mots en minuscules uniquement",
                    "Nombres en toutes lettres (un à dix)",
                    "Nombre de mots finissant par -ing",
                    "Nombre de mots exprimant des émotions",
                    "Nombre de négations",
                    "Nombre de mots répétés consécutivement",
                    "Longueur moyenne des mots"
                ],
                "Réponse": [
                    num_words, punctuation_count, num_years, num_emails, num_proper_names, num_long_words,
                    life_count, num_inner_quotes, num_lowercase_words, num_number_words, num_ing_verbs,
                    num_emotions, num_negations, num_repeated_words, avg_word_length
                ]
            }
            result_df = pd.DataFrame(data)
            csv_buffer = io.StringIO()
            result_df.to_csv(csv_buffer, index=False)
            csv_content = csv_buffer.getvalue()

            msg = EmailMessage()
            msg['Subject'] = "Résultats TP Regex - Étudiant"
            msg['From'] = email_address
            msg['To'] = teacher_email
            msg.set_content(f"Voici les réponses de l'étudiant ({email_address}) :\n\n{csv_content}")

            # Configuration SMTP Gmail
            smtp_server = "smtp.mail.yahoo.com"
            smtp_port = 587
            smtp_user = "selcuk_orkun@yahoo.com"  # Votre compte Gmail expéditeur
            smtp_password = "gervfabqarlxhgpg"   # App Password

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            st.success("Email envoyé avec succès !")
        except Exception as e:
            st.error(f"Erreur lors de l'envoi de l'email : {e}")
