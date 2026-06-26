import streamlit as st
import streamlit.components.v1 as components
import json
import os
import base64

st.set_page_config(
    page_title="Undangan Pernikahan Intan & Syahrial",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def load_photos():
    path = os.path.join(os.path.dirname(__file__), "photos.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

photos = load_photos()

if "wishes" not in st.session_state:
    st.session_state.wishes = [
        {"name": "Keluarga Besar", "text": "Semoga menjadi keluarga yang Sakinah, Mawaddah, Warahmah. Aamiin Ya Rabbal Alamin.", "time": "Baru saja"}
    ]

# Cari file MP3
music_file = os.path.join(os.path.dirname(__file__), "janji_suci_short.mp3")
music_exists = os.path.exists(music_file)

audio_b64 = ""
if music_exists:
    with open(music_file, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()

# ══════════════════════════════════════════════════════════════
#  STYLE — LUXURY GOLD & MIDNIGHT THEME
#  (FIX KECEPATAN: preconnect ke font, hanya load weight yang
#   benar2 dipakai, font-display:swap supaya teks tidak
#   "menunggu" font sebelum tampil)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Playfair+Display:wght@600;700;800&family=Tangerine:wght@700&display=swap&font-display=swap" rel="stylesheet">

<style>
* { margin:0; padding:0; box-sizing:border-box; }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 90% 50% at 50% -10%, rgba(201,168,76,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 70% 40% at 50% 110%, rgba(120,60,30,0.12) 0%, transparent 60%),
        linear-gradient(180deg, #0a0705 0%, #100c08 45%, #0a0705 100%) !important;
    min-height: 100vh;
}
[data-testid="stHeader"], [data-testid="stToolbar"], .stDeployButton,
section[data-testid="stSidebar"], #MainMenu, footer, header { display:none !important; visibility:hidden !important; }

[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 580px !important;
    margin: 0 auto !important;
}

body, .stMarkdown, p, div {
    font-family: 'Cormorant Garamond', serif !important;
    color: #e8d5b7 !important;
}

@keyframes fadeUp { from { opacity:0; transform:translateY(14px);} to {opacity:1; transform:translateY(0);} }
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-6px);} }

#texture-overlay {
    position: fixed; inset:0; pointer-events:none; z-index:0;
    background-image:
        repeating-linear-gradient(45deg, rgba(201,168,76,0.012) 0px, rgba(201,168,76,0.012) 1px, transparent 1px, transparent 26px),
        radial-gradient(ellipse 80% 35% at 50% 0%, rgba(201,168,76,0.07) 0%, transparent 70%),
        radial-gradient(ellipse 60% 30% at 50% 100%, rgba(140,70,40,0.08) 0%, transparent 70%);
}
#vignette {
    position: fixed; inset:0; pointer-events:none; z-index:0;
    box-shadow: inset 0 0 160px 60px rgba(0,0,0,0.55);
}
.gold-frame-edge {
    position: fixed; inset: 10px; pointer-events:none; z-index:1;
    border: 1px solid rgba(201,168,76,0.18);
}

/* ── HERO ── */
.inv-hero { text-align:center; padding:60px 28px 30px; position:relative; z-index:1; animation: fadeUp 1.2s ease; }
.inv-bismillah {
    font-size: 25px; letter-spacing: 3px;
    background: linear-gradient(100deg, #8a6a2e 0%, #f3d98a 25%, #c9a84c 50%, #f3d98a 75%, #8a6a2e 100%);
    background-size: 250% auto;
    -webkit-background-clip: text; background-clip:text; -webkit-text-fill-color: transparent;
    animation: shimmer 6s linear infinite;
    margin-bottom: 12px;
}
.inv-salam { font-size: 11px; letter-spacing: 2.5px; color:#c9a84c; opacity:0.55; text-transform: uppercase; font-style: italic; }
.inv-ornament { color:#c9a84c; opacity:0.3; font-size:13px; letter-spacing:8px; margin:18px 0; }
.flourish { display:block; width:100%; max-width:220px; margin:14px auto; opacity:0.55; }

/* ── PHOTO FRAME ── */
.inv-frame-wrap { position:relative; width:230px; margin:0 auto 22px; animation: fadeUp 1.4s ease; }
.inv-frame-wrap::before {
    content:''; position:absolute; inset:-10px; border:1px solid rgba(201,168,76,0.25); pointer-events:none;
}
.inv-frame-wrap img {
    width:100%; height:300px; object-fit:cover; display:block;
    border: 2px solid rgba(201,168,76,0.55);
    box-shadow: 0 18px 50px rgba(0,0,0,0.6), 0 0 0 6px rgba(10,7,5,0.9);
    filter: sepia(0.12) brightness(0.97) contrast(1.03);
}
.inv-frame-corner { position:absolute; width:24px; height:24px; border-color: rgba(201,168,76,0.75); border-style:solid; }
.ifc-tl{ top:-12px; left:-12px; border-width:1px 0 0 1px;} .ifc-tr{ top:-12px; right:-12px; border-width:1px 1px 0 0;}
.ifc-bl{ bottom:-12px; left:-12px; border-width:0 0 1px 1px;} .ifc-br{ bottom:-12px; right:-12px; border-width:0 1px 1px 0;}

.inv-gallery { display:flex; gap:7px; justify-content:center; margin:0 22px 34px; }
.inv-gallery img {
    flex:1; height:115px; object-fit:cover;
    border: 1px solid rgba(201,168,76,0.3);
    box-shadow: 0 8px 22px rgba(0,0,0,0.45);
    filter: sepia(0.1) brightness(0.95);
    transition: transform .35s ease, border-color .35s ease;
}
.inv-gallery img:hover { transform: translateY(-4px); border-color: rgba(201,168,76,0.65); }

/* ── COUPLE NAME ── */
.inv-couple-wrap { text-align:center; padding:0 28px 10px; position:relative; z-index:1; }
.inv-tag { font-size:9.5px; letter-spacing:5px; text-transform:uppercase; color:#c9a84c; opacity:0.55; margin-bottom:14px; display:block; }
.inv-name {
    font-family:'Playfair Display', serif !important; font-size:56px !important; font-weight:700 !important;
    background: linear-gradient(95deg, #9c7a35 0%, #f6e3a3 30%, #c9a84c 55%, #f6e3a3 75%, #9c7a35 100%);
    background-size: 250% auto;
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
    animation: shimmer 7s linear infinite;
    line-height:1.08; letter-spacing:1px;
}
.inv-amp { display:block; font-family:'Tangerine', cursive !important; font-size:46px !important; font-style:normal !important; color:rgba(201,168,76,0.55) !important; letter-spacing:2px; margin:0; }
.inv-date-tag { font-size:10.5px; letter-spacing:4px; color:#c9a84c; opacity:0.45; text-transform:uppercase; margin-top:16px; }

/* ── DIVIDER ── */
.inv-divider { display:flex; align-items:center; gap:12px; margin:30px auto; max-width:320px; padding:0 28px; position:relative; z-index:1; }
.inv-divider-line { flex:1; height:1px; background: linear-gradient(to right, transparent, rgba(201,168,76,0.45), transparent); }
.inv-divider-mark { width:6px; height:6px; border:1px solid rgba(201,168,76,0.6); transform:rotate(45deg); flex-shrink:0; }

/* ── CARD ── */
.inv-card {
    margin:0 22px 18px; padding:32px 26px;
    background: linear-gradient(180deg, rgba(201,168,76,0.035), rgba(201,168,76,0.01));
    border: 1px solid rgba(201,168,76,0.18);
    box-shadow: 0 12px 36px rgba(0,0,0,0.35), inset 0 0 30px rgba(201,168,76,0.02);
    position:relative; z-index:1;
}
.inv-card::before, .inv-card::after { content:''; position:absolute; width:14px; height:14px; border-color:rgba(201,168,76,0.55); border-style:solid; }
.inv-card::before { top:-1px; left:-1px; border-width:2px 0 0 2px; }
.inv-card::after  { bottom:-1px; right:-1px; border-width:0 2px 2px 0; }
.inv-card-label { font-size:9.5px; letter-spacing:4px; text-transform:uppercase; color:#c9a84c; opacity:0.55; text-align:center; margin-bottom:18px; }
.inv-body { font-size:14px; line-height:2.3; text-align:center; color:#ddc9a8 !important; opacity:0.9; }

/* ── MEMPELAI ── */
.inv-mempelai-name { font-family:'Playfair Display', serif !important; font-size:28px !important; font-weight:600 !important; color:#e3c873 !important; text-align:center; display:block; letter-spacing:1px; }
.inv-mempelai-sub { font-size:12.5px; color:#c9a84c; opacity:0.55; font-style:italic; text-align:center; margin-top:6px; }
.inv-sep-amp { text-align:center; margin:10px 0; font-family:'Tangerine', cursive; font-size:34px; color:rgba(201,168,76,0.4); letter-spacing:2px; position:relative; z-index:1; }

/* ── EVENTS ── */
.inv-events { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:0 22px 18px; position:relative; z-index:1; }
.inv-event {
    border:1px solid rgba(201,168,76,0.22); padding:26px 12px; text-align:center;
    background: linear-gradient(180deg, rgba(201,168,76,0.04), transparent);
    box-shadow: 0 10px 28px rgba(0,0,0,0.3);
}
.ev-lbl { font-size:8.5px; letter-spacing:3px; color:#c9a84c; opacity:0.55; text-transform:uppercase; margin-bottom:16px; }
.ev-num { font-family:'Playfair Display', serif !important; font-size:56px !important; font-weight:700 !important; color:#e3c873 !important; line-height:1; text-shadow: 0 0 18px rgba(201,168,76,0.25); }
.ev-my { font-size:9.5px; letter-spacing:2px; color:#c9a84c; opacity:0.5; text-transform:uppercase; margin:6px 0 12px; }
.ev-tm { font-size:12.5px; color:#ddc9a8; opacity:0.7; margin-bottom:8px; }
.ev-loc { font-size:11.5px; color:#c9a84c; opacity:0.55; line-height:1.8; font-style:italic; }

/* ── COUNTDOWN ── */
.inv-countdown {
    margin:0 22px 18px; padding:34px 18px;
    border:1px solid rgba(201,168,76,0.22);
    background: radial-gradient(ellipse 100% 100% at 50% 0%, rgba(201,168,76,0.05), transparent);
    text-align:center; position:relative; z-index:1;
    box-shadow: 0 12px 36px rgba(0,0,0,0.35);
}
.inv-countdown::before { content:''; position:absolute; inset:6px; border:1px solid rgba(201,168,76,0.12); pointer-events:none; }
.cd-row { display:flex; justify-content:center; align-items:flex-start; gap:10px; margin-top:20px; }
.cd-unit-wrap { text-align:center; min-width:58px; }
.cd-num {
    font-family:'Playfair Display', serif !important; font-size:48px !important; font-weight:700 !important;
    color:#e3c873 !important; display:block; line-height:1; letter-spacing:-1px;
    text-shadow: 0 0 20px rgba(201,168,76,0.3);
}
.cd-lbl { font-size:8.5px; letter-spacing:2px; text-transform:uppercase; color:#c9a84c; opacity:0.45; margin-top:8px; }
.cd-colon { font-family:'Playfair Display', serif; font-size:36px; color:rgba(201,168,76,0.3); line-height:1; padding-top:6px; flex-shrink:0; }

/* ── LOCATION ── */
.inv-map-btn {
    display:inline-block; padding:13px 38px; border:1px solid rgba(201,168,76,0.45);
    color:#e3c873 !important; font-family:'Cormorant Garamond', serif; font-size:11px; letter-spacing:4px;
    text-transform:uppercase; text-decoration:none !important; background: rgba(201,168,76,0.04);
    transition:all .35s; margin-top:18px;
}
.inv-map-btn:hover { background: rgba(201,168,76,0.12); border-color:#e3c873; box-shadow: 0 0 24px rgba(201,168,76,0.2); }

/* ── WISHES ── */
.wish-item { padding:16px 0; border-bottom:1px solid rgba(201,168,76,0.08); }
.wish-author { font-size:12.5px; color:#e3c873; opacity:0.8; font-weight:600; margin-bottom:6px; letter-spacing:0.5px; }
.wish-text { font-size:13.5px; color:#ddc9a8; opacity:0.75; font-style:italic; line-height:1.9; }
.wish-ts { font-size:9px; color:#c9a84c; opacity:0.3; margin-top:6px; letter-spacing:1px; }

/* ── FOOTER ── */
.inv-footer { text-align:center; padding:40px 28px 70px; border-top:1px solid rgba(201,168,76,0.1); position:relative; z-index:1; }
.inv-footer-names { font-family:'Playfair Display', serif !important; font-size:30px !important; font-weight:600 !important; color:rgba(201,168,76,0.8) !important; letter-spacing:2px; margin-bottom:10px; }
.inv-footer-sub { font-size:9.5px; letter-spacing:4px; color:#c9a84c; opacity:0.35; text-transform:uppercase; }
.inv-wassalam { font-size:11.5px; color:#c9a84c; opacity:0.3; font-style:italic; margin-top:18px; }

/* ── COVER / OPENING SCREEN ── */
#inv-cover {
    position:fixed; inset:0; z-index:99999;
    display:flex; align-items:center; justify-content:center;
    background:
        radial-gradient(ellipse 90% 60% at 50% 0%, rgba(201,168,76,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 70% 50% at 50% 100%, rgba(120,60,30,0.14) 0%, transparent 60%),
        linear-gradient(180deg, #0a0705 0%, #100c08 45%, #0a0705 100%);
    transition: opacity .2s ease, visibility .2s ease;
    will-change: opacity;
}
#inv-cover.cover-hidden { opacity:0; visibility:hidden; pointer-events:none; }
.cover-inner { text-align:center; padding:30px; max-width:380px; }
.cover-frame {
    border:1px solid rgba(201,168,76,0.35); padding:46px 30px; position:relative;
    background: linear-gradient(180deg, rgba(201,168,76,0.04), rgba(201,168,76,0.01));
    box-shadow: 0 20px 60px rgba(0,0,0,0.55);
}
.cover-frame::before, .cover-frame::after { content:''; position:absolute; width:22px; height:22px; border-color: rgba(201,168,76,0.65); border-style:solid; }
.cover-frame::before { top:-1px; left:-1px; border-width:2px 0 0 2px; }
.cover-frame::after  { bottom:-1px; right:-1px; border-width:0 2px 2px 0; }
.cover-kicker { font-size:10px; letter-spacing:5px; text-transform:uppercase; color:#c9a84c; opacity:0.6; margin-bottom:22px; }
.cover-names {
    font-family:'Playfair Display', serif !important; font-size:42px !important; font-weight:700 !important;
    background: linear-gradient(95deg, #9c7a35 0%, #f6e3a3 30%, #c9a84c 55%, #f6e3a3 75%, #9c7a35 100%);
    background-size: 250% auto; -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
    animation: shimmer 7s linear infinite; line-height:1.15;
}
.cover-amp { display:block; font-family:'Tangerine', cursive !important; font-size:30px !important; color:rgba(201,168,76,0.55) !important; margin:4px 0; }
.cover-date { font-size:11px; letter-spacing:3px; color:#c9a84c; opacity:0.5; text-transform:uppercase; margin:18px 0 30px; }
.cover-divider { width:60px; height:1px; background:rgba(201,168,76,0.4); margin:0 auto 28px; }
#cover-open-btn {
    display:inline-flex; align-items:center; gap:10px; padding:14px 36px; border:1px solid rgba(201,168,76,0.55);
    color:#e3c873; font-family:'Cormorant Garamond', serif; font-size:12px; letter-spacing:4px; text-transform:uppercase;
    background: rgba(201,168,76,0.06); cursor:pointer; transition: all .35s;
}
#cover-open-btn:hover { background: rgba(201,168,76,0.16); border-color:#e3c873; box-shadow:0 0 30px rgba(201,168,76,0.25); }
#cover-open-btn .env-ico { animation: float 2.4s ease-in-out infinite; font-size:14px; }

/* ── SCROLL REVEAL ── */
.reveal { opacity:0; transform: translateY(22px); transition: opacity .8s ease, transform .8s ease; }
.reveal.visible { opacity:1; transform: translateY(0); }

/* ── MUSIC BTN (rendered by component, positioned via fixed CSS) ── */
#music-btn {
    position:fixed; bottom:28px; right:28px; width:50px; height:50px; border-radius:50%;
    background: radial-gradient(circle at 35% 30%, rgba(40,30,15,0.95), rgba(10,7,5,0.97));
    border:1px solid rgba(201,168,76,0.55); color:#e3c873; font-size:18px; cursor:pointer; z-index:9999;
    display:flex; align-items:center; justify-content:center; box-shadow:0 4px 24px rgba(0,0,0,0.6);
    transition:all .3s ease; font-family:serif;
}
#music-btn:hover { border-color:#e3c873; box-shadow:0 0 24px rgba(201,168,76,0.35); }
#music-btn.playing { animation: ring 3s ease-in-out infinite; }
@keyframes ring {
    0%,100% { box-shadow:0 4px 24px rgba(0,0,0,0.6), 0 0 0 0 rgba(201,168,76,0.2); }
    50%     { box-shadow:0 4px 24px rgba(0,0,0,0.6), 0 0 0 10px rgba(201,168,76,0); }
}
#music-label {
    position:fixed; bottom:86px; right:18px; background: rgba(10,7,5,0.96);
    border:1px solid rgba(201,168,76,0.35); color:#e3c873; font-family:'Cormorant Garamond', serif;
    font-size:10.5px; letter-spacing:1.5px; padding:6px 16px; z-index:9999; pointer-events:none;
    opacity:0; transition:opacity .4s; white-space:nowrap;
}
#music-label.show { opacity:1; }

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
    background: linear-gradient(180deg, rgba(201,168,76,0.08), rgba(201,168,76,0.02)) !important;
    border:1px solid rgba(201,168,76,0.45) !important; color:#e3c873 !important;
    font-family:'Cormorant Garamond', serif !important; font-size:11px !important; letter-spacing:4px !important;
    text-transform:uppercase !important; padding:12px 24px !important; border-radius:0 !important; width:100%;
    transition: all .3s;
}
.stButton > button:hover { background: rgba(201,168,76,0.14) !important; border-color:#e3c873 !important; box-shadow: 0 0 20px rgba(201,168,76,0.2); }
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.02) !important; border:1px solid rgba(201,168,76,0.22) !important;
    border-radius:0 !important; color:#e8d5b7 !important; font-family:'Cormorant Garamond', serif !important; font-size:14px !important;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: rgba(201,168,76,0.55) !important; box-shadow:none !important; }
.stTextInput label, .stTextArea label, .stRadio label {
    color:#c9a84c !important; font-family:'Cormorant Garamond', serif !important; font-size:10px !important;
    letter-spacing:3px !important; text-transform:uppercase !important; opacity:0.55 !important;
}
.stRadio > div > label {
    color:#c9a84c !important; font-size:13px !important; letter-spacing:1px !important; text-transform:none !important;
    background:transparent !important; border:1px solid rgba(201,168,76,0.22) !important; padding:8px 18px !important; border-radius:0 !important;
}
.stTabs [data-baseweb="tab-list"] { background:transparent !important; gap:4px; }
.stTabs [data-baseweb="tab"] {
    background:transparent !important; border:1px solid rgba(201,168,76,0.22) !important; color:#c9a84c !important;
    font-family:'Cormorant Garamond', serif !important; font-size:11px !important; letter-spacing:2px !important;
    text-transform:uppercase !important; border-radius:0 !important;
}
.stTabs [aria-selected="true"] { border-color: rgba(201,168,76,0.55) !important; background: rgba(201,168,76,0.06) !important; }
.stSuccess, .stInfo, .stWarning { background: rgba(20,14,8,0.85) !important; border:1px solid rgba(201,168,76,0.3) !important; border-radius:0 !important; color:#e3c873 !important; }
hr { border-color: rgba(201,168,76,0.1) !important; }
</style>

<div id="texture-overlay"></div>
<div id="vignette"></div>
<div class="gold-frame-edge"></div>

<div id="inv-cover">
    <div class="cover-inner">
        <div class="cover-frame">
            <div class="cover-kicker">✦ The Wedding Of ✦</div>
            <div class="cover-names">Intan</div>
            <div class="cover-amp">&amp;</div>
            <div class="cover-names">Syahrial</div>
            <div class="cover-date">19 Juli 2026 &nbsp;·&nbsp; Namo Bintang</div>
            <div class="cover-divider"></div>
            <button id="cover-open-btn"><span class="env-ico">✉</span> Buka Undangan</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Audio element (lives in MAIN document so the component below can find it) ──
if audio_b64:
    st.markdown(f"""<audio id="bg-audio" loop preload="auto">
        <source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg"></audio>""", unsafe_allow_html=True)
else:
    st.markdown("""<audio id="bg-audio" loop preload="auto">
        <source src="https://ia800905.us.archive.org/19/items/FREE_background_music_dac/07_-_Music_Box.mp3" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-hero">
    <div class="inv-bismillah">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
    <div class="inv-ornament">— ✦ —</div>
    <div class="inv-salam">Assalamu'alaikum Warahmatullahi Wabarakatuh</div>
</div>
""", unsafe_allow_html=True)

if photos.get("foto1"):
    st.markdown(f"""
    <div style="padding:0 24px;margin-bottom:14px;position:relative;z-index:1">
        <div class="inv-frame-wrap">
            <div class="inv-frame-corner ifc-tl"></div>
            <div class="inv-frame-corner ifc-tr"></div>
            <div class="inv-frame-corner ifc-bl"></div>
            <div class="inv-frame-corner ifc-br"></div>
            <img src="data:image/png;base64,{photos['foto1']}" alt="Foto Mempelai" loading="eager"/>
        </div>
    </div>""", unsafe_allow_html=True)

if photos.get("foto2") and photos.get("foto3"):
    st.markdown(f"""
    <div class="inv-gallery">
        <img src="data:image/png;base64,{photos['foto1']}" alt="" loading="lazy"/>
        <img src="data:image/png;base64,{photos['foto2']}" alt="" loading="lazy"/>
        <img src="data:image/png;base64,{photos['foto3']}" alt="" loading="lazy"/>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="inv-couple-wrap">
    <span class="inv-tag">✦ Undangan Pernikahan ✦</span>
    <div class="inv-name">Intan</div>
    <div class="inv-amp">&amp;</div>
    <div class="inv-name">Syahrial</div>
    <div class="inv-date-tag">19 · Juli · 2026 &nbsp;·&nbsp; Desa Namo Bintang</div>
</div>
""", unsafe_allow_html=True)

def divider():
    st.markdown("""
    <div class="inv-divider" style="position:relative;z-index:1">
        <div class="inv-divider-line"></div>
        <div class="inv-divider-mark"></div>
        <div class="inv-divider-line"></div>
    </div>""", unsafe_allow_html=True)

divider()

st.markdown("""
<div class="inv-card">
    <div class="inv-card-label">— Dengan Rahmat Allah Subhanahu Wa Ta'ala —</div>
    <p class="inv-body">
        Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan.<br><br>
        Dengan memohon Ridha dan Rahmat-Nya, kami bermaksud menyelenggarakan
        pernikahan putra-putri kami. Maka dengan segala kerendahan hati,
        kami mengundang Bapak / Ibu / Saudara/i untuk hadir memberikan do'a restu.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="inv-card">
    <div class="inv-card-label">— Mempelai Wanita —</div>
    <span class="inv-mempelai-name">Intan Candra Nurul Hafizah</span>
    <div class="inv-mempelai-sub">Putri dari Alm. Bapak Fadli &amp; Ibu Sri Sumarti (Wiwik)</div>
</div>
<div class="inv-sep-amp">&amp;</div>
<div class="inv-card" style="margin-top:0">
    <div class="inv-card-label">— Mempelai Pria —</div>
    <span class="inv-mempelai-name">Syahrial</span>
    <div class="inv-mempelai-sub">Putra dari Alm. Bapak Paimo &amp; Ibu Suriani</div>
</div>
""", unsafe_allow_html=True)

divider()

st.markdown("""
<div class="inv-events">
    <div class="inv-event">
        <div class="ev-lbl">Akad Nikah</div>
        <div class="ev-num">17</div>
        <div class="ev-my">Juli · 2026</div>
        <div class="ev-tm">Jum'at · 08.00 WIB</div>
        <div class="ev-loc">Dusun II Sumberingin<br>Desa Namo Bintang</div>
    </div>
    <div class="inv-event">
        <div class="ev-lbl">Resepsi</div>
        <div class="ev-num">19</div>
        <div class="ev-my">Juli · 2026</div>
        <div class="ev-tm">Minggu · 10.00 WIB</div>
        <div class="ev-loc">Dusun II Sumberingin<br>Desa Namo Bintang</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  COUNTDOWN — the visible block (in main doc)
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-countdown">
    <div class="inv-card-label">— Menghitung Hari Menuju Hari Bahagia —</div>
    <div class="cd-row">
        <div class="cd-unit-wrap"><span class="cd-num" id="inv-cd-d">--</span><div class="cd-lbl">Hari</div></div>
        <div class="cd-colon">:</div>
        <div class="cd-unit-wrap"><span class="cd-num" id="inv-cd-h">--</span><div class="cd-lbl">Jam</div></div>
        <div class="cd-colon">:</div>
        <div class="cd-unit-wrap"><span class="cd-num" id="inv-cd-m">--</span><div class="cd-lbl">Menit</div></div>
        <div class="cd-colon">:</div>
        <div class="cd-unit-wrap"><span class="cd-num" id="inv-cd-s">--</span><div class="cd-lbl">Detik</div></div>
    </div>
</div>
<div id="music-label">♫ Janji Suci — Yovie &amp; Nuno</div>
<button id="music-btn" title="Musik">♫</button>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FIX MUSIK (final): Browser modern TIDAK akan mengizinkan audio
#  berbunyi otomatis tanpa interaksi user — trik mute/unmute pun
#  akan diblokir lagi. Solusi yang benar2 reliable: layar
#  "Buka Undangan" di atas. Begitu tombol itu ditekan, itu adalah
#  gesture asli dari user → browser pasti mengizinkan audio.play()
#  dijalankan tepat di event click tersebut. Jadi musik dan
#  tampilan undangan terbuka BERSAMAAN, tanpa delay.
#
#  Tambahan: animasi scroll-reveal supaya tiap bagian undangan
#  muncul dengan fade-up halus saat di-scroll (efek lebih mewah).
# ══════════════════════════════════════════════════════════════
components.html("""
<script>
(function() {
    var doc = window.parent.document;

    /* ── COUNTDOWN ── */
    var target = new Date('2026-07-19T10:00:00+07:00').getTime();
    function pad(n){ return n < 10 ? '0'+n : ''+n; }
    function tickCountdown() {
        var elD = doc.getElementById('inv-cd-d');
        if (!elD) { return; }
        var diff = Math.max(0, target - Date.now());
        doc.getElementById('inv-cd-d').textContent = pad(Math.floor(diff/86400000));
        doc.getElementById('inv-cd-h').textContent = pad(Math.floor((diff%86400000)/3600000));
        doc.getElementById('inv-cd-m').textContent = pad(Math.floor((diff%3600000)/60000));
        doc.getElementById('inv-cd-s').textContent = pad(Math.floor((diff%60000)/1000));
    }
    setInterval(tickCountdown, 1000);
    tickCountdown();

    if (window.parent.__invInit) { return; }
    window.parent.__invInit = true;

    /* Cover bersifat fixed full-screen, jadi tidak perlu mengunci
       overflow body — menghindari reflow halaman penuh saat dibuka */

    function setupAll() {
        var audio = doc.getElementById('bg-audio');
        var btn   = doc.getElementById('music-btn');
        var label = doc.getElementById('music-label');
        var cover = doc.getElementById('inv-cover');
        var openBtn = doc.getElementById('cover-open-btn');
        if (!audio || !btn || !label || !cover || !openBtn) { setTimeout(setupAll, 100); return; }

        var playing = false, labelTO = null;
        function showLabel(txt) {
            label.textContent = txt;
            label.classList.add('show');
            clearTimeout(labelTO);
            labelTO = setTimeout(function(){ label.classList.remove('show'); }, 3000);
        }
        function markPlaying() {
            playing = true;
            btn.textContent = '♫';
            btn.classList.add('playing');
            showLabel('♫ Janji Suci — Yovie & Nuno');
        }
        function markPaused() {
            playing = false;
            btn.textContent = '♪';
            btn.classList.remove('playing');
        }

        /* ── OPEN INVITATION: real user gesture -> audio is allowed ──
           PENTING: cover HARUS hilang dulu apapun yang terjadi,
           baru audio dicoba diputar terpisah (try/catch) supaya
           kalau musik error, tombol tetap berfungsi membuka
           undangan. */
        function openInvitation() {
            cover.classList.add('cover-hidden');
            /* tunda proses audio ke tick berikutnya supaya animasi
               cover sempat mulai render duluan, tidak nunggu decode audio */
            setTimeout(function() {
                try {
                    audio.muted = false;
                    audio.volume = 0.65;
                    var p = audio.play();
                    if (p && p.then) { p.then(markPlaying).catch(markPaused); }
                    else { markPlaying(); }
                } catch (err) {
                    markPaused();
                }
            }, 0);
        }
        openBtn.addEventListener('click', openInvitation);
        openBtn.addEventListener('touchend', function(e){ e.preventDefault(); openInvitation(); });

        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (playing) {
                audio.pause();
                markPaused();
                showLabel('⏸ Musik dijeda');
            } else {
                audio.play().then(markPlaying).catch(function(){});
            }
        });

        /* ── SCROLL REVEAL ── */
        var revealSelectors = '.inv-card, .inv-events, .inv-countdown, .inv-footer, .wish-item, .inv-couple-wrap, .inv-hero, .inv-frame-wrap, .inv-gallery';
        var revealEls = doc.querySelectorAll(revealSelectors);
        revealEls.forEach(function(el){ el.classList.add('reveal'); });

        var observer = new (window.parent.IntersectionObserver)(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });
        revealEls.forEach(function(el){ observer.observe(el); });

        /* Elemen yang sudah terlihat duluan (hero) langsung ditandai visible */
        setTimeout(function(){
            var hero = doc.querySelector('.inv-hero');
            if (hero) hero.classList.add('visible');
        }, 50);
    }
    setupAll();
})();
</script>
""", height=0)

# ══════════════════════════════════════════════════════════════
#  LOKASI
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-card" style="text-align:center;margin-top:4px">
    <div class="inv-card-label">— Lokasi Acara —</div>
    <div style="font-family:'Playfair Display',serif;font-size:19px;color:#e3c873;letter-spacing:1px;margin:8px 0 6px">
        Dusun II Sumberingin
    </div>
    <div style="font-size:12.5px;color:#ddc9a8;opacity:0.65;font-style:italic;line-height:2">
        Desa Namo Bintang<br>Minggu, 19 Juli 2026 &nbsp;·&nbsp; Pukul 10.00 WIB
    </div>
    <div style="margin-top:20px">
        <a class="inv-map-btn" href="https://maps.app.goo.gl/8G9hHHY9LzdGg5yc6" target="_blank">Buka Google Maps</a>
    </div>
</div>
""", unsafe_allow_html=True)

divider()

st.markdown("""
<div style="text-align:center;margin:0 24px 4px;position:relative;z-index:1">
    <div style="font-size:9.5px;letter-spacing:4px;text-transform:uppercase;color:#c9a84c;opacity:0.45;margin-bottom:10px">
        Serta Turut Mengundang Acara Khitanan
    </div>
    <div style="font-family:'Playfair Display',serif;font-size:23px;color:#e3c873;opacity:0.85;letter-spacing:1px">
        Ahmad Hanafi
    </div>
</div>
""", unsafe_allow_html=True)

divider()

st.markdown("""
<div class="inv-card"><div class="inv-card-label">— Turut Mengundang —</div></div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Pihak Wanita", "Pihak Pria"])

def list_html(items):
    rows = "".join([
        f'<li style="font-size:13px;color:#ddc9a8;opacity:0.7;padding:9px 0;border-bottom:1px solid rgba(201,168,76,0.08);line-height:1.6">{i}</li>'
        for i in items
    ])
    return f'<ul style="list-style:none;padding:4px 0 0">{rows}</ul>'

with tab1:
    wanita = [
        "Alm. Mandah / Ngatiyem — Kakek & Nenek",
        "Muri / Anik — Kakek & Nenek", "Dasem — Nenek",
        "Sukar / Iyet — Kakek & Nenek", "Ribut / Ngatisah — Kakek & Nenek",
        "Alm. Jarno / Muriatik — Kakek & Nenek", "Sawon — Kakek", "Karlan — Kakek",
        "Watik / Misjo — Wawak", "Gambreng / Tumik — Pakde & Bude",
        "Endang Susanti / Ust. Lukman S.Pd.I — Bibik & Oom",
        "Sri Wulan Handayani / Hendrik — Bibik & Oom",
        "Ema — Adik", "Ahmad Hanafi — Adik",
    ]
    st.markdown(list_html(wanita), unsafe_allow_html=True)

with tab2:
    pria = [
        "Marinem / Suparto — Nenek & Kakek",
        "Ngatiyem / Alm. Joni — Nenek & Kakek",
        "Alm. Paiko / Iyus — Wawak",
        "Dedi / Rika — Abang", "Yuda / Wulan — Abang",
        "Diki / Dina — Adik", "Igo Ardiansyah — Adik",
        "Sugik / Yanti — Lelek", "Minok / Susi — Lelek",
        "Rame / Santo — Bibik", "Yuni / Junedi — Bibik",
    ]
    st.markdown(list_html(pria), unsafe_allow_html=True)

divider()

st.markdown("""
<div class="inv-card">
    <div class="inv-card-label">— Konfirmasi Kehadiran —</div>
    <p class="inv-body" style="font-size:12.5px;margin-bottom:0">
        Merupakan suatu kehormatan apabila Bapak / Ibu / Saudara/i
        berkenan hadir memberikan do'a restu.
    </p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding:0 24px 20px">', unsafe_allow_html=True)
    rsvp_name   = st.text_input("", placeholder="Nama Anda", key="rsvp_name", label_visibility="collapsed")
    rsvp_status = st.radio("", ["Hadir", "Tidak Hadir"], horizontal=True, key="rsvp_status", label_visibility="collapsed")
    if st.button("Kirim Konfirmasi", key="submit_rsvp"):
        if rsvp_name.strip():
            if rsvp_status == "Hadir":
                st.success(f"Terima kasih, {rsvp_name}. Kami menantikan kehadiran Anda.")
            else:
                st.info(f"Terima kasih, {rsvp_name}. Semoga selalu dalam lindungan Allah.")
        else:
            st.warning("Mohon isi nama Anda terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="inv-card" style="margin-top:8px"><div class="inv-card-label">— Do'a &amp; Ucapan —</div></div>
""", unsafe_allow_html=True)

for w in st.session_state.wishes:
    st.markdown(f"""
    <div class="wish-item" style="padding:14px 24px">
        <div class="wish-author">{w['name']}</div>
        <div class="wish-text">{w['text']}</div>
        <div class="wish-ts">{w['time']}</div>
    </div>""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding:12px 24px 20px">', unsafe_allow_html=True)
    wish_name = st.text_input("", placeholder="Nama Anda", key="wish_name", label_visibility="collapsed")
    wish_text = st.text_area("", placeholder="Tulis do'a dan ucapan untuk kedua mempelai...", key="wish_text", label_visibility="collapsed", height=100)
    if st.button("Kirim Ucapan", key="submit_wish"):
        if wish_name.strip() and wish_text.strip():
            st.session_state.wishes.insert(0, {"name": wish_name.strip(), "text": wish_text.strip(), "time": "Baru saja"})
            st.rerun()
        else:
            st.warning("Mohon isi nama dan ucapan Anda.")
    st.markdown('</div>', unsafe_allow_html=True)

divider()

st.markdown("""
<div class="inv-card">
    <div class="inv-card-label">— QS. Ar-Rum: 21 —</div>
    <p class="inv-body" style="font-style:italic">
        "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu
        istri-istri dari jenismu sendiri, supaya kamu cenderung dan merasa tenteram
        kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang."
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="inv-footer">
    <div class="inv-ornament" style="margin-bottom:20px;font-size:11px;letter-spacing:12px">✦ ✦ ✦</div>
    <div class="inv-footer-names">Intan &amp; Syahrial</div>
    <div class="inv-footer-sub" style="margin-top:6px">19 Juli 2026 &nbsp;·&nbsp; Namo Bintang</div>
    <div style="margin-top:20px;font-size:11.5px;color:#c9a84c;opacity:0.3;font-style:italic">
        Wassalamu'alaikum Warahmatullahi Wabarakatuh
    </div>
    <div style="margin-top:14px;font-size:10px;color:#c9a84c;opacity:0.18;line-height:2">
        Kel. Mempelai Wanita — Alm. Bapak Fadli &amp; Ibu Sri Sumarti<br>
        Kel. Mempelai Pria — Alm. Bapak Paimo &amp; Ibu Suriani
    </div>
</div>
""", unsafe_allow_html=True)
