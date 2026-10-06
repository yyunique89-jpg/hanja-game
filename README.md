# 한자 탐험대

아이들이 태블릿에서 한자능력검정시험(한국어문회) 8급·7급Ⅱ·7급을 익히는 웹 게임.

- 한자 카드, 몬스터 퀴즈, 짝 맞추기, 따라 쓰기, 모의시험
- 한자 모험: 몬스터를 물리치고 한자 마왕까지 가는 RPG

## 고치는 방법
1. `src/template.html` 수정 (한자 데이터·게임 코드)
2. 대사가 바뀌었으면 `python tools/make_voice.py` (voice/*.json 생성)
3. `python build.py` → `index.html`

## 사용한 자료
- 획순: [hanzi-writer](https://hanziwriter.org) / hanzi-writer-data
- 효과음: [Kenney](https://kenney.nl) RPG Audio, Impact Sounds (CC0)
- 목소리: Microsoft Edge 뉴럴 음성(ko-KR-SunHiNeural)으로 생성
