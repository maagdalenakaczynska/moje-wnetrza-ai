import streamlit as st
import replicate
import os
import requests

# --- KONFIGURACJA ---
st.set_page_config(page_title="Architectural Visionary", layout="wide")

# STYLE (z naciskiem na Tropical Modernism)
STYLES = {
    "Tropical Modernism": "Tropical modernism architecture, raw concrete walls, warm teak wood slats, lush indoor jungle with palm trees, large floor-to-ceiling windows, cinematic sunlight, Brazilian brutalism, high-end luxury",
    "Desert Brutalism": "Desert brutalism, monolithic sandstone and concrete, minimalist desert garden, warm earth tones, sharp architectural shadows, luxury oasis",
    "Japandi Luxury": "Japandi interior, light oak wood, washi paper textures, matted black accents, zen atmosphere, wabi-sabi, extremely clean and minimalist",
    "Parisian Haussmann": "Parisian apartment, white ornate wall moldings, light herringbone oak parquet, marble fireplace, high ceilings, contemporary minimalist furniture",
    "Quiet Luxury": "Quiet luxury, high-end cashmere textures, dark mahogany wood, brass accents, neutral palette, sophisticated and rich atmosphere",
    "Industrial Loft": "New York industrial loft, exposed brick, black steel beams, polished concrete floors, factory windows, leather furniture"
}

# --- PANEL BOCZNY ---
with st.sidebar:
    st.title("⚙️ Konfiguracja")
    api_token = st.text_input("Wklej Replicate API Token:", type="password")
    if api_token:
        os.environ["REPLICATE_API_TOKEN"] = api_token
    st.info("Klucz API: replicate.com/account/api-tokens")
    st.warning("Ważne: Jeśli masz błędy 422/404, sprawdź czy masz podpiętą kartę na Replicate.com/billing")

# --- INTERFEJS ---
st.title("🏛️ Architectural Visionary")
st.write("Profesjonalne projektowanie wnętrz oparte na Twojej geometrii.")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Wgraj zdjęcie pokoju", type=["jpg", "png", "jpeg"])
    selected_style = st.selectbox("Wybierz styl architektoniczny:", list(STYLES.keys()))
    
    # Fidelity - im więcej, tym bardziej trzyma się oryginału
    fidelity = st.slider("Wierność strukturze (im wyżej, tym mniej zmian w układzie)", 0.1, 1.0, 0.8)
    
    generate_btn = st.button("GENERUJ PROJEKT ✨")

with col2:
    if uploaded_file:
        st.image(uploaded_file, caption="Twoje zdjęcie", use_container_width=True)
    else:
        st.info("Tu pojawi się wizualizacja po kliknięciu przycisku.")

# --- LOGIKA GENEROWANIA ---
if generate_btn:
    if not api_token:
        st.error("Błąd: Brak API Tokena!")
    elif not uploaded_file:
        st.error("Błąd: Wgraj zdjęcie!")
    else:
        with st.spinner(f"Przetwarzanie w stylu {selected_style}..."):
            try:
                # UŻYWAMY OFICJALNEGO MODELU SDXL CANNY (Najbardziej stabilny)
                output = replicate.run(
                    "mistralai/mistral-7b-instruct-v0.2", # Ignoruj to, to tylko test połączenia jeśli SDXL by padło
                    input={"prompt": "test"}
                )
                
                # To jest właściwe wywołanie modelu graficznego
                model_version = "cjwbw/controlnet-canny-sdxl:549c450f3711993478988771191024328570d44cfc587c672b10a26e85e0569a"
                
                prediction = replicate.run(
                    model_version,
                    input={
                        "image": uploaded_file,
                        "prompt": f"A high-end professional photo of a room, {STYLES[selected_style]}, architectural digest style, 8k, highly detailed, realistic texture",
                        "negative_prompt": "ugly, blurry, low quality, distorted, messy, cheap, bad architecture",
                        "condition_scale": fidelity,
                        "num_inference_steps": 35,
                        "guidance_scale": 7.5
                    }
                )

                if prediction and len(prediction) > 0:
                    image_url = prediction[0]
                    with col2:
                        st.image(image_url, caption=f"Styl: {selected_style}", use_container_width=True)
                        
                        # Pobieranie obrazu
                        img_res = requests.get(image_url)
                        st.download_button("Pobierz projekt", img_res.content, "projekt.png", "image/png")
                    st.success("Wizualizacja gotowa!")

            except Exception as e:
                st.error(f"Wystąpił błąd: {str(e)}")
                if "422" in str(e) or "401" in str(e):
                    st.info("💡 To błąd uprawnień. Wejdź na Replicate.com, przejdź do 'Billing' i upewnij się, że masz podpiętą kartę. API nie pozwala na darmowe generowanie obrazów SDXL bez zweryfikowanego konta.")
