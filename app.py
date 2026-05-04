import streamlit as st
import replicate
import os
import requests

# --- KONFIGURACJA ---
st.set_page_config(page_title="Architectural Visionary", layout="wide")

# --- STYLE ---
STYLES = {
    "Tropical Modernism": "raw concrete, teak wood, lush indoor jungle, floor-to-ceiling glass, architectural shadows",
    "Desert Brutalism": "monolithic sandstone, concrete, minimalist desert garden, warm earth tones, sharp shadows",
    "Japandi Luxury": "minimalist, light oak wood, washi paper textures, zen atmosphere, high-end furniture",
    "Parisian Haussmann": "ornate moldings, white walls, herringbone parquet, marble fireplace, high ceilings",
    "Quiet Luxury": "sophisticated, cashmere textures, neutral palette, rich wood, understated elegance",
    "Biophilic High-Tech": "living walls, organic shapes, futuristic glass, natural ventilation, lush greenery"
}

# --- PANEL BOCZNY ---
with st.sidebar:
    st.title("Ustawienia")
    api_token = st.text_input("Replicate API Token", type="password")
    if api_token:
        os.environ["REPLICATE_API_TOKEN"] = api_token
    st.info("Pobierz klucz z: replicate.com/account/api-tokens")

# --- INTERFEJS ---
st.title("🏛️ Architectural Visionary")
st.write("Wizaulizacja wnętrz z zachowaniem geometrii")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Wgraj zdjęcie pokoju", type=["jpg", "png", "jpeg"])
    selected_style = st.selectbox("Wybierz styl:", list(STYLES.keys()))
    fidelity = st.slider("Wierność strukturze", 0.1, 1.0, 0.7)
    btn = st.button("GENERUJ PROJEKT ✨")

# --- GENEROWANIE ---
if btn:
    if not api_token:
        st.error("Podaj API Token!")
    elif not uploaded_file:
        st.error("Wgraj zdjęcie!")
    else:
        with st.spinner("Przetwarzanie..."):
            try:
                # Budujemy prosty prompt
                style_desc = STYLES[selected_style]
                full_prompt = f"Professional interior design, {style_desc}
