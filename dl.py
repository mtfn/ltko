import os
import requests
import time
import json

# --- CONFIGURATION ---
output_dir = "audio_files"
data_file = "data.js"

phrases = [
    { "text": "저는 서울에서 태어나서 자랐어요.", "lang": "ko" },
    { "text": "부모님과 형제들도 서울에 사세요?", "lang": "ko" },
    { "text": "형은 취업해서 부산에 살아요.", "lang": "ko" },
    { "text": "남동생이 두 명 있어요. 저는 첫째예요.", "lang": "ko" },
    { "text": "둘째 남동생은 초등학생이에요.", "lang": "ko" },
    { "text": "저는 영국에 가서 가족들을 만날 거예요.", "lang": "ko" },
    { "text": "학교에서 멀어서 가까운 곳으로 이사하려고 해요.", "lang": "ko" },
    { "text": "기숙사에서는 방을 혼자 쓰세요?", "lang": "ko" },
    { "text": "룸메이트하고 같이 방을 쓸 거예요.", "lang": "ko" },
    { "text": "기숙사에 이사 와서 연락 주세요.", "lang": "ko" },
    { "text": "그림 그리는 것이 제 취미예요.", "lang": "ko" },
    { "text": "시간이 있을 때 보통 뭐 해요?", "lang": "ko" },
    { "text": "여행을 가서 사진을 많이 찍어요.", "lang": "ko" },
    { "text": "제주도에 여행 갔을 때 한라산에서 찍었어요.", "lang": "ko" },
    { "text": "네, 저는 어렸을 때 가 봤어요.", "lang": "ko" },
    { "text": "제가 한국 음식을 만들 수 있어요.", "lang": "ko" },
    { "text": "불고기와 떡볶이를 만들게요.", "lang": "ko" },
    { "text": "오늘 한국어 수업에서 친구들한테 물어봐요.", "lang": "ko" },
    { "text": "그레이스 씨는 테니스 치는 걸 좋아하니까 같이 테니스를 쳐요.", "lang": "ko" },
    { "text": "한국어 반 친구들을 초대하고 싶은데 다음 주 월요일에 시험이 있어요.", "lang": "ko" }
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
