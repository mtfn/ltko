import os
import requests
import time
import json

# --- CONFIGURATION ---
output_dir = "audio_files"
data_file = "data.js"

phrases = [
    { "text": "한국어 반 친구들이 많이 가는 것 같아요.", "lang": "ko"},
    { "text": "한국에 온 동생하고 여행을 가요.", "lang": "ko"},
    { "text": "하얀 색처럼 밝은 색이 어울리는 편이에요.", "lang": "ko"},
    { "text": "키가 큰 편이어서 굽이 낮은 신발이 어울려요.", "lang": "ko"},
    { "text": "추천해 준 스타일이 정말 마음에 들어요.", "lang": "ko"},
    { "text": "지난 봄 방학에 제주도에서 찍은 사진이에요.", "lang": "ko"},
    { "text": "파란 모자를 쓰고 까만 셔츠를 입은 사람이에요.", "lang": "ko"},
    { "text": "보통 혼자 여행을 하는 편이에요.", "lang": "ko"},
    { "text": "제주도에 유명한 음식이 많아서 많이 먹었어요.", "lang": "ko"},
    { "text": "이번에는 한국어 반 친구들과 같이 갔어요.", "lang": "ko"},
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
