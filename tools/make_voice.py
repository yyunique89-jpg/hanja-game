# 게임 대사를 뉴럴 음성(Edge TTS)으로 미리 녹음 -> voice/<pack>.json  {대사: mp3 base64}
# 대사 목록은 템플릿의 voiceLines()에서 가져옴 (node 필요). 이미 녹음된 대사는 건너뜀.
# 사용: python tools/make_voice.py
import asyncio, base64, json, subprocess, re
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent.parent
VOICE = 'ko-KR-SunHiNeural'

def lines():
    html = (ROOT / 'artifact.html').read_text(encoding='utf-8')   # build.py 먼저 실행
    main = re.findall(r'<script>([\s\S]*?)</script>', html)[-1].split('/* ================= 이벤트')[0]
    js = ("global.localStorage={getItem:()=>null,setItem:()=>{}};"
          "global.document={querySelector:()=>({textContent:'',classList:{add(){},remove(){}}}),addEventListener(){},getElementById:()=>({addEventListener(){}})};"
          "global.speechSynthesis={getVoices:()=>[],cancel(){},speak(){}};global.STROKES={};global.window={addEventListener(){}};global.history={state:null,replaceState(){},pushState(){}};"
          + main + ";process.stdout.write(JSON.stringify(voiceLines()))")
    tmp = ROOT / 'tools' / '_lines.js'; tmp.write_text(js, encoding='utf-8')
    r = subprocess.run(['node', str(tmp)], capture_output=True, text=True, encoding='utf-8'); tmp.unlink()
    if r.returncode: raise SystemExit(r.stderr)
    return json.loads(r.stdout)

def rate_for(text):
    return '-8%' if len(text) <= 6 else '+0%'   # 짧은 훈음은 또박또박

async def synth(text, sem):
    async with sem:
        for _ in range(4):
            try:
                c = edge_tts.Communicate(text, VOICE, rate=rate_for(text), pitch='+6Hz')
                buf = b''
                async for ch in c.stream():
                    if ch['type'] == 'audio': buf += ch['data']
                if buf: return text, base64.b64encode(buf).decode()
            except Exception:
                await asyncio.sleep(1.5)
        print('실패:', text); return text, None

async def main():
    packs = lines(); (ROOT / 'voice').mkdir(exist_ok=True); sem = asyncio.Semaphore(8)
    for name, texts in packs.items():
        f = ROOT / 'voice' / f'{name}.json'
        have = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {}
        todo = [t for t in dict.fromkeys(texts) if t not in have]
        for t, b in await asyncio.gather(*(synth(t, sem) for t in todo)):
            if b: have[t] = b
        keep = {t: have[t] for t in texts if t in have}
        f.write_text(json.dumps(keep, ensure_ascii=False), encoding='utf-8')
        print(f'{name}: {len(keep)}개, {f.stat().st_size // 1024} KB (새로 {len(todo)}개)')

asyncio.run(main())
