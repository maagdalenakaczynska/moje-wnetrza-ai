import streamlit as st
import replicate
import os
import requests

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Architectural Visionary AI", layout="wide")

# Stylizacja CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #1f1f2e; color: white; font-weight: bold; }
    .stSelectbox label, .stSlider label { font-weight: bold; color: #1f1f2e; }
    </style>
    """, unsafe_allow_html=True)

# --- BOCZNY PANEL ---
with st.sidebar:
    st.title("⚙️ Ustawienia")
    api_key = st.text_input("Replicate API Token:", type="password")
    if api_key:
        os.environ["REPLICATE_API_TOKEN"] = api_key
    st.info("Klucz API pobierzesz z: replicate.com/account/api-tokens")

# --- BIBLIOTEKA STYLÓW ---
STYLES = {
    "Tropical Modernism": "Tropical modernism, raw concrete, teak wood, lush indoor plants, large glass walls, cinematic lighting, Brazilian architecture",
    "Desert Brutalism": "Desert brutalism, sandstone, monolithic concrete, minimalist cacti garden, warm earth tones, sharp shadows",
    "Japandi Luxury": "Japandi, minimalist, light oak, paper textures, zen, high-end furniture, wabi-sabi",
    "Parisian Modern": "Modern Parisian apartment, white moldings, herringbone floor, marble, elegant, airy",
    "Quiet Luxury": "Quiet luxury, high-end materials, cashmere, dark wood, sophisticated, beige and grey palette",
    "Industrial Loft": "Industrial loft, exposed brick, black steel, high ceilings, large windows, leather and metal",
    "Mediterranean Zen": "Mediterranean zen, white plaster, arched openings, olive wood, terracotta, sun-drenched",
    "Biophilic Future": "Biophilic design, living walls, organic shapes, futuristic architecture, natural light"
}

# --- INTERFEJS GŁÓWNY ---
st.title("🏛️ Architectural Visionary")
st.write("Wgraj zdjęcie, aby zmienić swoje wnętrze z zachowaniem wymiarów.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Twoje zdjęcie")
    uploaded_file = st.file_uploader("Wybierz plik (JPG/PNG)", type=["jpg", "jpeg", "png"])
    
    selected_style = st.selectbox("Wybierz styl architektoniczny:", list(STYLES.keys()))
    
    # Prompt to serce AI
    custom_prompt = STYLES[selected_style]
    
    # Suwak siły zmian
    prompt_strength = st.slider("Wierność oryginałowi (Im więcej, tym mniej zmian w strukturze)", 0.5, 1.0, 0.8)
    
    generate_btn = st.button("GENERUJ WIZUALIZACJĘ ✨")

with col2:
    st.subheader("2. Wynik")
    if uploaded_file:
        st.image(uploaded_file, caption="Oryginał", use_container_width=True)
    else:
        st.write("Tu pojawi się Twój nowy projekt.")

# --- LOGIKA GENEROWANIA ---
if generate_btn:
    if not api_key:
        st.error("Wklej swój API Token w lewym panelu!")
    elif uploaded_file is None:
        st.error("Wgraj zdjęcie!")
    else:
        with st.spinner("Przetwarzanie... To potrwa około 20 sekund."):
            try:
                # UŻYWAMY NOWEGO, SPRAWDZONEGO MODELU
                output = replicate.run(
                    "lucataco/interior-ai:042302324905d45d8b72e12e7ef63e3d489f6d149021e7d23a1059f8a370e70a",
                    input={
                        "image": uploaded_file,
                        "prompt": f"A high-end {custom_prompt}, architectural photography, 8k, highly detailed",
                        "image_strength": prompt_strength, # To kontroluje jak bardzo trzymamy się zdjęcia
                        "num_inference_steps": 50,
                        "guidance_scale": 7.5
                    }
                )
                
                # Model zwraca URL do obrazu
                image_url = output
                st.image(image_url, caption=f"Styl: {selected_style}", use_container_width=True)
                
                # Przycisk pobierania
                img_response = requests.get(image_url)
                st.download_button("Pobierz projekt", img_response.content, "projekt.png", "image/png")
                st.success("Wizualizacja gotowa!")

            except Exception as e:
                st.error(f"Wystąpił błąd: {str(e)}")
                st.info("Jeśli widzisz błąd 422, oznacza to że Replicate znów zmieniło wersję modelu. Napisz do mnie, a podam Ci najnowszą.")
