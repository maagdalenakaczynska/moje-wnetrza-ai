import streamlit as st
import replicate
import os
import requests

# --- KONFIGURACJA ---
st.set_page_config(page_title="Architectural Visionary", layout="wide")

# STYLE
STYLES = {
    "Tropical Modernism": "Tropical modernism, raw concrete, warm teak wood, lush indoor jungle, floor-to-ceiling glass, architectural shadows, luxury resort style",
    "Desert Brutalism": "Desert brutalism, monolithic sandstone, concrete, minimalist desert garden, warm earth tones, sharp architectural lines",
    "Japandi Luxury": "Japandi, minimalist, light oak wood, washi paper textures, zen, wabi-sabi aesthetics",
    "Parisian Haussmann": "Parisian apartment, ornate white moldings, herringbone parquet, marble fireplace, high ceilings",
    "Quiet Luxury": "Quiet luxury, high-end materials, cashmere textures, dark wood, sophisticated minimalist palette",
    "Biophilic High-Tech": "Biophilic design, living green walls, organic shapes, futuristic glass, natural ventilation"
}

# --- PANEL BOCZNY ---
with st.sidebar:
    st.title("⚙️ Ustawienia")
    token = st.text_input("Wklej Replicate API Token:", type="password")
    if token:
        os.environ["REPLICATE_API_TOKEN"] = token
    
    st.markdown("---")
    st.write("### Instrukcja:")
    st.write("1. Załóż konto na Replicate.com")
    st.write("2. Podepnij kartę w zakładce Billing (wymagane przez API)")
    st.write("3. Skopiuj 'Default Token'")

# --- INTERFEJS ---
st.title("🏛️ Architectural Visionary")
st.subheader("Wizualizacja premium z zachowaniem struktury wnętrza")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Wgraj zdjęcie pokoju", type=["jpg", "png", "jpeg"])
    selected_style = st.selectbox("Wybierz styl:", list(STYLES.keys()))
    
    # Fidelity - im wyższe, tym bardziej trzyma się Twoich ścian
    fidelity = st.slider("Wierność strukturze ścian (0.8 = mocno)", 0.1, 1.0, 0.7)
    
    generate_btn = st.button("GENERUJ PROJEKT ✨")

with col2:
    if uploaded_file:
        st.image(uploaded_file, caption="Twoje zdjęcie", use_container_width=True)
    else:
        st.info("Tu pojawi się Twoja wizualizacja")

# --- LOGIKA GENEROWANIA ---
if generate_btn:
    if not token:
        st.error("Błąd: Brak API Tokena!")
    elif not uploaded_file:
        st.error("Błąd: Wgraj zdjęcie!")
    else:
        with st.spinner(f"Szukam najlepszej wersji modelu i projektuję..."):
            try:
                # KROK 1: Inteligentne pobieranie modelu
                model_path = "lucataco/interior-ai"
                model = replicate.models.get(model_path)
                # Pobieramy najnowszą dostępną wersję z serwera
                version = model.versions.list()[0]
                
                # KROK 2: Uruchomienie
                full_prompt = f"A professional high-end interior design of a room in {STYLES[selected_style]} style, architectural digest photography, 8k, highly detailed, realistic materials"
                
                output = version.predict(
                    image=uploaded_file,
                    prompt=full_prompt,
                    image_strength=fidelity, # Model lucataco używa tej nazwy
                    num_inference_steps=50,
                    guidance_scale=7.5
                )

                # KROK 3: Wyświetlanie
                if output:
                    # Model lucataco zwraca bezpośredni URL lub listę
                    image_url = output[0] if isinstance(output, list) else output
                    with col2:
                        st.image(image_url, caption=f"Projekt: {selected_style}", use_container_width=True)
                        
                        img_res = requests.get(image_url)
                        st.download_button("Pobierz projekt", img_res.content, "projekt.png", "image/png")
                    st.success("Gotowe!")
                
            except Exception as e:
                st.error(f"Błąd: {str(e)}")
                if "422" in str(e):
                    st.warning("Prawdopodobnie musisz podpiąć kartę na Replicate.com, aby korzystać z tego modelu przez API.")
