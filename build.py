# src/template.html + src/strokes.js + src/sfx.js 를 한 파일로 합치기
#   index.html    : GitHub Pages 등 일반 웹용 (완전한 HTML 문서)
#   artifact.html : Claude 아티팩트용 (머리말 없이 본문만, 게시할 때 자동으로 감싸짐)
# 목소리는 voice/*.json 으로 따로 둠 (tools/make_voice.py 로 생성)
from pathlib import Path
root = Path(__file__).parent
body = (root/'src/template.html').read_text(encoding='utf-8')
body = body.replace('/*STROKES*/', (root/'src/strokes.js').read_text(encoding='utf-8'))
body = body.replace('/*SFX*/', (root/'src/sfx.js').read_text(encoding='utf-8'))
head = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#DCEDFC">
<style>*,*::before,*::after{box-sizing:border-box}body{margin:0}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}</style>
'''
(root/'artifact.html').write_text(body, encoding='utf-8')
(root/'index.html').write_text(head + body.replace('<div id="app">', '</head>\n<body>\n<div id="app">', 1) + '\n</body>\n</html>\n', encoding='utf-8')
print('built index.html / artifact.html', len(body)//1024, 'KB')
