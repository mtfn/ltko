import os
import requests
import time
import json

# --- CONFIGURATION ---
output_dir = "audio_files"
data_file = "data.js"

# Added a few more phrases so you can test the grid navigation
phrases = [
    { "text": "요즘 날씨가 참 따뜻하고 좋네요. ", "lang": "ko" },
    { "text": "이번 주말에 전주 한옥 마을에 가려고 해요.", "lang": "ko" },
    { "text": "전주가 서울에서 멀지요?", "lang": "ko" },
    { "text": "시험이 있어서 도서관에서 공부하려고 해요.", "lang": "ko" },
    { "text": "시험이 많네요. 그럼 열심히 공부하세요.", "lang": "ko" },
    { "text": "등산 가려고 했는데 비가 많이 와서 못 갔어요.", "lang": "ko" },
    { "text": "집에서 청소하고 쉬었어요.", "lang": "ko" },
    { "text": "부산은 날씨가 좋아서 구경을 많이 했어요.", "lang": "ko" },
    { "text": "부산에서 어느 곳을 추천해요?", "lang": "ko" },
    { "text": "해운대하고 자갈치 시장에 꼭 가 보세요.", "lang": "ko" },
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
