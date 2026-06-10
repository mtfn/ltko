import os
import requests
import time
import json

# --- CONFIGURATION ---
output_dir = "audio_files"
data_file = "data.js"

phrases = [
    { "text": "소포를 어디로 보내실 겁니까?", "lang": "ko"},
    { "text": "보통 우편으로는 일주일이 걸립니다.", "lang": "ko"},
    { "text": "미국 샌디에이고로 보내고 싶은데 얼마나 걸릴까요?", "lang": "ko"},
    { "text": "소포 안에 깨지는 물건이 있습니까?", "lang": "ko"},
    { "text": "체크 카드를 만들고 싶습니다.", "lang": "ko"},
    { "text": "먼저 은행 계좌를 만드셔야 됩니다.", "lang": "ko"},
    { "text": "외국인이시니까 여권이 필요합니다.", "lang": "ko"},
    { "text": "이 신청서를 작성해 주십시오.", "lang": "ko"},
    { "text": "마지막에 서명해 주십시오.", "lang": "ko"},
    { "text": "체크카드를 오늘 바로 받을 수 있을까요?", "lang": "ko"},
    { "text": "가족들한테 줄 선물을 검색하고 있어요.", "lang": "ko"},
    { "text": "버스를 타고 안국역에서 내려서 걸어가면 돼요.", "lang": "ko"},
    { "text": "그럼 저는 지하철을 타는게 좋겠어요.", "lang": "ko"},
    { "text": "유나 씨, 추천하고 싶은 공예품이 있어요.", "lang": "ko"},
    { "text": "부채나 찻잔 세트나 수저 세트 어때요?", "lang": "ko"},
    { "text": "새로 생긴 학교 앞 음식점에 가 본 적이 있어요?", "lang": "ko"},
    { "text": "음식이 아주 맛있고 서비스도 좋아요.", "lang": "ko"},
    { "text": "테이블이 여섯 개 밖에 없어서 오래 기다렸어요.", "lang": "ko"},
    { "text": "오늘 가려고 하는데 일찍 가는게 좋겠네요.", "lang": "ko"},
    { "text": "아르바이트를 하거나 자격증 시험 공부를 할 거예요.", "lang": "ko"},
]

# --- SETUP ---
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

updated_phrases = []

print(f"--- Starting Download of {len(phrases)} files ---")

for index, item in enumerate(phrases):
    text = item['text']
    lang = item['lang']
    filename = f"audio_{index}.mp3"
    filepath = os.path.join(output_dir, filename)
    
    # Check if file already exists to skip re-downloading
    if not os.path.exists(filepath):
        url = "https://translate.google.com/translate_tts"
        params = { "ie": "UTF-8", "tl": lang, "client": "tw-ob", "q": text }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded: {filename}")
            time.sleep(1) # Be polite to the API
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"⏭️  Skipped (Exists): {filename}")

    # Add index and path to data
    item['id'] = index
    item['audio_src'] = f"{output_dir}/{filename}"
    updated_phrases.append(item)

# Write JS file
js_content = f"const FLASHCARD_DATA = {json.dumps(updated_phrases, indent=4, ensure_ascii=False)};"
with open(data_file, "w", encoding="utf-8") as f:
    f.write(js_content)

print("--- Done! ---")
