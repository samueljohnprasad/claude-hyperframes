# // ponytail: generate full script audio with bm_george at speed 1.0, trim silence > 0.24s, extract word timestamps
import os
import json
import numpy as np
import soundfile as sf
from kokoro import KPipeline
from faster_whisper import WhisperModel

os.makedirs("audio", exist_ok=True)
os.makedirs("src", exist_ok=True)

sentences = [
    # Hook Line 1 (under 6 words):
    "Building everything from scratch hurts.",
    # Hook Line 2:
    "These five open source titans will supercharge your developer workflow forever.",
    # Point 1 (React):
    "React powers interactive user interfaces across millions of modern web applications.",
    # Point 2 (Transformers):
    "Transformers lets you run cutting edge artificial intelligence in three lines.",
    # Point 3 (FastAPI):
    "FastAPI delivers production ready asynchronous backend microservices with automatic documentation.",
    # Point 4 (Tauri):
    "Tauri builds blazingly fast desktop software using tiny web frontends.",
    # Point 5 (Supabase):
    "Supabase gives you scalable Postgres databases, authentication, and realtime storage instantly.",
    # Closing:
    "Star these five repositories now before building everything from scratch."
]

pipe = KPipeline(lang_code='b')
audio_chunks = []
sr = 24000

for idx, s in enumerate(sentences):
    print(f"Generating sentence {idx+1}/{len(sentences)}...")
    for _, _, chunk in pipe(s, voice='bm_george', speed=1.0):
        audio_chunks.append(chunk)
    # Pause between sentences before trimming
    audio_chunks.append(np.zeros(int(sr * 0.40)))

raw_audio = np.concatenate(audio_chunks)
print(f"Raw audio length: {len(raw_audio)/sr:.2f} s")

# Trim pauses > 0.24 s where truly silent in 0.03 s windows
win_samples = int(0.03 * sr) # 720 samples
max_pause_samples = int(0.24 * sr) # 5760 samples (8 windows)
silence_thresh_db = -42.0

num_windows = len(raw_audio) // win_samples
silent = np.zeros(num_windows, dtype=bool)

for i in range(num_windows):
    win = raw_audio[i*win_samples : (i+1)*win_samples]
    rms = np.sqrt(np.mean(win**2)) + 1e-9
    db = 20 * np.log10(rms)
    if db < silence_thresh_db:
        silent[i] = True

trimmed_windows = []
current_silent_run = 0

for i in range(num_windows):
    win = raw_audio[i*win_samples : (i+1)*win_samples]
    if silent[i]:
        current_silent_run += 1
        if current_silent_run <= (max_pause_samples // win_samples):
            trimmed_windows.append(win)
    else:
        current_silent_run = 0
        trimmed_windows.append(win)

final_audio = np.concatenate(trimmed_windows)
final_audio = final_audio / (np.max(np.abs(final_audio)) + 1e-6) * 0.95

voice_path = "audio/voice.wav"
sf.write(voice_path, final_audio, sr)
total_duration = len(final_audio) / sr
print(f"Final trimmed audio: {voice_path} ({total_duration:.2f} s)")

# Faster-whisper word-level transcription
print("Running faster-whisper on voice.wav...")
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(voice_path, word_timestamps=True, language="en")

words = []
for seg in segments:
    for w in seg.words:
        cleaned = w.word.strip()
        if cleaned:
            words.append({
                "word": cleaned,
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "prob": round(w.probability, 3)
            })

print(f"Transcribed {len(words)} words. Duration: {total_duration:.2f}s")

output_data = {
    "duration": round(total_duration, 3),
    "words": words,
    "sentences": sentences
}

with open("transcript.json", "w") as f:
    json.dump(output_data, f, indent=2)

print("Saved transcript.json successfully!")
