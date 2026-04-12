import os
import requests
import time
import json

# --- CONFIGURATION ---
output_dir = "audio_files"
data_file = "data.js"

phrases = [
    { "text": "잘 지내는데 요즘 좀 바빠요.", "lang": "ko" },
    { "text": "요즘 일이 많아서 스트레스가 많아요.", "lang": "ko" },
    { "text": "프로젝트가 끝나면 좀 쉬고 싶어요.", "lang": "ko" },
    { "text": "저는 운전하면서 노래를 크게 불러요.", "lang": "ko" },
    { "text": "좋은 방법이네요. 스트레스가 잘 풀리겠어요.", "lang": "ko" },
    { "text": "스트레스를 받으면 공원에서 테니스를 쳐요.", "lang": "ko" },
    { "text": "지난 학기가 너무 힘들어서 방학동안 쉬었어.", "lang": "ko" },
    { "text": "커피숍에서 아르바이트를 시작했어.", "lang": "ko" },
    { "text": "영화도 많이 보고 책도 여러 권 읽었어.", "lang": "ko" },
    { "text": "스칼렛이 대학원에 합격을 했대.", "lang": "ko" },
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
