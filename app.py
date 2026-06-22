import streamlit as st
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
music_file = os.path.join(os.path.dirname(__file__), "janji_suci.mp3")
music_exists = os.path.exists(music_file)

# ── Encode audio ──
audio_b64 = ""
if music_exists:
    with open(music_file, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()

# ══════════════════════════════════════════════════════════════
#  FULL PAGE HTML — satu blok besar agar script & elemen sinkron
# ══════════════════════════════════════════════════════════════
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Playfair+Display:wght@400;600;700&family=IM+Fell+English+SC&display=swap" rel="stylesheet">

<style>
/* ── RESET & BASE ── */
* { margin:0; padding:0; box-sizing:border-box; }

[data-testid="stAppViewContainer"] {
    background: #0f0b08 !important;
    min-height: 100vh;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
.stDeployButton,
section[data-testid="stSidebar"],
#MainMenu, footer, header { display:none !important; visibility:hidden !important; }

[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 560px !important;
    margin: 0 auto !important;
}

body, .stMarkdown, p, div {
    font-family: 'Cormorant Garamond', serif !important;
    color: #e8d5b7 !important;
}

/* ── SUBTLE TEXTURE OVERLAY ── */
#texture-overlay {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
        radial-gradient(ellipse 80% 40% at 50% 0%,   rgba(180,140,80,0.06) 0%, transparent 70%),
        radial-gradient(ellipse 60% 30% at 50% 100%, rgba(120,60,40,0.07) 0%, transparent 70%);
}

/* ── MUSIC BUTTON ── */
#music-btn {
    position: fixed;
    bottom: 28px; right: 28px;
    width: 48px; height: 48px;
    border-radius: 50%;
    background: rgba(15,11,8,0.95);
    border: 1px solid rgba(180,148,80,0.5);
    color: #c9a84c;
    font-size: 18px;
    cursor: pointer;
    z-index: 9999;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 2px 20px rgba(0,0,0,0.5);
    transition: all 0.3s ease;
    font-family: serif;
}
#music-btn:hover { border-color:#c9a84c; background:rgba(201,168,76,0.08); }
#music-btn.playing { animation: ring 3s ease-in-out infinite; }
@keyframes ring {
    0%,100% { box-shadow: 0 2px 20px rgba(0,0,0,0.5), 0 0 0 0 rgba(201,168,76,0.15); }
    50%      { box-shadow: 0 2px 20px rgba(0,0,0,0.5), 0 0 0 8px rgba(201,168,76,0); }
}
#music-label {
    position: fixed;
    bottom: 84px; right: 20px;
    background: rgba(15,11,8,0.95);
    border: 1px solid rgba(180,148,80,0.3);
    color: #c9a84c;
    font-family: 'Cormorant Garamond', serif;
    font-size: 10.5px; letter-spacing: 1.5px;
    padding: 5px 14px;
    z-index: 9999;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.4s;
    white-space: nowrap;
}
#music-label.show { opacity: 1; }

/* ══════════════════════════════════════
   LAYOUT SECTIONS
══════════════════════════════════════ */

/* ── HERO ── */
.inv-hero {
    text-align: center;
    padding: 56px 28px 36px;
    position: relative; z-index: 1;
}
.inv-bismillah {
    font-size: 24px;
    color: #c9a84c;
    letter-spacing: 3px;
    text-shadow: 0 0 30px rgba(201,168,76,0.2);
    margin-bottom: 10px;
}
.inv-salam {
    font-size: 11px; letter-spacing: 2.5px;
    color: #c9a84c; opacity: 0.5;
    text-transform: uppercase; font-style: italic;
}
.inv-ornament {
    color: #c9a84c; opacity: 0.25;
    font-size: 13px; letter-spacing: 8px;
    margin: 18px 0;
}

/* ── PHOTO FRAME ── */
.inv-frame-wrap {
    position: relative;
    width: 220px;
    margin: 0 auto 20px;
}
.inv-frame-wrap img {
    width: 100%;
    height: 290px;
    object-fit: cover;
    display: block;
    border: 1px solid rgba(201,168,76,0.4);
    filter: sepia(0.1) brightness(0.95);
}
.inv-frame-corner {
    position: absolute;
    width: 20px; height: 20px;
    border-color: rgba(201,168,76,0.6); border-style: solid;
}
.ifc-tl { top:-3px; left:-3px; border-width:1px 0 0 1px; }
.ifc-tr { top:-3px; right:-3px; border-width:1px 1px 0 0; }
.ifc-bl { bottom:-3px; left:-3px; border-width:0 0 1px 1px; }
.ifc-br { bottom:-3px; right:-3px; border-width:0 1px 1px 0; }

/* ── GALLERY ── */
.inv-gallery {
    display: flex; gap: 6px;
    justify-content: center;
    margin: 0 24px 32px;
}
.inv-gallery img {
    flex: 1; height: 110px;
    object-fit: cover;
    border: 1px solid rgba(201,168,76,0.2);
    filter: sepia(0.08) brightness(0.95);
    transition: border-color 0.3s;
}
.inv-gallery img:hover { border-color: rgba(201,168,76,0.5); }

/* ── COUPLE NAME ── */
.inv-couple-wrap {
    text-align: center;
    padding: 0 28px 8px;
    position: relative; z-index: 1;
}
.inv-tag {
    font-size: 9px; letter-spacing: 5px;
    text-transform: uppercase; color: #c9a84c; opacity: 0.4;
    margin-bottom: 12px; display: block;
}
.inv-name {
    font-family: 'Playfair Display', serif !important;
    font-size: 52px !important;
    font-weight: 700 !important;
    color: #c9a84c !important;
    line-height: 1.1;
    letter-spacing: 1px;
}
.inv-amp {
    display: block;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 28px !important;
    font-style: italic !important;
    color: rgba(201,168,76,0.4) !important;
    letter-spacing: 4px;
    margin: 4px 0;
}
.inv-date-tag {
    font-size: 10px; letter-spacing: 4px;
    color: #c9a84c; opacity: 0.35;
    text-transform: uppercase; margin-top: 14px;
}

/* ── DIVIDER ── */
.inv-divider {
    display: flex; align-items: center; gap: 12px;
    margin: 28px auto;
    max-width: 300px; padding: 0 28px;
    position: relative; z-index: 1;
}
.inv-divider-line {
    flex: 1; height: 1px;
    background: linear-gradient(to right, transparent, rgba(201,168,76,0.3), transparent);
}
.inv-divider-mark {
    width: 4px; height: 4px;
    background: rgba(201,168,76,0.3);
    transform: rotate(45deg); flex-shrink: 0;
}

/* ── CARD ── */
.inv-card {
    margin: 0 24px 16px;
    padding: 28px 26px;
    border-top: 1px solid rgba(201,168,76,0.12);
    border-bottom: 1px solid rgba(201,168,76,0.12);
    position: relative; z-index: 1;
}
.inv-card-label {
    font-size: 9px; letter-spacing: 4px;
    text-transform: uppercase; color: #c9a84c;
    opacity: 0.4; text-align: center; margin-bottom: 16px;
}
.inv-body {
    font-size: 13.5px; line-height: 2.2;
    text-align: center; color: #ddc9a8 !important;
    opacity: 0.85;
}

/* ── MEMPELAI ── */
.inv-mempelai-name {
    font-family: 'Playfair Display', serif !important;
    font-size: 26px !important; font-weight: 600 !important;
    color: #c9a84c !important;
    text-align: center; display: block;
    letter-spacing: 1px;
}
.inv-mempelai-sub {
    font-size: 12px; color: #c9a84c; opacity: 0.45;
    font-style: italic; text-align: center; margin-top: 5px;
}
.inv-sep-amp {
    text-align: center; margin: 12px 0;
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px; font-style: italic;
    color: rgba(201,168,76,0.25);
    letter-spacing: 4px;
    position: relative; z-index: 1;
}

/* ── EVENTS ── */
.inv-events {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
    margin: 0 24px 16px; position: relative; z-index: 1;
}
.inv-event {
    border: 1px solid rgba(201,168,76,0.15);
    padding: 22px 12px; text-align: center;
}
.ev-lbl { font-size: 8px; letter-spacing: 3px; color: #c9a84c; opacity: 0.4; text-transform: uppercase; margin-bottom: 14px; }
.ev-num {
    font-family: 'Playfair Display', serif !important;
    font-size: 52px !important; font-weight: 700 !important;
    color: #c9a84c !important; line-height: 1;
}
.ev-my { font-size: 9px; letter-spacing: 2px; color: #c9a84c; opacity: 0.35; text-transform: uppercase; margin: 5px 0 10px; }
.ev-tm { font-size: 12px; color: #ddc9a8; opacity: 0.6; margin-bottom: 6px; }
.ev-loc { font-size: 11px; color: #c9a84c; opacity: 0.4; line-height: 1.7; font-style: italic; }

/* ── COUNTDOWN ── */
.inv-countdown {
    margin: 0 24px 16px;
    padding: 30px 20px;
    border: 1px solid rgba(201,168,76,0.1);
    text-align: center;
    position: relative; z-index: 1;
}
.cd-row { display: flex; justify-content: center; align-items: flex-start; gap: 8px; margin-top: 18px; }
.cd-unit-wrap { text-align: center; min-width: 54px; }
.cd-num {
    font-family: 'Playfair Display', serif !important;
    font-size: 46px !important; font-weight: 700 !important;
    color: #c9a84c !important; display: block; line-height: 1;
    letter-spacing: -1px;
}
.cd-lbl { font-size: 8px; letter-spacing: 2px; text-transform: uppercase; color: #c9a84c; opacity: 0.3; margin-top: 6px; }
.cd-colon {
    font-family: 'Playfair Display', serif;
    font-size: 36px; color: rgba(201,168,76,0.2);
    line-height: 1; padding-top: 5px; flex-shrink: 0;
}

/* ── LOCATION ── */
.inv-map-btn {
    display: inline-block;
    padding: 12px 36px;
    border: 1px solid rgba(201,168,76,0.35);
    color: #c9a84c !important;
    font-family: 'Cormorant Garamond', serif;
    font-size: 11px; letter-spacing: 4px; text-transform: uppercase;
    text-decoration: none !important;
    background: transparent;
    transition: all 0.3s;
    margin-top: 16px;
}
.inv-map-btn:hover { background: rgba(201,168,76,0.05); border-color: #c9a84c; }

/* ── WISHES ── */
.wish-item {
    padding: 14px 0;
    border-bottom: 1px solid rgba(201,168,76,0.06);
}
.wish-author { font-size: 12px; color: #c9a84c; opacity: 0.7; font-weight: 600; margin-bottom: 5px; }
.wish-text { font-size: 13px; color: #ddc9a8; opacity: 0.7; font-style: italic; line-height: 1.8; }
.wish-ts { font-size: 9px; color: #c9a84c; opacity: 0.25; margin-top: 5px; letter-spacing: 1px; }

/* ── FOOTER ── */
.inv-footer {
    text-align: center;
    padding: 36px 28px 60px;
    border-top: 1px solid rgba(201,168,76,0.07);
    position: relative; z-index: 1;
}
.inv-footer-names {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important; font-weight: 600 !important;
    color: rgba(201,168,76,0.7) !important;
    letter-spacing: 2px; margin-bottom: 8px;
}
.inv-footer-sub { font-size: 9px; letter-spacing: 4px; color: #c9a84c; opacity: 0.25; text-transform: uppercase; }
.inv-wassalam { font-size: 11px; color: #c9a84c; opacity: 0.2; font-style: italic; margin-top: 16px; }

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    color: #c9a84c !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 11px !important; letter-spacing: 4px !important;
    text-transform: uppercase !important;
    padding: 11px 24px !important; border-radius: 0 !important;
    width: 100%;
}
.stButton > button:hover {
    background: rgba(201,168,76,0.05) !important;
    border-color: #c9a84c !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.015) !important;
    border: 1px solid rgba(201,168,76,0.15) !important;
    border-radius: 0 !important;
    color: #e8d5b7 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(201,168,76,0.4) !important;
    box-shadow: none !important;
}
.stTextInput label, .stTextArea label, .stRadio label {
    color: #c9a84c !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 10px !important; letter-spacing: 3px !important;
    text-transform: uppercase !important; opacity: 0.45 !important;
}
.stRadio > div > label {
    color: #c9a84c !important; font-size: 13px !important;
    letter-spacing: 1px !important; text-transform: none !important;
    background: transparent !important;
    border: 1px solid rgba(201,168,76,0.15) !important;
    padding: 8px 18px !important; border-radius: 0 !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: 1px solid rgba(201,168,76,0.15) !important;
    color: #c9a84c !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 11px !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    border-color: rgba(201,168,76,0.4) !important;
    background: rgba(201,168,76,0.04) !important;
}
.stSuccess, .stInfo, .stWarning {
    background: rgba(20,14,8,0.8) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    border-radius: 0 !important;
    color: #c9a84c !important;
}
hr { border-color: rgba(201,168,76,0.07) !important; }
</style>

<!-- ══ TEXTURE ══ -->
<div id="texture-overlay"></div>

<!-- ══ MUSIC ══ -->
<div id="music-label">♫ Janji Suci — Yovie &amp; Nuno</div>
<button id="music-btn" title="Musik">♫</button>
""", unsafe_allow_html=True)

# ── Audio element ──
if audio_b64:
    st.markdown(f"""
    <audio id="bg-audio" loop preload="auto">
        <source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg">
    </audio>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <audio id="bg-audio" loop preload="auto">
        <source src="https://ia800905.us.archive.org/19/items/FREE_background_music_dac/07_-_Music_Box.mp3" type="audio/mpeg">
    </audio>""", unsafe_allow_html=True)

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

# ── Foto utama ──
if photos.get("foto1"):
    st.markdown(f"""
    <div style="padding:0 24px;margin-bottom:12px;position:relative;z-index:1">
        <div class="inv-frame-wrap">
            <div class="inv-frame-corner ifc-tl"></div>
            <div class="inv-frame-corner ifc-tr"></div>
            <div class="inv-frame-corner ifc-bl"></div>
            <div class="inv-frame-corner ifc-br"></div>
            <img src="data:image/png;base64,{photos['foto1']}" alt="Foto Mempelai"/>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Gallery ──
if photos.get("foto2") and photos.get("foto3"):
    st.markdown(f"""
    <div class="inv-gallery">
        <img src="data:image/png;base64,{photos['foto1']}" alt=""/>
        <img src="data:image/png;base64,{photos['foto2']}" alt=""/>
        <img src="data:image/png;base64,{photos['foto3']}" alt=""/>
    </div>""", unsafe_allow_html=True)

# ── Nama Mempelai ──
st.markdown("""
<div class="inv-couple-wrap">
    <span class="inv-tag">✦ Undangan Pernikahan ✦</span>
    <div class="inv-name">Intan</div>
    <div class="inv-amp">&amp;</div>
    <div class="inv-name">Syahrial</div>
    <div class="inv-date-tag">19 · Juli · 2026 &nbsp;·&nbsp; Desa Namo Bintang</div>
</div>
""", unsafe_allow_html=True)

# ── DIVIDER ──
def divider():
    st.markdown("""
    <div class="inv-divider" style="position:relative;z-index:1">
        <div class="inv-divider-line"></div>
        <div class="inv-divider-mark"></div>
        <div class="inv-divider-line"></div>
    </div>""", unsafe_allow_html=True)

divider()

# ══════════════════════════════════════════════════════════════
#  PEMBUKA
# ══════════════════════════════════════════════════════════════
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

# ══════════════════════════════════════════════════════════════
#  MEMPELAI
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-card">
    <div class="inv-card-label">— Mempelai Wanita —</div>
    <span class="inv-mempelai-name">Intan Candra Nurul Hafizah</span>
    <div class="inv-mempelai-sub">Putri dari Alm. Bapak Fadli &amp; Ibu Sri Sumarti (Wiwik)</div>
</div>
<div class="inv-sep-amp">—&nbsp;&amp;&nbsp;—</div>
<div class="inv-card" style="margin-top:0">
    <div class="inv-card-label">— Mempelai Pria —</div>
    <span class="inv-mempelai-name">Syahrial</span>
    <div class="inv-mempelai-sub">Putra dari Alm. Bapak Paimo &amp; Ibu Suriani</div>
</div>
""", unsafe_allow_html=True)

divider()

# ══════════════════════════════════════════════════════════════
#  EVENTS
# ══════════════════════════════════════════════════════════════
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
#  COUNTDOWN — id unik, script inline langsung setelah elemen
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-countdown">
    <div class="inv-card-label">— Menghitung Hari Menuju Hari Bahagia —</div>
    <div class="cd-row">
        <div class="cd-unit-wrap">
            <span class="cd-num" id="inv-cd-d">--</span>
            <div class="cd-lbl">Hari</div>
        </div>
        <div class="cd-colon">:</div>
        <div class="cd-unit-wrap">
            <span class="cd-num" id="inv-cd-h">--</span>
            <div class="cd-lbl">Jam</div>
        </div>
        <div class="cd-colon">:</div>
        <div class="cd-unit-wrap">
            <span class="cd-num" id="inv-cd-m">--</span>
            <div class="cd-lbl">Menit</div>
        </div>
        <div class="cd-colon">:</div>
        <div class="cd-unit-wrap">
            <span class="cd-num" id="inv-cd-s">--</span>
            <div class="cd-lbl">Detik</div>
        </div>
    </div>
</div>

<script>
/* ── COUNTDOWN ─────────────────────────────────── */
(function startCountdown() {
    var ids = { d:'inv-cd-d', h:'inv-cd-h', m:'inv-cd-m', s:'inv-cd-s' };
    var target = new Date('2026-07-19T10:00:00+07:00').getTime();

    function pad(n){ return n < 10 ? '0'+n : ''+n; }

    function tick() {
        /* Cari elemen — jika belum ada, tunggu */
        var elD = document.getElementById(ids.d);
        if (!elD) { setTimeout(tick, 200); return; }

        var now  = Date.now();
        var diff = Math.max(0, target - now);

        var days  = Math.floor(diff / 86400000);
        var hours = Math.floor((diff % 86400000) / 3600000);
        var mins  = Math.floor((diff % 3600000)  / 60000);
        var secs  = Math.floor((diff % 60000)    / 1000);

        document.getElementById(ids.d).textContent = pad(days);
        document.getElementById(ids.h).textContent = pad(hours);
        document.getElementById(ids.m).textContent = pad(mins);
        document.getElementById(ids.s).textContent = pad(secs);
    }

    /* Coba segera; jika DOM belum siap, coba lagi */
    tick();
    setInterval(tick, 1000);
})();

/* ── MUSIC ─────────────────────────────────────── */
(function initMusic() {
    var audio    = document.getElementById('bg-audio');
    var btn      = document.getElementById('music-btn');
    var label    = document.getElementById('music-label');
    if (!audio || !btn) { setTimeout(initMusic, 300); return; }

    var playing  = false;
    var labelTO  = null;

    function showLabel(txt) {
        label.textContent = txt;
        label.classList.add('show');
        clearTimeout(labelTO);
        labelTO = setTimeout(function(){ label.classList.remove('show'); }, 3000);
    }

    function doPlay() {
        audio.volume = 0.65;
        var p = audio.play();
        if (p) p.then(function(){
            playing = true;
            btn.textContent = '♫';
            btn.classList.add('playing');
            showLabel('♫ Janji Suci — Yovie & Nuno');
        }).catch(function(){
            btn.textContent = '♪';
            btn.classList.remove('playing');
            showLabel('Klik ♪ untuk memutar musik');
        });
    }

    /* Autoplay setelah interaksi pertama user */
    function onFirstInteract() {
        if (!playing) doPlay();
        document.removeEventListener('click',    onFirstInteract);
        document.removeEventListener('scroll',   onFirstInteract);
        document.removeEventListener('touchstart', onFirstInteract);
    }
    document.addEventListener('click',     onFirstInteract, { once: true });
    document.addEventListener('scroll',    onFirstInteract, { once: true });
    document.addEventListener('touchstart',onFirstInteract, { once: true });

    /* Coba langsung (autoplay policy permissive) */
    setTimeout(doPlay, 600);

    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (playing) {
            audio.pause();
            playing = false;
            btn.textContent = '♪';
            btn.classList.remove('playing');
            showLabel('⏸ Musik dijeda');
        } else {
            doPlay();
        }
    });
})();
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  LOKASI
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-card" style="text-align:center;margin-top:4px">
    <div class="inv-card-label">— Lokasi Acara —</div>
    <div style="font-family:'Playfair Display',serif;font-size:18px;color:#c9a84c;letter-spacing:1px;margin:8px 0 5px">
        Dusun II Sumberingin
    </div>
    <div style="font-size:12px;color:#ddc9a8;opacity:0.55;font-style:italic;line-height:2">
        Desa Namo Bintang<br>Minggu, 19 Juli 2026 &nbsp;·&nbsp; Pukul 10.00 WIB
    </div>
    <div style="margin-top:18px">
        <a class="inv-map-btn" href="https://maps.app.goo.gl/8G9hHHY9LzdGg5yc6" target="_blank">
            Buka Google Maps
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

divider()

# ══════════════════════════════════════════════════════════════
#  KHITANAN
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;margin:0 24px 4px;position:relative;z-index:1">
    <div style="font-size:9px;letter-spacing:4px;text-transform:uppercase;color:#c9a84c;opacity:0.35;margin-bottom:10px">
        Serta Turut Mengundang Acara Khitanan
    </div>
    <div style="font-family:'Playfair Display',serif;font-size:22px;color:#c9a84c;opacity:0.7;letter-spacing:1px">
        Ahmad Hanafi
    </div>
</div>
""", unsafe_allow_html=True)

divider()

# ══════════════════════════════════════════════════════════════
#  TURUT MENGUNDANG
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-card">
    <div class="inv-card-label">— Turut Mengundang —</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Pihak Wanita", "Pihak Pria"])

def list_html(items):
    rows = "".join([
        f'<li style="font-size:13px;color:#ddc9a8;opacity:0.65;padding:8px 0;border-bottom:1px solid rgba(201,168,76,0.05);line-height:1.6">{i}</li>'
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

# ══════════════════════════════════════════════════════════════
#  RSVP
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-card">
    <div class="inv-card-label">— Konfirmasi Kehadiran —</div>
    <p class="inv-body" style="font-size:12px;margin-bottom:0">
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

# ══════════════════════════════════════════════════════════════
#  DO'A & UCAPAN
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-card" style="margin-top:8px">
    <div class="inv-card-label">— Do'a &amp; Ucapan —</div>
</div>
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
            st.session_state.wishes.insert(0, {
                "name": wish_name.strip(),
                "text": wish_text.strip(),
                "time": "Baru saja"
            })
            st.rerun()
        else:
            st.warning("Mohon isi nama dan ucapan Anda.")
    st.markdown('</div>', unsafe_allow_html=True)

divider()

# ══════════════════════════════════════════════════════════════
#  AYAT
# ══════════════════════════════════════════════════════════════
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

# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="inv-footer">
    <div class="inv-ornament" style="margin-bottom:20px;font-size:11px;letter-spacing:12px">✦ ✦ ✦</div>
    <div class="inv-footer-names">Intan &amp; Syahrial</div>
    <div class="inv-footer-sub" style="margin-top:6px">19 Juli 2026 &nbsp;·&nbsp; Namo Bintang</div>
    <div style="margin-top:20px;font-size:11px;color:#c9a84c;opacity:0.18;font-style:italic">
        Wassalamu'alaikum Warahmatullahi Wabarakatuh
    </div>
    <div style="margin-top:14px;font-size:10px;color:#c9a84c;opacity:0.12;line-height:2">
        Kel. Mempelai Wanita — Alm. Bapak Fadli &amp; Ibu Sri Sumarti<br>
        Kel. Mempelai Pria — Alm. Bapak Paimo &amp; Ibu Suriani
    </div>
</div>
""", unsafe_allow_html=True)
