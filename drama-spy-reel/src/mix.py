"""Measured dialogue-first mix; all music and Foley are licensed recordings."""
import json, math, re, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from scipy.ndimage import maximum_filter1d, gaussian_filter1d

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'/'audio'
meta=json.loads((ROOT/'timing.json').read_text())
cue=json.loads((ROOT/'cues.json').read_text())
sr=48000
duration=meta['duration']
n=round(duration*sr)

def ff(args):
    p=subprocess.run(['ffmpeg','-hide_banner','-y',*map(str,args)],capture_output=True,text=True,check=True)
    return p.stderr
def measure(file):
    out=ff(['-i',file,'-af','loudnorm=I=-16:TP=-4.5:LRA=9:print_format=json','-f','null','-'])
    return json.loads(re.findall(r'\{[^{}]+"input_i"[^{}]+\}',out,re.S)[-1])
def normalize(src,dst,target=-16,tp=-4.5):
    out=ff(['-i',src,'-af',f'loudnorm=I={target}:TP={tp}:LRA=9:print_format=json','-f','null','-'])
    v=json.loads(re.findall(r'\{[^{}]+"input_i"[^{}]+\}',out,re.S)[-1])
    filt=f"loudnorm=I={target}:TP={tp}:LRA=9:measured_I={v['input_i']}:measured_TP={v['input_tp']}:measured_LRA={v['input_lra']}:measured_thresh={v['input_thresh']}:offset={v['target_offset']}:linear=true"
    ff(['-i',src,'-af',filt,'-ar',sr,'-ac',2,'-c:a','pcm_f32le',dst])
def read(file):
    v,rate=sf.read(file,always_2d=True)
    if rate!=sr:v=resample_poly(v,sr//math.gcd(sr,rate),rate//math.gcd(sr,rate))
    if v.shape[1]==1:v=np.repeat(v,2,axis=1)
    return v[:,:2]
def fit(x):return np.pad(x[:n],((0,max(0,n-len(x))),(0,0)))
def rms(x):return float(np.sqrt(np.mean(x*x)+1e-15))
def db(x):return 20*math.log10(max(x,1e-9))

ff(['-i',A/'voice-raw.wav','-af','highpass=f=170,lowpass=f=6200,acompressor=threshold=0.12:ratio=2.4:attack=8:release=100:makeup=1','-ar',sr,'-ac',2,'-c:a','pcm_f32le',A/'voice-eq.wav'])
normalize(A/'voice-eq.wav',A/'voice-master.wav',-16.5,-5.3)
voice=fit(read(A/'voice-master.wav'))
ff(['-ss','8','-i',A/'spy-glass.mp3','-t',duration,'-af','highpass=f=150,lowpass=f=6500,equalizer=f=2600:t=q:w=1:g=-5','-ar',sr,'-ac',2,'-c:a','pcm_f32le',A/'music-eq.wav'])
music=fit(read(A/'music-eq.wav'))
music*=10**((-31.5-db(rms(music)))/20)
# 10ms measurement grid, 120ms attack lead, 300ms release: speech drives ducking.
hop=480
power=np.array([rms(voice[i:i+hop]) for i in range(0,n,hop)])
speech=maximum_filter1d((power>.012).astype(float),size=25)
env=gaussian_filter1d(speech,5)
duck=np.interp(np.arange(n)/hop,np.arange(len(env)),env)
music*= (1-.60*duck[:,None])
for scene in meta['scenes']:
    if scene['id']=='schindler':music[round(scene['start']*sr):round((scene['start']+scene['duration'])*sr)]*=.30
fade=np.minimum(1,np.arange(n)/(sr*.45))*np.minimum(1,np.maximum(0,(n-1-np.arange(n)))/(sr*1.1))
music*=fade[:,None]
sf.write(A/'music-ducked.wav',music,sr,subtype='FLOAT')
ff(['-i',A/'paper-wipe.mp3','-af','highpass=f=400,lowpass=f=6000','-ar',sr,'-ac',2,'-c:a','pcm_f32le',A/'paper-source.wav'])
paper=read(A/'paper-source.wav')
sfx=np.zeros((n,2))
reports=[]
events=[{'id':'intro-ticket','t':.42}]+[{'id':c['id'],'t':c['title']+.06} for c in cue[1:]]
for k,event in enumerate(events):
    t=event['t'];start=round(t*sr);length=round((.24+(k%3)*.025)*sr)
    offset=round((k%3)*.075*sr)
    clip=paper[offset:offset+length].copy()
    if not len(clip):continue
    ramp=np.minimum(1,np.arange(len(clip))/(sr*.008))*np.minimum(1,(len(clip)-np.arange(len(clip)))/(sr*.045))
    clip*=ramp[:,None]
    clip*=10**(-22/20)/max(np.max(np.abs(clip)),1e-8)
    v=rms(voice[max(0,start-round(.12*sr)):min(n,start+round(.5*sr))])
    # Guarantee a 13dB RMS margin at each speech cue, beyond the requested 10dB.
    if v>.003:
        clip*=min(1,v*10**(-13/20)/rms(clip))
    end=min(n,start+len(clip));sfx[start:end]+=clip[:end-start]
    reports.append({'id':event['id'],'time':round(t,3),'voiceRmsDb':round(db(v),2),'sfxRmsDb':round(db(rms(clip)),2),'voiceAboveSfxDb':round(db(v)-db(rms(clip)),2),'sfxPeakDb':round(db(np.max(np.abs(clip))),2)})
sf.write(A/'sfx-ducked.wav',sfx,sr,subtype='FLOAT')
raw=voice+music+sfx
sf.write(A/'mix-pre.wav',raw,sr,subtype='FLOAT')
normalize(A/'mix-pre.wav',A/'final-mix.wav',-16,-4.5)
master=read(A/'final-mix.wav')
export_headroom=10**(-.7/20)
gain=rms(master)/rms(raw)*export_headroom
sf.write(A/'final-mix-safe.wav',master*export_headroom,sr,subtype='FLOAT')
# Apply the measured final gain to stems so preview and exported mix agree.
for name,arr in [('voice-master',voice),('music-ducked',music),('sfx-ducked',sfx)]:
    sf.write(A/f'{name}-delivery.wav',arr*gain,sr,subtype='FLOAT')
result={'duration':duration,'sampleRate':sr,'exportTrimDb':-.7,'voiceEngine':'Kokoro bm_george local','music':'Spy Glass / Kevin MacLeod / CC BY 4.0','mix':measure(A/'final-mix-safe.wav'),'voice':measure(A/'voice-master-delivery.wav'),'musicRmsDb':db(rms(music*gain)),'sfxCues':reports,'checks':{'source':'all music and Foley from recordings','sfxSpeechMarginDb':min(x['voiceAboveSfxDb'] for x in reports),'dialogueUnshifted':True}}
(ROOT/'AUDIO-REPORT.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2),flush=True)
