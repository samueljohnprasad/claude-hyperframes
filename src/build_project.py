# // ponytail: comprehensive project builder ensuring 100% adherence to rules & HyperFrames contract
import json
import math
import soundfile as sf
import numpy as np

# Load transcript
with open("transcript.json") as f:
    transcript = json.load(f)

words = transcript["words"]
total_dur = transcript["duration"]
video_dur = 35.5

# Calculate 30fps mouth shapes from audio loudness
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

# Compress mouth shapes into intervals
mouth_intervals = []
cur_m = mouth_timeline[0]
start_f = 0
for f in range(1, total_frames):
    if mouth_timeline[f] != cur_m:
        mouth_intervals.append({"m": cur_m, "t": round(start_f / fps, 3)})
        cur_m = mouth_timeline[f]
        start_f = f
mouth_intervals.append({"m": cur_m, "t": round(start_f / fps, 3)})

# Precompute 13x23 halftone wipe grid coordinates & center delays
cols, rows = 13, 23
cx, cy = 6, 11
max_dist = math.sqrt(6**2 + 11**2) # ~12.53
dots = []
for r in range(rows):
    for c in range(cols):
        x = round((c + 0.5) * (1080 / cols), 1)
        y = round((r + 0.5) * (1920 / rows), 1)
        dist = math.sqrt((c - cx)**2 + (r - cy)**2)
        norm_dist = dist / max_dist
        delay = round(norm_dist * 0.22, 3)
        dots.append({"x": x, "y": y, "delay": delay, "id": f"d_{r}_{c}"})

with open("src/dots.json", "w") as f:
    json.dump(dots, f)

print(f"Computed {len(mouth_intervals)} mouth transitions and {len(dots)} wipe dots.")
