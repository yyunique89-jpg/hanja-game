# src/template.html + src/strokes.js + src/sfx.js -> index.html (한 파일로 합치기)
# 목소리는 voice/*.json 으로 따로 게시 (tools/make_voice.py 로 생성)
from pathlib import Path
root = Path(__file__).parent
html = (root/'src/template.html').read_text(encoding='utf-8')
html = html.replace('/*STROKES*/', (root/'src/strokes.js').read_text(encoding='utf-8'))
html = html.replace('/*SFX*/', (root/'src/sfx.js').read_text(encoding='utf-8'))
(root/'index.html').write_text(html, encoding='utf-8')
print('index.html built', len(html)//1024, 'KB')
