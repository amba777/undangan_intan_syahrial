import streamlit as st
import json, os

st.set_page_config(
    page_title="Undangan Pernikahan Intan & Syahrial",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Load photos ──
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

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

[data-testid="stAppViewContainer"]{
    background:#0d0208 !important;
    background-image:
        radial-gradient(ellipse at 20% 0%,rgba(255,182,193,0.07) 0%,transparent 45%),
        radial-gradient(ellipse at 80% 5%,rgba(255,182,193,0.05) 0%,transparent 40%),
        radial-gradient(ellipse at 50% 100%,rgba(139,28,46,0.12) 0%,transparent 50%) !important;
}
[data-testid="stHeader"]{background:transparent !important}
[data-testid="stToolbar"]{display:none !important}
.stDeployButton{display:none !important}
section[data-testid="stSidebar"]{display:none !important}
#MainMenu,footer,header{visibility:hidden !important}
[data-testid="block-container"]{padding:0 !important;max-width:540px !important;margin:0 auto !important}
body,.stMarkdown,p,div{font-family:'Cormorant Garamond',serif !important;color:#f5e6d3 !important}

/* sakura canvas fixed */
#sk-canvas{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1}

/* music btn */
#mu-btn{
    position:fixed;bottom:22px;right:22px;width:50px;height:50px;border-radius:50%;
    background:rgba(13,2,8,0.9);border:1.5px solid #c9a84c;color:#c9a84c;
    font-size:20px;cursor:pointer;z-index:9999;display:flex;align-items:center;
    justify-content:center;box-shadow:0 0 20px rgba(201,168,76,0.3);transition:all .3s;
}
#mu-btn:hover{background:rgba(201,168,76,0.15);transform:scale(1.1)}
#mu-tip{
    position:fixed;bottom:80px;right:18px;background:rgba(13,2,8,0.93);
    border:1px solid rgba(201,168,76,0.35);color:#c9a84c;
    font-family:'Cormorant Garamond',serif;font-size:11px;letter-spacing:1.5px;
    padding:6px 14px;z-index:9999;white-space:nowrap;opacity:0;
    transition:opacity .4s;pointer-events:none;
}
#mu-tip.show{opacity:1}

/* HERO */
.hero-wrap{text-align:center;padding:64px 24px 36px;position:relative}
.bismillah-text{font-size:22px;color:#c9a84c;margin-bottom:6px;letter-spacing:2px;text-shadow:0 0 20px rgba(201,168,76,.3)}
.salam-text{font-size:12px;color:#c9a84c;opacity:.75;font-style:italic;letter-spacing:1.5px}
.sakura-branch{font-size:28px;margin:14px 0 20px;filter:drop-shadow(0 0 10px rgba(255,160,180,.5))}

/* photo frame */
.frame-outer{position:relative;width:245px;margin:0 auto 16px}
.frame-outer img{width:100%;height:315px;object-fit:cover;display:block;border:1.5px solid rgba(201,168,76,.55);outline:5px solid rgba(13,2,8,.85);outline-offset:-9px}
.frame-corner{position:absolute;width:24px;height:24px;border-color:#c9a84c;border-style:solid}
.fc-tl{top:-4px;left:-4px;border-width:2px 0 0 2px}
.fc-tr{top:-4px;right:-4px;border-width:2px 2px 0 0}
.fc-bl{bottom:-4px;left:-4px;border-width:0 0 2px 2px}
.fc-br{bottom:-4px;right:-4px;border-width:0 2px 2px 0}
.fp{position:absolute;font-size:18px;filter:drop-shadow(0 0 4px rgba(255,160,180,.5));pointer-events:none}
.fp-tl{top:-14px;left:-14px;transform:rotate(-30deg)}
.fp-tr{top:-14px;right:-14px;transform:rotate(30deg)}
.fp-bl{bottom:-14px;left:-14px;transform:rotate(-150deg)}
.fp-br{bottom:-14px;right:-14px;transform:rotate(150deg)}

/* gallery */
.gallery-row{display:flex;gap:8px;justify-content:center;margin:0 0 26px;padding:0 20px}
.gallery-row img{width:calc(33.33% - 6px);height:115px;object-fit:cover;border:1px solid rgba(201,168,76,.3);transition:border-color .3s,transform .3s}
.gallery-row img:hover{border-color:#c9a84c;transform:scale(1.03)}

/* couple name */
.undangan-label{font-size:10px;letter-spacing:6px;text-transform:uppercase;color:#c9a84c;opacity:.55;margin-bottom:8px}
.couple-script{font-family:'Great Vibes',cursive !important;font-size:62px !important;color:#c9a84c !important;line-height:1.05;text-shadow:0 0 40px rgba(201,168,76,.3),0 0 80px rgba(255,160,180,.1)}
.ampersand-script{font-family:'Great Vibes',cursive !important;font-size:38px !important;color:#8b1c2e !important;display:block;margin:-6px 0}
.date-sub{font-size:11px;letter-spacing:3px;color:#c9a84c;opacity:.45;margin-top:12px;text-transform:uppercase}

/* divider */
.gold-divider{display:flex;align-items:center;gap:10px;margin:22px auto;max-width:320px;padding:0 24px}
.gd-line{flex:1;height:1px;background:linear-gradient(to right,transparent,#c9a84c,transparent)}
.gd-petal{font-size:14px;filter:drop-shadow(0 0 4px rgba(255,160,180,.5))}
.gd-diamond{width:6px;height:6px;background:#c9a84c;transform:rotate(45deg);flex-shrink:0}

/* section card */
.s-card{margin:0 20px 20px;border:1px solid rgba(201,168,76,.2);padding:28px 24px;position:relative;background:rgba(139,28,46,.04);backdrop-filter:blur(2px)}
.s-card-top::before{content:'';position:absolute;top:-1px;left:16px;right:16px;height:1px;background:linear-gradient(to right,transparent,#c9a84c,transparent)}
.s-card::after{content:'';position:absolute;bottom:-1px;left:16px;right:16px;height:1px;background:linear-gradient(to right,transparent,#c9a84c,transparent)}
.s-label{font-size:9px;letter-spacing:4px;text-transform:uppercase;color:#c9a84c;opacity:.6;margin-bottom:14px;text-align:center}
.intro-p{font-size:13.5px;line-height:2.1;text-align:center;color:#e8d5c0 !important;opacity:.88}

/* mempelai */
.mempelai-name{font-family:'Great Vibes',cursive !important;font-size:42px !important;color:#c9a84c !important;text-align:center;display:block;line-height:1.15;text-shadow:0 0 24px rgba(201,168,76,.2)}
.mempelai-parents{font-size:12px;color:#c9a84c;opacity:.65;font-style:italic;text-align:center;margin-top:4px}

/* events */
.events-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:0 20px 20px}
.event-card{border:1px solid rgba(201,168,76,.3);padding:22px 14px;text-align:center;background:rgba(255,182,193,.03);position:relative;overflow:hidden}
.event-card::before{content:'🌸';position:absolute;top:6px;right:8px;font-size:14px;opacity:.2}
.ev-type{font-size:9px;letter-spacing:3px;text-transform:uppercase;color:#c9a84c;margin-bottom:10px}
.ev-day{font-family:'Playfair Display',serif !important;font-size:44px !important;font-weight:700 !important;color:#c9a84c !important;line-height:1}
.ev-monthyear{font-size:10px;letter-spacing:2px;color:#c9a84c;opacity:.65;text-transform:uppercase;margin:4px 0 10px}
.ev-time{font-size:12px;color:#e8d5c0;opacity:.75;margin-bottom:8px}
.ev-loc{font-size:11px;color:#c9a84c;opacity:.6;line-height:1.6;font-style:italic}

/* countdown */
.countdown-wrap{margin:0 20px 20px;padding:28px 20px;border:1px solid rgba(201,168,76,.15);background:linear-gradient(135deg,rgba(139,28,46,.08),rgba(255,182,193,.04));text-align:center;position:relative;overflow:hidden}
.countdown-wrap::before{content:'🌸  🌸  🌸';position:absolute;top:8px;left:50%;transform:translateX(-50%);font-size:11px;opacity:.2;letter-spacing:8px}
.cd-grid{display:flex;justify-content:center;gap:12px;margin-top:16px}
.cd-block{text-align:center;min-width:58px}
.cd-num{font-family:'Playfair Display',serif !important;font-size:40px !important;font-weight:700 !important;color:#c9a84c !important;display:block;line-height:1;text-shadow:0 0 24px rgba(201,168,76,.35)}
.cd-unit{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#c9a84c;opacity:.5;margin-top:5px}
.cd-sep{font-family:'Playfair Display',serif;font-size:32px;color:#c9a84c;opacity:.35;align-self:flex-start;padding-top:6px;line-height:1}

/* khitanan */
.khit-card{margin:0 20px 20px;border:1px solid rgba(201,168,76,.22);padding:24px;text-align:center;background:rgba(255,182,193,.02)}
.khit-also{font-size:9px;letter-spacing:4px;color:#c9a84c;opacity:.5;text-transform:uppercase;margin-bottom:8px}
.khit-title{font-family:'Great Vibes',cursive !important;font-size:36px !important;color:#c9a84c !important;margin-bottom:4px}
.khit-name{font-family:'Playfair Display',serif !important;font-size:20px !important;color:#f5e6d3 !important;letter-spacing:1px}

/* wish */
.wish-item{padding:12px 0;border-bottom:1px solid rgba(201,168,76,.08)}
.wish-name-label{font-size:12px;color:#c9a84c;font-weight:600;margin-bottom:4px}
.wish-body{font-size:13px;color:#e8d5c0;opacity:.78;font-style:italic;line-height:1.7}
.wish-time{font-size:10px;color:#c9a84c;opacity:.4;margin-top:4px}

/* footer */
.footer-wrap{text-align:center;padding:32px 24px 60px;border-top:1px solid rgba(201,168,76,.1)}
.footer-names{font-family:'Great Vibes',cursive !important;font-size:34px !important;color:#c9a84c !important;margin-bottom:8px}
.footer-sub{font-size:10px;letter-spacing:3px;color:#c9a84c;opacity:.4;text-transform:uppercase;margin-bottom:12px}
.wassalam{font-size:11px;color:#c9a84c;opacity:.3;font-style:italic}

/* streamlit overrides */
hr{border-color:rgba(201,168,76,.1) !important}
.stButton>button{background:transparent !important;border:1px solid rgba(201,168,76,.5) !important;color:#c9a84c !important;font-family:'Cormorant Garamond',serif !important;font-size:11px !important;letter-spacing:3px !important;text-transform:uppercase !important;padding:10px 20px !important;border-radius:0 !important;width:100%}
.stButton>button:hover{background:rgba(201,168,76,.12) !important;border-color:#c9a84c !important}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:rgba(255,255,255,.03) !important;border:1px solid rgba(201,168,76,.25) !important;border-radius:0 !important;color:#f5e6d3 !important;font-family:'Cormorant Garamond',serif !important;font-size:14px !important}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:#c9a84c !important;box-shadow:none !important}
.stTextInput label,.stTextArea label,.stRadio label{color:#c9a84c !important;font-family:'Cormorant Garamond',serif !important;font-size:11px !important;letter-spacing:2px !important;text-transform:uppercase !important;opacity:.7 !important}
.stRadio>div>label{color:#c9a84c !important;font-size:13px !important;letter-spacing:1px !important;text-transform:none !important;background:rgba(201,168,76,.04) !important;border:1px solid rgba(201,168,76,.2) !important;padding:8px 16px !important;border-radius:0 !important}
.stSuccess,.stInfo{background:rgba(139,28,46,.2) !important;border:1px solid rgba(201,168,76,.3) !important;border-radius:0 !important;color:#c9a84c !important}
</style>

<!-- SAKURA CANVAS -->
<canvas id="sk-canvas"></canvas>

<!-- MUSIC BTN & TOOLTIP -->
<div id="mu-tip">🎵 Janji Suci — Yovie &amp; Nuno</div>
<button id="mu-btn" onclick="muToggle()">♪</button>

<!-- WELCOME OVERLAY — rendered as a normal div so pointer events work -->
<div id="wc-overlay" style="
    position:fixed;inset:0;
    background:rgba(10,2,6,0.9);
    display:flex;flex-direction:column;
    align-items:center;justify-content:center;
    z-index:99999;
">
  <div onclick="wcOpen()" style="
    border:1px solid rgba(201,168,76,0.55);
    padding:40px 52px;text-align:center;
    background:rgba(13,2,8,0.75);
    max-width:300px;cursor:pointer;
    transition:transform .2s;
  " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
    <div style="font-size:40px;margin-bottom:14px;filter:drop-shadow(0 0 14px rgba(255,160,180,.8))">🌸</div>
    <div style="font-family:'Great Vibes',cursive;font-size:30px;color:#c9a84c;line-height:1.2;margin-bottom:10px">
      Undangan<br>Pernikahan
    </div>
    <div style="font-size:10px;letter-spacing:4px;color:#c9a84c;opacity:.65;text-transform:uppercase;margin-bottom:28px">
      Intan &amp; Syahrial
    </div>
    <div style="
      border:1px solid #c9a84c;padding:13px 28px;
      font-family:'Cormorant Garamond',serif;
      font-size:11px;letter-spacing:3px;text-transform:uppercase;
      color:#c9a84c;margin-bottom:14px;
      background:rgba(201,168,76,0.06);
    ">♪ &nbsp; Buka Undangan</div>
    <div style="font-size:10px;color:#c9a84c;opacity:.4;letter-spacing:1px">
      🎵 Janji Suci — Yovie &amp; Nuno
    </div>
  </div>
</div>

<!-- AUDIO -->
<audio id="au" loop>
  <source src="https://ia800905.us.archive.org/19/items/FREE_background_music_dac/07_-_Music_Box.mp3" type="audio/mpeg">
</audio>

<script>
/* ═══════ SAKURA ═══════ */
(function(){
  var c=document.getElementById('sk-canvas');
  if(!c) return;
  var x=c.getContext('2d'),P=[],W,H;
  function rsz(){ W=c.width=window.innerWidth; H=c.height=window.innerHeight; }
  rsz(); window.addEventListener('resize',rsz);

  function drawFlower(x2,y,r,rot,alpha){
    x.save(); x.globalAlpha=alpha; x.translate(x2,y); x.rotate(rot);
    var cols=[[255,182,193],[255,160,175],[255,200,212],[250,145,165],[255,220,228]];
    var c2=cols[Math.floor(Math.random()*cols.length)];
    for(var i=0;i<5;i++){
      var a=(i/5)*Math.PI*2-Math.PI/2;
      x.save(); x.rotate(a);
      x.beginPath();
      x.ellipse(0,-r*.6,r*.38,r*.62,0,0,Math.PI*2);
      x.fillStyle='rgba('+c2[0]+','+c2[1]+','+c2[2]+',.88)';
      x.fill(); x.restore();
    }
    for(var j=0;j<5;j++){
      var aj=(j/5)*Math.PI*2-Math.PI/2;
      x.beginPath(); x.moveTo(0,0);
      x.lineTo(Math.cos(aj)*r*.5,Math.sin(aj)*r*.5);
      x.strokeStyle='rgba(210,90,120,.2)'; x.lineWidth=.5; x.stroke();
    }
    x.beginPath(); x.arc(0,0,r*.2,0,Math.PI*2);
    x.fillStyle='rgba(255,230,170,.95)'; x.fill();
    for(var k=0;k<5;k++){
      var ak=(k/5)*Math.PI*2;
      x.beginPath(); x.arc(Math.cos(ak)*r*.3,Math.sin(ak)*r*.3,r*.07,0,Math.PI*2);
      x.fillStyle='rgba(255,200,80,.9)'; x.fill();
    }
    x.restore();
  }

  function sp(){
    return{
      x:Math.random()*W,y:-25,r:4+Math.random()*9,
      rot:Math.random()*Math.PI*2,spin:(Math.random()-.5)*.035,
      vx:(Math.random()-.5)*1.0,vy:.5+Math.random()*1.2,
      alpha:.45+Math.random()*.5,
      sway:Math.random()*Math.PI*2,
      swayS:.012+Math.random()*.018,swayA:.5+Math.random()*1.0
    };
  }
  for(var i=0;i<70;i++){ var p=sp(); p.y=Math.random()*H; P.push(p); }

  function frame(){
    x.clearRect(0,0,W,H);
    if(P.length<75&&Math.random()<.22) P.push(sp());
    for(var i=P.length-1;i>=0;i--){
      var p=P[i];
      p.sway+=p.swayS; p.x+=p.vx+Math.sin(p.sway)*p.swayA;
      p.y+=p.vy; p.rot+=p.spin;
      drawFlower(p.x,p.y,p.r,p.rot,p.alpha);
      if(p.y>H+40||p.x<-80||p.x>W+80) P.splice(i,1);
    }
    requestAnimationFrame(frame);
  }
  frame();
})();

/* ═══════ COUNTDOWN (runs every second via setInterval) ═══════ */
(function(){
  function pad(n){return String(n).padStart(2,'0')}
  function tick(){
    var diff=new Date('2026-07-19T10:00:00+07:00').getTime()-Date.now();
    if(diff<0)diff=0;
    var vals=[Math.floor(diff/86400000),Math.floor((diff%86400000)/3600000),
              Math.floor((diff%3600000)/60000),Math.floor((diff%60000)/1000)];
    ['cd-days','cd-hours','cd-mins','cd-secs'].forEach(function(id,i){
      var el=document.getElementById(id);
      if(el)el.textContent=pad(vals[i]);
    });
  }
  tick();
  setInterval(tick,1000);
})();

/* ═══════ MUSIC ═══════ */
var muPlaying=false, muStarted=false;
var YT='https://www.youtube.com/watch?v=NMK3aFMbz9M';

function wcOpen(){
  var ov=document.getElementById('wc-overlay');
  var au=document.getElementById('au');
  ov.style.transition='opacity .6s';
  ov.style.opacity='0';
  setTimeout(function(){ov.style.display='none';},650);
  au.play().then(function(){
    muPlaying=true; muStarted=true;
    document.getElementById('mu-btn').innerHTML='♪';
    muTip('🎵 Janji Suci — Yovie & Nuno');
  }).catch(function(){
    muStarted=false;
    document.getElementById('mu-btn').innerHTML='🎵';
    muTip('Tap 🎵 untuk buka musik di YouTube');
  });
}

function muToggle(){
  if(!muStarted){ window.open(YT,'_blank'); muTip('Membuka YouTube...'); return; }
  var au=document.getElementById('au');
  var btn=document.getElementById('mu-btn');
  if(muPlaying){
    au.pause(); btn.innerHTML='♩'; btn.style.opacity='.5'; muPlaying=false; muTip('⏸ Musik dijeda');
  } else {
    au.play(); btn.innerHTML='♪'; btn.style.opacity='1'; muPlaying=true; muTip('▶ Janji Suci — Yovie & Nuno');
  }
}

function muTip(msg){
  var t=document.getElementById('mu-tip');
  t.textContent=msg; t.classList.add('show');
  setTimeout(function(){t.classList.remove('show');},3000);
}
</script>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────
def divider():
    st.markdown("""
    <div class="gold-divider">
        <div class="gd-line"></div><div class="gd-petal">🌸</div>
        <div class="gd-diamond"></div><div class="gd-petal">🌸</div>
        <div class="gd-line"></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
    <div class="bismillah-text">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</div>
    <div class="sakura-branch">🌸 🌿 🌸</div>
    <div class="salam-text">Assalamu'alaikum Warahmatullahi Wabarakatuh</div>
</div>""", unsafe_allow_html=True)

# Foto utama
if photos.get("foto1"):
    st.markdown(f"""
    <div style="padding:0 20px;margin-bottom:14px">
      <div class="frame-outer">
        <div class="frame-corner fc-tl"></div><div class="frame-corner fc-tr"></div>
        <div class="frame-corner fc-bl"></div><div class="frame-corner fc-br"></div>
        <span class="fp fp-tl">🌸</span><span class="fp fp-tr">🌸</span>
        <span class="fp fp-bl">🌸</span><span class="fp fp-br">🌸</span>
        <img src="data:image/png;base64,{photos['foto1']}" alt="Foto Mempelai"/>
      </div>
    </div>""", unsafe_allow_html=True)

# Gallery
if photos.get("foto2") and photos.get("foto3"):
    st.markdown(f"""
    <div class="gallery-row">
        <img src="data:image/png;base64,{photos['foto1']}" alt="1"/>
        <img src="data:image/png;base64,{photos['foto2']}" alt="2"/>
        <img src="data:image/png;base64,{photos['foto3']}" alt="3"/>
    </div>""", unsafe_allow_html=True)

# Nama
st.markdown("""
<div style="text-align:center;padding:0 24px 4px">
    <div class="undangan-label">🌸 Undangan Pernikahan 🌸</div>
    <div class="couple-script">Intan</div>
    <div class="ampersand-script">&</div>
    <div class="couple-script">Syahrial</div>
    <div class="date-sub">19 Juli 2026 · Desa Namo Bintang</div>
</div>""", unsafe_allow_html=True)

divider()

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
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  MEMPELAI
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 8px">
    <div class="s-label">— Mempelai Wanita —</div>
    <span class="mempelai-name">Intan Candra Nurul Hafiyah</span>
    <div class="mempelai-parents">Putri dari Alm. Bapak Fadli &amp; Ibu Sri Sumarti (Wiwik)</div>
</div>
<div style="text-align:center;margin:10px 0;font-size:28px;filter:drop-shadow(0 0 8px rgba(255,160,180,.5))">🌸</div>
<div style="text-align:center;margin:-4px 0 10px">
    <span style="font-family:'Great Vibes',cursive;font-size:44px;color:#8b1c2e">&amp;</span>
</div>
<div class="s-card" style="margin:0 20px 24px">
    <div class="s-label">— Mempelai Pria —</div>
    <span class="mempelai-name">Syahrial / Gombeng</span>
    <div class="mempelai-parents">Putra dari Alm. Bapak Paimo &amp; Ibu Suriani</div>
</div>""", unsafe_allow_html=True)

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
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  COUNTDOWN — pure JS, no Streamlit refresh needed
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="countdown-wrap">
    <div class="s-label">— Menghitung Hari Menuju Hari Bahagia —</div>
    <div class="cd-grid">
        <div class="cd-block"><span class="cd-num" id="cd-days">--</span><div class="cd-unit">Hari</div></div>
        <div class="cd-sep">:</div>
        <div class="cd-block"><span class="cd-num" id="cd-hours">--</span><div class="cd-unit">Jam</div></div>
        <div class="cd-sep">:</div>
        <div class="cd-block"><span class="cd-num" id="cd-mins">--</span><div class="cd-unit">Menit</div></div>
        <div class="cd-sep">:</div>
        <div class="cd-block"><span class="cd-num" id="cd-secs">--</span><div class="cd-unit">Detik</div></div>
    </div>
</div>
<script>
(function startCD(){
  function pad(n){return String(n).padStart(2,'0')}
  function tick(){
    var diff=new Date('2026-07-19T10:00:00+07:00').getTime()-Date.now();
    if(diff<0)diff=0;
    var v=[Math.floor(diff/86400000),Math.floor((diff%86400000)/3600000),
           Math.floor((diff%3600000)/60000),Math.floor((diff%60000)/1000)];
    ['cd-days','cd-hours','cd-mins','cd-secs'].forEach(function(id,i){
      var el=document.getElementById(id);
      if(el)el.textContent=pad(v[i]);
    });
  }
  tick();
  var iv=setInterval(tick,1000);
  // re-attach if DOM replaced by Streamlit re-render
  window._cdiv=iv;
})();
</script>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  LOKASI
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 16px;text-align:center">
    <div class="s-label">— Lokasi Acara —</div>
    <div style="font-size:28px;margin:6px 0;filter:drop-shadow(0 0 8px rgba(255,160,180,.5))">🌸 📍 🌸</div>
    <div style="font-family:'Playfair Display',serif;font-size:17px;color:#c9a84c;margin:10px 0 6px;letter-spacing:1px">
        Dusun II Sumberingin
    </div>
    <div style="font-size:12px;color:#e8d5c0;opacity:.7;font-style:italic;line-height:2">
        Desa Namo Bintang<br>Minggu, 19 Juli 2026 · Pukul 10.00 WIB
    </div>
</div>
<div style="text-align:center;margin:0 20px 24px">
    <a href="https://maps.app.goo.gl/8G9hHHY9LzdGg5yc6" target="_blank"
       style="display:inline-block;padding:14px 40px;border:1px solid #c9a84c;
              color:#c9a84c;font-family:'Cormorant Garamond',serif;
              font-size:12px;letter-spacing:4px;text-transform:uppercase;
              text-decoration:none;background:rgba(201,168,76,.05)">
        🗺️ &nbsp; Buka Google Maps
    </a>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  KHITANAN
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="khit-card">
    <div class="khit-also">— Serta Khitanan —</div>
    <div style="font-size:20px;margin:6px 0;opacity:.35">🌸</div>
    <div class="khit-title">Ahmad Hanafi</div>
</div>""", unsafe_allow_html=True)

divider()

# ══════════════════════════════════════════════════════════════
#  TURUT MENGUNDANG
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 4px">
    <div class="s-label">— 🌸 Turut Mengundang 🌸 —</div>
</div>""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌸 Pihak Wanita", "🎩 Pihak Pria"])

with tab1:
    wanita = [
        "Alm. Mandah / Ngatiyem (Kakek & Nenek)", "Muri / Anik (Kakek & Nenek)",
        "Dasem (Nenek)", "Sukar / Iyet (Kakek & Nenek)", "Ribut / Ngatisah (Kakek & Nenek)",
        "Alm. Jarno / Muriatik (Kakek & Nenek)", "Sawon (Kakek)", "Karlan (Kakek)",
        "Watik / Misjo (Wawak)", "Gambreng / Tumik (Pakde & Bude)",
        "Endang Susanti / Ust. Lukman S.Pd.I (Bibik & Oom)",
        "Sri Wulan Handayani / Hendrik (Bibik & Oom)", "Ema (Adik)", "Ahamad Hanafi (Adik)",
    ]
    st.markdown("".join([
        f'<div style="font-size:13px;color:#e8d5c0;opacity:.78;padding:7px 4px;'
        f'border-bottom:1px solid rgba(255,182,193,.07);line-height:1.5">🌸 {i}</div>'
        for i in wanita]), unsafe_allow_html=True)

with tab2:
    pria = [
        "Marinem / Suparto (Nenek & Kakek)", "Ngatiyem / Alm. Joni (Nenek & Kakek)",
        "Alm. Paiko / Iyus (Wawak)", "Dedi / Rika (Abang)", "Yuda / Wulan (Abang)",
        "Diki / Dina (Adik)", "Igo Ardiansyah (Adik)", "Sugik / Yanti (Lelek)",
        "Minok / Susi (Lelek)", "Rame / Santo (Bibik)", "Yuni / Junedi (Bibik)",
    ]
    st.markdown("".join([
        f'<div style="font-size:13px;color:#e8d5c0;opacity:.78;padding:7px 4px;'
        f'border-bottom:1px solid rgba(255,182,193,.07);line-height:1.5">🌸 {i}</div>'
        for i in pria]), unsafe_allow_html=True)

divider()

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
</div>""", unsafe_allow_html=True)

with st.container():
    rsvp_name = st.text_input("", placeholder="Nama Anda...", key="rsvp_name", label_visibility="collapsed")
    rsvp_status = st.radio("", ["🌸 Hadir", "✦ Tidak Hadir"], horizontal=True, key="rsvp_status", label_visibility="collapsed")
    if st.button("Kirim Konfirmasi", key="submit_rsvp"):
        if rsvp_name.strip():
            if "Tidak" not in rsvp_status:
                st.success(f"🌸 Terima kasih, {rsvp_name}! Kami menantikan kehadiran Anda.")
            else:
                st.info(f"✦ Terima kasih, {rsvp_name}. Semoga selalu dalam lindungan Allah.")
        else:
            st.warning("Mohon isi nama Anda terlebih dahulu.")

divider()

# ══════════════════════════════════════════════════════════════
#  DO'A & UCAPAN
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card s-card-top" style="margin:0 20px 0">
    <div class="s-label">— 🌸 Do'a &amp; Ucapan 🌸 —</div>
</div>""", unsafe_allow_html=True)

for w in st.session_state.wishes:
    st.markdown(f"""
    <div class="wish-item" style="padding:12px 4px">
        <div class="wish-name-label">🌸 {w['name']}</div>
        <div class="wish-body">{w['text']}</div>
        <div class="wish-time">{w['time']}</div>
    </div>""", unsafe_allow_html=True)

wish_name = st.text_input("", placeholder="Nama Anda...", key="wish_name", label_visibility="collapsed")
wish_text = st.text_area("", placeholder="Tulis do'a dan ucapan untuk kedua mempelai...", key="wish_text", label_visibility="collapsed", height=100)
if st.button("Kirim Ucapan 🌸", key="submit_wish"):
    if wish_name.strip() and wish_text.strip():
        st.session_state.wishes.insert(0, {"name": wish_name.strip(), "text": wish_text.strip(), "time": "Baru saja"})
        st.rerun()
    else:
        st.warning("Mohon isi nama dan ucapan Anda.")

divider()

# ══════════════════════════════════════════════════════════════
#  AYAT
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="s-card" style="margin:0 20px 20px">
    <div class="s-label">— QS. Ar-Rum: 21 —</div>
    <div style="font-size:22px;text-align:center;margin-bottom:14px;filter:drop-shadow(0 0 6px rgba(255,160,180,.4))">🌸 🌿 🌸</div>
    <p style="font-size:13px;line-height:2.2;text-align:center;color:#e8d5c0;opacity:.82;font-style:italic">
        "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu
        istri-istri dari jenismu sendiri, supaya kamu cenderung dan merasa tenteram
        kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang."
    </p>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer-wrap">
    <div style="font-size:28px;margin-bottom:16px;filter:drop-shadow(0 0 10px rgba(255,160,180,.5))">🌸 🌿 🌸</div>
    <div class="footer-names">Intan &amp; Syahrial</div>
    <div class="footer-sub">19 Juli 2026 · Namo Bintang</div>
    <div style="font-size:16px;color:#c9a84c;opacity:.2;margin:14px 0;letter-spacing:10px">✦ ✦ ✦</div>
    <div class="wassalam">Wassalamu'alaikum Warahmatullahi Wabarakatuh</div>
    <div style="margin-top:20px;font-size:10px;color:#c9a84c;opacity:.18;letter-spacing:1px;line-height:2.2">
        Kel. Mempelai Wanita · Alm. Bapak Fadli &amp; Ibu Sri Sumarti (Wiwik)<br>
        Kel. Mempelai Pria · Alm. Bapak Paimo &amp; Ibu Suriani
    </div>
    <div style="margin-top:24px;font-size:22px;opacity:.18">🌸 🌸 🌸</div>
</div>""", unsafe_allow_html=True)
