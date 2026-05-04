import streamlit as st
import replicate
import os
import requests

# --- KONFIGURACJA ---
st.set_page_config(page_title="Architectural Visionary", layout="wide")

# STYLE (z naciskiem na Twoje ulubione)
STYLES = {
    "Tropical Modernism": "Tropical modernism, raw concrete, teak wood, lush indoor jungle, floor-to-ceiling glass, architectural shadows, luxury resort vibe",
    "Desert Brutalism": "Desert brutalism, sandstone, monolithic concrete, minimalist desert garden, warm earth tones, sharp architectural lines",
    "Japandi Luxury": "Japandi, minimalist, light oak wood, washi paper textures, zen, high-end furniture, wabi-sabi aesthetics",
    "Parisian Haussmann": "Parisian apartment, ornate white moldings, herringbone parquet, marble fireplace, high ceilings, contemporary luxury",
    "Quiet Luxury": "Quiet luxury, high-end materials, cashmere textures, dark wood, sophisticated minimalist palette",
    "Biophilic High-Tech": "Biophilic design, living green walls, organic shapes, futuristic glass, natural ventilation"
}

# --- PANEL BOCZNY ---
with st.sidebar:
    st.title("⚙️ Ustawienia")
    api_token = st.text_input("Wklej Replicate API Token:", type="password")
    if api_token:
        os.environ["REPLICATE_API_TOKEN"] = api_token
    st.info("Token znajdziesz na: replicate.com/account/api-tokens")
    st.markdown("---")
    st.write("Wskazówka: Jeśli masz błąd, upewnij się, że masz podpiętą kartę na Replicate.")

# --- INTERFEJS ---
st.title("🏛️ Architectural Visionary")
st.subheader("Wizualizacja premium z zachowaniem geometrii pomieszczenia")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Wgraj zdjęcie pokoju", type=["jpg", "png", "jpeg"])
    selected_style = st.selectbox("Wybierz styl architektoniczny:", list(STYLES.keys()))
    
    # Fidelity - im wyższe, tym bardziej AI trzyma się Twoich ścian
    fidelity = st.slider("Wierność strukturze ścian", 0.1, 1.0, 0.8)
    
    generate_btn = st.button("GENERUJ WIZUALIZACJĘ ✨")

with col2:
    if uploaded_file:
        st.image(uploaded_file, caption="Twoje zdjęcie", use_container_width=True)
    else:
        st.info("Czekam na zdjęcie...")

# --- LOGIKA GENEROWANIA ---
if generate_btn:
    if not api_token:
        st.error("Błąd: Brak API Tokena w lewym panelu!")
    elif not uploaded_file:
        st.error("Błąd: Najpierw wgraj zdjęcie!")
    else:
        with st.spinner(f"Przetwarzanie stylu {selected_style}..."):
            try:
                # UŻYWAMY MODELU CANNY-SDXL (Najbardziej stabilny sposób na geometrię)
                # Model: cjwbw/controlnet-canny-sdxl
                output = replicate.run(
                    "cjwbw/controlnet-canny-sdxl:549c450f3711993478988771191024328570d44cfc587c672b10a26e85e0569a",
                    input={
                        "image": uploaded_file,
                        "prompt": f"A high-end, professional interior design of a room in {STYLES[selected_style]} style, architectural digest photography, 8k, highly detailed, realistic materials",
                        "negative_prompt": "low quality, blurry, distorted, messy, cheap, unrealistic, bad proportions",
                        "condition_scale": fidelity,
                        "num_inference_steps": 30,
                        "guidance_scale": 7.5
                    }
                )

                if output and len(output) > 0:
                    image_url = output[0]
                    with col2:
                        st.image(image_url, caption=f"Projekt: {selected_style}", use_container_width=True)
                        
                        # Pobieranie
                        img_res = requests.get(image_url)
                        st.download_button("Pobierz projekt", img_res.content, "projekt.png", "image/png")
                    st.success("Wizualizacja gotowa!")
                else:
                    st.error("AI nie zwróciło obrazu. Spróbuj ponownie.")

            except Exception as e:
                st.error(f"Wystąpił błąd: {str(e)}")
                if "401" in str(e) or "403" in str(e):
                    st.warning("Sprawdź, czy Twój klucz API jest poprawny i czy masz środki na koncie Replicate.")
