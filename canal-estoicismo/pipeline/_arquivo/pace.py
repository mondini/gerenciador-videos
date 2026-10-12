"""Slow the narration: lengthen each pause and apply a gentle pitch-preserving tempo.
Writes in/<b>_slow.wav and pace.json with a time map (orig -> new) for cue conversion."""
import json, re, subprocess, numpy as np, wave, sys, os

TEMPO = 0.92          # 8% slower speech, pitch preserved
SR = 44100

def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32)

def silences(path):
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'silencedetect=noise=-38dB:d=0.3',
                          '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([0-9.]+)', out)]
    en = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', out)]
    return list(zip(st, en))

res = json.load(open('pace.json')) if os.path.exists('pace.json') else {}
for b in (sys.argv[1:] or ['b1', 'b2']):
    x = load(f'in/{b}.mp3')
    sil = [(s, e) for s, e in silences(f'in/{b}.mp3') if s > 0.05 and e < len(x) / SR - 0.05]
    pieces, cur, inserted = [], 0, []
    acc = 0.0
    for s, e in sil:
        mid = int((s + e) / 2 * SR)
        extra = 0.55 * (e - s) + 0.25
        pieces.append(x[cur:mid]); pieces.append(np.zeros(int(extra * SR), np.float32))
        acc += extra; inserted.append(((s + e) / 2, acc)); cur = mid
    pieces.append(x[cur:])
    y = np.concatenate(pieces)
    with wave.open(f'in/{b}_pad.wav', 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'in/{b}_pad.wav', '-af', f'atempo={TEMPO}',
                    f'in/{b}_slow.wav'], check=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                f'in/{b}_slow.wav'], capture_output=True, text=True).stdout)
    res[b] = {'inserted': inserted, 'tempo': TEMPO, 'dur': dur, 'orig': len(x) / SR}
    print(b, round(len(x) / SR, 2), '->', round(dur, 2))
json.dump(res, open('pace.json', 'w'), indent=1)
