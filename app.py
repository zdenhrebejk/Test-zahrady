import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Test e-mailu", page_icon="📧")

st.title("📬 Testovací odeslání e-mailu přes EmailJS")

with open("email_sender.html", "r", encoding="utf-8") as file:
    email_component = file.read()

components.html(email_component, height=100)

if st.button("📨 Odeslat testovací e-mail"):
    st.info("Odesílám e-mail…")

    components.html("""
        <script>
          const payload = {
            jmeno: "Testovací Jméno",
            email: "test@zkouska.cz",
            lokalita: "Praha",
            plocha: "150",
            pocet_habru: "25",
            zavlaha: "Ano",
            cena: "59999"
          };

          window.parent.postMessage({ type: "SEND_EMAIL", payload }, "*");

          window.addEventListener("message", function(event){
            if (event.data === "SUCCESS") {
              alert("✅ Testovací e-mail úspěšně odeslán.");
            }
            if (event.data === "ERROR") {
              alert("❌ Nepodařilo se odeslat testovací e-mail.");
            }
          }, false);
        </script>
    """, height=0)
