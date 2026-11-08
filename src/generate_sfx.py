# // ponytail: deterministic studio-quality sound generator for exact frame alignment
import os
import numpy as np
import soundfile as sf
from scipy import signal

os.makedirs("audio", exist_ok=True)
sr = 44100

def create_pop():
    dur = 0.12
    t = np.linspace(0, dur, int(sr * dur), False)
    freq = 700 * np.exp(-t * 35) + 80
    phase = 2 * np.pi * np.cumsum(freq) / sr
    body = np.sin(phase) * np.exp(-t * 40)
    # Transient click at start
    click = np.random.normal(0, 0.4, len(t)) * np.exp(-t * 200)
    out = 0.8 * body + 0.3 * click
    # Peak at 0.01s
    out = out / (np.max(np.abs(out)) + 1e-9)
    return out

def create_whoosh():
    dur = 0.45
    t = np.linspace(0, dur, int(sr * dur), False)
    noise = np.random.normal(0, 1.0, len(t))
    # Filter noise with sweeping bandpass
    sos = signal.butter(4, [200, 2400], btype='bandpass', fs=sr, output='sos')
    filtered = signal.sosfilt(sos, noise)
    # Envelope with peak at 0.18s
    env = np.sin(np.pi * (t / dur)) ** 2
    out = filtered * env
    out = out / (np.max(np.abs(out)) + 1e-9)
    return out

def create_tick():
    dur = 0.05
    t = np.linspace(0, dur, int(sr * dur), False)
    f1 = np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 120)
    f2 = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 180)
    click = np.random.normal(0, 0.5, len(t)) * np.exp(-t * 400)
    out = 0.6 * f1 + 0.3 * f2 + 0.3 * click
    out = out / (np.max(np.abs(out)) + 1e-9)
    return out

def create_typing():
    dur = 0.08
    t = np.linspace(0, dur, int(sr * dur), False)
    click = np.random.normal(0, 0.8, len(t)) * np.exp(-t * 250)
    thump = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 80)
    out = 0.7 * click + 0.5 * thump
    out = out / (np.max(np.abs(out)) + 1e-9)
    return out

def create_thud():
    dur = 0.35
    t = np.linspace(0, dur, int(sr * dur), False)
    # Sub bass sweep 90Hz -> 35Hz
    freq = 80 * np.exp(-t * 8) + 30
    phase = 2 * np.pi * np.cumsum(freq) / sr
    sub = np.sin(phase) * np.exp(-t * 12)
    punch = np.sin(2 * np.pi * 140 * t) * np.exp(-t * 45)
    impact = np.random.normal(0, 0.4, len(t)) * np.exp(-t * 160)
    out = 0.8 * sub + 0.5 * punch + 0.3 * impact
    out = out / (np.max(np.abs(out)) + 1e-9)
    return out

def create_music(duration=36.0):
    t = np.linspace(0, duration, int(sr * duration), False)
    # Dark suspenseful drone in D minor (D2=73.4Hz, A2=110Hz, F2=87.3Hz)
    drone1 = np.sin(2 * np.pi * 73.4 * t) * 0.4
    drone2 = np.sin(2 * np.pi * 110.0 * t + 0.5) * 0.25
    drone3 = np.sin(2 * np.pi * 87.3 * t + 1.2) * 0.2
    # Slow LFO filter / beating
    lfo = (np.sin(2 * np.pi * 0.15 * t) + 1.0) * 0.5
    drones = (drone1 + drone2 * (0.8 + 0.2 * lfo) + drone3)
    
    # Pulse heartbeat every 1.2 s
    pulse_freq = 1.0 / 1.2
    pulse_phase = (t * pulse_freq) % 1.0
    pulse_env = np.exp(-pulse_phase * 14) * (pulse_phase < 0.25)
    pulse = np.sin(2 * np.pi * 55 * t) * pulse_env * 0.45
    
    # Subtle eerie chime notes (D4=293.7, F4=349.2, C#4=277.2)
    chimes = np.zeros_like(t)
    notes = [
        (2.0, 293.66), (5.5, 349.23), (9.0, 277.18), (13.5, 293.66),
        (18.0, 349.23), (22.5, 277.18), (27.0, 293.66), (31.5, 349.23)
    ]
    for start_t, freq in notes:
        idx_start = int(start_t * sr)
        note_dur = 2.5
        idx_end = min(len(t), idx_start + int(note_dur * sr))
        t_note = np.linspace(0, note_dur, idx_end - idx_start, False)
        chime_wave = np.sin(2 * np.pi * freq * t_note) * np.exp(-t_note * 2.2)
        chimes[idx_start:idx_end] += chime_wave * 0.18

    mix = drones + pulse + chimes
    # 0.8s fade out at end
    fade_len = int(0.8 * sr)
    fade_curve = np.linspace(1.0, 0.0, fade_len)
    mix[-fade_len:] *= fade_curve
    
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.9
    return mix

print("Synthesizing SFX...")
sf.write("audio/pop.wav", create_pop(), sr)
sf.write("audio/whoosh.wav", create_whoosh(), sr)
sf.write("audio/tick.wav", create_tick(), sr)
sf.write("audio/typing.wav", create_typing(), sr)
sf.write("audio/thud.wav", create_thud(), sr)
print("Synthesizing eerie background music...")
sf.write("audio/music.wav", create_music(36.0), sr)
print("All audio assets generated successfully!")
