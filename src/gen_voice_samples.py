# // ponytail: minimal script to generate 3 kokoro voice samples for line 1
import os
import soundfile as sf
import numpy as np
from kokoro import KPipeline

os.makedirs("audio_samples", exist_ok=True)
text = "Building everything from scratch hurts"

# 1. Adam (US Male)
print("Generating Voice 1: am_adam...")
pipe_a = KPipeline(lang_code='a')
chunks_adam = []
for _, _, audio in pipe_a(text, voice='am_adam', speed=1.1):
    chunks_adam.append(audio)
audio_adam = np.concatenate(chunks_adam)
sf.write("audio_samples/line1_voice1_adam.wav", audio_adam, 24000)

# 2. Michael (US Male)
print("Generating Voice 2: am_michael...")
chunks_michael = []
for _, _, audio in pipe_a(text, voice='am_michael', speed=1.1):
    chunks_michael.append(audio)
audio_michael = np.concatenate(chunks_michael)
sf.write("audio_samples/line1_voice2_michael.wav", audio_michael, 24000)

# 3. George (UK Male)
print("Generating Voice 3: bm_george...")
pipe_b = KPipeline(lang_code='b')
chunks_george = []
for _, _, audio in pipe_b(text, voice='bm_george', speed=1.1):
    chunks_george.append(audio)
audio_george = np.concatenate(chunks_george)
sf.write("audio_samples/line1_voice3_george.wav", audio_george, 24000)

print("All 3 samples generated successfully!")
