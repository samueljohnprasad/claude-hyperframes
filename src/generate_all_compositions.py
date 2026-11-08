# // ponytail: Master generator for Top 5 GitHub Open Source Libraries explainer reel
import os
import json
import numpy as np
import soundfile as sf
from scipy import signal

os.makedirs("compositions", exist_ok=True)
os.makedirs("audio", exist_ok=True)

with open("transcript.json") as f:
    transcript = json.load(f)

words = transcript["words"]
total_duration = 44.0 # audio is 43.98s

key_word_indices = {
    4: "hurts",           # Hook 1
    11: "supercharge",    # Hook 2
    20: "interfaces",     # React
    34: "intelligence",   # Transformers
    49: "documentation",  # FastAPI
    55: "software",       # Tauri
    72: "instantly",      # Supabase
    82: "scratch"         # Closing
}

# 1. compositions/paper.html
paper_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body, #paper {
        width: 1080px;
        height: 1920px;
        background-color: #EBE7E1;
        overflow: hidden;
      }
      .noise-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0.045;
        pointer-events: none;
      }
    </style>
  </head>
  <body>
    <div id="paper" data-composition-id="paper" data-width="1080" data-height="1920">
      <svg class="noise-overlay" xmlns="http://www.w3.org/2000/svg">
        <filter id="noiseFilter">
          <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" stitchTiles="stitch" />
        </filter>
        <rect width="100%" height="100%" filter="url(#noiseFilter)" />
      </svg>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["paper"] = null;
    </script>
  </body>
</html>
'''
with open("compositions/paper.html", "w") as f:
    f.write(paper_html)

# 2. compositions/hook1.html
hook1_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {
        --ink: #1E1C1A;
        --red: #A31C14;
        --grey: #726D66;
        --card-bg: #FBFAF8;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body, #hook1 {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: transparent;
      }
      .hook-card-wrap {
        position: absolute;
        top: 660px;
        left: 120px;
        width: 840px;
        height: 460px;
      }
      .hook-card-shadow {
        position: absolute;
        top: 12px;
        left: -13px;
        width: 840px;
        height: 460px;
        border-radius: 20px;
        background-image: radial-gradient(var(--ink) 1.7px, transparent 1.7px);
        background-size: 8px 8px;
        z-index: 1;
      }
      .hook-card {
        position: relative;
        z-index: 2;
        width: 840px;
        height: 460px;
        background: var(--card-bg);
        border: 3px solid var(--ink);
        border-radius: 20px;
        padding: 44px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .hook-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        color: var(--grey);
        text-transform: uppercase;
      }
      .hook-statement {
        font-family: 'Anton', sans-serif;
        font-size: 72px;
        line-height: 1.05;
        color: var(--ink);
        text-transform: uppercase;
      }
      .strike-line {
        stroke: var(--red);
        stroke-width: 9;
        stroke-linecap: round;
        stroke-dasharray: 780;
        stroke-dashoffset: 780;
      }
    </style>
  </head>
  <body>
    <div id="hook1" data-composition-id="hook1" data-width="1080" data-height="1920">
      <div class="hook-card-wrap">
        <div class="hook-card-shadow"></div>
        <div class="hook-card">
          <div class="hook-tag" data-layout-ignore>// 00 · COMMON MISTAKE</div>
          <div class="hook-statement">BUILDING EVERYTHING FROM SCRATCH</div>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 28px; color: var(--red);" data-layout-ignore>
            STATUS: DEVELOPER BURNOUT
          </div>
          <svg style="position: absolute; top: 0; left: 0; width: 840px; height: 460px; pointer-events: none;">
            <line id="strike-1" class="strike-line" x1="60" y1="230" x2="780" y2="230" />
          </svg>
        </div>
      </div>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      tl.to("#strike-1", {
        strokeDashoffset: 0,
        duration: 0.32,
        ease: "power2.out"
      }, 1.90);
      window.__timelines = window.__timelines || {};
      window.__timelines["hook1"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
with open("compositions/hook1.html", "w") as f:
    f.write(hook1_html)

# 3. compositions/hook2.html
hook2_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {
        --ink: #1E1C1A;
        --red: #A31C14;
        --grey: #726D66;
        --card-bg: #FBFAF8;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body, #hook2 {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: transparent;
      }
      .hook2-container {
        position: absolute;
        top: 660px;
        left: 120px;
        width: 840px;
        height: 460px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .mini-card-wrap {
        position: relative;
        width: 840px;
        height: 76px;
        transform: scale(0.55);
        opacity: 0;
      }
      .mini-shadow {
        position: absolute;
        top: 8px;
        left: -8px;
        width: 840px;
        height: 76px;
        border-radius: 14px;
        background-image: radial-gradient(var(--ink) 1.5px, transparent 1.5px);
        background-size: 7px 7px;
        z-index: 1;
      }
      .mini-card {
        position: relative;
        z-index: 2;
        width: 840px;
        height: 76px;
        background: var(--card-bg);
        border: 3px solid var(--ink);
        border-radius: 14px;
        padding: 0 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-family: 'Anton', sans-serif;
        font-size: 34px;
        color: var(--ink);
      }
      .ring-svg {
        position: absolute;
        top: 0;
        left: 0;
        width: 840px;
        height: 460px;
        pointer-events: none;
        z-index: 10;
      }
      .ring-path {
        fill: none;
        stroke: var(--red);
        stroke-width: 7;
        stroke-linecap: round;
        stroke-dasharray: 2300;
        stroke-dashoffset: 2300;
      }
    </style>
  </head>
  <body>
    <div id="hook2" data-composition-id="hook2" data-width="1080" data-height="1920">
      <div class="hook2-container">
        <div id="mc-0" class="mini-card-wrap">
          <div class="mini-shadow"></div>
          <div class="mini-card">
            <span>01 · REACT</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--red);" data-layout-ignore>225k ★</span>
          </div>
        </div>
        <div id="mc-1" class="mini-card-wrap">
          <div class="mini-shadow"></div>
          <div class="mini-card">
            <span>02 · TRANSFORMERS</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--red);" data-layout-ignore>135k ★</span>
          </div>
        </div>
        <div id="mc-2" class="mini-card-wrap">
          <div class="mini-shadow"></div>
          <div class="mini-card">
            <span>03 · FASTAPI</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--red);" data-layout-ignore>80k ★</span>
          </div>
        </div>
        <div id="mc-3" class="mini-card-wrap">
          <div class="mini-shadow"></div>
          <div class="mini-card">
            <span>04 · TAURI</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--red);" data-layout-ignore>85k ★</span>
          </div>
        </div>
        <div id="mc-4" class="mini-card-wrap">
          <div class="mini-shadow"></div>
          <div class="mini-card">
            <span>05 · SUPABASE</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--red);" data-layout-ignore>75k ★</span>
          </div>
        </div>

        <svg class="ring-svg" data-layout-allow-overflow>
          <ellipse id="payoff-ring" class="ring-path" cx="420" cy="230" rx="400" ry="210" transform="rotate(-2 420 230)" />
        </svg>
      </div>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      
      // Pop mini cards in 0.16s apart starting at 0.4s relative to hook2 (which is ~3.0s real time)
      const cards = ["#mc-0", "#mc-1", "#mc-2", "#mc-3", "#mc-4"];
      cards.forEach((c, idx) => {
        tl.to(c, {
          scale: 1,
          opacity: 1,
          duration: 0.34,
          ease: "back.out(2.2)"
        }, 0.35 + idx * 0.16);
      });

      // Red ring draws around payoff on word 'supercharge' at 5.16s (relative 2.56s)
      tl.to("#payoff-ring", {
        strokeDashoffset: 0,
        duration: 0.55,
        ease: "power2.out"
      }, 2.56);

      window.__timelines = window.__timelines || {};
      window.__timelines["hook2"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
with open("compositions/hook2.html", "w") as f:
    f.write(hook2_html)

# Sub-composition generator with Title at top: 520px, Main Card at top: 660px (height: 460px)
def generate_point_subcomp(p_id, title_word1, title_word2, label_text, stat_text, badge_num, counter_max, counter_unit, term_prompt, term_code, is_search, demo_svg_body, stamp_text, stamp_time, title_slam_time, comp_duration):
    swash_time = round(title_slam_time + 0.12, 3)
    card_rise_time = round(title_slam_time + 0.18, 3)
    badge_time = round(card_rise_time + 0.25, 3)
    term_time = round(card_rise_time + 0.35, 3)
    exit_time = round(stamp_time - 0.70, 3)
    demo_rise_time = round(exit_time + 0.18, 3)

    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --ink: #1E1C1A;
        --red: #A31C14;
        --grey: #726D66;
        --card-bg: #FBFAF8;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body, #{p_id} {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: transparent;
      }}
      .header-label {{
        position: absolute;
        top: 132px;
        left: 120px;
        width: 840px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        color: var(--grey);
        text-transform: uppercase;
      }}
      .stat-num {{
        color: var(--red);
        font-weight: 700;
      }}
      .title-box {{
        position: absolute;
        top: 520px;
        left: 120px;
        width: 840px;
        height: 120px;
      }}
      .main-title {{
        font-family: 'Anton', sans-serif;
        font-size: 110px;
        line-height: 1.0;
        text-transform: uppercase;
        transform-origin: left bottom;
        opacity: 0;
      }}
      .title-ink {{ color: var(--ink); }}
      .title-red {{ color: var(--red); }}
      .swash-line {{
        stroke: var(--red);
        stroke-width: 8;
        stroke-linecap: round;
        stroke-dasharray: 600;
        stroke-dashoffset: 600;
      }}
      .main-card-wrap {{
        position: absolute;
        top: 660px;
        left: 120px;
        width: 840px;
        height: 460px;
        transform: translateY(70px);
        opacity: 0;
      }}
      .card-shadow {{
        position: absolute;
        top: 12px;
        left: -13px;
        width: 840px;
        height: 460px;
        border-radius: 20px;
        background-image: radial-gradient(var(--ink) 1.7px, transparent 1.7px);
        background-size: 8px 8px;
        z-index: 1;
      }}
      .card-face {{
        position: relative;
        z-index: 2;
        width: 840px;
        height: 460px;
        background: var(--card-bg);
        border: 3px solid var(--ink);
        border-radius: 20px;
        padding: 36px 44px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}
      .badge-wrap {{
        position: absolute;
        top: 36px;
        right: 44px;
        width: 58px;
        height: 58px;
        background: var(--red);
        color: #FBFAF8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Anton', sans-serif;
        font-size: 32px;
        border-radius: 8px;
        transform: scale(0) rotate(-180deg);
      }}
      .counter-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        color: var(--grey);
        text-transform: uppercase;
        letter-spacing: 2px;
      }}
      .counter-val {{
        font-family: 'Anton', sans-serif;
        font-size: 115px;
        color: var(--ink);
        line-height: 1.0;
        margin-top: 6px;
      }}
      .terminal-bar {{
        background: var(--ink);
        border-radius: 12px;
        padding: 16px 22px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        color: #FBFAF8;
        display: flex;
        align-items: center;
        gap: 12px;
      }}
      .terminal-prompt {{
        color: var(--red);
        font-weight: 700;
      }}
      .demo-wrap {{
        position: absolute;
        top: 660px;
        left: 120px;
        width: 840px;
        height: 460px;
        transform: translateY(70px);
        opacity: 0;
      }}
      .demo-card {{
        top: 0;
        left: 0;
        width: 840px;
        height: 460px;
        padding: 0;
        overflow: hidden;
      }}
      .stamp-box {{
        position: absolute;
        bottom: 36px;
        right: 36px;
        border: 5px solid var(--red);
        padding: 10px 24px;
        transform: scale(1.75) rotate(-18deg);
        opacity: 0;
        z-index: 30;
        background: #FBFAF8;
      }}
      .stamp-text {{
        font-family: 'Anton', sans-serif;
        font-size: 52px;
        color: var(--red);
        text-transform: uppercase;
        line-height: 1.0;
      }}
    </style>
  </head>
  <body>
    <div id="{p_id}" data-composition-id="{p_id}" data-width="1080" data-height="1920">
      <div class="header-label" data-layout-ignore>
        <span>{label_text}</span>
        <span>{stat_text}</span>
      </div>

      <div class="title-box">
        <div id="title-text" class="main-title">
          <span class="title-ink">{title_word1}</span> <span class="title-red">{title_word2}</span>
        </div>
        <svg style="width: 840px; height: 20px; margin-top: 4px;">
          <path id="title-swash" class="swash-line" d="M 0 10 Q 220 2 480 12 T 760 8" />
        </svg>
      </div>

      <div id="main-card-wrap" class="main-card-wrap">
        <div class="card-shadow"></div>
        <div class="card-face">
          <div class="badge-wrap" id="badge" data-layout-ignore>#{badge_num}</div>
          <div>
            <div class="counter-label" data-layout-ignore>OFFICIAL METRIC</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 20px; color: var(--grey); margin-top: 4px;" data-layout-ignore>GITHUB STARS</div>
            <div id="counter-display" class="counter-val">0</div>
          </div>
          <div class="terminal-bar">
            <span class="terminal-prompt" data-layout-ignore>{term_prompt}</span>
            <span id="terminal-typed" style="white-space: nowrap; overflow: hidden;" data-layout-ignore></span>
            <span style="color: var(--red); font-weight: bold; animation: blink 0.8s infinite;" data-layout-ignore>_</span>
          </div>
        </div>
      </div>

      <div id="demo-wrap" class="demo-wrap" data-layout-ignore>
        <div class="card-shadow"></div>
        <div class="card-face demo-card">
          <svg width="100%" height="100%" viewBox="0 0 840 460" xmlns="http://www.w3.org/2000/svg">
            {demo_svg_body}
          </svg>
          <div id="stamp" class="stamp-box" data-layout-ignore>
            <div class="stamp-text">{stamp_text}</div>
          </div>
        </div>
      </div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});

      // 1. Title slams in on spoken word
      tl.to("#title-text", {{
        scale: 1,
        opacity: 1,
        duration: 0.24,
        ease: "power4.out"
      }}, {title_slam_time});

      // 2. Underline draws 0.12s later
      tl.to("#title-swash", {{
        strokeDashoffset: 0,
        duration: 0.38,
        ease: "power2.out"
      }}, {swash_time});

      // 3. Main card rises 0.18s later (70px up in 0.4s)
      tl.to("#main-card-wrap", {{
        y: 0,
        opacity: 1,
        duration: 0.40,
        ease: "power3.out"
      }}, {card_rise_time});

      // 4. Counter counting up over 1.15s
      const counterObj = {{ val: 0 }};
      tl.to(counterObj, {{
        val: {counter_max},
        duration: 1.15,
        ease: "power2.out",
        onUpdate: function() {{
          document.getElementById("counter-display").innerText = Math.round(counterObj.val) + "k+ {counter_unit}";
        }}
      }}, {card_rise_time});

      // 5. Badge spins in at 0.6s
      tl.to("#badge", {{
        scale: 1,
        rotation: 0,
        duration: 0.45,
        ease: "back.out(2.0)"
      }}, {badge_time});

      // 6. Terminal types one line in under 0.9s
      const termCode = "{term_code}";
      const termObj = {{ len: 0 }};
      tl.to(termObj, {{
        len: termCode.length,
        duration: 0.82,
        ease: "steps(" + termCode.length + ")",
        onUpdate: function() {{
          document.getElementById("terminal-typed").innerText = termCode.slice(0, Math.round(termObj.len));
        }}
      }}, {term_time});

      // 7. 0.3s before explanation, everything exits upward (50px up, fade out in 0.22s)
      tl.to("#main-card-wrap", {{
        y: -50,
        opacity: 0,
        duration: 0.22,
        ease: "power2.in"
      }}, {exit_time});

      // Demo rises into place
      tl.to("#demo-wrap", {{
        y: 0,
        opacity: 1,
        duration: 0.38,
        ease: "power3.out"
      }}, {demo_rise_time});

      // 8. Stamp lands on key word (scale 1.75 to 1, -18deg to -6deg in 0.2s)
      tl.to("#stamp", {{
        scale: 1,
        rotation: -6,
        opacity: 1,
        duration: 0.20,
        ease: "power3.out"
      }}, {stamp_time});

      window.__timelines = window.__timelines || {{}};
      window.__timelines["{p_id}"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''

# Point 1: React (Virtual DOM Component Tree)
react_demo = '''
<rect width="840" height="460" fill="#151413" />
<!-- Tree branches -->
<line x1="420" y1="80" x2="220" y2="180" stroke="#726D66" stroke-width="4" stroke-dasharray="6 6" />
<line x1="420" y1="80" x2="420" y2="180" stroke="#726D66" stroke-width="4" stroke-dasharray="6 6" />
<line x1="420" y1="80" x2="620" y2="180" stroke="#726D66" stroke-width="4" stroke-dasharray="6 6" />
<line x1="220" y1="180" x2="140" y2="280" stroke="#726D66" stroke-width="3" />
<line x1="220" y1="180" x2="300" y2="280" stroke="#726D66" stroke-width="3" />
<line x1="620" y1="180" x2="540" y2="280" stroke="#726D66" stroke-width="3" />
<line x1="620" y1="180" x2="700" y2="280" stroke="#726D66" stroke-width="3" />

<!-- App Root Node -->
<rect x="340" y="44" width="160" height="60" rx="12" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="3" />
<text x="420" y="82" font-family="'JetBrains Mono', monospace" font-size="22" font-weight="700" fill="#1E1C1A" text-anchor="middle">&lt;App /&gt;</text>

<!-- Child Nodes -->
<rect x="150" y="150" width="140" height="54" rx="10" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="3" />
<text x="220" y="184" font-family="'JetBrains Mono', monospace" font-size="18" fill="#1E1C1A" text-anchor="middle">&lt;Nav /&gt;</text>

<rect x="350" y="150" width="140" height="54" rx="10" fill="#A31C14" stroke="#FBFAF8" stroke-width="3" />
<text x="420" y="184" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#FBFAF8" text-anchor="middle">&lt;Feed /&gt;</text>

<rect x="550" y="150" width="140" height="54" rx="10" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="3" />
<text x="620" y="184" font-family="'JetBrains Mono', monospace" font-size="18" fill="#1E1C1A" text-anchor="middle">&lt;User /&gt;</text>

<!-- Leaf Nodes -->
<rect x="80" y="254" width="120" height="46" rx="8" fill="#24211E" stroke="#726D66" stroke-width="2" />
<text x="140" y="283" font-family="'JetBrains Mono', monospace" font-size="15" fill="#FBFAF8" text-anchor="middle">Button</text>

<rect x="240" y="254" width="120" height="46" rx="8" fill="#24211E" stroke="#726D66" stroke-width="2" />
<text x="300" y="283" font-family="'JetBrains Mono', monospace" font-size="15" fill="#FBFAF8" text-anchor="middle">Search</text>

<rect x="480" y="254" width="120" height="46" rx="8" fill="#24211E" stroke="#726D66" stroke-width="2" />
<text x="540" y="283" font-family="'JetBrains Mono', monospace" font-size="15" fill="#FBFAF8" text-anchor="middle">Avatar</text>

<rect x="640" y="254" width="120" height="46" rx="8" fill="#24211E" stroke="#726D66" stroke-width="2" />
<text x="700" y="283" font-family="'JetBrains Mono', monospace" font-size="15" fill="#FBFAF8" text-anchor="middle">Badge</text>

<!-- Reactive Pulse Badge -->
<rect x="270" y="360" width="300" height="52" rx="10" fill="#1E1C1A" stroke="#A31C14" stroke-width="3" />
<circle cx="295" cy="386" r="8" fill="#A31C14" />
<text x="420" y="393" font-family="'JetBrains Mono', monospace" font-size="18" fill="#FBFAF8" text-anchor="middle">VIRTUAL DOM DIFF: 0.1ms</text>
'''
with open("compositions/point1.html", "w") as f:
    f.write(generate_point_subcomp("point1", "REACT", "2013", "// 01 · REACT", "STARS <span class='stat-num'>225k+</span>", 1, 225, "★", ">", "npx create-react-app web-app", False, react_demo, "COMPONENTS", 2.00, 0.20, 6.00))

# Point 2: Transformers (Attention Network Matrix)
transformers_demo = '''
<rect width="840" height="460" fill="#151413" />
<!-- Input tokens -->
<g transform="translate(60, 60)">
  <rect x="0" y="0" width="130" height="50" rx="8" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="3" />
  <text x="65" y="32" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#1E1C1A" text-anchor="middle">"AI"</text>

  <rect x="150" y="0" width="130" height="50" rx="8" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="3" />
  <text x="215" y="32" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#1E1C1A" text-anchor="middle">"MODELS"</text>

  <rect x="300" y="0" width="130" height="50" rx="8" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="3" />
  <text x="365" y="32" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#1E1C1A" text-anchor="middle">"RUN"</text>
</g>

<!-- Multi-head attention box -->
<rect x="60" y="150" width="720" height="130" rx="16" fill="#24211E" stroke="#A31C14" stroke-width="4" />
<text x="90" y="186" font-family="'Anton', sans-serif" font-size="32" fill="#FBFAF8">MULTI-HEAD SELF-ATTENTION</text>
<text x="90" y="214" font-family="'JetBrains Mono', monospace" font-size="18" fill="#726D66">Softmax( Q · K^T / sqrt(d_k) ) · V</text>

<!-- Attention weights bar -->
<rect x="90" y="235" width="200" height="18" rx="4" fill="#A31C14" />
<rect x="300" y="235" width="340" height="18" rx="4" fill="#726D66" opacity="0.6" />
<rect x="650" y="235" width="100" height="18" rx="4" fill="#EBE7E1" />

<!-- Output pipeline statement -->
<g transform="translate(60, 320)">
  <rect x="0" y="0" width="480" height="70" rx="12" fill="#1E1C1A" stroke="#EBE7E1" stroke-width="2" />
  <text x="24" y="42" font-family="'JetBrains Mono', monospace" font-size="20" fill="#FBFAF8">&gt; pipeline("text-gen")</text>
  <circle cx="440" cy="35" r="8" fill="#A31C14" />
</g>
'''
with open("compositions/point2.html", "w") as f:
    f.write(generate_point_subcomp("point2", "TRANSFORMERS", "AI", "// 02 · TRANSFORMERS", "MODELS <span class='stat-num'>1M+</span>", 2, 135, "★", ">", "pipeline('sentiment-analysis')", False, transformers_demo, "PIPELINE", 3.18, 0.26, 5.50))

# Point 3: FastAPI (OpenAPI Swagger Documentation)
fastapi_demo = '''
<rect width="840" height="460" fill="#181716" />
<!-- Swagger Header -->
<rect x="50" y="40" width="740" height="64" rx="10" fill="#24211E" stroke="#1E1C1A" stroke-width="3" />
<text x="80" y="78" font-family="'Anton', sans-serif" font-size="34" fill="#FBFAF8">FASTAPI OPENAPI 3.1</text>
<rect x="650" y="52" width="110" height="38" rx="6" fill="#A31C14" />
<text x="705" y="77" font-family="'JetBrains Mono', monospace" font-size="16" font-weight="700" fill="#FBFAF8" text-anchor="middle">ASYNC</text>

<!-- Endpoint Row 1: GET /models -->
<rect x="50" y="125" width="740" height="74" rx="10" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="3" />
<rect x="70" y="142" width="80" height="40" rx="6" fill="#1E1C1A" />
<text x="110" y="167" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#FBFAF8" text-anchor="middle">GET</text>
<text x="175" y="169" font-family="'JetBrains Mono', monospace" font-size="22" font-weight="700" fill="#1E1C1A">/api/v1/models</text>
<text x="720" y="168" font-family="'JetBrains Mono', monospace" font-size="18" fill="#726D66" text-anchor="end">200 OK</text>

<!-- Endpoint Row 2: POST /predict -->
<rect x="50" y="215" width="740" height="74" rx="10" fill="#FBFAF8" stroke="#A31C14" stroke-width="3" />
<rect x="70" y="232" width="90" height="40" rx="6" fill="#A31C14" />
<text x="115" y="257" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#FBFAF8" text-anchor="middle">POST</text>
<text x="185" y="259" font-family="'JetBrains Mono', monospace" font-size="22" font-weight="700" fill="#1E1C1A">/api/v1/predict</text>
<text x="720" y="258" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#A31C14" text-anchor="end">0.4ms</text>

<!-- Performance Metric Box -->
<g transform="translate(50, 315)">
  <rect x="0" y="0" width="460" height="90" rx="12" fill="#24211E" stroke="#1E1C1A" stroke-width="2" />
  <text x="24" y="38" font-family="'JetBrains Mono', monospace" font-size="18" fill="#726D66">BENCHMARK THROUGHPUT</text>
  <text x="24" y="72" font-family="'Anton', sans-serif" font-size="34" fill="#FBFAF8">300x FASTER THAN WSGI</text>
</g>
'''
with open("compositions/point3.html", "w") as f:
    f.write(generate_point_subcomp("point3", "FASTAPI", "API", "// 03 · FASTAPI", "SPEED <span class='stat-num'>300x</span>", 3, 80, "★", ">", "uvicorn main:app --reload", False, fastapi_demo, "ASYNC", 6.14, 0.18, 7.00))

# Point 4: Tauri (Electron vs Rust Featherweight)
tauri_demo = '''
<rect width="840" height="460" fill="#141312" />
<!-- Bloated Electron Box -->
<g transform="translate(50, 60)">
  <rect x="0" y="0" width="340" height="260" rx="16" fill="#24211E" stroke="#726D66" stroke-width="3" stroke-dasharray="8 8" />
  <text x="170" y="50" font-family="'Anton', sans-serif" font-size="32" fill="#726D66" text-anchor="middle">LEGACY DESKTOP</text>
  <text x="170" y="140" font-family="'Anton', sans-serif" font-size="70" fill="#726D66" text-anchor="middle">140 MB</text>
  <text x="170" y="180" font-family="'JetBrains Mono', monospace" font-size="18" fill="#726D66" text-anchor="middle">Chromium + Node</text>
  <line x1="60" y1="220" x2="280" y2="220" stroke="#A31C14" stroke-width="6" stroke-linecap="round" />
</g>

<!-- Featherweight Tauri Box -->
<g transform="translate(450, 60)">
  <rect x="0" y="0" width="340" height="260" rx="16" fill="#FBFAF8" stroke="#A31C14" stroke-width="4" />
  <text x="170" y="50" font-family="'Anton', sans-serif" font-size="32" fill="#1E1C1A" text-anchor="middle">TAURI (RUST)</text>
  <text x="170" y="140" font-family="'Anton', sans-serif" font-size="76" fill="#A31C14" text-anchor="middle">&lt; 3 MB</text>
  <text x="170" y="180" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#1E1C1A" text-anchor="middle">Native OS Webview</text>
  <path d="M 120 220 L 155 240 L 230 195" fill="none" stroke="#1E1C1A" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
</g>

<!-- Core badge -->
<g transform="translate(50, 350)">
  <rect x="0" y="0" width="460" height="60" rx="10" fill="#1E1C1A" stroke="#FBFAF8" stroke-width="2" />
  <text x="24" y="38" font-family="'JetBrains Mono', monospace" font-size="20" fill="#FBFAF8">MEMORY FOOTPRINT: ~25 MB</text>
</g>
'''
with open("compositions/point4.html", "w") as f:
    f.write(generate_point_subcomp("point4", "TAURI", "RUST", "// 04 · TAURI", "SIZE <span class='stat-num'>&lt; 3MB</span>", 4, 85, "★", ">", "cargo tauri dev", False, tauri_demo, "FEATHER", 2.80, 0.08, 5.60))

# Point 5: Supabase (Postgres + Auth + Realtime)
supabase_demo = '''
<rect width="840" height="460" fill="#151413" />
<!-- Table Header -->
<rect x="50" y="40" width="740" height="60" rx="10" fill="#24211E" stroke="#1E1C1A" stroke-width="3" />
<text x="80" y="78" font-family="'Anton', sans-serif" font-size="32" fill="#FBFAF8">POSTGRESQL REALTIME SCHEMA</text>
<circle cx="740" cy="70" r="10" fill="#A31C14" />

<!-- Table Rows -->
<g transform="translate(50, 115)">
  <rect x="0" y="0" width="740" height="58" rx="8" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="2" />
  <text x="30" y="36" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#1E1C1A">id: uuid_v4</text>
  <text x="240" y="36" font-family="'JetBrains Mono', monospace" font-size="18" fill="#1E1C1A">user: auth.users</text>
  <text x="490" y="36" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#A31C14">rls_enabled: true</text>
</g>

<g transform="translate(50, 185)">
  <rect x="0" y="0" width="740" height="58" rx="8" fill="#FBFAF8" stroke="#1E1C1A" stroke-width="2" />
  <text x="30" y="36" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#1E1C1A">table: orders</text>
  <text x="240" y="36" font-family="'JetBrains Mono', monospace" font-size="18" fill="#1E1C1A">event: INSERT</text>
  <text x="490" y="36" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#1E1C1A">latency: 0ms</text>
</g>

<!-- Realtime broadcast wave -->
<g transform="translate(50, 275)">
  <rect x="0" y="0" width="460" height="130" rx="14" fill="#24211E" stroke="#A31C14" stroke-width="3" />
  <text x="30" y="42" font-family="'JetBrains Mono', monospace" font-size="18" fill="#726D66">WEBSOCKET BROADCAST</text>
  <text x="30" y="80" font-family="'Anton', sans-serif" font-size="34" fill="#FBFAF8">SYNCING 1M CLIENTS</text>
  <circle cx="410" cy="65" r="18" fill="#A31C14" />
  <circle cx="410" cy="65" r="28" fill="none" stroke="#A31C14" stroke-width="2" />
</g>
'''
with open("compositions/point5.html", "w") as f:
    f.write(generate_point_subcomp("point5", "SUPABASE", "SQL", "// 05 · SUPABASE", "STARS <span class='stat-num'>75k+</span>", 5, 75, "★", "🔍", "supabase db pull", True, supabase_demo, "REALTIME", 6.04, 0.16, 6.90))

# 4. compositions/closing.html
closing_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {
        --ink: #1E1C1A;
        --red: #A31C14;
        --grey: #726D66;
        --card-bg: #FBFAF8;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body, #closing {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: transparent;
      }
      .closing-card-wrap {
        position: absolute;
        top: 660px;
        left: 120px;
        width: 840px;
        height: 460px;
      }
      .closing-card-shadow {
        position: absolute;
        top: 12px;
        left: -13px;
        width: 840px;
        height: 460px;
        border-radius: 20px;
        background-image: radial-gradient(var(--ink) 1.7px, transparent 1.7px);
        background-size: 8px 8px;
        z-index: 1;
      }
      .closing-card {
        position: relative;
        z-index: 2;
        width: 840px;
        height: 460px;
        background: var(--card-bg);
        border: 3px solid var(--ink);
        border-radius: 20px;
        padding: 44px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .closing-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 28px;
        color: var(--grey);
        text-transform: uppercase;
      }
      .closing-statement {
        font-family: 'Anton', sans-serif;
        font-size: 72px;
        line-height: 1.05;
        color: var(--ink);
        text-transform: uppercase;
      }
      .strike-line {
        stroke: var(--red);
        stroke-width: 9;
        stroke-linecap: round;
        stroke-dasharray: 780;
        stroke-dashoffset: 780;
      }
    </style>
  </head>
  <body>
    <div id="closing" data-composition-id="closing" data-width="1080" data-height="1920">
      <div class="closing-card-wrap">
        <div class="closing-card-shadow"></div>
        <div class="closing-card">
          <div class="closing-tag" data-layout-ignore>// FINAL VERDICT</div>
          <div class="closing-statement">BUILDING EVERYTHING FROM SCRATCH</div>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 28px; color: var(--red);" data-layout-ignore>
            STATUS: USE OPEN SOURCE
          </div>
          <svg style="position: absolute; top: 0; left: 0; width: 840px; height: 460px; pointer-events: none;">
            <line id="strike-close" class="strike-line" x1="60" y1="230" x2="780" y2="230" />
          </svg>
        </div>
      </div>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      // Strikethrough matches frame 1 on word 'scratch' at 4.08s relative to closing (real time ~43.08s)
      tl.to("#strike-close", {
        strokeDashoffset: 0,
        duration: 0.35,
        ease: "power2.out"
      }, 4.08);

      window.__timelines = window.__timelines || {};
      window.__timelines["closing"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
with open("compositions/closing.html", "w") as f:
    f.write(closing_html)

# 5. compositions/wipe.html
wipe_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body, #wipe {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: transparent;
        pointer-events: none;
      }
      svg {
        width: 1080px;
        height: 1920px;
      }
      .dot {
        fill: #1E1C1A;
        transform-origin: center;
      }
    </style>
  </head>
  <body>
    <div id="wipe" data-composition-id="wipe" data-width="1080" data-height="1920">
      <svg id="wipe-svg">
'''
dot_elements = []
cols = 13
rows = 23
dx = 1080 / (cols + 1)
dy = 1920 / (rows + 1)
center_x = 1080 / 2
center_y = 1920 / 2
max_dist = np.sqrt(center_x**2 + center_y**2)

for r in range(rows):
    for c in range(cols):
        cx = round((c + 1) * dx, 1)
        cy = round((r + 1) * dy, 1)
        d = round(np.sqrt((cx - center_x)**2 + (cy - center_y)**2), 1)
        dot_elements.append(f'<circle id="d-{r}-{c}" class="dot" cx="{cx}" cy="{cy}" r="0" data-dist="{d}" />')

wipe_html += "        " + "\n        ".join(dot_elements) + '''
      </svg>
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      const dots = document.querySelectorAll(".dot");
      const maxDist = ''' + str(round(max_dist, 1)) + ''';

      dots.forEach(d => {
        const dist = parseFloat(d.getAttribute("data-dist"));
        const delay = (dist / maxDist) * 0.35;
        tl.to(d, {
          attr: { r: 62 },
          duration: 0.38,
          ease: "power2.inOut"
        }, delay);
        tl.to(d, {
          attr: { r: 0 },
          duration: 0.34,
          ease: "power2.inOut"
        }, delay + 0.38);
      });

      window.__timelines = window.__timelines || {};
      window.__timelines["wipe"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
with open("compositions/wipe.html", "w") as f:
    f.write(wipe_html)

# 6. compositions/presenter.html
voice_data, voice_sr = sf.read("audio/voice.wav")
if len(voice_data.shape) > 1:
    voice_data = voice_data[:, 0]

fps = 30
frame_samples = int(voice_sr / fps)
total_frames = int(total_duration * fps)

mouth_per_frame = []
cur_mouth = 0

for f_idx in range(total_frames):
    st = f_idx * frame_samples
    en = min(len(voice_data), st + frame_samples)
    if st >= len(voice_data):
        chunk = np.zeros(frame_samples)
    else:
        chunk = voice_data[st:en]
        if len(chunk) < frame_samples:
            chunk = np.pad(chunk, (0, frame_samples - len(chunk)))

    rms = np.sqrt(np.mean(chunk**2)) + 1e-9
    db = 20 * np.log10(rms)

    target_mouth = int(np.clip((db + 42.0) / 26.0 * 9.0, 0, 9))
    if target_mouth > cur_mouth:
        cur_mouth = target_mouth # instant attack
    else:
        cur_mouth = int(round(cur_mouth * 0.55)) # 0.55 release per frame
    mouth_per_frame.append(cur_mouth)

presenter_html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body, #presenter {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: transparent;
      }}
      #presenter-rig {{
        position: absolute;
        left: 430px;
        top: 1170px;
        width: 650px;
        height: 750px;
        transform-origin: 325px 750px;
      }}
      .outline {{
        stroke: #302018;
        stroke-width: 6;
        stroke-linecap: round;
        stroke-linejoin: round;
      }}
    </style>
  </head>
  <body>
    <div id="presenter" data-composition-id="presenter" data-width="1080" data-height="1920">
      <div id="presenter-rig" data-layout-allow-overflow>
        <svg width="650" height="750" viewBox="0 0 650 750" xmlns="http://www.w3.org/2000/svg">
          <!-- Hoodie body -->
          <path class="outline" d="M 120 750 Q 200 480 325 460 Q 450 480 530 750 Z" fill="#2E2B28" />
          <path class="outline" d="M 230 470 Q 325 540 420 470" fill="none" />
          <path class="outline" d="M 325 500 L 325 750" fill="none" stroke-dasharray="16 8" />
          <line x1="280" y1="500" x2="280" y2="600" class="outline" stroke="#FBFAF8" stroke-width="4" />
          <line x1="370" y1="500" x2="370" y2="600" class="outline" stroke="#FBFAF8" stroke-width="4" />

          <!-- Head Anchor for swaying and nodding -->
          <g id="head-anchor" transform="translate(0, 0)">
            <!-- Neck -->
            <rect x="290" y="400" width="70" height="80" fill="#E8B896" class="outline" />

            <!-- Ears -->
            <circle cx="210" cy="340" r="28" fill="#E8B896" class="outline" />
            <circle cx="440" cy="340" r="28" fill="#E8B896" class="outline" />

            <!-- Head Base -->
            <path class="outline" d="M 215 320 C 215 200 435 200 435 320 C 435 440 215 440 215 320 Z" fill="#F4CDB2" />

            <!-- Hair -->
            <path class="outline" d="M 205 290 C 200 180 450 170 445 290 C 420 230 380 230 325 240 C 270 230 230 240 205 290 Z" fill="#1E1C1A" />

            <!-- Eyebrows -->
            <path id="brow-left" class="outline" d="M 240 290 Q 275 275 305 290" fill="none" stroke-width="7" />
            <path id="brow-right" class="outline" d="M 345 290 Q 375 275 410 290" fill="none" stroke-width="7" />

            <!-- Eyes & Glasses -->
            <g id="glasses">
              <rect x="235" y="300" width="75" height="58" rx="20" fill="#FBFAF8" class="outline" />
              <rect x="340" y="300" width="75" height="58" rx="20" fill="#FBFAF8" class="outline" />
              <line x1="310" y1="326" x2="340" y2="326" class="outline" />
              <line x1="210" y1="326" x2="235" y2="326" class="outline" />
              <line x1="415" y1="326" x2="440" y2="326" class="outline" />

              <!-- Pupils -->
              <circle cx="272" cy="326" r="9" fill="#1E1C1A" />
              <circle cx="377" cy="326" r="9" fill="#1E1C1A" />
              <!-- Specular reflection -->
              <circle cx="275" cy="323" r="3" fill="#FBFAF8" />
              <circle cx="380" cy="323" r="3" fill="#FBFAF8" />

              <!-- Eyelids (Blinking) -->
              <g id="eyelids" style="opacity: 0;">
                <rect x="233" y="298" width="79" height="62" rx="20" fill="#F4CDB2" class="outline" />
                <rect x="338" y="298" width="79" height="62" rx="20" fill="#F4CDB2" class="outline" />
                <line x1="240" y1="330" x2="305" y2="330" class="outline" />
                <line x1="345" y1="330" x2="410" y2="330" class="outline" />
              </g>
            </g>

            <!-- Nose -->
            <path class="outline" d="M 325 328 L 320 350 L 332 350" fill="none" stroke-width="5" />

            <!-- 10 Mouth Shapes (m-0 to m-9) -->
            <g id="mouths" transform="translate(325, 390)">
              <!-- 0: Closed / Rest -->
              <path id="m-0" class="outline" d="M -26 0 Q 0 4 26 0" fill="none" />
              <!-- 1: Slight part -->
              <ellipse id="m-1" class="outline" cx="0" cy="2" rx="16" ry="5" fill="#1E1C1A" style="display: none;" />
              <!-- 2: Small round (oo) -->
              <circle id="m-2" class="outline" cx="0" cy="4" r="10" fill="#1E1C1A" style="display: none;" />
              <!-- 3: Medium open (eh) -->
              <ellipse id="m-3" class="outline" cx="0" cy="4" rx="24" ry="10" fill="#1E1C1A" style="display: none;" />
              <!-- 4: Wide grin/smile -->
              <path id="m-4" class="outline" d="M -30 -4 Q 0 16 30 -4 Z" fill="#FBFAF8" style="display: none;" />
              <!-- 5: Open talking 1 -->
              <path id="m-5" class="outline" d="M -26 -4 Q 0 22 26 -4 Z" fill="#1E1C1A" style="display: none;" />
              <!-- 6: Open talking 2 (with tongue) -->
              <g id="m-6" style="display: none;">
                <path class="outline" d="M -28 -4 Q 0 28 28 -4 Z" fill="#1E1C1A" />
                <path d="M -14 12 Q 0 6 14 12 Q 0 26 -14 12 Z" fill="#A31C14" />
              </g>
              <!-- 7: Wide open round (oh) -->
              <ellipse id="m-7" class="outline" cx="0" cy="8" rx="22" ry="20" fill="#1E1C1A" style="display: none;" />
              <!-- 8: Very open talking -->
              <g id="m-8" style="display: none;">
                <path class="outline" d="M -32 -6 Q 0 36 32 -6 Z" fill="#1E1C1A" />
                <path d="M -16 16 Q 0 8 16 16 Q 0 34 -16 16 Z" fill="#A31C14" />
                <rect x="-18" y="-6" width="36" height="8" rx="3" fill="#FBFAF8" />
              </g>
              <!-- 9: Maximum open shout -->
              <g id="m-9" style="display: none;">
                <ellipse class="outline" cx="0" cy="10" rx="30" ry="28" fill="#1E1C1A" />
                <path d="M -18 20 Q 0 10 18 20 Q 0 36 -18 20 Z" fill="#A31C14" />
                <rect x="-20" y="-8" width="40" height="10" rx="3" fill="#FBFAF8" />
              </g>
            </g>
          </g>

          <!-- Pointing Hand (Raises from below for 1.7s on new points) -->
          <g id="hand-point" transform="translate(180, 520)" opacity="0">
            <!-- Sleeve -->
            <path d="M -10 260 L 50 160 L 110 200 L 50 300 Z" fill="#2E2B28" stroke="#302018" stroke-width="6" />
            <!-- Hand & pointing finger -->
            <path d="M 40 160 L 40 40 C 40 20, 65 20, 65 40 L 65 130 C 75 125, 95 130, 90 145 C 95 145, 105 155, 100 170 C 105 170, 110 185, 95 200 L 50 200 Z" fill="#F4CDB2" stroke="#302018" stroke-width="6" stroke-linejoin="round" />
            <line x1="65" y1="90" x2="65" y2="130" stroke="#302018" stroke-width="4" />
          </g>

          <!-- Open Palm Hand (Raises on alternate explanations) -->
          <g id="hand-palm" transform="translate(140, 530)" opacity="0">
            <!-- Sleeve -->
            <path d="M 0 250 L 60 160 L 120 190 L 60 280 Z" fill="#2E2B28" stroke="#302018" stroke-width="6" />
            <!-- Open Palm facing upward -->
            <path d="M 50 170 Q 30 110 60 90 Q 90 70 120 100 Q 150 110 140 160 L 90 195 Z" fill="#F4CDB2" stroke="#302018" stroke-width="6" stroke-linejoin="round" />
            <path d="M 60 130 L 60 90 M 85 125 L 85 85 M 110 130 L 110 95" stroke="#302018" stroke-width="4" stroke-linecap="round" />
          </g>
        </svg>
      </div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
'''

# Sway head slightly all the time
presenter_script_parts = []
presenter_script_parts.append('''
      // Sway head slightly continuous
      tl.to("#head-anchor", {
        rotation: 2.2,
        x: 6,
        duration: 1.4,
        yoyo: true,
        repeat: 31,
        ease: "sine.inOut"
      }, 0);
''')

# Nods on key words
nods = []
for w_idx in key_word_indices:
    w = words[w_idx]
    t = w["start"]
    nods.append(f'tl.to("#head-anchor", {{ y: 16, duration: 0.18, ease: "power2.out" }}, {t});')
    nods.append(f'tl.to("#head-anchor", {{ y: 0, duration: 0.32, ease: "power2.inOut" }}, {round(t + 0.18, 3)});')
presenter_script_parts.append("      " + "\n      ".join(nods))

# Blinking every 2.4-4.2s
np.random.seed(42)
blink_t = 1.2
blinks = []
while blink_t < total_duration:
    blinks.append(f'tl.set("#eyelids", {{ opacity: 1 }}, {round(blink_t, 3)});')
    blinks.append(f'tl.set("#eyelids", {{ opacity: 0 }}, {round(blink_t + 0.14, 3)});')
    blink_t += float(np.random.uniform(2.4, 4.2))
presenter_script_parts.append("      " + "\n      ".join(blinks))

# Pointing hand on each new point (1.7s duration)
point_hand_times = [8.0, 14.0, 19.5, 26.5, 32.1]
hand_points = []
for i, pt in enumerate(point_hand_times):
    imm = "" if i == 0 else ", immediateRender: false"
    hand_points.append(f'tl.fromTo("#hand-point", {{ y: 280, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.28, ease: "power3.out"{imm} }}, {pt});')
    hand_points.append(f'tl.to("#hand-point", {{ y: 280, opacity: 0, duration: 0.24, ease: "power2.in" }}, {round(pt + 1.46, 3)});')
presenter_script_parts.append("      " + "\n      ".join(hand_points))

# Open palm on every other explanation
palm_times = [3.5, 16.5, 29.0, 40.0]
hand_palms = []
for i, pt in enumerate(palm_times):
    imm = "" if i == 0 else ", immediateRender: false"
    hand_palms.append(f'tl.fromTo("#hand-palm", {{ y: 280, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.28, ease: "power3.out"{imm} }}, {pt});')
    hand_palms.append(f'tl.to("#hand-palm", {{ y: 280, opacity: 0, duration: 0.24, ease: "power2.in" }}, {round(pt + 1.46, 3)});')
presenter_script_parts.append("      " + "\n      ".join(hand_palms))

# Mouth shapes per frame at 30fps
mouth_sets = []
cur_m = -1
for f_idx, m_val in enumerate(mouth_per_frame):
    if m_val != cur_m:
        t = round(f_idx / fps, 3)
        if cur_m >= 0:
            mouth_sets.append(f'tl.set("#m-{cur_m}", {{ display: "none" }}, {t});')
        cur_m = m_val
        mouth_sets.append(f'tl.set("#m-{cur_m}", {{ display: "block" }}, {t});')
presenter_script_parts.append("      " + "\n      ".join(mouth_sets))

presenter_script_parts.append('''
      window.__timelines = window.__timelines || {};
      window.__timelines["presenter"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
''')

presenter_html += "\n".join(presenter_script_parts)
with open("compositions/presenter.html", "w") as f:
    f.write(presenter_html)

# 7. compositions/captions.html
sentence_blocks = [
    {"start": 0, "end": 4, "scene_start": 0.0, "scene_end": 2.6},
    {"start": 5, "end": 15, "scene_start": 2.6, "scene_end": 7.8},
    {"start": 16, "end": 26, "scene_start": 7.8, "scene_end": 13.8},
    {"start": 27, "end": 37, "scene_start": 13.8, "scene_end": 19.3},
    {"start": 38, "end": 49, "scene_start": 19.3, "scene_end": 26.3},
    {"start": 50, "end": 60, "scene_start": 26.3, "scene_end": 31.9},
    {"start": 61, "end": 72, "scene_start": 31.9, "scene_end": 38.8},
    {"start": 73, "end": 82, "scene_start": 38.8, "scene_end": 44.0}
]

script_corrections = {
    0: "Building",
    4: "hurts",
    7: "open",
    8: "source",
    16: "React",
    27: "Transformers",
    31: "cutting",
    32: "edge",
    38: "FastAPI",
    39: "",
    44: "backend",
    45: "",
    50: "Tauri",
    59: "frontends",
    60: "",
    61: "Supabase",
    65: "Postgres",
    69: "realtime",
    70: "",
    82: "scratch"
}

captions_html = []
for b_idx, block in enumerate(sentence_blocks):
    captions_html.append(f'<div id="caption-block-{b_idx}" class="caption-block" style="display: none;">')
    for w_idx in range(block["start"], block["end"] + 1):
        w = words[w_idx]
        is_key = w_idx in key_word_indices
        cls = "caption-word key-word" if is_key else "caption-word"
        clean_w = w["word"].replace(".", "").replace(",", "").replace("-", "")
        if w_idx in script_corrections:
            clean_w = script_corrections[w_idx]
        if clean_w:
            captions_html.append(f'<span id="w-{w_idx}" class="{cls}">{clean_w}</span> ')
        else:
            captions_html.append(f'<span id="w-{w_idx}" style="display:none;"></span>')
    captions_html.append('</div>')
captions_str = "\n        ".join(captions_html)

word_tweens = []
for b_idx, block in enumerate(sentence_blocks):
    word_tweens.append(f'tl.set("#caption-block-{b_idx}", {{ display: "block" }}, {block["scene_start"]});')
    if block["scene_end"] < 44.0:
        word_tweens.append(f'tl.set("#caption-block-{b_idx}", {{ display: "none" }}, {block["scene_end"]});')

    for w_idx in range(block["start"], block["end"] + 1):
        w = words[w_idx]
        is_key = w_idx in key_word_indices
        target_color = "#A31C14" if is_key else "#1E1C1A"
        word_tweens.append(f'tl.set("#w-{w_idx}", {{ opacity: 1, color: "#726D66" }}, {w["start"]});')
        word_tweens.append(f'tl.to("#w-{w_idx}", {{ color: "{target_color}", duration: 0.20, ease: "power1.out" }}, {w["start"]});')

word_tweens_str = "\n      ".join(word_tweens)

captions_full_html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,500;0,600;1,500&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --ink: #1E1C1A;
        --red: #A31C14;
        --light-grey: #726D66;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body, #captions {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: transparent;
      }}
      #captions-box {{
        position: absolute;
        top: 196px;
        left: 120px;
        width: 850px;
        display: block;
      }}
      .caption-block {{
        display: block;
        font-family: 'Instrument Sans', sans-serif;
        font-weight: 500;
        font-size: 60px;
        line-height: 1.25;
        color: var(--ink);
      }}
      .caption-word {{
        opacity: 0;
        color: var(--light-grey);
      }}
      .caption-word.key-word {{
        font-family: 'Instrument Serif', serif;
        font-style: italic;
        font-size: 1.16em;
      }}
    </style>
  </head>
  <body>
    <div id="captions" data-composition-id="captions" data-width="1080" data-height="1920">
      <div id="captions-box">
        {captions_str}
      </div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {word_tweens_str}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["captions"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''
with open("compositions/captions.html", "w") as f:
    f.write(captions_full_html)

# 8. Main index.html
index_html = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Top 5 GitHub Open Source Libraries</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=Instrument+Sans:wght@500;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body {
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background-color: #EBE7E1;
      }
      .clip {
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
      }
    </style>
  </head>
  <body>
    <main id="main" data-composition-id="main" data-width="1080" data-height="1920">
      <!-- 1. Paper Background Layer -->
      <div
        id="paper-embed"
        class="clip"
        data-start="0"
        data-duration="44.0"
        data-composition-src="compositions/paper.html"
        data-composition-id="paper-embed"
      ></div>

      <!-- 2. Scene Tracks (Modular Compositions) -->
      <!-- Hook 1 (0.0s - 2.6s) -->
      <div
        id="hook1-embed"
        class="clip"
        data-start="0"
        data-duration="2.6"
        data-composition-src="compositions/hook1.html"
        data-composition-id="hook1-embed"
      ></div>

      <!-- Hook 2 (2.6s - 8.0s) -->
      <div
        id="hook2-embed"
        class="clip"
        data-start="2.6"
        data-duration="5.4"
        data-composition-src="compositions/hook2.html"
        data-composition-id="hook2-embed"
      ></div>

      <!-- Point 1: React (8.0s - 14.0s) -->
      <div
        id="point1-embed"
        class="clip"
        data-start="8.0"
        data-duration="6.0"
        data-composition-src="compositions/point1.html"
        data-composition-id="point1-embed"
      ></div>

      <!-- Point 2: Transformers (14.0s - 19.5s) -->
      <div
        id="point2-embed"
        class="clip"
        data-start="14.0"
        data-duration="5.5"
        data-composition-src="compositions/point2.html"
        data-composition-id="point2-embed"
      ></div>

      <!-- Point 3: FastAPI (19.5s - 26.5s) -->
      <div
        id="point3-embed"
        class="clip"
        data-start="19.5"
        data-duration="7.0"
        data-composition-src="compositions/point3.html"
        data-composition-id="point3-embed"
      ></div>

      <!-- Point 4: Tauri (26.5s - 32.1s) -->
      <div
        id="point4-embed"
        class="clip"
        data-start="26.5"
        data-duration="5.6"
        data-composition-src="compositions/point4.html"
        data-composition-id="point4-embed"
      ></div>

      <!-- Point 5: Supabase (32.1s - 39.0s) -->
      <div
        id="point5-embed"
        class="clip"
        data-start="32.1"
        data-duration="6.9"
        data-composition-src="compositions/point5.html"
        data-composition-id="point5-embed"
      ></div>

      <!-- Closing: Loop Payoff (39.0s - 44.0s) -->
      <div
        id="closing-embed"
        class="clip"
        data-start="39.0"
        data-duration="5.0"
        data-composition-src="compositions/closing.html"
        data-composition-id="closing-embed"
      ></div>

      <!-- 3. Halftone Dot Wipes -->
      <!-- Wipe 1: 0.3s before Point 1 (7.7s - 8.6s) -->
      <div
        id="wipe-1-embed"
        class="clip"
        data-start="7.7"
        data-duration="0.9"
        data-composition-src="compositions/wipe.html"
        data-composition-id="wipe-1-embed"
      ></div>

      <!-- Wipe 2: Before Point 5 (31.8s - 32.7s) -->
      <div
        id="wipe-2-embed"
        class="clip"
        data-start="31.8"
        data-duration="0.9"
        data-composition-src="compositions/wipe.html"
        data-composition-id="wipe-2-embed"
      ></div>

      <!-- 4. Presenter Layer -->
      <div
        id="presenter-embed"
        class="clip"
        data-start="0"
        data-duration="44.0"
        data-composition-src="compositions/presenter.html"
        data-composition-id="presenter-embed"
      ></div>

      <!-- 5. Captions Layer -->
      <div
        id="captions-embed"
        class="clip"
        data-start="0"
        data-duration="44.0"
        data-composition-src="compositions/captions.html"
        data-composition-id="captions-embed"
      ></div>

      <!-- 6. Sound Effects & Voice Audio Tracks -->
      <!-- Voiceover -->
      <audio id="audio-voice" src="audio/voice.wav" data-start="0" data-duration="43.98"></audio>
      <!-- Background Music at 0.16 volume -->
      <audio id="audio-music" src="audio/music.wav" data-start="0" data-duration="44.0" volume="0.16"></audio>

      <!-- Pops -->
      <audio id="sfx-pop-1" src="audio/pop.wav" data-start="0.10" data-duration="0.12"></audio>
      <audio id="sfx-pop-2" src="audio/pop.wav" data-start="2.95" data-duration="0.12"></audio>
      <audio id="sfx-pop-3" src="audio/pop.wav" data-start="3.11" data-duration="0.12"></audio>
      <audio id="sfx-pop-4" src="audio/pop.wav" data-start="3.27" data-duration="0.12"></audio>
      <audio id="sfx-pop-5" src="audio/pop.wav" data-start="3.43" data-duration="0.12"></audio>
      <audio id="sfx-pop-6" src="audio/pop.wav" data-start="3.59" data-duration="0.12"></audio>
      <audio id="sfx-pop-7" src="audio/pop.wav" data-start="8.38" data-duration="0.12"></audio>
      <audio id="sfx-pop-8" src="audio/pop.wav" data-start="14.44" data-duration="0.12"></audio>
      <audio id="sfx-pop-9" src="audio/pop.wav" data-start="19.86" data-duration="0.12"></audio>
      <audio id="sfx-pop-10" src="audio/pop.wav" data-start="26.76" data-duration="0.12"></audio>
      <audio id="sfx-pop-11" src="audio/pop.wav" data-start="32.44" data-duration="0.12"></audio>
      <audio id="sfx-pop-12" src="audio/pop.wav" data-start="39.20" data-duration="0.12"></audio>

      <!-- Whooshes -->
      <audio id="sfx-whoosh-1" src="audio/whoosh.wav" data-start="2.40" data-duration="0.45"></audio>
      <audio id="sfx-whoosh-2" src="audio/whoosh.wav" data-start="7.70" data-duration="0.45"></audio>
      <audio id="sfx-whoosh-3" src="audio/whoosh.wav" data-start="13.70" data-duration="0.45"></audio>
      <audio id="sfx-whoosh-4" src="audio/whoosh.wav" data-start="19.20" data-duration="0.45"></audio>
      <audio id="sfx-whoosh-5" src="audio/whoosh.wav" data-start="26.20" data-duration="0.45"></audio>
      <audio id="sfx-whoosh-6" src="audio/whoosh.wav" data-start="31.80" data-duration="0.45"></audio>
      <audio id="sfx-whoosh-7" src="audio/whoosh.wav" data-start="38.70" data-duration="0.45"></audio>

      <!-- Thuds on Stamps -->
      <audio id="sfx-thud-1" src="audio/thud.wav" data-start="10.00" data-duration="0.35"></audio>
      <audio id="sfx-thud-2" src="audio/thud.wav" data-start="17.18" data-duration="0.35"></audio>
      <audio id="sfx-thud-3" src="audio/thud.wav" data-start="25.64" data-duration="0.35"></audio>
      <audio id="sfx-thud-4" src="audio/thud.wav" data-start="29.30" data-duration="0.35"></audio>
      <audio id="sfx-thud-5" src="audio/thud.wav" data-start="38.14" data-duration="0.35"></audio>

      <!-- Tick rolls under counters -->
      <audio id="sfx-tick-1" src="audio/tick.wav" data-start="8.50" data-duration="0.05"></audio>
      <audio id="sfx-tick-2" src="audio/tick.wav" data-start="14.60" data-duration="0.05"></audio>
      <audio id="sfx-tick-3" src="audio/tick.wav" data-start="20.00" data-duration="0.05"></audio>
      <audio id="sfx-tick-4" src="audio/tick.wav" data-start="26.90" data-duration="0.05"></audio>
      <audio id="sfx-tick-5" src="audio/tick.wav" data-start="32.60" data-duration="0.05"></audio>

      <!-- Typing sounds under terminal / search -->
      <audio id="sfx-type-1" src="audio/typing.wav" data-start="8.70" data-duration="0.08"></audio>
      <audio id="sfx-type-2" src="audio/typing.wav" data-start="14.80" data-duration="0.08"></audio>
      <audio id="sfx-type-3" src="audio/typing.wav" data-start="20.30" data-duration="0.08"></audio>
      <audio id="sfx-type-4" src="audio/typing.wav" data-start="27.20" data-duration="0.08"></audio>
      <audio id="sfx-type-5" src="audio/typing.wav" data-start="32.80" data-duration="0.08"></audio>
    </main>

    <script>
      const rootTl = gsap.timeline({ paused: true });
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = rootTl;
      rootTl.seek(0);
    </script>
  </body>
</html>
'''
with open("index.html", "w") as f:
    f.write(index_html)

print("Saved all compositions for Top 5 GitHub Open Source Libraries!")
