import streamlit as st
import replicate
import os
import requests

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Architectural Visionary AI", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1a1a2e; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #16213e; border: 1px solid #4ecca3; }
    </style>
    """, unsafe_allow_html=True)

# --- BOCZNY PANEL ---
with st.sidebar:
    st.title("⚙️ Konfiguracja")
    api_key = st.text_input("Wklej swój Replicate API Token:", type="password")
    if api_key:
        os.environ["REPLICATE_API_TOKEN"] = api_key
    st.info("Token znajdziesz na: replicate.com/account/api-tokens")
    st.markdown("---")
    st.markdown("### O aplikacji")
    st.write("Aplikacja używa AI do transformacji wnętrz przy zachowaniu 100% geometrii ścian.")

# --- STYLE ---
STYLES = {
    "Tropical Modernism": "raw concrete architecture, warm teak wood accents, lush indoor jungle, floor-to-ceiling glass, architectural shadows, luxury tropical vibe, Brazilian brutalism",
    "Desert Brutalism": "monolithic sandstone structures, minimalist desert landscaping, warm earth tones, sharp architectural lines, deep shadows, Palm Springs aesthetic",
    "Japandi Luxury": "perfect mix of Japanese minimalism and Scandinavian warmth, light oak wood, washi paper, matted black metal, serene zen atmosphere",
    "Parisian Haussmann": "classic French moldings, white walls, light herringbone parquet, marble fireplace, high ceilings, contemporary luxury furniture",
    "Quiet Luxury": "understated elegance, high-end fabrics, neutral beige palette, rich wood textures, sophisticated minimalist lighting",
    "Biophilic High-Tech": "living green walls integrated into walls, organic shapes, futuristic materials, smart glass, abundance of natural plants"
}

# --- INTERFEJS ---
st.title("🏛️ Architectural Visionary")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Wgraj zdjęcie wnętrza")
    uploaded_file = st.file_uploader("Zdjęcie Twojego pokoju (JPG/PNG)", type=["jpg", "jpeg", "png"])
    
    selected_style = st.selectbox("Wybierz styl architektoniczny:", list(STYLES.keys()))
    
    # Dodatkowa precyzja
    fidelity = st.slider("Wierność strukturze (0.8 = bardzo wiernie)", 0.1, 1.0, 0.75)
    
    generate_btn = st.button("STWÓRZ WIZUALIZACJĘ ✨")

with col2:
    st.subheader("2. Projekt")
    if uploaded_file:
        st.image(uploaded_file, caption="Oryginał", use_container_width=True)
    else:
        st.info("Tu pojawi się wygenerowany projekt.")

# --- LOGIKA GENEROWANIA ---
if generate_btn:
    if not api_key:
        st.error("Wklej API Token w lewym panelu!")
    elif uploaded_file is None:
        st.error("Wgraj zdjęcie!")
    else:
        with st.spinner(f"Projektuję w stylu {selected_style}..."):
            try:
                # --- INTELIGENTNE POBIERANIE MODELU ---
                # Używamy modelu xue-pals/controlnet-interior-design (bardzo mocny do wymiarów)
                model_name = "xue-pals/controlnet-interior-design"
                model = replicate.models.get(model_name)
                # Pobieramy ZAWSZE najnowszą wersję, żeby uniknąć błędu 422
                latest_version = model.versions.list()[0]
                
                # Uruchomienie generowania
                output = latest_version.predict(
                    image=uploaded_file,
                    prompt=f"A professional high-end {ST
