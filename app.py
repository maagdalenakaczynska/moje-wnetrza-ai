import streamlit as st
import replicate
import os

# --- KONFIGURACJA ---
st.set_page_config(page_title="Architectural Visionary AI", layout="wide")

# Tutaj wstaw swój klucz API lub ustaw go w ustawieniach Streamlit
REPLICATE_API_TOKEN = st.sidebar.text_input("Wklej swój Replicate API Token", type="password")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# --- BIBLIOTEKA WYRAFINOWANYCH STYLÓW ---
STYLES = {
    "Tropical Modernism": "raw concrete, warm teak wood, lush tropical indoor plants, large floor-to-ceiling glass, cinematic sunset lighting, brutalist elements, Brazilian architecture style",
    "Desert Brutalism": "monolithic sandstone structures, minimalist desert garden, terracotta tones, circular architectural cutouts, harsh sunlight and deep shadows",
    "Japandi Luxury": "organic shapes, light oak wood, washi paper textures, matted black metal accents, wabi-sabi aesthetics, extremely calm and high-end",
    "Haussmannian Contemporary": "classic Parisian moldings, herringbone oak parquet, marble fireplace, modern minimalist furniture, high ceilings, soft daylight",
    "Biophilic High-Tech": "integrated smart home systems, living green walls, futuristic glass shapes, natural ventilation, high-end sustainable materials"
}

# --- INTERFEJS ---
st.title("🏛️ Architectural Visionary")
st.markdown("Twoja profesjonalna aplikacja do projektowania wnętrz z zachowaniem geometrii.")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Wgraj zdjęcie swojego wnętrza (zachowamy jego wymiary)", type=["jpg", "jpeg", "png"])
    selected_style = st.selectbox("Wybierz styl architektoniczny:", list(STYLES.keys()))
    
    strength = st.slider("Siła zmian (jak bardzo AI może zaszaleć?)", 0.0, 1.0, 0.8)
    
    generate_btn = st.button("GENERUJ WIZUALIZACJĘ ✨")

# --- LOGIKA GENEROWANIA ---
if generate_btn:
    if not REPLICATE_API_TOKEN:
        st.error("Proszę, podaj klucz API w bocznym panelu.")
    elif uploaded_file is None:
        st.error("Wgraj zdjęcie wnętrza.")
    else:
        with col2:
            with st.spinner("Analizuję geometrię i nakładam styl..."):
                try:
                    # Używamy modelu ControlNet Canny, który "widzi" krawędzie ścian
                    # Model: fadirat/controlnet-interior-design lub podobne oparte na SDXL
                    output = replicate.run(
                        "xpals/controlnet-interior-design:8beff3369491f63a6559797d028298647c3af25050591c0e3ad35cae373c892d",
                        input={
                            "image": uploaded_file,
                            "prompt": f"Luxury interior design of a room in {selected_style} style, architectural photography, highly detailed, 8k, professional lighting",
                            "negative_prompt": "deformed, messy, blurry, low quality, cheap furniture, unrealistic, floating objects",
                            "structure_fidelity": strength,
                            "num_outputs": 1
                        }
                    )
                    
                    st.image(output[0], caption=f"Twoja wizualizacja: {selected_style}", use_column_width=True)
                    st.success("Gotowe! AI zachowało strukturę Twojego pokoju.")
                    
                    with open("design.png", "wb") as f:
                        # Możliwość pobrania
                        st.download_button("Pobierz projekt", output[0], "projekt.png")
                
                except Exception as e:
                    st.error(f"Wystąpił błąd: {e}")
