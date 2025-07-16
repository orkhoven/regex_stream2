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

    # Fonction de feedback avec tick/cross
    def input_with_feedback(label, correct_answer, multiple_answers=False):
        user_input = st.text_input(label, key=label)
        feedback = ""
        if user_input:
            if multiple_answers:
                if user_input.strip() in [str(ans).strip() for ans in correct_answer]:
                    feedback = "✅"
                else:
                    feedback = "❌"
            else:
                if user_input.strip() == str(correct_answer):
                    feedback = "✅"
                else:
                    feedback = "❌"
        st.markdown(feedback)
        return user_input

    num_words = input_with_feedback("Nombre de mots dans le texte :", len(re.findall(r"\\b\\w+\\b", text)))
    punctuation_count = input_with_feedback("Nombre de signes de ponctuation :", len(re.findall(r"[^\\w\\s]", text)))
    num_years = input_with_feedback("Nombre d’années (ex: 1999, 2024) :", len(re.findall(r"\\b\\d{4}\\b", text)))
    num_emails = input_with_feedback("Nombre d’adresses e-mail :", len(re.findall(r"[\\w.-]+@[\\w.-]+", text)))
    num_proper_names = input_with_feedback("Nombre de noms propres (Prénom Nom) :", "?")
    num_long_words = input_with_feedback("Nombre de mots de plus de 6 lettres :", len(re.findall(r"\\b\\w{7,}\\b", text)))
    life_count = input_with_feedback("Nombre d’occurrences du mot « life » (insensible à la casse) :", len(re.findall(r"life", text, re.IGNORECASE)))
    num_inner_quotes = input_with_feedback("Nombre de guillemets dans des guillemets :", len(re.findall(r'“.*?["\'].*?["\'].*?”', text)))
    num_lowercase_words = input_with_feedback("Nombre de mots en minuscules uniquement :", len(re.findall(r"\\b[a-z]+\\b", text)))
    num_number_words = input_with_feedback("Nombres en toutes lettres (un à dix) :", len(re.findall(r"\\b(un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)\\b", text, re.IGNORECASE)))
    num_ing_verbs = input_with_feedback("Nombre de mots finissant par -ing :", len(re.findall(r"\\b\\w+ing\\b", text)))
    num_emotions = input_with_feedback("Nombre de mots exprimant des émotions (love, hate, fear, hope, joy, sadness) :", len(re.findall(r"\\b(love|hate|fear|hope|joy|sadness)\\b", text, re.IGNORECASE)))
    num_negations = input_with_feedback("Nombre de négations (not, never, no) :", len(re.findall(r"\\b(not|never|no)\\b", text)))
    num_repeated_words = input_with_feedback("Nombre de mots répétés consécutivement (exemple : very very) :", len(re.findall(r"\\b(\\w+) \\1\\b", text, re.IGNORECASE)))
    avg_word_length = input_with_feedback("Longueur moyenne des mots (arrondie à 2 décimales) :", round(sum(len(w) for w in re.findall(r"\\b\\w+\\b", text)) / len(re.findall(r"\\b\\w+\\b", text)), 2))

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

            # Configuration SMTP Yahoo
            smtp_server = "smtp.mail.yahoo.com"
            smtp_port = 587
            smtp_user = "selcuk_orkun@yahoo.com"  # Votre compte Yahoo expéditeur
            smtp_password = "gervfabqarlxhgpg"   # App Password

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)

            st.success("Email envoyé avec succès !")
        except Exception as e:
            st.error(f"Erreur lors de l'envoi de l'email : {e}")
