import streamlit as st
import replicate
import os

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Architectural Visionary AI", layout="wide", initial_sidebar_state="expanded")

# Stylizacja CSS dla lepszego wyglądu
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2c3e50; color: white; }
    </style>
    """, unsafe_allow_stdio=True)

# --- BOCZNY PANEL ---
with st.sidebar:
    st.title("Ustawienia")
    api_key = st.text_input("Wklej Replicate API Token:", type="password")
    if api_key:
        os.environ["REPLICATE_API_TOKEN"] = api_key
    st.info("Klucz znajdziesz na: replicate.com/account/api-tokens")

# --- ROZBUDOWANA BIBLIOTEKA STYLÓW ---
STYLES = {
    "Tropical Modernism": "raw concrete, warm teak wood panels, lush indoor tropical garden, massive floor-to-ceiling glass, architectural shadows, Brazilian brutalism inspired, luxury jungle vibe",
    "Desert Brutalism": "monolithic sandstone and concrete, minimalist desert landscaping, warm earth tones, circular cutouts, high contrast lighting, Palm Springs luxury meets brutalist shapes",
    "Japandi Luxury": "seamless blend of Japanese minimalism and Scandinavian warmth, light oak wood, washi paper textures, matted black accents, zen atmosphere, low-profile furniture",
    "Parisian Haussmann (Modern)": "classic ornate white wall moldings, light herringbone oak parquet, marble fireplace, contemporary art, high ceilings, large windows with soft daylight",
    "Quiet Luxury / Old Money": "high-end cashmere textures, dark mahogany wood, brass accents, understated elegance, neutral palette, rich textures, classic architectural proportions",
    "Biophilic High-Tech": "integrated vertical green walls, smart glass, organic flowing architectural shapes, natural wood and stone, air-purifying plants, futuristic eco-living",
    "Industrial Loft (New York)": "exposed red brick, black steel beams, polished concrete floors, double-height ceilings, large factory windows, leather furniture, vintage Edison lighting",
    "Mediterranean Zen": "whitewashed plaster walls, terracotta tiles, olive wood accents, arched doorways, soft linen fabrics, relaxed coastal luxury, warm sun-drenched atmosphere",
    "Art Deco Revival": "bold geometric patterns, velvet upholstery, gold and chrome details, dark lacquered wood, glamorous lighting, rich jewel tones (emerald, navy)",
    "Scandinavian Hygge": "cozy minimalist, light woods, wool rugs, fireplace, soft white walls, functional furniture, plenty of natural light"
}

# --- INTERFEJS GŁÓWNY ---
st.title("🏛️ Architectural Visionary")
st.subheader("Profesjonalna wizaulizacja wnętrz z zachowaniem geometrii ścian")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 1. Prześlij zdjęcie")
    uploaded_file = st.file_uploader("Wgraj zdjęcie pokoju (format JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    st.markdown("### 2. Wybierz styl i parametry")
    selected_style = st.selectbox("Styl architektoniczny:", list(STYLES.keys()))
    
    # Suwak Structure Fidelity - kluczowy dla wymiarów
    fidelity = st.slider("Wierność wymiarom (Structure Fidelity)", 0.3, 0.8, 0.7, help="Wyższa wartość bardziej trzyma się Twoich ścian. Niższa pozwala AI na więcej zmian w architekturze.")
    
    generate_btn = st.button("GENERUJ PROJEKT ✨")

with col2:
    st.markdown("### 3. Wizualizacja")
    if uploaded_file:
        st.image(uploaded_file, caption="Twoje oryginalne wnętrze", use_container_width=True)
    else:
        st.info("Czekam na zdjęcie...")

# --- LOGIKA GENEROWANIA ---
if generate_btn:
    if not api_key:
        st.error("Błąd: Musisz podać Replicate API Token w panelu bocznym!")
    elif uploaded_file is None:
        st.error("Błąd: Wgraj zdjęcie przed kliknięciem przycisku.")
    else:
        with st.spinner(f"Projektowanie w stylu {selected_style}... To potrwa około 20-30 sekund."):
            try:
                # Wywołanie modelu jagadeesh-j/interior-ai
                output = replicate.run(
                    "jagadeesh-j/interior-ai:7660b445372ca620785167667d7a16744036125a22e86209b552f483864a7813",
                    input={
                        "image": uploaded_file,
                        "prompt": f"A high-end, photorealistic interior design of a room in {selected_style} style, architectural digest photography, 8k resolution, highly detailed, professional cinematic lighting, realistic textures",
                        "negative_prompt": "low quality, blurry, distorted, messy, unrealistic, cheap furniture, bad anatomy, deformed furniture, weird perspective",
                        "num_samples": 1,
                        "guidance_scale": 8,
                        "structure_fidelity": fidelity
                    }
                )
                
                # Wyświetlenie wyniku
                with col2:
                    st.image(output[0], caption=f"Projekt: {selected_style}", use_container_width=True)
                    st.success("Wizualizacja gotowa!")
                    
                    # Opcja pobierania
                    st.download_button(
                        label="Pobierz zdjęcie",
                        data=output[0],
                        file_name=f"projekt_{selected_style.lower().replace(' ', '_')}.png",
                        mime="image/png"
                    )
            
            except Exception as e:
                st.error(f"Wystąpił błąd podczas generowania: {str(e)}")
                st.info("Sprawdź, czy Twój klucz API jest poprawny i czy masz środki na koncie Replicate.")

# --- STOPKA ---
st.markdown("---")
st.caption("Aplikacja wykorzystuje AI (Stable Diffusion + ControlNet) do przekształcania obrazu przy zachowaniu jego struktury geometrycznej.")
