import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zahradní nabídka", page_icon="🌿", layout="centered")

st.markdown("<h1 style='color:green;'>Poptávka realizace zahrady</h1>", unsafe_allow_html=True)

# HTML komponenta pro EmailJS
with open("email_sender.html", "r", encoding="utf-8") as file:
    email_component = file.read()

components.html(email_component, height=100)

with st.form("zahrada_form"):
    st.subheader("Základní informace")
    jmeno = st.text_input("Vaše jméno")
    email = st.text_input("Váš e-mail")
    plocha = st.number_input("Plocha trávníku (m²)", min_value=0)
    pocet_habru = st.number_input("Počet habrů", min_value=0)
    zavlaha = st.checkbox("Přejete si automatickou závlahu?")
    lokalita = st.text_input("Místo realizace")

    st.subheader("Odhad času a ceny")
    odeslat = st.form_submit_button("Vypočítat nabídku a odeslat e-mail")

if odeslat:
    cena_travnik = plocha * 190
    cena_habry = pocet_habru * 150
    cena_zavlaha = 0
    if zavlaha:
        zavlaha_base = 3500
        zavlaha_extra = max(0, (plocha - 10) / 5) * 500
        cena_zavlaha = zavlaha_base + zavlaha_extra

    doprava = 5000
    prace = 400 * 8

    celkova_cena = cena_travnik + cena_habry + cena_zavlaha + doprava + prace

    st.success(f"Předběžná cena: {int(celkova_cena)} Kč")

    st.markdown(f"""
    **Jméno:** {jmeno}  
    **E-mail:** {email}  
    **Lokalita:** {lokalita}  
    **Trávník:** {plocha} m² → {int(cena_travnik)} Kč  
    **Habry:** {pocet_habru} ks → {int(cena_habry)} Kč  
    **Závlaha:** {'Ano' if zavlaha else 'Ne'} → {int(cena_zavlaha)} Kč  
    **Doprava:** {doprava} Kč  
    **Práce zahradníka:** {prace} Kč  
    **Celkem:** {int(celkova_cena)} Kč
    """)

    # JavaScript – odešle zprávu do iframe s daty
    components.html(f"""
        <script>
          const payload = {{
            jmeno: "{jmeno}",
            email: "{email}",
            lokalita: "{lokalita}",
            plocha: "{plocha}",
            habry: "{pocet_habru}",
            zavlaha: "{'Ano' if zavlaha else 'Ne'}",
            cena: "{int(celkova_cena)}"
          }};
          window.parent.postMessage({{ type: "SEND_EMAIL", payload }}, "*");
        </script>
    """, height=0)
