import streamlit as st
import json
import os
from datetime import datetime
import pytz

st.set_page_config(
    page_title="Undangan Pernikahan Intan & Syahrial",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load photos
@st.cache_data
def load_photos():
    path = os.path.join(os.path.dirname(__file__), "photos.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

photos = load_photos()

# Session state for wishes & rsvp
if "wishes" not in st.session_state:
    st.session_state.wishes = [
        {"name": "Keluarga Besar", "text": "Semoga menjadi keluarga yang Sakinah, Mawaddah, Warahmah. Aamiin Ya Rabbal Alamin.", "time": "Baru saja"}
    ]
if "rsvp_sent" not in st.session_state:
    st.session_state.rsvp_sent = False

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css">

<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] {
    background: #0a0305 !important;
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(139,28,46,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, rgba(139,28,46,0.10) 0%, transparent 50%) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
.stDeployButton { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 520px !important;
    margin: 0 auto !important;
}

/* ── Global font ── */
body, .stMarkdown, p, div {
    font-family: 'Cormorant Garamond', serif !important;
    color: #f5e6d3 !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }

/* ─────────────────────── COMPONENTS ─────────────────────── */

/* Hero */
.hero-wrap {
    text-align: center;
    padding: 56px 24px 36px;
    position: relative;
    overflow: hidden;
}

.bismillah-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px;
    color: #c9a84c;
    margin-bottom: 4px;
    letter-spacing: 2px;
}

.salam-text {
    font-size: 13px;
    color: #c9a84c;
    opacity: 0.8;
    font-style: italic;
    letter-spacing: 1px;
    margin-bottom: 32px;
}

/* Photo frame */
.frame-outer {
    position: relative;
    width: 230px;
    margin: 0 auto 32px;
}

.frame-outer img {
    width: 100%;
    height: 300px;
    object-fit: cover;
    display: block;
    border: 1px solid rgba(201,168,76,0.5);
    outline: 4px solid rgba(10,3,5,0.8);
    outline-offset: -8px;
}

.frame-corner {
    position: absolute;
    width: 22px;
    height: 22px;
    border-color: #c9a84c;
    border-style: solid;
}
.fc-tl { top: -3px; left: -3px; border-width: 2px 0 0 2px; }
.fc-tr { top: -3px; right: -3px; border-width: 2px 2px 0 0; }
.fc-bl { bottom: -3px; left: -3px; border-width: 0 0 2px 2px; }
.fc-br { bottom: -3px; right: -3px; border-width: 0 2px 2px 0; }

/* Slide gallery */
.gallery-row {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin: 0 0 32px;
    padding: 0 20px;
}

.gallery-row img {
    width: calc(33.33% - 6px);
    height: 110px;
    object-fit: cover;
    border: 1px solid rgba(201,168,76,0.3);
    cursor: pointer;
    transition: border-color 0.3s;
}

.gallery-row img:hover { border-color: #c9a84c; }

/* Title undangan */
.undangan-label {
    font-size: 10px;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: #c9a84c;
    opacity: 0.6;
    margin-bottom: 8px;
}

.couple-script {
    font-family: 'Great Vibes', cursive !important;
    font-size: 58px !important;
    color: #c9a84c !important;
    line-height: 1.05;
    text-shadow: 0 0 40px rgba(201,168,76,0.25);
}

.ampersand-script {
    font-family: 'Great Vibes', cursive !important;
    font-size: 36px !important;
    color: #8b1c2e !important;
    display: block;
    margin: -6px 0;
}

/* Gold divider */
.gold-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 20px auto;
    max-width: 300px;
    padding: 0 24px;
}
.gd-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, transparent, #c9a84c, transparent);
}
.gd-diamond {
    width: 7px;
    height: 7px;
    background: #c9a84c;
    transform: rotate(45deg);
    flex-shrink: 0;
}

/* Section card */
.s-card {
    margin: 0 20px 20px;
    border: 1px solid rgba(201,168,76,0.2);
    padding: 28px 24px;
    position: relative;
    background: rgba(139,28,46,0.05);
}
.s-card-top::before {
    content: '';
    position: absolute;
    top: -1px; left: 16px; right: 16px;
    height: 1px;
    background: linear-gradient(to right, transparent, #c9a84c, transparent);
}
.s-card::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 16px; right: 16px;
    height: 1px;
    background: linear-gradient(to right, transparent, #c9a84c, transparent);
}

.s-label {
    font-size: 9px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #c9a84c;
    opacity: 0.6;
    margin-bottom: 14px;
    text-align: center;
}

.intro-p {
    font-size: 13.5px;
    line-height: 2;
    text-align: center;
    color: #e8d5c0 !important;
    opacity: 0.88;
}

/* Mempelai */
.mempelai-name {
    font-family: 'Great Vibes', cursive !important;
    font-size: 40px !important;
    color: #c9a84c !important;
    text-align: center;
    display: block;
    line-height: 1.1;
    text-shadow: 0 0 24px rgba(201,168,76,0.2);
}

.mempelai-parents {
    font-size: 12px;
    color: #c9a84c;
    opacity: 0.65;
    font-style: italic;
    text-align: center;
    margin-top: 4px;
}

/* Events grid */
.events-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 0 20px 20px;
}

.event-card {
    border: 1px solid rgba(201,168,76,0.3);
    padding: 22px 14px;
    text-align: center;
    background: rgba(201,168,76,0.03);
    position: relative;
}

.ev-type {
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 10px;
}

.ev-day {
    font-family: 'Playfair Display', serif !important;
    font-size: 42px !important;
    font-weight: 700 !important;
    color: #c9a84c !important;
    line-height: 1;
}

.ev-monthyear {
    font-size: 10px;
    letter-spacing: 2px;
    color: #c9a84c;
    opacity: 0.65;
    text-transform: uppercase;
    margin: 4px 0 10px;
}

.ev-time {
    font-size: 12px;
    color: #e8d5c0;
    opacity: 0.75;
    margin-bottom: 8px;
}

.ev-loc {
    font-size: 11px;
    color: #c9a84c;
    opacity: 0.6;
    line-height: 1.6;
    font-style: italic;
}

/* Countdown */
.countdown-wrap {
    margin: 0 20px 20px;
    padding: 28px 20px;
    border: 1px solid rgba(201,168,76,0.15);
    background: rgba(139,28,46,0.07);
    text-align: center;
}

.cd-grid {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 16px;
}

.cd-block { text-align: center; min-width: 52px; }

.cd-num {
    font-family: 'Playfair Display', serif !important;
    font-size: 38px !important;
    font-weight: 700 !important;
    color: #c9a84c !important;
    display: block;
    line-height: 1;
    text-shadow: 0 0 20px rgba(201,168,76,0.3);
}

.cd-unit {
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #c9a84c;
    opacity: 0.5;
    margin-top: 5px;
}

.cd-sep {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    color: #c9a84c;
    opacity: 0.35;
    align-self: flex-start;
    padding-top: 6px;
    line-height: 1;
}

/* Khitanan */
.khit-card {
    margin: 0 20px 20px;
    border: 1px solid rgba(201,168,76,0.22);
    padding: 24px;
    text-align: center;
    background: rgba(201,168,76,0.03);
}

.khit-also { font-size: 9px; letter-spacing: 4px; color: #c9a84c; opacity: 0.5; text-transform: uppercase; margin-bottom: 8px; }
.khit-title { font-family: 'Great Vibes', cursive !important; font-size: 34px !important; color: #c9a84c !important; margin-bottom: 4px; }
.khit-name { font-family: 'Playfair Display', serif !important; font-size: 20px !important; color: #f5e6d3 !important; letter-spacing: 1px; }

/* Turut mengundang tabs */
.tab-buttons {
    display: flex;
    margin: 0 20px 0;
    border-bottom: 1px solid rgba(201,168,76,0.2);
}

/* Wish item */
.wish-item {
    padding: 12px 0;
    border-bottom: 1px solid rgba(201,168,76,0.08);
}
.wish-name-label { font-size: 12px; color: #c9a84c; font-weight: 600; margin-bottom: 4px; }
.wish-body { font-size: 13px; color: #e8d5c0; opacity: 0.78; font-style: italic; line-height: 1.7; }
.wish-time { font-size: 10px; color: #c9a84c; opacity: 0.4; margin-top: 4px; }

/* Ayat */
.ayat-text {
    font-size: 13px;
    line-height: 2.1;
    text-align: center;
    color: #e8d5c0 !important;
    opacity: 0.8;
    font-style: italic;
}

/* Footer */
.footer-wrap {
    text-align: center;
    padding: 32px 24px 48px;
    border-top: 1px solid rgba(201,168,76,0.1);
}

.footer-names {
    font-family: 'Great Vibes', cursive !important;
    font-size: 32px !important;
    color: #c9a84c !important;
    margin-bottom: 8px;
}

.footer-sub {
    font-size: 10px;
    letter-spacing: 3px;
    color: #c9a84c;
    opacity: 0.4;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.wassalam {
    font-size: 11px;
    color: #c9a84c;
    opacity: 0.3;
    font-style: italic;
}

/* Streamlit button override */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(201,168,76,0.5) !important;
    color: #c9a84c !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 11px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
    transition: all 0.3s !important;
    width: 100%;
}

.stButton > button:hover {
    background: rgba(201,168,76,0.12) !important;
    border-color: #c9a84c !important;
}

.stButton > button:active {
    background: rgba(139,28,46,0.3) !important;
}

/* Text input / text area override */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(201,168,76,0.25) !important;
    border-radius: 0 !important;
    color: #f5e6d3 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 14px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #c9a84c !important;
    box-shadow: none !important;
}

.stTextInput label, .stTextArea label, .stRadio label {
    color: #c9a84c !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    opacity: 0.7 !important;
}

/* Radio button */
.stRadio > div { gap: 12px !important; }
.stRadio > div > label {
    color: #c9a84c !important;
    font-size: 13px !important;
    letter-spacing: 1px !important;
    text-transform: none !important;
    background: rgba(201,168,76,0.05) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    padding: 8px 16px !important;
    border-radius: 0 !important;
}

/* Success / info message */
.stSuccess, .stInfo {
    background: rgba(139,28,46,0.2) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    border-radius: 0 !important;
    color: #c9a84c !important;
}

/* Divider */
hr { border-color: rgba(201,168,76,0.1) !important; }

/* Corner ornaments top */
.corner-ornament-tl {
    position: fixed;
    top: 0; left: 50%;
    transform: translateX(-260px);
    width: 80px; height: 80px;
    pointer-events: none;
    z-index: 999;
    opacity: 0.4;
}
</style>
""", unsafe_allow_html=True)


# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────
def gold_divider():
    st.markdown("""
    <div class="gold-divider">
        <div class="gd-line"></div>
        <div class="gd-diamond"></div>
        <div class="gd-diamond" style="margin:0 -4px"></div>
        <div class="gd-diamond"></div>
        <div class="gd-line"></div>
    </div>""", unsafe_allow_html=True)

def section_label(text):
    st.markdown(f'<div class="s-label">— {text} —</div>', unsafe_allow_html=True)

def countdown_html():
    tz = pytz.timezone("Asia/Jakarta")
    now = datetime.now(tz)
    target = tz.localize(datetime(2026, 7, 19, 10, 0, 0))
    diff = target - now
    if diff.total_seconds() <= 0:
        d = h = m = s = 0
    else:
        total = int(diff.total_seconds())
        d = total // 86400
        h = (total % 86400) // 3600
        m = (total % 3600) // 60
        s = total % 60
    return f"""
    <div class="countdown-wrap">
        <div class="s-label">— Menghitung Hari Menuju Hari Bahagia —</div>
        <div class="cd-grid">
            <div class="cd-block"><span class="cd-num">{d:02d}</span><div class="cd-unit">Hari</div></div>
            <div class="cd-sep">:</div>
            <div class="cd-block"><span class="cd-num">{h:02d}</span><div class="cd-unit">Jam</div></div>
            <div class="cd-sep">:</div>
            <div class="cd-block"><span class="cd-num">{m:02d}</span><div class="cd-unit">Menit</div></div>
            <div class="cd-sep">:</div>
            <div class="cd-block"><span class="cd-num">{s:02d}</span><div class="cd-unit">Detik</div></div>
        </div>
    </div>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  HERO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="bismillah-text">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
    <div class="salam-text">Assalamu'alaikum Warahmatullahi Wabarakatuh</div>
</div>
""", unsafe_allow_html=True)

# Main photo
if photos.get("foto1"):
    st.markdown(f"""
    <div style="padding:0 20px;margin-bottom:16px">
        <div class="frame-outer">
            <div class="frame-corner fc-tl"></div>
            <div class="frame-corner fc-tr"></div>
            <div class="frame-corner fc-bl"></div>
            <div class="frame-corner fc-br"></div>
            <img src="data:image/png;base64,{photos['foto1']}" alt="Foto Mempelai"/>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Gallery row
if photos.get("foto2") and photos.get("foto3"):
    st.markdown(f"""
    <div class="gallery-row">
        <img src="data:image/png;base64,{photos['foto1']}" alt="foto 1"/>
        <img src="data:image/png;base64,{photos['foto2']}" alt="foto 2"/>
        <img src="data:image/png;base64,{photos['foto3']}" alt="foto 3"/>
    </div>
    """, unsafe_allow_html=True)

# Couple names
st.markdown("""
<div style="text-align:center;padding:0 24px">
    <div class="undangan-label">Undangan Pernikahan</div>
    <div class="couple-script">Intan</div>
    <div class="ampersand-script">&</div>
    <div class="couple-script">Syahrial</div>
    <div style="font-size:11px;letter-spacing:2px;color:#c9a84c;opacity:0.45;margin-top:12px;text-transform:uppercase">
        19 Juli 2026 · Desa Namo Bintang
    </div>
</div>
""", unsafe_allow_html=True)

gold_divider()

# ═══════════════════════════════════════════════════════════════════════════════
#  PEMBUKA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 20px">
    <div class="s-label">— Dengan Rahmat Allah Subhanahu Wa Ta'ala —</div>
    <p class="intro-p">
        Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan.<br><br>
        Ya Allah, perkenankanlah kami menikahkan putra-putri kami untuk mengikuti
        Sunnah Rasul-Mu, melakukan Syariat Agama-Mu dalam rangka membentuk keluarga
        yang Sakinah, Mawaddah, Warahmah. Maka izinkanlah kami menikahkannya.
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  MEMPELAI
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 8px">
    <div class="s-label">— Mempelai Wanita —</div>
    <span class="mempelai-name">Intan Candra Nurul Hafizah</span>
    <div class="mempelai-parents">Putri dari Alm. Bapak Fadli &amp; Ibu Sri Sumarti (Wiwik)</div>
</div>
<div style="text-align:center;margin:8px 0">
    <span style="font-family:'Great Vibes',cursive;font-size:40px;color:#8b1c2e">&amp;</span>
</div>
<div class="s-card" style="margin:0 20px 24px">
    <div class="s-label">— Mempelai Pria —</div>
    <span class="mempelai-name">Syahrial / Gombeng</span>
    <div class="mempelai-parents">Putra dari Alm. Bapak Paimo &amp; Ibu Suriani</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  EVENTS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="events-grid">
    <div class="event-card">
        <div class="ev-type">✦ Akad Nikah ✦</div>
        <div class="ev-day">17</div>
        <div class="ev-monthyear">Juli · 2026</div>
        <div class="ev-time">Jum'at · 08.00 WIB - Selesai</div>
        <div class="ev-loc">Dusun II Sumberingin<br>Desa Namo Bintang</div>
    </div>
    <div class="event-card">
        <div class="ev-type">✦ Resepsi ✦</div>
        <div class="ev-day">19</div>
        <div class="ev-monthyear">Juli · 2026</div>
        <div class="ev-time">Minggu · 10.00 WIB - Selesai</div>
        <div class="ev-loc">Dusun II Sumberingin<br>Desa Namo Bintang</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  COUNTDOWN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(countdown_html(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  LOCATION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 20px;text-align:center">
    <div class="s-label">— Lokasi Acara —</div>
    <div style="font-size:28px;color:#8b1c2e;margin:4px 0">📍</div>
    <div style="font-family:'Playfair Display',serif;font-size:16px;color:#c9a84c;margin:10px 0 6px">
        Dusun II Sumberingin
    </div>
    <div style="font-size:12px;color:#e8d5c0;opacity:0.7;font-style:italic;line-height:1.8">
        Desa Namo Bintang<br>
        Minggu, 19 Juli 2026 · Pukul 10.00 WIB
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🗺️  Buka Google Maps", key="maps"):
        st.markdown("""
        <script>window.open('https://maps.app.goo.gl/8G9hHHY9LzdGg5yc6','_blank');</script>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-top:8px">
            <a href="https://maps.app.goo.gl/8G9hHHY9LzdGg5yc6" target="_blank"
               style="color:#c9a84c;font-size:11px;letter-spacing:2px;text-decoration:none;
               text-transform:uppercase;border-bottom:1px solid rgba(201,168,76,0.4);padding-bottom:2px">
               Klik di sini untuk buka peta ↗
            </a>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  KHITANAN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="khit-card">
    <div class="khit-also">— Serta Khitanan —</div>
    <div class="khit-title">Ahmad Hanafi</div>
</div>
""", unsafe_allow_html=True)

gold_divider()

# ═══════════════════════════════════════════════════════════════════════════════
#  TURUT MENGUNDANG
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 4px">
    <div class="s-label">— Turut Mengundang —</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💐 Pihak Wanita", "🎩 Pihak Pria"])

with tab1:
    wanita_list = [
        "Alm. Mandah / Ngatiyem (Kakek & Nenek)",
        "Muri / Anik (Kakek & Nenek)",
        "Dasem (Nenek)",
        "Sukar / Iyet (Kakek & Nenek)",
        "Ribut / Ngatisah (Kakek & Nenek)",
        "Alm. Jarno / Muriatik (Kakek & Nenek)",
        "Sawon (Kakek)",
        "Karlan (Kakek)",
        "Watik / Misjo (Wawak)",
        "Gambreng / Tumik (Pakde & Bude)",
        "Endang Susanti / Ust. Lukman S.Pd.I (Bibik & Oom)",
        "Sri Wulan Handayani / Hendrik (Bibik & Oom)",
        "Ema (Adik)",
        "Ahamad Hanafi (Adik)",
    ]
    items_html = "".join([
        f'<li style="font-size:13px;color:#e8d5c0;opacity:0.75;padding:6px 0;border-bottom:1px solid rgba(201,168,76,0.07);line-height:1.5">{i}</li>'
        for i in wanita_list
    ])
    st.markdown(f'<ul style="list-style:none;padding:12px 0 0">{items_html}</ul>', unsafe_allow_html=True)

with tab2:
    pria_list = [
        "Marinem / Suparto (Nenek & Kakek)",
        "Ngatiyem / Alm. Joni (Nenek & Kakek)",
        "Alm. Paiko / Iyus (Wawak)",
        "Dedi / Rika (Abang)",
        "Yuda / Wulan (Abang)",
        "Diki / Dina (Adik)",
        "Igo Ardiansyah (Adik)",
        "Sugik / Yanti (Lelek)",
        "Minok / Susi (Lelek)",
        "Rame / Santo (Bibik)",
        "Yuni / Junedi (Bibik)",
    ]
    items_html2 = "".join([
        f'<li style="font-size:13px;color:#e8d5c0;opacity:0.75;padding:6px 0;border-bottom:1px solid rgba(201,168,76,0.07);line-height:1.5">{i}</li>'
        for i in pria_list
    ])
    st.markdown(f'<ul style="list-style:none;padding:12px 0 0">{items_html2}</ul>', unsafe_allow_html=True)

gold_divider()

# ═══════════════════════════════════════════════════════════════════════════════
#  RSVP
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 0">
    <div class="s-label">— Konfirmasi Kehadiran —</div>
    <p class="intro-p" style="font-size:12px;margin-bottom:0">
        Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila<br>
        Bapak / Ibu / Saudara/i berkenan hadir memberikan Do'a Restu.
    </p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding:0 20px 20px">', unsafe_allow_html=True)
    rsvp_name = st.text_input("", placeholder="Nama Anda...", key="rsvp_name", label_visibility="collapsed")
    rsvp_status = st.radio(
        "", ["✦ Hadir", "✦ Tidak Hadir"], horizontal=True, key="rsvp_status", label_visibility="collapsed"
    )
    if st.button("Kirim Konfirmasi", key="submit_rsvp"):
        if rsvp_name.strip():
            hadir = "Hadir" in rsvp_status
            if hadir:
                st.success(f"✦ Terima kasih, {rsvp_name}! Kami menantikan kehadiran Anda.")
            else:
                st.info(f"✦ Terima kasih atas kabarnya, {rsvp_name}. Semoga selalu dalam lindungan Allah.")
        else:
            st.warning("Mohon isi nama Anda terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  UCAPAN & DOA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 0">
    <div class="s-label">— Do'a &amp; Ucapan —</div>
</div>
""", unsafe_allow_html=True)

# Show existing wishes
for w in st.session_state.wishes:
    st.markdown(f"""
    <div class="wish-item" style="padding:12px 20px">
        <div class="wish-name-label">{w['name']}</div>
        <div class="wish-body">{w['text']}</div>
        <div class="wish-time">{w['time']}</div>
    </div>""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding:12px 20px 20px">', unsafe_allow_html=True)
    wish_name = st.text_input("", placeholder="Nama Anda...", key="wish_name", label_visibility="collapsed")
    wish_text = st.text_area("", placeholder="Tulis do'a dan ucapan untuk kedua mempelai...", key="wish_text", label_visibility="collapsed", height=100)
    if st.button("Kirim Ucapan ✦", key="submit_wish"):
        if wish_name.strip() and wish_text.strip():
            st.session_state.wishes.insert(0, {
                "name": wish_name.strip(),
                "text": wish_text.strip(),
                "time": "Baru saja"
            })
            st.rerun()
        else:
            st.warning("Mohon isi nama dan ucapan Anda.")
    st.markdown('</div>', unsafe_allow_html=True)

gold_divider()

# ═══════════════════════════════════════════════════════════════════════════════
#  AYAT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 20px">
    <div class="s-label">— QS. Ar-Rum: 21 —</div>
    <p class="ayat-text">
        "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu
        istri-istri dari jenismu sendiri, supaya kamu cenderung dan merasa tenteram
        kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang."
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-wrap">
    <svg width="120" height="1" viewBox="0 0 120 1" style="display:block;margin:0 auto 20px;opacity:0.25">
        <rect width="120" height="1" fill="#c9a84c"/>
    </svg>
    <div class="footer-names">Intan &amp; Syahrial</div>
    <div class="footer-sub">19 Juli 2026 · Namo Bintang</div>
    <div style="font-size:18px;color:#c9a84c;opacity:0.3;margin:12px 0">✦ ✦ ✦</div>
    <div class="wassalam">Wassalamu'alaikum Warahmatullahi Wabarakatuh</div>
    <div style="margin-top:20px;font-size:10px;color:#c9a84c;opacity:0.2;letter-spacing:1px">
        Kel. Mempelai Wanita · Alm. Bapak Fadli &amp; Ibu Sri Sumarti (Wiwik)<br>
        Kel. Mempelai Pria · Alm. Bapak Paimo &amp; Ibu Suriani
    </div>
</div>
""", unsafe_allow_html=True)
