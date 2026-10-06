# Kenney CC0 효과음(ogg) -> 짧은 mp3 base64 -> src/sfx.js
# 사용: python tools/make_sfx.py <kenney 압축 푼 폴더들이 있는 경로>
import sys, base64, json
from pathlib import Path
import numpy as np, soundfile as sf, lameenc

SRC = Path(sys.argv[1])
ROOT = Path(__file__).resolve().parent.parent
PICK = {
    'slash1': 'kenney_rpg-audio/Audio/knifeSlice.ogg',
    'slash2': 'kenney_rpg-audio/Audio/knifeSlice2.ogg',
    'shing':  'kenney_rpg-audio/Audio/drawKnife1.ogg',
    'shing2': 'kenney_rpg-audio/Audio/drawKnife2.ogg',
    'chop':   'kenney_rpg-audio/Audio/chop.ogg',
    'hit1':   'kenney_impact-sounds/Audio/impactPunch_heavy_000.ogg',
    'hit2':   'kenney_impact-sounds/Audio/impactPunch_heavy_001.ogg',
    'hit3':   'kenney_impact-sounds/Audio/impactPunch_heavy_002.ogg',
    'crit':   'kenney_impact-sounds/Audio/impactPlate_heavy_000.ogg',
    'metal':  'kenney_impact-sounds/Audio/impactMetal_heavy_001.ogg',
    'shield': 'kenney_impact-sounds/Audio/impactMetal_medium_000.ogg',
    'hurt':   'kenney_impact-sounds/Audio/impactSoft_heavy_000.ogg',
    'hurt2':  'kenney_impact-sounds/Audio/impactPunch_medium_001.ogg',
    'bite':   'kenney_impact-sounds/Audio/impactMining_000.ogg',
    'die':    'kenney_impact-sounds/Audio/impactWood_heavy_000.ogg',
    'step1':  'kenney_impact-sounds/Audio/footstep_grass_000.ogg',
    'step2':  'kenney_impact-sounds/Audio/footstep_grass_001.ogg',
    'coins':  'kenney_rpg-audio/Audio/handleCoins.ogg',
    'chest':  'kenney_rpg-audio/Audio/doorOpen_1.ogg',
    'flip':   'kenney_rpg-audio/Audio/bookFlip1.ogg',
    'open':   'kenney_rpg-audio/Audio/bookOpen.ogg',
    'potion': 'kenney_rpg-audio/Audio/metalPot1.ogg',
}

def to_mp3(path):
    d, sr = sf.read(str(path), dtype='float32')
    if d.ndim > 1: d = d.mean(axis=1)
    d = d / max(1e-6, np.abs(d).max()) * 0.9
    pcm = (d * 32767).astype('<i2').tobytes()
    enc = lameenc.Encoder(); enc.set_bit_rate(96); enc.set_in_sample_rate(sr)
    enc.set_channels(1); enc.set_quality(2)
    return enc.encode(pcm) + enc.flush()

out = {k: base64.b64encode(to_mp3(SRC / v)).decode() for k, v in PICK.items()}
(ROOT / 'src/sfx.js').write_text('const SFX=' + json.dumps(out) + ';', encoding='utf-8')
print('sfx.js', sum(len(v) for v in out.values()) // 1024, 'KB')
