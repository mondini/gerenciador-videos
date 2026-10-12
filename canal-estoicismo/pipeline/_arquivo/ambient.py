"""Generate a soft ambient drone (original, no third-party audio) for the preview."""
import numpy as np, wave, sys
SR = 44100
dur = float(sys.argv[1])
t = np.arange(int(SR * dur)) / SR
rng = np.random.default_rng(7)

def tone(f, amp, lfo_rate, phase):
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * lfo_rate * t + phase)
    return amp * lfo * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t + 0.3))

# low D minor-ish open chord, very slow breathing
sig = (tone(73.42, 0.30, 0.031, 0.0) + tone(110.0, 0.22, 0.023, 1.3) +
       tone(146.83, 0.14, 0.037, 2.1) + tone(220.0, 0.06, 0.019, 0.7))
# soft wind: low-passed noise with slow swell
n = rng.standard_normal(len(t))
k = np.exp(-np.arange(400) / 80.0); k /= k.sum()
wind = np.convolve(n, k, mode='same')
wind *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t + 0.4) ** 2
sig += 0.9 * wind
sig /= np.max(np.abs(sig))
fade = np.minimum(1, np.minimum(t / 3.0, (dur - t) / 3.0))
sig *= fade * 0.9
L = sig; R = np.roll(sig, int(0.013 * SR))
st = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open('ambient.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('ok')
