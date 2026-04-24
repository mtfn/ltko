import os
import requests
import time
import json

# --- CONFIGURATION ---
output_dir = "audio_files"
data_file = "data.js"

phrases = [
    { "text": "머리가 아프고 열이 나요.", "lang": "ko" },
    { "text": "언제부터 증상이 있었어요?", "lang": "ko" },
    { "text": "먼저 체온을 재 보겠습니다", "lang": "ko" },
    { "text": "식사하신 후에 약을 복용하세요.", "lang": "ko" },
    { "text": "증상이 없어지면 병원에 안 오셔도 됩니다.", "lang": "ko" },
    { "text": "소화가 안 되고 배가 많이 아파요.", "lang": "ko" },
    { "text": "소화제도 먹었는데 효과가 없네요.", "lang": "ko" },
    { "text": "소화가 안 되는데 참으면 안 돼요.", "lang": "ko" },
    { "text": "수업은 걱정 안 해도 돼요.", "lang": "ko" },
    { "text": "병원에 다녀온 후에 푹 쉬세요.", "lang": "ko" }
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
