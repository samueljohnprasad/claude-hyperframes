"""Generate separate narration lines with real Kokoro token timestamps."""
import os
os.environ['HF_HUB_OFFLINE'] = '1'
import json
from pathlib import Path
import numpy as np
import soundfile as sf
import espeakng_loader
from phonemizer.backend.espeak.wrapper import EspeakWrapper
EspeakWrapper.set_library(espeakng_loader.get_library_path())
os.environ['ESPEAK_DATA_PATH'] = espeakng_loader.get_data_path()
from kokoro import KPipeline
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'audio'
OUT.mkdir(parents=True, exist_ok=True)
LINES = [
    ('intro', "Five Hollywood thrillers that still know how to make your pulse race. Here's my countdown."),
    ('silence', "Number five: The Silence of the Lambs. A rookie investigator enters the mind of a dangerous killer. Chilling, intelligent, and unforgettable."),
    ('se7en', "Number four: Se7en. Two detectives hunt a murderer who turns the seven deadly sins into clues. Bleak, precise, and relentlessly tense."),
    ('psycho', "Number three: Psycho. One motel check-in changes movie history. Hitchcock turns ordinary spaces into traps, then rewrites the rules."),
    ('prestige', "Number two: The Prestige. Two rival magicians sacrifice everything for the perfect trick. Watch closely: every detail is part of the illusion."),
    ('darkknight', "Number one: The Dark Knight. A city descends into chaos when Batman faces an enemy who turns fear into a weapon. Grand, grim, and endlessly rewatchable."),
    ('outro', "Save this thriller watchlist. Which one keeps you awake?")
]
pipe = KPipeline(lang_code='b')
asr = WhisperModel('base', device='cpu', compute_type='int8', local_files_only=True)
sr = 24000
all_audio = [np.zeros(int(.24 * sr), dtype=np.float32)]
cursor = .24
scenes = []
for index, (key, text) in enumerate(LINES):
    print(f'Generating {key}...', flush=True)
    chunks, words, local = [], [], 0.0
    for _, _, result_audio in pipe(text, voice='bm_george', speed=1.04):
        chunk = np.asarray(result_audio)
        chunks.append(chunk)
        local += len(chunk)/sr
    audio = np.concatenate(chunks).astype(np.float32)
    sf.write(OUT / f'voice-{key}.wav', audio, sr)
    segments, _ = asr.transcribe(str(OUT / f'voice-{key}.wav'), word_timestamps=True, language='en', initial_prompt=text, condition_on_previous_text=False, beam_size=5)
    for segment in segments:
        for token in segment.words:
            words.append({'word':token.word.strip(), 'start':round(token.start,4), 'end':round(token.end,4)})
    scene_start = 0 if index == 0 else cursor - .16
    gap = .40 if index < len(LINES)-1 else 1.8
    scenes.append({'id':key,'text':text,'start':round(scene_start,4),'voiceStart':round(cursor,4),'speechDuration':len(audio)/sr,'words':words})
    all_audio.extend([audio, np.zeros(int(gap*sr),dtype=np.float32)])
    cursor += len(audio)/sr + gap
    print(f'{key}: {local:.2f}s, {len(words)} aligned tokens', flush=True)
duration = np.ceil(cursor*24)/24
raw = np.concatenate(all_audio)
raw = np.pad(raw,(0,max(0,round(duration*sr)-len(raw))))
sf.write(OUT / 'voice-raw.wav',raw,sr,subtype='FLOAT')
for i,s in enumerate(scenes):
    s['duration'] = round((scenes[i+1]['start'] if i+1<len(scenes) else duration)-s['start'],4)
(ROOT / 'timing.json').write_text(json.dumps({'duration':duration,'fps':24,'scenes':scenes},indent=2),encoding='utf8')
print(f'DONE: {duration:.3f}s',flush=True)
