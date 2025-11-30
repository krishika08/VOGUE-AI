import streamlit as st
import joblib
import time
import requests
import matplotlib.pyplot as plt
from sklearn import tree
from streamlit_lottie import st_lottie
from weather_module import get_weather

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Style AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ASSETS ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_hanger = load_lottieurl("https://lottie.host/629df572-8812-426c-8238-662d55639688/d73T7pSgP2.json")

# --- ROBUST MODEL LOADING ---
@st.cache_resource
def load_resources():
    try:
        model = joblib.load('model.pkl')
        le_weather = joblib.load('le_weather.pkl')
        le_event = joblib.load('le_event.pkl')
        le_skin = joblib.load('le_skin.pkl')
        le_outfit = joblib.load('le_outfit.pkl')
        return model, le_weather, le_event, le_skin, le_outfit
    except Exception as e:
        return None, None, None, None, None

model, le_weather, le_event, le_skin, le_outfit = load_resources()

def safe_transform(encoder, value, default_value):
    try:
        if value in encoder.classes_:
            return encoder.transform([value])[0]
        else:
            return encoder.transform([default_value])[0]
    except:
        return 0 

# --- SEASONAL COLOR LOGIC ---
def get_advanced_color_palette(skin_tone, undertone):
    if undertone == "Cool" and skin_tone in ["Medium", "Dark"]:
        return {
            "Season": "Winter ❄",
            "Desc": "Bold, sharp, high-contrast colors.",
            "Power": {"Black": "#000000", "White": "#FFFFFF", "Crimson": "#DC143C", "Navy": "#000080", "Royal Blue": "#104E8B", "Emerald": "#50C878"},
            "Neutrals": ["#808080", "#C0C0C0", "#2F4F4F"],
            "Avoid": ["#D2691E", "#FFD700", "#F4A460"]
        }
    elif undertone == "Cool" and skin_tone == "Light":
        return {
            "Season": "Summer ☀",
            "Desc": "Soft, cool, muted pastels.",
            "Power": {"Powder Blue": "#B0E0E6", "Lavender": "#E6E6FA", "Rose": "#FFB6C1", "Mint": "#98FB98", "Slate": "#778899", "Steel": "#4682B4"},
            "Neutrals": ["#F5F5F5", "#708090", "#A9A9A9"],
            "Avoid": ["#000000", "#FFA500", "#FFFF00"]
        }
    elif undertone == "Warm" and skin_tone in ["Medium", "Dark"]:
        return {
            "Season": "Autumn 🍂",
            "Desc": "Rich, earthy, golden hues.",
            "Power": {"Olive": "#808000", "Chocolate": "#8B4513", "Gold": "#DAA520", "Brick Red": "#B22222", "Rust": "#D2691E", "Forest": "#556B2F"},
            "Neutrals": ["#F5F5DC", "#DEB887", "#8B0000"],
            "Avoid": ["#FF69B4", "#00FFFF", "#E6E6FA"]
        }
    else: 
        return {
            "Season": "Spring 🌸",
            "Desc": "Bright, fresh, vibrant shades.",
            "Power": {"Coral": "#FF7F50", "Turquoise": "#40E0D0", "Gold": "#FFD700", "Salmon": "#FFA07A", "Aqua": "#7FFFD4", "OrangeRed": "#FF4500"},
            "Neutrals": ["#FFF8DC", "#F0E68C", "#D2B48C"],
            "Avoid": ["#000000", "#696969", "#800000"]
        }

# --- UPGRADED DYNAMIC MANNEQUINS (WITH FACES) ---
def get_mannequin_svg(gender, color_hex):
    skin_color = "#FAD7C0"
    hair_color = "#4A3B2F"
    shoe_color = "#333333"
    
    if gender == "Men":
        # Stylized Male Figure with Face, Hair, Shirt, Pants, Shoes
        return f"""
        <svg width="200" height="450" viewBox="0 0 200 450" xmlns="http://www.w3.org/2000/svg">
            <path d="M70,40 Q100,20 130,40 Q140,60 135,80 L65,80 Q60,60 70,40" fill="{hair_color}"/>
            <ellipse cx="100" cy="75" rx="35" ry="45" fill="{skin_color}"/>
            <circle cx="85" cy="70" r="3" fill="#333"/> <circle cx="115" cy="70" r="3" fill="#333"/>
            <path d="M90,100 Q100,105 110,100" stroke="#333" fill="none"/>
            <rect x="85" y="115" width="30" height="25" fill="{skin_color}"/>
            <path d="M50,140 Q100,160 150,140 L160,180 L140,180 L140,280 L60,280 L60,180 L40,180 Z" fill="{color_hex}" stroke="#222" stroke-width="1"/>
            <path d="M40,180 L20,250" stroke="{skin_color}" stroke-width="15" stroke-linecap="round"/>
            <path d="M160,180 L180,250" stroke="{skin_color}" stroke-width="15" stroke-linecap="round"/>
            <path d="M60,280 L140,280 L135,400 L100,370 L65,400 Z" fill="#3A3A3A"/>
            <ellipse cx="65" cy="415" rx="20" ry="10" fill="{shoe_color}"/>
            <ellipse cx="135" cy="415" rx="20" ry="10" fill="{shoe_color}"/>
        </svg>
        """
    else:
        # Stylized Female Figure with Face, Hair, Dress, Shoes
        return f"""
        <svg width="200" height="450" viewBox="0 0 200 450" xmlns="http://www.w3.org/2000/svg">
            <path d="M60,50 Q100,10 140,50 L150,110 Q100,90 50,110 Z" fill="{hair_color}"/>
            <ellipse cx="100" cy="75" rx="32" ry="40" fill="{skin_color}"/>
            <circle cx="88" cy="72" r="2.5" fill="#333"/> <circle cx="112" cy="72" r="2.5" fill="#333"/>
            <path d="M92,95 Q100,100 108,95" stroke="#333" fill="none"/>
            <rect x="90" y="110" width="20" height="20" fill="{skin_color}"/>
            <path d="M65,130 Q100,150 135,130 L155,300 Q100,320 45,300 Z" fill="{color_hex}" stroke="#222" stroke-width="1"/>
            <path d="M65,130 L35,220" stroke="{skin_color}" stroke-width="12" stroke-linecap="round"/>
            <path d="M135,130 L165,220" stroke="{skin_color}" stroke-width="12" stroke-linecap="round"/>
            <path d="M85,300 L85,400 M115,300 L115,400" stroke="{skin_color}" stroke-width="14"/>
            <path d="M75,400 L95,400 L90,420 L75,415 Z" fill="{shoe_color}"/>
            <path d="M105,400 L125,400 L125,415 L110,420 Z" fill="{shoe_color}"/>
        </svg>
        """

# --- DYNAMIC HERO IMAGES ---
def get_hero_image(weather_condition):
    images = {
        "Rainy": "https://images.unsplash.com/photo-1534260164206-2a3a4a72891d?q=80&w=2070&auto=format&fit=crop",
        "Hot": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2073&auto=format&fit=crop",
        "Cold": "https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=2070&auto=format&fit=crop",
        "Moderate": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?q=80&w=2073&auto=format&fit=crop",
        "Default": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?q=80&w=2073&auto=format&fit=crop"
    }
    return images.get(weather_condition, images["Default"])

# --- CINEMATIC CSS ---
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Prata&display=swap');

* { font-family: 'Inter', sans-serif; }

/* APP BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0E0E0E 0%, #1A1A1A 100%);
}

/* HEADINGS */
h1, h2, h3 {
    font-family: 'Prata', serif !important;
    color: #F5D78B !important;
    letter-spacing: 1px;
}

/* SUBTEXT */
p, label, span, div {
    color: #EDEDED !important;
}

/* INPUT FIELDS */
.stTextInput>div>div>input,
.stSelectbox>div>div>div,
.stRadio label {
    background: rgba(255,255,255,0.03);
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #333;
    color: #fff !important;
    transition: 0.3s;
}

.stTextInput>div>div>input:focus,
.stSelectbox>div:hover,
.stRadio label:hover {
    border: 1px solid #F5D78B;
    box-shadow: 0 0 15px rgba(245, 215, 139, 0.4);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #ffdd95, #f4c56a);
    padding: 15px 25px;
    border-radius: 10px;
    border: none;
    color: #111;
    font-weight: 700;
    letter-spacing: 1px;
    transition: 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 30px rgba(255, 225, 160, 0.5);
}

/* GLASS CARD */
.glass-card {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 0 40px rgba(0,0,0,0.4);
    backdrop-filter: blur(12px);
}

/* HERO SECTION */
.hero-box {
    border-radius: 20px;
    overflow: hidden;
    height: 350px;
    position: relative;
    margin-bottom: 40px;
    box-shadow: 0 0 60px rgba(255,255,255,0.08);
}
.hero-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.45;
}
.hero-glass {
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 40px;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
}
.hero-title {
    font-size: 65px;
    font-family: 'Prata', serif;
    text-align: center;
    color: #fff;
}
.hero-sub {
    text-align: center;
    letter-spacing: 6px;
    color: #F5D78B;
    font-size: 13px;
}

/* WARDROBE CARD */
.wardrobe-card {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s ease;
    text-align: center;
}
.wardrobe-card:hover {
    transform: scale(1.05);
    border-color: #F5D78B;
    box-shadow: 0 0 25px rgba(245,215,139,0.3);
}

/* BUY LINK */
.buy-link {
    color: #F5D78B !important;
    padding: 6px 10px;
    border: 1px solid #F5D78B;
    font-size: 11px;
    border-radius: 6px;
    display: inline-block;
    margin-top: 8px;
    transition: 0.3s;
}
.buy-link:hover {
    background: #F5D78B;
    color: #000 !important;
}

/* MANNEQUIN BOX */
.mannequin-box {
    border-radius: 20px;
    padding: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.1);
    height: 520px;
    display: flex;
    align-items: center;
    justify-content: center;
}

</style>
""", unsafe_allow_html=True)


def split_outfit(outfit_str):
    parts = outfit_str.split('+')
    while len(parts) < 3: parts.append("Accessories")
    return [p.strip() for p in parts]

# --- APP LOGIC ---

if 'weather_cat' not in st.session_state:
    st.session_state['weather_cat'] = "Default"

current_hero = get_hero_image(st.session_state['weather_cat'])
st.markdown(f"""
    <div class="hero-box">
        <img src="{current_hero}" class="hero-img">
        <div class="hero-glass">
            <h1 class="hero-title">VOGUE AI</h1>
            <p class="hero-sub">The Intelligent Wardrobe Consultant</p>
        </div>
    </div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.8], gap="large")

with col_left:
    st.markdown("### 1. Style Profile")
    with st.container():
        # Gender selection is now crucial for the try-on
        gender = st.radio("Gender", ["Women", "Men"], horizontal=True)
        city = st.text_input("📍 City", "Paris")
        event = st.selectbox("📅 Occasion", ["Casual", "Office", "Party", "Gym", "Wedding"])
        
        c1, c2 = st.columns(2)
        with c1:
            skin_tone = st.selectbox("🎨 Skin Tone", ["Light", "Medium", "Dark"])
        with c2:
            undertone = st.selectbox("🌡 Undertone", ["Cool", "Warm"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("GENERATE LOOK"):
            if model:
                with st.spinner("Consulting Neural Stylist..."):
                    time.sleep(1.2)
                    
                    weather_cat, temp = get_weather(city)
                    st.session_state['weather_cat'] = weather_cat 
                    color_data = get_advanced_color_palette(skin_tone, undertone)
                    
                    try:
                        w_enc = safe_transform(le_weather, weather_cat, "Moderate")
                        e_enc = safe_transform(le_event, event, "Casual")
                        s_enc = safe_transform(le_skin, skin_tone, "Medium")
                        
                        pred = model.predict([[w_enc, e_enc, s_enc]])
                        outfit = le_outfit.inverse_transform(pred)[0]
                        
                        st.session_state['res'] = {
                            'outfit': outfit, 'w': weather_cat, 
                            't': temp, 'color_data': color_data,
                            'gender': gender # Store gender for the try-on
                        }
                    except Exception as e:
                        st.error(f"Error: {e}")

with col_right:
    if 'res' in st.session_state:
        res = st.session_state['res']
        c_data = res['color_data']
        
        # --- SPLIT LAYOUT FOR RESULTS ---
        r_col1, r_col2 = st.columns([1.5, 1])
        
        with r_col1:
            # OUTFIT & DETAILS
            st.markdown(f"""<div class="glass-card">""", unsafe_allow_html=True)
            st.markdown(f"""
                <span style="border: 1px solid #E5C07B; padding: 5px 15px; font-size: 10px; letter-spacing: 2px; color: #E5C07B;">AI CURATED</span>
                <h1 style="font-size: 38px; margin: 15px 0; color: #FFF;">{res['outfit']}</h1>
                <p style="color: #AAA;">{res['w']} • {res['t']}°C</p>
            """, unsafe_allow_html=True)
            
            parts = split_outfit(res['outfit'])
            cols = st.columns(3)
            icons = ["🧥", "👖", "👞"]
            
            for i, col in enumerate(cols):
                with col:
                    item = parts[i] if i < len(parts) else 'Accessory'
                    link = f"https://www.amazon.in/s?k={item.replace(' ', '+')}"
                    st.markdown(f"""
                    <div class="wardrobe-card">
                        <div style="font-size:24px;">{icons[i]}</div>
                        <div style="font-size:10px; font-weight:bold; color:#FFF; margin-top:5px;">{item}</div>
                        <a href="{link}" target="_blank" class="buy-link">Shop</a>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # COLOR PALETTE
            st.markdown(f"""<div class="glass-card">""", unsafe_allow_html=True)
            st.markdown(f"""<h3>Your {c_data['Season']} Palette</h3>""", unsafe_allow_html=True)
            
            # Interactive Color Selector
            st.write("👇 *Click a color to visualize:*")
            color_options = c_data['Power']
            # Use radio button for color selection
            selected_color_name = st.radio("Select Color", list(color_options.keys()), horizontal=True)
            selected_color_hex = color_options[selected_color_name]
            
            st.markdown("</div>", unsafe_allow_html=True)

        with r_col2:
            # VIRTUAL TRY-ON MANNEQUIN
            st.markdown(f"""<div class="glass-card" style="text-align:center;">""", unsafe_allow_html=True)
            st.markdown("<h4>VIRTUAL TRY-ON</h4>", unsafe_allow_html=True)
            
            # Generate the SVG based on GENDER and SELECTED COLOR
            svg_code = get_mannequin_svg(res['gender'], selected_color_hex)
            
            # Render SVG inside a styled box
            st.markdown(f'<div class="mannequin-box">{svg_code}</div>', unsafe_allow_html=True)
            st.caption(f"Visualizing: {selected_color_name} on {res['gender']}")
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
            <div style="text-align: center; padding: 50px; opacity: 0.5;">
                <h3 style="color: #444 !important;">Awaiting Input...</h3>
            </div>
        """, unsafe_allow_html=True)
        if lottie_hanger:
            st_lottie(lottie_hanger, height=200)

with st.expander("Show Neural Network Logic"):
    if model:
        fig, ax = plt.subplots(figsize=(25, 12))
        fig.patch.set_facecolor('#FFFFFF') 
        ax.set_facecolor('#FFFFFF')
        tree.plot_tree(model, feature_names=["Weather", "Event", "Skin"], class_names=le_outfit.classes_, filled=True, rounded=True, fontsize=10, precision=0, ax=ax)
        st.pyplot(fig)