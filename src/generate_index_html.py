# // ponytail: script to compile index.html with all required HyperFrames tracks, timings, and presenter rig
import json

with open("transcript.json") as f:
    transcript = json.load(f)

words = transcript["words"]

# Precompute key word indices
key_word_indices = {
    4: "scary.",       # Line 1
    9: "ruin",         # Line 2
    29: "nightmare.",  # Tumbbad
    36: "terror,",     # Bramayugam
    55: "ghost.",      # Bhoothakalam
    70: "scare.",      # Raat
    83: "paranoia.",   # 13B
    97: "scary."       # Closing
}

# Group words into sentence blocks for captions
sentence_blocks = [
    {"start": 0, "end": 4, "scene_start": 0.0, "scene_end": 1.8},
    {"start": 5, "end": 16, "scene_start": 1.8, "scene_end": 5.3},
    {"start": 17, "end": 29, "scene_start": 5.3, "scene_end": 10.25},
    {"start": 30, "end": 40, "scene_start": 10.25, "scene_end": 14.8},
    {"start": 41, "end": 55, "scene_start": 14.8, "scene_end": 19.8},
    {"start": 56, "end": 70, "scene_start": 19.8, "scene_end": 25.25},
    {"start": 71, "end": 83, "scene_start": 25.25, "scene_end": 31.25},
    {"start": 84, "end": 97, "scene_start": 31.25, "scene_end": 35.5}
]

# Generate captions HTML
captions_html = []
for b_idx, block in enumerate(sentence_blocks):
    captions_html.append(f'<div id="caption-block-{b_idx}" class="caption-block" style="display: none;">')
    for w_idx in range(block["start"], block["end"] + 1):
        w = words[w_idx]
        is_key = w_idx in key_word_indices
        cls = "caption-word key-word" if is_key else "caption-word"
        clean_w = w["word"].replace(".", "").replace(",", "")
        captions_html.append(f'<span id="w-{w_idx}" class="{cls}" data-start="{w["start"]}">{clean_w}</span> ')
    captions_html.append('</div>')

captions_str = "\n        ".join(captions_html)

# Read dots for wipes
with open("src/dots.json") as f:
    dots = json.load(f)

wipe_svg_circles = []
for d in dots:
    wipe_svg_circles.append(f'<circle class="wipe-dot" data-delay="{d["delay"]}" cx="{d["x"]}" cy="{d["y"]}" r="0" fill="#1E1C1A" />')
wipe_dots_str = "\n          ".join(wipe_svg_circles)

# Generate GSAP word animations
word_tweens = []
for b_idx, block in enumerate(sentence_blocks):
    # Show block at its scene start, hide at scene end
    word_tweens.append(f'tl.set("#caption-block-{b_idx}", {{ display: "block" }}, {block["scene_start"]});')
    if block["scene_end"] < 35.5:
        word_tweens.append(f'tl.set("#caption-block-{b_idx}", {{ display: "none" }}, {block["scene_end"]});')
    
    for w_idx in range(block["start"], block["end"] + 1):
        w = words[w_idx]
        is_key = w_idx in key_word_indices
        target_color = "#D7372C" if is_key else "#1E1C1A"
        # Word appears in light grey #B5AFA7 on frame it's spoken, turns ink (or red) in 0.2s
        word_tweens.append(f'tl.set("#w-{w_idx}", {{ opacity: 1, color: "#B5AFA7" }}, {w["start"]});')
        word_tweens.append(f'tl.to("#w-{w_idx}", {{ color: "{target_color}", duration: 0.20, ease: "power1.out" }}, {w["start"]});')

word_tweens_str = "\n      ".join(word_tweens)

# Read mouth intervals from build_project
import soundfile as sf
import numpy as np

audio, sr = sf.read("audio/voice.wav")
fps = 30
frame_samples = int(sr / fps)
total_frames = int(len(audio) / frame_samples)
min_db, max_db = -42.0, -16.0
prev = 0.0
mouth_timeline = []

for f in range(total_frames):
    chunk = audio[f*frame_samples : (f+1)*frame_samples]
    rms = np.sqrt(np.mean(chunk**2)) + 1e-9
    db = 20 * np.log10(rms)
    raw_val = max(0.0, min(1.0, (db - min_db) / (max_db - min_db)))
    if raw_val >= prev:
        val = raw_val
    else:
        val = prev * 0.55 + raw_val * 0.45
    prev = val
    mouth_idx = int(round(val * 9.0))
    mouth_timeline.append(mouth_idx)

mouth_sets = []
cur_m = mouth_timeline[0]
mouth_sets.append(f'tl.set(".mouth-shape", {{ display: "none" }}, 0);')
mouth_sets.append(f'tl.set("#m-{cur_m}", {{ display: "block" }}, 0);')

for f in range(1, total_frames):
    if mouth_timeline[f] != cur_m:
        cur_m = mouth_timeline[f]
        t = round(f / fps, 3)
        mouth_sets.append(f'tl.set(".mouth-shape", {{ display: "none" }}, {t});')
        mouth_sets.append(f'tl.set("#m-{cur_m}", {{ display: "block" }}, {t});')

mouth_sets_str = "\n      ".join(mouth_sets)

# Nods on key words
nods = []
for w_idx in key_word_indices:
    w = words[w_idx]
    t = w["start"]
    nods.append(f'tl.to("#head-anchor", {{ y: 16, rotation: 1.5, duration: 0.18, ease: "power2.out" }}, {t});')
    nods.append(f'tl.to("#head-anchor", {{ y: 0, rotation: 0, duration: 0.32, ease: "power2.inOut" }}, {round(t + 0.18, 3)});')
nods_str = "\n      ".join(nods)

# Deterministic blinks (0.14s every 2.4-4.2s)
blink_times = [2.6, 5.8, 9.2, 12.8, 16.2, 19.8, 23.4, 27.0, 30.6, 33.8]
blinks = []
for bt in blink_times:
    blinks.append(f'tl.to(".eyelid-path", {{ scaleY: 1, duration: 0.07, ease: "power1.in" }}, {bt});')
    blinks.append(f'tl.to(".eyelid-path", {{ scaleY: 0, duration: 0.07, ease: "power1.out" }}, {round(bt + 0.07, 3)});')
blinks_str = "\n      ".join(blinks)

# Pointing hand raises for 1.7s at every new point
hand_point_times = [5.30, 10.25, 14.80, 19.80, 25.25]
hand_point_tweens = []
for pt in hand_point_times:
    hand_point_tweens.append(f'tl.fromTo("#hand-pointing", {{ y: 280, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.28, ease: "power3.out" }}, {pt});')
    hand_point_tweens.append(f'tl.to("#hand-pointing", {{ y: 280, opacity: 0, duration: 0.24, ease: "power2.in" }}, {round(pt + 1.46, 3)});')
hand_point_str = "\n      ".join(hand_point_tweens)

# Open palm on every other explanation
hand_palm_times = [7.60, 17.00, 27.50]
hand_palm_tweens = []
for pt in hand_palm_times:
    hand_palm_tweens.append(f'tl.fromTo("#hand-palm", {{ y: 280, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.28, ease: "power3.out" }}, {pt});')
    hand_palm_tweens.append(f'tl.to("#hand-palm", {{ y: 280, opacity: 0, duration: 0.24, ease: "power2.in" }}, {round(pt + 1.46, 3)});')
hand_palm_str = "\n      ".join(hand_palm_tweens)

# Halftone dot wipes animation (Wipe 1 at 5.00s, Wipe 2 at 24.95s)
wipe_tweens = []
for wipe_start, wipe_id in [(5.00, "#wipe-1"), (24.95, "#wipe-2")]:
    wipe_tweens.append(f'tl.set("{wipe_id}", {{ display: "block" }}, {wipe_start});')
    # Loop over all dots using GSAP stagger/custom logic
    wipe_tweens.append(f'''
      document.querySelectorAll("{wipe_id} .wipe-dot").forEach(dot => {{
        const delay = parseFloat(dot.getAttribute("data-delay"));
        tl.to(dot, {{ attr: {{ r: 62 }}, duration: 0.34, ease: "power2.in" }}, {round(wipe_start, 3)} + delay);
        tl.to(dot, {{ attr: {{ r: 0 }}, duration: 0.34, ease: "power2.out" }}, {round(wipe_start + 0.38, 3)} + delay);
      }});
    ''')
    wipe_tweens.append(f'tl.set("{wipe_id}", {{ display: "none" }}, {round(wipe_start + 0.90, 3)});')
wipe_tweens_str = "\n      ".join(wipe_tweens)

html_content = f'''<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Top 5 Indian Horror Movies</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Anton&family=Instrument+Sans:ital,wght@0,500;0,600;1,500&family=Instrument+Serif:ital@1&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --paper: #EBE7E1;
        --ink: #1E1C1A;
        --red: #D7372C;
        --grey: #8A857E;
        --light-grey: #B5AFA7;
        --card-bg: #FBFAF8;
        --outline: #302018;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: var(--paper);
        font-family: 'Instrument Sans', sans-serif;
        color: var(--ink);
      }}

      /* Base layout & full-frame clip */
      #root {{
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
      }}
      .clip {{
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
      }}

      /* Paper grain texture overlay */
      #paper-texture {{
        position: absolute;
        inset: 0;
        background-color: var(--paper);
        pointer-events: none;
        z-index: 0;
      }}
      .grain-svg {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        opacity: 0.35;
        pointer-events: none;
      }}

      /* Halftone shadow helper */
      .halftone-card {{
        position: absolute;
        background: var(--card-bg);
        border: 3px solid var(--ink);
        border-radius: 20px;
      }}
      .halftone-shadow {{
        position: absolute;
        background-image: radial-gradient(var(--ink) 0.85px, transparent 0.85px);
        background-size: 8px 8px;
        border-radius: 20px;
        pointer-events: none;
      }}

      /* Scene 0 Hook Line 1 Problem Card */
      #scene-hook-1 {{
        z-index: 2;
      }}
      .hook-card-wrap {{
        position: absolute;
        top: 480px;
        left: 120px;
        width: 840px;
        height: 520px;
      }}
      .hook-card-shadow {{
        top: 12px;
        left: -13px;
        width: 840px;
        height: 520px;
      }}
      .hook-card {{
        top: 0;
        left: 0;
        width: 840px;
        height: 520px;
        padding: 50px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}
      .hook-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        color: var(--grey);
        text-transform: uppercase;
      }}
      .hook-statement {{
        font-family: 'Anton', sans-serif;
        font-size: 84px;
        line-height: 1.05;
        color: var(--ink);
        text-transform: uppercase;
      }}
      .strike-line {{
        stroke: var(--red);
        stroke-width: 9;
        stroke-linecap: round;
        stroke-dasharray: 780;
        stroke-dashoffset: 780;
      }}

      /* Scene 1 Hook Line 2 Payoff Cards */
      #scene-hook-2 {{
        z-index: 2;
      }}
      .payoff-grid {{
        position: absolute;
        top: 440px;
        left: 120px;
        width: 840px;
        height: 600px;
        display: flex;
        flex-direction: column;
        gap: 20px;
      }}
      .mini-card-wrap {{
        position: relative;
        width: 840px;
        height: 96px;
        transform: scale(0.55);
        opacity: 0;
      }}
      .mini-card-shadow {{
        top: 12px;
        left: -13px;
        width: 840px;
        height: 96px;
      }}
      .mini-card {{
        top: 0;
        left: 0;
        width: 840px;
        height: 96px;
        padding: 0 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
      }}
      .mini-title {{
        font-family: 'Anton', sans-serif;
        font-size: 42px;
        color: var(--ink);
        text-transform: uppercase;
      }}
      .mini-year {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        color: var(--red);
        font-weight: 700;
      }}
      .payoff-ring-svg {{
        position: absolute;
        top: 410px;
        left: 90px;
        width: 900px;
        height: 660px;
        pointer-events: none;
        z-index: 10;
      }}
      .payoff-ring-path {{
        stroke: var(--red);
        stroke-width: 8;
        stroke-linecap: round;
        fill: none;
        stroke-dasharray: 2600;
        stroke-dashoffset: 2600;
      }}

      /* Scene 7 Closing Scene */
      #scene-closing {{
        z-index: 2;
        opacity: 0;
      }}
      .closing-card-wrap {{
        position: absolute;
        top: 480px;
        left: 120px;
        width: 840px;
        height: 520px;
      }}

      /* Captions Container (top left x 120, y 196, 850 wide) */
      #captions-track {{
        position: absolute;
        top: 196px;
        left: 120px;
        width: 850px;
        z-index: 15;
        pointer-events: none;
      }}
      .caption-block {{
        font-family: 'Instrument Sans', sans-serif;
        font-weight: 500;
        font-size: 62px;
        line-height: 1.25;
        color: var(--ink);
        text-transform: none;
      }}
      .caption-word {{
        opacity: 0;
        color: var(--light-grey);
      }}
      .caption-word.key-word {{
        font-family: 'Instrument Serif', serif;
        font-style: italic;
        font-size: 1.16em;
        line-height: 1;
      }}

      /* Cartoon Presenter Rig (x 430, y 1170, 650x770) */
      #presenter-container {{
        position: absolute;
        top: 1170px;
        left: 430px;
        width: 650px;
        height: 770px;
        z-index: 12;
        pointer-events: none;
      }}
      .presenter-svg {{
        width: 650px;
        height: 770px;
        overflow: visible;
      }}

      /* Halftone Dot Wipes Track */
      .wipe-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 1920px;
        z-index: 30;
        pointer-events: none;
        display: none;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="35.5">
      <!-- TRACK 0: PAPER GROUND WITH FINE NOISE GRAIN -->
      <div id="paper-ground" class="clip" data-start="0" data-duration="35.5" data-track-index="0">
        <div id="paper-texture">
          <svg class="grain-svg" viewBox="0 0 1080 1920">
            <filter id="noiseFilter">
              <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch" />
              <feColorMatrix type="matrix" values="0 0 0 0 0.12  0 0 0 0 0.11  0 0 0 0 0.10  0 0 0 0.08 0" />
            </filter>
            <rect width="1080" height="1920" filter="url(#noiseFilter)" />
          </svg>
        </div>
      </div>

      <!-- TRACK 1: SCENES -->
      <!-- Scene 0: Hook Line 1 Problem Card -->
      <div id="scene-hook-1" class="clip" data-start="0" data-duration="1.80" data-track-index="1">
        <div class="hook-card-wrap">
          <div class="halftone-shadow hook-card-shadow"></div>
          <div class="halftone-card hook-card">
            <div class="hook-tag">// 00 · COMMON MYTH</div>
            <div class="hook-statement">INDIAN HORROR = NOT SCARY</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--red);">
              STATUS: COMPLETELY FALSE
            </div>
            <svg style="position: absolute; top: 0; left: 0; width: 840px; height: 520px; pointer-events: none;">
              <line id="strike-1" class="strike-line" x1="60" y1="280" x2="780" y2="280" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Scene 1: Hook Line 2 Payoff Cards -->
      <div id="scene-hook-2" class="clip" data-start="1.80" data-duration="3.50" data-track-index="1">
        <div class="payoff-grid">
          <div id="mini-1" class="mini-card-wrap">
            <div class="halftone-shadow mini-card-shadow"></div>
            <div class="halftone-card mini-card">
              <span class="mini-title">01 · TUMBBAD</span><span class="mini-year">2018</span>
            </div>
          </div>
          <div id="mini-2" class="mini-card-wrap">
            <div class="halftone-shadow mini-card-shadow"></div>
            <div class="halftone-card mini-card">
              <span class="mini-title">02 · BRAMAYUGAM</span><span class="mini-year">2024</span>
            </div>
          </div>
          <div id="mini-3" class="mini-card-wrap">
            <div class="halftone-shadow mini-card-shadow"></div>
            <div class="halftone-card mini-card">
              <span class="mini-title">03 · BHOOTHAKALAM</span><span class="mini-year">2022</span>
            </div>
          </div>
          <div id="mini-4" class="mini-card-wrap">
            <div class="halftone-shadow mini-card-shadow"></div>
            <div class="halftone-card mini-card">
              <span class="mini-title">04 · RAAT</span><span class="mini-year">1992</span>
            </div>
          </div>
          <div id="mini-5" class="mini-card-wrap">
            <div class="halftone-shadow mini-card-shadow"></div>
            <div class="halftone-card mini-card">
              <span class="mini-title">05 · 13B</span><span class="mini-year">2009</span>
            </div>
          </div>
        </div>
        <svg class="payoff-ring-svg" viewBox="0 0 900 660">
          <path id="payoff-ring-path" class="payoff-ring-path" d="M 450 40 C 780 40, 860 160, 860 330 C 860 500, 780 620, 450 620 C 120 620, 40 500, 40 330 C 40 160, 120 40, 450 40 Z" />
        </svg>
      </div>

      <!-- Point 1 Sub-comp -->
      <div id="point1-embed" class="clip" data-start="5.30" data-duration="4.95" data-composition-src="compositions/point1.html" data-composition-id="point1-embed" data-track-index="1"></div>

      <!-- Point 2 Sub-comp -->
      <div id="point2-embed" class="clip" data-start="10.25" data-duration="4.55" data-composition-src="compositions/point2.html" data-composition-id="point2-embed" data-track-index="1"></div>

      <!-- Point 3 Sub-comp -->
      <div id="point3-embed" class="clip" data-start="14.80" data-duration="5.00" data-composition-src="compositions/point3.html" data-composition-id="point3-embed" data-track-index="1"></div>

      <!-- Point 4 Sub-comp -->
      <div id="point4-embed" class="clip" data-start="19.80" data-duration="5.45" data-composition-src="compositions/point4.html" data-composition-id="point4-embed" data-track-index="1"></div>

      <!-- Point 5 Sub-comp -->
      <div id="point5-embed" class="clip" data-start="25.25" data-duration="6.00" data-composition-src="compositions/point5.html" data-composition-id="point5-embed" data-track-index="1"></div>

      <!-- Scene 7: Closing Scene Loop Back -->
      <div id="scene-closing" class="clip" data-start="31.25" data-duration="4.25" data-track-index="1">
        <div class="closing-card-wrap">
          <div class="halftone-shadow hook-card-shadow"></div>
          <div id="closing-card-inner" class="halftone-card hook-card">
            <div class="hook-tag">// FINAL VERDICT</div>
            <div id="closing-heading" class="hook-statement">SURVIVE ALL FIVE</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 24px; color: var(--red);">
              THEN DARE CLAIM INDIAN HORROR IS NOT SCARY
            </div>
            <svg style="position: absolute; top: 0; left: 0; width: 840px; height: 520px; pointer-events: none;">
              <line id="strike-closing" class="strike-line" x1="60" y1="280" x2="780" y2="280" />
            </svg>
          </div>
        </div>
      </div>

      <!-- TRACK 2: PRESENTER SVG RIG -->
      <div id="presenter-container" class="clip" data-start="0" data-duration="35.5" data-track-index="2">
        <svg class="presenter-svg" viewBox="0 0 650 770">
          <!-- Hoodie Torso & Shoulders -->
          <g id="torso-group">
            <!-- Hoodie body -->
            <path d="M 120 770 C 120 560, 240 500, 360 500 C 480 500, 600 560, 600 770 Z" fill="#35302D" stroke="var(--outline)" stroke-width="6" stroke-linejoin="round" />
            <!-- Inner collar fold -->
            <path d="M 280 500 Q 360 560 440 500" stroke="var(--outline)" stroke-width="6" stroke-linecap="round" fill="none" />
            <!-- Drawstrings -->
            <path d="M 330 540 L 330 630" stroke="#EBE7E1" stroke-width="5" stroke-linecap="round" />
            <path d="M 390 540 L 390 630" stroke="#EBE7E1" stroke-width="5" stroke-linecap="round" />
            <circle cx="330" cy="635" r="5" fill="var(--red)" />
            <circle cx="390" cy="635" r="5" fill="var(--red)" />
          </g>

          <!-- Head Anchor for Sway & Nods -->
          <g id="head-anchor" transform-origin="360 460">
            <!-- Neck -->
            <rect x="315" y="440" width="90" height="90" rx="10" fill="#F2C4A2" stroke="var(--outline)" stroke-width="6" />

            <!-- Head Group -->
            <g id="head-group" transform-origin="360 300">
              <!-- Ears -->
              <circle cx="210" cy="310" r="28" fill="#F2C4A2" stroke="var(--outline)" stroke-width="6" />
              <path d="M 205 300 Q 215 310 205 320" stroke="var(--outline)" stroke-width="4" fill="none" />
              <circle cx="510" cy="310" r="28" fill="#F2C4A2" stroke="var(--outline)" stroke-width="6" />
              <path d="M 515 300 Q 505 310 515 320" stroke="var(--outline)" stroke-width="4" fill="none" />

              <!-- Face Shape -->
              <path d="M 230 220 C 230 110, 490 110, 490 220 C 490 350, 430 460, 360 460 C 290 460, 230 350, 230 220 Z" fill="#F2C4A2" stroke="var(--outline)" stroke-width="6" stroke-linejoin="round" />

              <!-- Stylish Hair -->
              <path d="M 215 200 C 215 90, 310 50, 400 60 C 490 70, 505 130, 505 190 C 470 140, 390 130, 340 145 C 290 160, 240 180, 215 200 Z" fill="#231C18" stroke="var(--outline)" stroke-width="6" stroke-linejoin="round" />

              <!-- Eyebrows -->
              <path d="M 270 230 Q 310 215 335 230" stroke="var(--outline)" stroke-width="7" stroke-linecap="round" fill="none" />
              <path d="M 385 230 Q 410 215 450 230" stroke="var(--outline)" stroke-width="7" stroke-linecap="round" fill="none" />

              <!-- Eyes Base -->
              <ellipse cx="305" cy="270" rx="28" ry="24" fill="#FBFAF8" stroke="var(--outline)" stroke-width="5" />
              <circle cx="310" cy="270" r="11" fill="var(--ink)" />
              <circle cx="314" cy="266" r="3.5" fill="#FBFAF8" />

              <ellipse cx="415" cy="270" rx="28" ry="24" fill="#FBFAF8" stroke="var(--outline)" stroke-width="5" />
              <circle cx="420" cy="270" r="11" fill="var(--ink)" />
              <circle cx="424" cy="266" r="3.5" fill="#FBFAF8" />

              <!-- Eyelids for Blinking -->
              <g id="eyelids" transform-origin="360 270">
                <path class="eyelid-path" d="M 277 246 Q 305 270 333 246 L 333 240 L 277 240 Z" fill="#F2C4A2" transform="scale(1, 0)" transform-origin="305 246" />
                <path class="eyelid-path" d="M 387 246 Q 415 270 443 246 L 443 240 L 387 240 Z" fill="#F2C4A2" transform="scale(1, 0)" transform-origin="415 246" />
              </g>

              <!-- Stylish Glasses -->
              <g id="glasses-group">
                <!-- Left frame -->
                <rect x="265" y="235" width="80" height="70" rx="18" fill="none" stroke="var(--ink)" stroke-width="8" />
                <!-- Right frame -->
                <rect x="375" y="235" width="80" height="70" rx="18" fill="none" stroke="var(--ink)" stroke-width="8" />
                <!-- Bridge -->
                <path d="M 345 260 Q 360 250 375 260" stroke="var(--ink)" stroke-width="8" stroke-linecap="round" fill="none" />
                <!-- Temples -->
                <line x1="265" y1="260" x2="215" y2="280" stroke="var(--ink)" stroke-width="6" stroke-linecap="round" />
                <line x1="455" y1="260" x2="505" y2="280" stroke="var(--ink)" stroke-width="6" stroke-linecap="round" />
              </g>

              <!-- Nose -->
              <path d="M 355 285 Q 365 315 350 325 L 365 325" stroke="var(--outline)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none" />

              <!-- 10 Mouth Shapes (m-0 to m-9) -->
              <g id="mouth-anchor" transform="translate(360, 380)">
                <!-- m-0: Closed subtle smile -->
                <g id="m-0" class="mouth-shape">
                  <path d="M -30 0 Q 0 6 30 0" stroke="var(--outline)" stroke-width="6" stroke-linecap="round" fill="none" />
                </g>
                <!-- m-1: Slightly parted -->
                <g id="m-1" class="mouth-shape" style="display: none;">
                  <path d="M -26 -4 Q 0 8 26 -4 Q 0 -6 -26 -4 Z" fill="#141210" stroke="var(--outline)" stroke-width="5" />
                  <line x1="-16" y1="-3" x2="16" y2="-3" stroke="#FBFAF8" stroke-width="3" />
                </g>
                <!-- m-2: Small round 'o' -->
                <g id="m-2" class="mouth-shape" style="display: none;">
                  <ellipse cx="0" cy="0" rx="16" ry="14" fill="#141210" stroke="var(--outline)" stroke-width="5" />
                </g>
                <!-- m-3: Medium 'ah' -->
                <g id="m-3" class="mouth-shape" style="display: none;">
                  <path d="M -28 -6 C -28 20, 28 20, 28 -6 Z" fill="#141210" stroke="var(--outline)" stroke-width="6" />
                  <ellipse cx="0" cy="8" rx="14" ry="6" fill="var(--red)" />
                </g>
                <!-- m-4: Wide open 'AH' -->
                <g id="m-4" class="mouth-shape" style="display: none;">
                  <path d="M -34 -10 C -34 28, 34 28, 34 -10 Z" fill="#141210" stroke="var(--outline)" stroke-width="6" />
                  <path d="M -22 -10 L 22 -10 L 18 -4 L -18 -4 Z" fill="#FBFAF8" />
                  <ellipse cx="0" cy="14" rx="18" ry="8" fill="var(--red)" />
                </g>
                <!-- m-5: Wide stretch 'ee' -->
                <g id="m-5" class="mouth-shape" style="display: none;">
                  <path d="M -36 -2 Q 0 -8 36 -2 Q 0 12 -36 -2 Z" fill="#141210" stroke="var(--outline)" stroke-width="5" />
                  <path d="M -30 -1 Q 0 -6 30 -1 L 28 4 Q 0 8 -28 4 Z" fill="#FBFAF8" />
                </g>
                <!-- m-6: Puckered 'oo' -->
                <g id="m-6" class="mouth-shape" style="display: none;">
                  <ellipse cx="0" cy="0" rx="12" ry="18" fill="#141210" stroke="var(--outline)" stroke-width="6" />
                </g>
                <!-- m-7: Clenched teeth 'th/s' -->
                <g id="m-7" class="mouth-shape" style="display: none;">
                  <rect x="-30" y="-6" width="60" height="14" rx="4" fill="#141210" stroke="var(--outline)" stroke-width="5" />
                  <line x1="-24" y1="1" x2="24" y2="1" stroke="#FBFAF8" stroke-width="6" />
                </g>
                <!-- m-8: Lower lip bite 'f/v' -->
                <g id="m-8" class="mouth-shape" style="display: none;">
                  <path d="M -28 0 Q 0 -4 28 0 Q 0 14 -28 0 Z" fill="#141210" stroke="var(--outline)" stroke-width="5" />
                  <path d="M -20 0 L 20 0 L 16 6 L -16 6 Z" fill="#FBFAF8" />
                </g>
                <!-- m-9: Full shout / intense open -->
                <g id="m-9" class="mouth-shape" style="display: none;">
                  <path d="M -38 -14 C -34 36, 34 36, 38 -14 Z" fill="#141210" stroke="var(--outline)" stroke-width="6" />
                  <path d="M -24 -14 L 24 -14 L 18 -6 L -18 -6 Z" fill="#FBFAF8" />
                  <ellipse cx="0" cy="18" rx="20" ry="10" fill="var(--red)" />
                </g>
              </g>
            </g>
          </g>

          <!-- Pointing Hand (Raises from below for 1.7s on new points) -->
          <g id="hand-pointing" transform="translate(180, 520)" opacity="0">
            <!-- Sleeve -->
            <path d="M -10 260 L 50 160 L 110 200 L 50 300 Z" fill="#35302D" stroke="var(--outline)" stroke-width="6" />
            <!-- Hand & pointing finger -->
            <path d="M 40 160 L 40 40 C 40 20, 65 20, 65 40 L 65 130 C 75 125, 95 130, 90 145 C 95 145, 105 155, 100 170 C 105 170, 110 185, 95 200 L 50 200 Z" fill="#F2C4A2" stroke="var(--outline)" stroke-width="6" stroke-linejoin="round" />
            <line x1="65" y1="90" x2="65" y2="130" stroke="var(--outline)" stroke-width="4" />
          </g>

          <!-- Open Palm Hand (Raises on alternate explanations) -->
          <g id="hand-palm" transform="translate(140, 530)" opacity="0">
            <!-- Sleeve -->
            <path d="M 0 250 L 60 160 L 120 190 L 60 280 Z" fill="#35302D" stroke="var(--outline)" stroke-width="6" />
            <!-- Open Palm facing upward -->
            <path d="M 50 170 Q 30 110 60 90 Q 90 70 120 100 Q 150 110 140 160 L 90 195 Z" fill="#F2C4A2" stroke="var(--outline)" stroke-width="6" stroke-linejoin="round" />
            <path d="M 60 130 L 60 90 M 85 125 L 85 85 M 110 130 L 110 95" stroke="var(--outline)" stroke-width="4" stroke-linecap="round" />
          </g>
        </svg>
      </div>

      <!-- TRACK 3: CAPTIONS -->
      <div id="captions-track" class="clip" data-start="0" data-duration="35.5" data-track-index="3">
        {captions_str}
      </div>

      <!-- TRACK 4: HALFTONE DOT WIPES -->
      <!-- Wipe 1: before Point 1 (start 5.00s, dur 0.90s) -->
      <div id="wipe-1" class="wipe-overlay" data-start="5.00" data-duration="0.90" data-track-index="4">
        <svg width="1080" height="1920" viewBox="0 0 1080 1920">
          {wipe_dots_str}
        </svg>
      </div>

      <!-- Wipe 2: before Point 5 (start 24.95s, dur 0.90s) -->
      <div id="wipe-2" class="wipe-overlay" data-start="24.95" data-duration="0.90" data-track-index="4">
        <svg width="1080" height="1920" viewBox="0 0 1080 1920">
          {wipe_dots_str}
        </svg>
      </div>

      <!-- SOUND TRACKS -->
      <!-- Voiceover -->
      <audio src="audio/voice.wav" data-start="0" data-duration="35.31" data-track-index="10" data-volume="1.0"></audio>
      <!-- Background Music (0.16 volume, 0.8s fade out) -->
      <audio src="audio/music.wav" data-start="0" data-duration="35.5" data-track-index="11" data-volume="0.16" data-fade-out="0.8"></audio>
      <!-- SFX tracks -->
      <audio src="audio/pop.wav" data-start="0.10" data-duration="0.12" data-track-index="12"></audio>
      <audio src="audio/pop.wav" data-start="2.00" data-duration="0.12" data-track-index="13"></audio>
      <audio src="audio/pop.wav" data-start="2.16" data-duration="0.12" data-track-index="14"></audio>
      <audio src="audio/pop.wav" data-start="2.32" data-duration="0.12" data-track-index="15"></audio>
      <audio src="audio/pop.wav" data-start="2.48" data-duration="0.12" data-track-index="16"></audio>
      <audio src="audio/pop.wav" data-start="2.64" data-duration="0.12" data-track-index="17"></audio>
      <audio src="audio/whoosh.wav" data-start="5.00" data-duration="0.45" data-track-index="18"></audio>
      <audio src="audio/tick.wav" data-start="5.70" data-duration="0.05" data-track-index="19"></audio>
      <audio src="audio/typing.wav" data-start="6.20" data-duration="0.08" data-track-index="20"></audio>
      <audio src="audio/thud.wav" data-start="9.52" data-duration="0.35" data-track-index="21"></audio>
      <audio src="audio/thud.wav" data-start="12.72" data-duration="0.35" data-track-index="22"></audio>
      <audio src="audio/thud.wav" data-start="19.42" data-duration="0.35" data-track-index="23"></audio>
      <audio src="audio/whoosh.wav" data-start="24.95" data-duration="0.45" data-track-index="24"></audio>
      <audio src="audio/thud.wav" data-start="25.02" data-duration="0.35" data-track-index="25"></audio>
      <audio src="audio/thud.wav" data-start="30.44" data-duration="0.35" data-track-index="26"></audio>
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});

      // Continuous subtle head sway
      tl.to("#head-group", {{
        rotation: 2.2,
        x: 4,
        duration: 2.1,
        yoyo: true,
        repeat: 16,
        ease: "sine.inOut"
      }}, 0);

      // Scene 0: Strike-through line draws at 1.22s on word "scary"
      tl.to("#strike-1", {{
        strokeDashoffset: 0,
        duration: 0.32,
        ease: "power2.out"
      }}, 1.22);

      // Scene 1: 5 Small Cards pop in 0.16s apart
      const popCards = ["#mini-1", "#mini-2", "#mini-3", "#mini-4", "#mini-5"];
      popCards.forEach((c, idx) => {{
        const popTime = 2.00 + idx * 0.16;
        tl.to(c, {{
          scale: 1.0,
          opacity: 1,
          duration: 0.34,
          ease: "back.out(2.2)"
        }}, popTime);
      }});

      // Red ring draws around payoff at 3.14s on word "ruin"
      tl.to("#payoff-ring-path", {{
        strokeDashoffset: 0,
        duration: 0.85,
        ease: "power2.out"
      }}, 3.14);

      // Scene 7: Closing scene payoff & seamless loop match
      tl.to("#scene-closing", {{ opacity: 1, duration: 0.25 }}, 31.25);
      tl.to("#strike-closing", {{ strokeDashoffset: 0, duration: 0.32, ease: "power2.out" }}, 34.60);

      // On final frame, morph closing card title to match Scene 0 perfectly for loop
      tl.to("#closing-heading", {{
        duration: 0.1,
        onComplete: () => {{
          const h = document.getElementById("closing-heading");
          if (h) h.textContent = "INDIAN HORROR = NOT SCARY";
        }}
      }}, 35.30);

      // Presenter Head Nods on Key Words
      {nods_str}

      // Presenter Blinks
      {blinks_str}

      // Pointing Hand
      {hand_point_str}

      // Open Palm Hand
      {hand_palm_str}

      // Captions Word Timings
      {word_tweens_str}

      // Presenter Mouth Shapes precomputed
      {mouth_sets_str}

      // Halftone Dot Wipes
      {wipe_tweens_str}

      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
'''

with open("index.html", "w") as f:
    f.write(html_content)

print("Generated index.html successfully!")
