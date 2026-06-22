import streamlit as st
import json
import os
import base64

st.set_page_config(
    page_title="Undangan Pernikahan Intan & Syahrial",
    page_icon="🌸",
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

# Check for music file with various possible names
music_file_names = [
    "janji-suci.mp3",
    "Vovie & Nuno - Janji Suci (Video Clip).mp3",
    "Vovie & Nuno - Janji Suci.mp3",
    "Janji Suci.mp3"
]

music_file = None
for name in music_file_names:
    test_path = os.path.join(os.path.dirname(__file__), name)
    if os.path.exists(test_path):
        music_file = test_path
        break

music_exists = music_file is not None

# ══════════════════════════════════════════════════════════════
#  GLOBAL STYLES + ELEGANT SAKURA BACKGROUND
# ══════════════════════════════════════════════════════════════
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">

<style>
* { margin:0; padding:0; box-sizing:border-box; }

[data-testid="stAppViewContainer"] {
    background: #0d0208 !important;
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
.stDeployButton { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden !important; }

[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 540px !important;
    margin: 0 auto !important;
}

body, .stMarkdown, p, div {
    font-family: 'Cormorant Garamond', serif !important;
    color: #f5e6d3 !important;
}

/* ── ELEGANT SAKURA BACKGROUND ── */
#sakura-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.sakura-petal-bg {
    position: absolute;
    opacity: 0.06;
    font-size: 28px;
    animation: floatPetal 20s infinite ease-in-out;
    color: #ffb6c1;
}
@keyframes floatPetal {
    0% { transform: translate(0, 0) rotate(0deg); opacity: 0.06; }
    25% { transform: translate(30px, -20px) rotate(90deg); opacity: 0.10; }
    50% { transform: translate(-20px, -40px) rotate(180deg); opacity: 0.04; }
    75% { transform: translate(20px, -60px) rotate(270deg); opacity: 0.10; }
    100% { transform: translate(0, -80px) rotate(360deg); opacity: 0.06; }
}
.sakura-petal-bg:nth-child(1) { left: 5%; animation-delay: 0s; animation-duration: 22s; }
.sakura-petal-bg:nth-child(2) { left: 15%; animation-delay: 3s; animation-duration: 18s; font-size: 20px; }
.sakura-petal-bg:nth-child(3) { left: 30%; animation-delay: 6s; animation-duration: 25s; }
.sakura-petal-bg:nth-child(4) { left: 45%; animation-delay: 2s; animation-duration: 20s; font-size: 24px; }
.sakura-petal-bg:nth-child(5) { left: 60%; animation-delay: 8s; animation-duration: 23s; }
.sakura-petal-bg:nth-child(6) { left: 75%; animation-delay: 4s; animation-duration: 19s; font-size: 22px; }
.sakura-petal-bg:nth-child(7) { left: 88%; animation-delay: 10s; animation-duration: 21s; }
.sakura-petal-bg:nth-child(8) { left: 50%; animation-delay: 12s; animation-duration: 26s; font-size: 18px; }

/* Soft glow overlay */
#glow-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    background: 
        radial-gradient(ellipse at 20% 10%, rgba(255,182,193,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(255,182,193,0.03) 0%, transparent 40%),
        radial-gradient(ellipse at 50% 100%, rgba(139,28,46,0.06) 0%, transparent 50%);
}

/* ── MUSIC BUTTON ── */
#music-btn {
    position: fixed;
    bottom: 24px; right: 24px;
    width: 52px; height: 52px;
    border-radius: 50%;
    background: rgba(13,2,8,0.9);
    border: 1.5px solid #c9a84c;
    color: #c9a84c;
    font-size: 22px;
    cursor: pointer;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 24px rgba(201,168,76,0.2);
    transition: all 0.3s;
}
#music-btn:hover { background: rgba(201,168,76,0.15); transform: scale(1.1); }
#music-btn.paused { opacity: 0.55; }
#music-btn.playing {
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 24px rgba(201,168,76,0.2); }
    50% { box-shadow: 0 0 40px rgba(201,168,76,0.4), 0 0 60px rgba(255,160,180,0.1); }
    100% { box-shadow: 0 0 24px rgba(201,168,76,0.2); }
}

#music-indicator {
    position: fixed;
    bottom: 84px; right: 20px;
    background: rgba(13,2,8,0.92);
    border: 1px solid rgba(201,168,76,0.35);
    color: #c9a84c;
    font-family: 'Cormorant Garamond', serif;
    font-size: 11px;
    letter-spacing: 1.5px;
    padding: 6px 14px;
    z-index: 9999;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.4s;
    pointer-events: none;
}
#music-indicator.show { opacity: 1; }

/* ── HERO ── */
.hero-wrap {
    text-align: center;
    padding: 40px 24px 30px;
    position: relative;
    z-index: 1;
}
.bismillah-text {
    font-size: 22px;
    color: #c9a84c;
    margin-bottom: 6px;
    letter-spacing: 2px;
    text-shadow: 0 0 20px rgba(201,168,76,0.3);
}
.salam-text {
    font-size: 12px;
    color: #c9a84c;
    opacity: 0.75;
    font-style: italic;
    letter-spacing: 1.5px;
}
.sakura-branch {
    text-align: center;
    font-size: 32px;
    margin: 12px 0 24px;
    filter: drop-shadow(0 0 8px rgba(255,160,180,0.2));
    opacity: 0.6;
}

/* ── PHOTO FRAME ── */
.frame-outer {
    position: relative;
    width: 240px;
    margin: 0 auto 20px;
}
.frame-outer img {
    width: 100%;
    height: 310px;
    object-fit: cover;
    display: block;
    border: 1.5px solid rgba(201,168,76,0.55);
    outline: 5px solid rgba(13,2,8,0.85);
    outline-offset: -9px;
}
.frame-corner {
    position: absolute;
    width: 24px; height: 24px;
    border-color: #c9a84c;
    border-style: solid;
}
.fc-tl { top:-4px; left:-4px; border-width:2px 0 0 2px; }
.fc-tr { top:-4px; right:-4px; border-width:2px 2px 0 0; }
.fc-bl { bottom:-4px; left:-4px; border-width:0 0 2px 2px; }
.fc-br { bottom:-4px; right:-4px; border-width:0 2px 2px 0; }
.frame-petal {
    position: absolute;
    font-size: 14px;
    filter: drop-shadow(0 0 4px rgba(255,160,180,0.3));
    pointer-events: none;
    opacity: 0.5;
}
.fp-tl { top:-10px; left:-10px; transform:rotate(-30deg); }
.fp-tr { top:-10px; right:-10px; transform:rotate(30deg); }
.fp-bl { bottom:-10px; left:-10px; transform:rotate(-150deg); }
.fp-br { bottom:-10px; right:-10px; transform:rotate(150deg); }

/* ── GALLERY ── */
.gallery-row {
    display: flex; gap: 8px;
    justify-content: center;
    margin: 0 0 28px;
    padding: 0 20px;
}
.gallery-row img {
    width: calc(33.33% - 6px);
    height: 115px;
    object-fit: cover;
    border: 1px solid rgba(201,168,76,0.3);
    transition: border-color 0.3s, transform 0.3s;
}
.gallery-row img:hover { border-color:#c9a84c; transform:scale(1.03); }

/* ── COUPLE NAME ── */
.undangan-label {
    font-size: 10px; letter-spacing: 6px;
    text-transform: uppercase; color:#c9a84c; opacity:0.55; margin-bottom:8px;
}
.couple-script {
    font-family:'Great Vibes',cursive !important;
    font-size:62px !important; color:#c9a84c !important;
    line-height:1.05;
    text-shadow: 0 0 40px rgba(201,168,76,0.3), 0 0 80px rgba(255,160,180,0.1);
}
.ampersand-script {
    font-family:'Great Vibes',cursive !important;
    font-size:38px !important; color:#8b1c2e !important;
    display:block; margin:-6px 0;
}
.date-sub {
    font-size:11px; letter-spacing:3px; color:#c9a84c;
    opacity:0.45; margin-top:12px; text-transform:uppercase;
}

/* ── GOLD DIVIDER ── */
.gold-divider {
    display:flex; align-items:center; gap:10px;
    margin:22px auto; max-width:320px; padding:0 24px;
}
.gd-line { flex:1; height:1px; background:linear-gradient(to right,transparent,#c9a84c,transparent); opacity:0.4; }
.gd-petal { font-size:12px; filter:drop-shadow(0 0 4px rgba(255,160,180,0.3)); opacity:0.4; }
.gd-diamond { width:4px;height:4px;background:#c9a84c;transform:rotate(45deg);flex-shrink:0; opacity:0.4; }

/* ── SECTION CARD ── */
.s-card {
    margin:0 20px 20px;
    border:1px solid rgba(201,168,76,0.12);
    padding:28px 24px;
    position:relative;
    background:rgba(139,28,46,0.03);
    z-index: 1;
    backdrop-filter: blur(2px);
}
.s-card-top::before {
    content:''; position:absolute;
    top:-1px; left:16px; right:16px; height:1px;
    background:linear-gradient(to right,transparent,#c9a84c,transparent);
    opacity:0.4;
}
.s-card::after {
    content:''; position:absolute;
    bottom:-1px; left:16px; right:16px; height:1px;
    background:linear-gradient(to right,transparent,#c9a84c,transparent);
    opacity:0.4;
}
.s-label {
    font-size:9px; letter-spacing:4px; text-transform:uppercase;
    color:#c9a84c; opacity:0.5; margin-bottom:14px; text-align:center;
}
.intro-p { font-size:13.5px; line-height:2.1; text-align:center; color:#e8d5c0 !important; opacity:0.85; }

/* ── MEMPELAI ── */
.mempelai-name {
    font-family:'Great Vibes',cursive !important;
    font-size:38px !important; color:#c9a84c !important;
    text-align:center; display:block; line-height:1.15;
    text-shadow:0 0 24px rgba(201,168,76,0.15);
}
.mempelai-parents { font-size:12px; color:#c9a84c; opacity:0.55; font-style:italic; text-align:center; margin-top:4px; }

/* ── EVENTS ── */
.events-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:0 20px 20px; z-index:1; position:relative; }
.event-card {
    border:1px solid rgba(201,168,76,0.2);
    padding:22px 14px; text-align:center;
    background:rgba(255,182,193,0.02);
    position:relative; overflow:hidden;
}
.event-card::before {
    content:'🌸';
    position:absolute; top:6px; right:8px;
    font-size:12px; opacity:0.15;
}
.ev-type { font-size:9px; letter-spacing:3px; text-transform:uppercase; color:#c9a84c; margin-bottom:10px; opacity:0.7; }
.ev-day { font-family:'Playfair Display',serif !important; font-size:44px !important; font-weight:700 !important; color:#c9a84c !important; line-height:1; }
.ev-monthyear { font-size:10px; letter-spacing:2px; color:#c9a84c; opacity:0.55; text-transform:uppercase; margin:4px 0 10px; }
.ev-time { font-size:12px; color:#e8d5c0; opacity:0.7; margin-bottom:8px; }
.ev-loc { font-size:11px; color:#c9a84c; opacity:0.5; line-height:1.6; font-style:italic; }

/* ── COUNTDOWN ── */
.countdown-wrap {
    margin:0 20px 20px; padding:28px 20px;
    border:1px solid rgba(201,168,76,0.1);
    background:linear-gradient(135deg,rgba(139,28,46,0.05),rgba(255,182,193,0.02));
    text-align:center; position:relative; overflow:hidden;
    z-index: 1;
}
.countdown-wrap::before {
    content:'🌸';
    position:absolute; top:8px; left:50%; transform:translateX(-50%);
    font-size:14px; opacity:0.1;
}
.cd-grid { display:flex; justify-content:center; gap:12px; margin-top:16px; }
.cd-block { text-align:center; min-width:56px; }
.cd-num {
    font-family:'Playfair Display',serif !important;
    font-size:40px !important; font-weight:700 !important; color:#c9a84c !important;
    display:block; line-height:1;
    text-shadow:0 0 24px rgba(201,168,76,0.2);
}
.cd-unit { font-size:9px; letter-spacing:2px; text-transform:uppercase; color:#c9a84c; opacity:0.4; margin-top:5px; }
.cd-sep { font-family:'Playfair Display',serif; font-size:32px; color:#c9a84c; opacity:0.25; align-self:flex-start; padding-top:6px; line-height:1; }

/* ── LOCATION ── */
.khit-card { margin:0 20px 20px; border:1px solid rgba(201,168,76,0.15); padding:24px; text-align:center; background:rgba(255,182,193,0.015); z-index:1; position:relative; }
.khit-also { font-size:9px; letter-spacing:4px; color:#c9a84c; opacity:0.4; text-transform:uppercase; margin-bottom:8px; }
.khit-title { font-family:'Great Vibes',cursive !important; font-size:36px !important; color:#c9a84c !important; margin-bottom:4px; }

/* ── WISH ── */
.wish-item { padding:12px 0; border-bottom:1px solid rgba(201,168,76,0.06); }
.wish-name-label { font-size:12px; color:#c9a84c; font-weight:600; margin-bottom:4px; opacity:0.8; }
.wish-body { font-size:13px; color:#e8d5c0; opacity:0.75; font-style:italic; line-height:1.7; }
.wish-time { font-size:10px; color:#c9a84c; opacity:0.3; margin-top:4px; }

/* ── FOOTER ── */
.footer-wrap { text-align:center; padding:32px 24px 56px; border-top:1px solid rgba(201,168,76,0.08); position:relative; z-index:1; }
.footer-names { font-family:'Great Vibes',cursive !important; font-size:34px !important; color:#c9a84c !important; margin-bottom:8px; }
.footer-sub { font-size:10px; letter-spacing:3px; color:#c9a84c; opacity:0.35; text-transform:uppercase; margin-bottom:12px; }
.wassalam { font-size:11px; color:#c9a84c; opacity:0.25; font-style:italic; }

/* ── STREAMLIT OVERRIDES ── */
hr { border-color:rgba(201,168,76,0.08) !important; }
.stButton > button {
    background:transparent !important; border:1px solid rgba(201,168,76,0.4) !important;
    color:#c9a84c !important; font-family:'Cormorant Garamond',serif !important;
    font-size:11px !important; letter-spacing:3px !important; text-transform:uppercase !important;
    padding:10px 20px !important; border-radius:0 !important; width:100%;
}
.stButton > button:hover { background:rgba(201,168,76,0.1) !important; border-color:#c9a84c !important; }
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background:rgba(255,255,255,0.02) !important; border:1px solid rgba(201,168,76,0.2) !important;
    border-radius:0 !important; color:#f5e6d3 !important;
    font-family:'Cormorant Garamond',serif !important; font-size:14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus { border-color:#c9a84c !important; box-shadow:none !important; }
.stTextInput label, .stTextArea label, .stRadio label {
    color:#c9a84c !important; font-family:'Cormorant Garamond',serif !important;
    font-size:11px !important; letter-spacing:2px !important; text-transform:uppercase !important; opacity:0.6 !important;
}
.stRadio > div > label {
    color:#c9a84c !important; font-size:13px !important; letter-spacing:1px !important; text-transform:none !important;
    background:rgba(201,168,76,0.03) !important; border:1px solid rgba(201,168,76,0.15) !important;
    padding:8px 16px !important; border-radius:0 !important;
}
.stSuccess, .stInfo { background:rgba(139,28,46,0.15) !important; border:1px solid rgba(201,168,76,0.2) !important; border-radius:0 !important; color:#c9a84c !important; }
</style>

<!-- ══ ELEGANT SAKURA BACKGROUND ══ -->
<div id="sakura-bg">
    <div class="sakura-petal-bg">🌸</div>
    <div class="sakura-petal-bg">🌸</div>
    <div class="sakura-petal-bg">🌸</div>
    <div class="sakura-petal-bg">🌸</div>
    <div class="sakura-petal-bg">🌸</div>
    <div class="sakura-petal-bg">🌸</div>
    <div class="sakura-petal-bg">🌸</div>
    <div class="sakura-petal-bg">🌸</div>
</div>
<div id="glow-overlay"></div>

<!-- ══ MUSIC BUTTON ══ -->
<div id="music-indicator">🎵 Janji Suci — Yovie &amp; Nuno</div>
<button id="music-btn" class="playing">♪</button>

<!-- ══ AUDIO ══ -->
<audio id="bg-audio" loop preload="auto">
""", unsafe_allow_html=True)

# Use local MP3 if exists
if music_exists:
    with open(music_file, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <source src="data:audio/mpeg;base64,{audio_data}" type="audio/mpeg">
    """, unsafe_allow_html=True)
else:
    # Fallback ke musik online
    st.markdown("""
    <source src="https://ia800905.us.archive.org/19/items/FREE_background_music_dac/07_-_Music_Box.mp3" type="audio/mpeg">
    """, unsafe_allow_html=True)

st.markdown("""
</audio>

<script>
// ============================================================
// ELEGANT SAKURA BACKGROUND - floating petals
// ============================================================
(function(){
    var petals = document.querySelectorAll('.sakura-petal-bg');
    petals.forEach(function(petal, index) {
        var duration = 18 + Math.random() * 10;
        var delay = Math.random() * 15;
        var startX = Math.random() * 90 + 5;
        var size = 18 + Math.random() * 20;
        petal.style.left = startX + '%';
        petal.style.fontSize = size + 'px';
        petal.style.animationDuration = duration + 's';
        petal.style.animationDelay = delay + 's';
        petal.style.opacity = 0.04 + Math.random() * 0.08;
    });
})();

// ============================================================
// MUSIC - Janji Suci by Yovie & Nuno
// ============================================================
(function(){
    var audio = document.getElementById('bg-audio');
    var btn = document.getElementById('music-btn');
    var indicator = document.getElementById('music-indicator');
    
    var isPlaying = false;
    var tooltipTimeout = null;
    
    function showIndicator(msg) {
        if (!indicator) return;
        indicator.textContent = msg;
        indicator.classList.add('show');
        clearTimeout(tooltipTimeout);
        tooltipTimeout = setTimeout(function(){
            indicator.classList.remove('show');
        }, 3000);
    }
    
    // Auto-play music
    if (audio) {
        audio.volume = 0.7;
        var promise = audio.play();
        if (promise !== undefined) {
            promise.then(function(){
                isPlaying = true;
                btn.textContent = '♪';
                btn.classList.remove('paused');
                btn.classList.add('playing');
                showIndicator('🎵 Janji Suci — Yovie & Nuno');
            }).catch(function(){
                isPlaying = false;
                btn.textContent = '🎵';
                btn.classList.add('paused');
                btn.classList.remove('playing');
                showIndicator('🔇 Klik untuk putar musik');
            });
        }
    }
    
    // Toggle music
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        if (!audio) return;
        
        if (isPlaying) {
            audio.pause();
            btn.textContent = '♩';
            btn.classList.add('paused');
            btn.classList.remove('playing');
            isPlaying = false;
            showIndicator('⏸ Musik dijeda');
        } else {
            audio.play().then(function(){
                btn.textContent = '♪';
                btn.classList.remove('paused');
                btn.classList.add('playing');
                isPlaying = true;
                showIndicator('▶ Janji Suci — Yovie & Nuno');
            }).catch(function(){
                showIndicator('❌ Gagal memutar musik');
            });
        }
    });
    
    // Handle audio ended
    audio.addEventListener('ended', function() {
        audio.currentTime = 0;
        audio.play();
    });
})();

// ============================================================
// COUNTDOWN - FIXED (berjalan setiap detik)
// ============================================================
(function(){
    function pad(n){ return String(n).padStart(2,'0'); }
    
    function updateCountdown(){
        var target = new Date('2026-07-19T10:00:00+07:00').getTime();
        var now = Date.now();
        var diff = Math.max(0, target - now);
        
        var days = Math.floor(diff / 86400000);
        var hours = Math.floor((diff % 86400000) / 3600000);
        var minutes = Math.floor((diff % 3600000) / 60000);
        var seconds = Math.floor((diff % 60000) / 1000);
        
        var ids = ['cd-days', 'cd-hours', 'cd-mins', 'cd-secs'];
        var vals = [days, hours, minutes, seconds];
        
        for(var i = 0; i < ids.length; i++){
            var el = document.getElementById(ids[i]);
            if(el) {
                el.textContent = pad(vals[i]);
            }
        }
    }
    
    // Jalankan langsung dan setiap detik
    updateCountdown();
    setInterval(updateCountdown, 1000);
})();
</script>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────
def gold_divider():
    st.markdown("""
    <div class="gold-divider">
        <div class="gd-line"></div>
        <div class="gd-petal">🌸</div>
        <div class="gd-diamond"></div>
        <div class="gd-petal">🌸</div>
        <div class="gd-line"></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CONTENT
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="bismillah-text">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
    <div class="sakura-branch">🌸 🌿 🌸</div>
    <div class="salam-text">Assalamu'alaikum Warahmatullahi Wabarakatuh</div>
</div>
""", unsafe_allow_html=True)

# ── Foto Utama ──
if photos.get("foto1"):
    st.markdown(f"""
    <div style="padding:0 20px;margin-bottom:14px">
        <div class="frame-outer">
            <div class="frame-corner fc-tl"></div><div class="frame-corner fc-tr"></div>
            <div class="frame-corner fc-bl"></div><div class="frame-corner fc-br"></div>
            <span class="frame-petal fp-tl">🌸</span>
            <span class="frame-petal fp-tr">🌸</span>
            <span class="frame-petal fp-bl">🌸</span>
            <span class="frame-petal fp-br">🌸</span>
            <img src="data:image/png;base64,{photos['foto1']}" alt="Foto Mempelai"/>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Gallery ──
if photos.get("foto2") and photos.get("foto3"):
    st.markdown(f"""
    <div class="gallery-row">
        <img src="data:image/png;base64,{photos['foto1']}" alt="foto 1"/>
        <img src="data:image/png;base64,{photos['foto2']}" alt="foto 2"/>
        <img src="data:image/png;base64,{photos['foto3']}" alt="foto 3"/>
    </div>""", unsafe_allow_html=True)

# ── Nama Mempelai ──
st.markdown("""
<div style="text-align:center;padding:0 24px 4px">
    <div class="undangan-label">🌸 Undangan Pernikahan 🌸</div>
    <div class="couple-script">Intan</div>
    <div class="ampersand-script">&</div>
    <div class="couple-script">Syahrial</div>
    <div class="date-sub">19 Juli 2026 · Desa Namo Bintang</div>
</div>
""", unsafe_allow_html=True)

gold_divider()

# ══════════════════════════════════════════════════════════════
#  PEMBUKA
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 20px">
    <div class="s-label">— 🌸 Dengan Rahmat Allah Subhanahu Wa Ta'ala 🌸 —</div>
    <p class="intro-p">
        Maha Suci Allah yang telah menciptakan makhluk-Nya berpasang-pasangan.<br><br>
        Ya Allah, perkenankanlah kami menikahkan putra-putri kami untuk mengikuti
        Sunnah Rasul-Mu, melakukan Syariat Agama-Mu dalam rangka membentuk keluarga
        yang Sakinah, Mawaddah, Warahmah. Maka izinkanlah kami menikahkannya.
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  MEMPELAI
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 8px">
    <div class="s-label">— Mempelai Wanita —</div>
    <span class="mempelai-name">Intan Candra Nurul Hafizah</span>
    <div class="mempelai-parents">Putri dari Alm. Bapak Fadli &amp; Ibu Sri Sumarti (Wiwik)</div>
</div>
<div style="text-align:center;margin:10px 0;font-size:24px;filter:drop-shadow(0 0 6px rgba(255,160,180,0.2));opacity:0.5">🌸</div>
<div style="text-align:center;margin:-4px 0 10px">
    <span style="font-family:'Great Vibes',cursive;font-size:42px;color:#8b1c2e;opacity:0.7">&amp;</span>
</div>
<div class="s-card" style="margin:0 20px 24px">
    <div class="s-label">— Mempelai Pria —</div>
    <span class="mempelai-name">Syahrial / Gombeng</span>
    <div class="mempelai-parents">Putra dari Alm. Bapak Paimo &amp; Ibu Suriani</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  EVENTS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="events-grid">
    <div class="event-card">
        <div class="ev-type">✦ Akad Nikah ✦</div>
        <div class="ev-day">17</div>
        <div class="ev-monthyear">Juli · 2026</div>
        <div class="ev-time">Jum'at · 08.00 WIB</div>
        <div class="ev-loc">Dusun II Sumberingin<br>Desa Namo Bintang</div>
    </div>
    <div class="event-card">
        <div class="ev-type">✦ Resepsi ✦</div>
        <div class="ev-day">19</div>
        <div class="ev-monthyear">Juli · 2026</div>
        <div class="ev-time">Minggu · 10.00 WIB</div>
        <div class="ev-loc">Dusun II Sumberingin<br>Desa Namo Bintang</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  COUNTDOWN
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="countdown-wrap">
    <div class="s-label">— Menghitung Hari Menuju Hari Bahagia —</div>
    <div class="cd-grid">
        <div class="cd-block"><span class="cd-num" id="cd-days">00</span><div class="cd-unit">Hari</div></div>
        <div class="cd-sep">:</div>
        <div class="cd-block"><span class="cd-num" id="cd-hours">00</span><div class="cd-unit">Jam</div></div>
        <div class="cd-sep">:</div>
        <div class="cd-block"><span class="cd-num" id="cd-mins">00</span><div class="cd-unit">Menit</div></div>
        <div class="cd-sep">:</div>
        <div class="cd-block"><span class="cd-num" id="cd-secs">00</span><div class="cd-unit">Detik</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  LOKASI
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 16px;text-align:center">
    <div class="s-label">— Lokasi Acara —</div>
    <div style="font-size:28px;margin:4px 0;filter:drop-shadow(0 0 8px rgba(255,160,180,0.15));opacity:0.4">📍</div>
    <div style="font-family:'Playfair Display',serif;font-size:17px;color:#c9a84c;margin:10px 0 6px;letter-spacing:1px">
        Dusun II Sumberingin
    </div>
    <div style="font-size:12px;color:#e8d5c0;opacity:0.65;font-style:italic;line-height:2">
        Desa Namo Bintang<br>
        Minggu, 19 Juli 2026 · Pukul 10.00 WIB
    </div>
</div>
<div style="text-align:center;margin:0 20px 24px">
    <a href="https://maps.app.goo.gl/8G9hHHY9LzdGg5yc6" target="_blank"
       style="display:inline-block;padding:14px 40px;
              border:1px solid #c9a84c;
              color:#c9a84c;font-family:'Cormorant Garamond',serif;
              font-size:12px;letter-spacing:4px;text-transform:uppercase;
              text-decoration:none;background:rgba(201,168,76,0.04);
              transition:all 0.3s">
        🗺️ &nbsp; Buka Google Maps
    </a>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  KHITANAN
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="khit-card">
    <div class="khit-also">— Serta Khitanan —</div>
    <div style="font-size:18px;margin:4px 0;opacity:0.2">🌸</div>
    <div class="khit-title">Ahmad Hanafi</div>
</div>
""", unsafe_allow_html=True)

gold_divider()

# ══════════════════════════════════════════════════════════════
#  TURUT MENGUNDANG
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 4px">
    <div class="s-label">— 🌸 Turut Mengundang 🌸 —</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌸 Pihak Wanita", "🎩 Pihak Pria"])

with tab1:
    wanita = [
        "Alm. Mandah / Ngatiyem (Kakek & Nenek)",
        "Muri / Anik (Kakek & Nenek)", "Dasem (Nenek)",
        "Sukar / Iyet (Kakek & Nenek)", "Ribut / Ngatisah (Kakek & Nenek)",
        "Alm. Jarno / Muriatik (Kakek & Nenek)", "Sawon (Kakek)", "Karlan (Kakek)",
        "Watik / Misjo (Wawak)", "Gambreng / Tumik (Pakde & Bude)",
        "Endang Susanti / Ust. Lukman S.Pd.I (Bibik & Oom)",
        "Sri Wulan Handayani / Hendrik (Bibik & Oom)",
        "Ema (Adik)", "Ahamad Hanafi (Adik)",
    ]
    html = "".join([f'<li style="font-size:13px;color:#e8d5c0;opacity:0.7;padding:7px 0;border-bottom:1px solid rgba(255,182,193,0.05);line-height:1.5">🌸 {i}</li>' for i in wanita])
    st.markdown(f'<ul style="list-style:none;padding:12px 0 4px">{html}</ul>', unsafe_allow_html=True)

with tab2:
    pria = [
        "Marinem / Suparto (Nenek & Kakek)", "Ngatiyem / Alm. Joni (Nenek & Kakek)",
        "Alm. Paiko / Iyus (Wawak)", "Dedi / Rika (Abang)", "Yuda / Wulan (Abang)",
        "Diki / Dina (Adik)", "Igo Ardiansyah (Adik)", "Sugik / Yanti (Lelek)",
        "Minok / Susi (Lelek)", "Rame / Santo (Bibik)", "Yuni / Junedi (Bibik)",
    ]
    html2 = "".join([f'<li style="font-size:13px;color:#e8d5c0;opacity:0.7;padding:7px 0;border-bottom:1px solid rgba(255,182,193,0.05);line-height:1.5">🌸 {i}</li>' for i in pria])
    st.markdown(f'<ul style="list-style:none;padding:12px 0 4px">{html2}</ul>', unsafe_allow_html=True)

gold_divider()

# ══════════════════════════════════════════════════════════════
#  RSVP
# ══════════════════════════════════════════════════════════════
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
    rsvp_status = st.radio("", ["🌸 Hadir", "✦ Tidak Hadir"], horizontal=True, key="rsvp_status", label_visibility="collapsed")
    if st.button("Kirim Konfirmasi", key="submit_rsvp"):
        if rsvp_name.strip():
            if "Hadir" in rsvp_status and "Tidak" not in rsvp_status:
                st.success(f"🌸 Terima kasih, {rsvp_name}! Kami menantikan kehadiran Anda.")
            else:
                st.info(f"✦ Terima kasih, {rsvp_name}. Semoga selalu dalam lindungan Allah.")
        else:
            st.warning("Mohon isi nama Anda terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  DO'A & UCAPAN
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 0">
    <div class="s-label">— 🌸 Do'a &amp; Ucapan 🌸 —</div>
</div>
""", unsafe_allow_html=True)

for w in st.session_state.wishes:
    st.markdown(f"""
    <div class="wish-item" style="padding:12px 20px">
        <div class="wish-name-label">🌸 {w['name']}</div>
        <div class="wish-body">{w['text']}</div>
        <div class="wish-time">{w['time']}</div>
    </div>""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="padding:12px 20px 20px">', unsafe_allow_html=True)
    wish_name = st.text_input("", placeholder="Nama Anda...", key="wish_name", label_visibility="collapsed")
    wish_text = st.text_area("", placeholder="Tulis do'a dan ucapan untuk kedua mempelai...", key="wish_text", label_visibility="collapsed", height=100)
    if st.button("Kirim Ucapan 🌸", key="submit_wish"):
        if wish_name.strip() and wish_text.strip():
            st.session_state.wishes.insert(0, {"name": wish_name.strip(), "text": wish_text.strip(), "time": "Baru saja"})
            st.rerun()
        else:
            st.warning("Mohon isi nama dan ucapan Anda.")
    st.markdown('</div>', unsafe_allow_html=True)

gold_divider()

# ══════════════════════════════════════════════════════════════
#  AYAT
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 20px">
    <div class="s-label">— QS. Ar-Rum: 21 —</div>
    <div style="font-size:20px;text-align:center;margin-bottom:12px;filter:drop-shadow(0 0 6px rgba(255,160,180,0.15));opacity:0.4">🌸 🌿 🌸</div>
    <p style="font-size:13px;line-height:2.2;text-align:center;color:#e8d5c0;opacity:0.75;font-style:italic">
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
<div class="footer-wrap">
    <div style="font-size:24px;margin-bottom:16px;filter:drop-shadow(0 0 8px rgba(255,160,180,0.15));opacity:0.3">🌸 🌿 🌸</div>
    <div class="footer-names">Intan &amp; Syahrial</div>
    <div class="footer-sub">19 Juli 2026 · Namo Bintang</div>
    <div style="font-size:14px;color:#c9a84c;opacity:0.15;margin:12px 0;letter-spacing:8px">✦ ✦ ✦</div>
    <div class="wassalam">Wassalamu'alaikum Warahmatullahi Wabarakatuh</div>
    <div style="margin-top:20px;font-size:10px;color:#c9a84c;opacity:0.15;letter-spacing:1px;line-height:2">
        Kel. Mempelai Wanita · Alm. Bapak Fadli &amp; Ibu Sri Sumarti (Wiwik)<br>
        Kel. Mempelai Pria · Alm. Bapak Paimo &amp; Ibu Suriani
    </div>
    <div style="margin-top:24px;font-size:16px;opacity:0.1">🌸 🌸 🌸</div>
</div>
""", unsafe_allow_html=True)
