from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import textdistance
import requests
from bs4 import BeautifulSoup

# إنشاء تطبيق FastAPI
app = FastAPI()

# ===== إضافة CORS لتجنب مشاكل Method Not Allowed من المتصفح =====
origins = ["*"]  # يمكن تعديلها لاحقًا لتحديد نطاق معين
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # يسمح بـ GET, POST, OPTIONS
    allow_headers=["*"],
)

# ===== نموذج البيانات =====
class TextData(BaseModel):
    content: str

# ===== دالة لجلب مقتطفات من جوجل =====
def search_google_snippets(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        url = f"https://www.google.com/search?q={query}"
        resp = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.find_all("div", class_="BNeawe")
        snippets = [r.get_text() for r in results]
        return " ".join(snippets)
    except Exception:
        return ""

# ===== مسار API لفحص الانتحال =====
@app.post("/api/check")
async def check_plagiarism(data: TextData):
    text = data.content.strip()
    if not text:
        return {"percent": 0, "table_html": "<tr><td>No text provided.</td></tr>"}

    sentences = text.split(".")
    total = len(sentences)
    matches = 0
    result_rows = ""

    for sentence in sentences:
        if len(sentence.split()) < 4:
            continue
        snippet = search_google_snippets(sentence[:70])
        if snippet:
            similarity = textdistance.jaccard(sentence.lower(), snippet.lower())
            percent = round(similarity * 100, 2)
            if percent > 40:
                matches += 1
                result_rows += f"<tr><td>{sentence}</td><td>{percent}% match</td></tr>"

    plagiarism_percent = round((matches / total) * 100, 2) if total else 0

    if not result_rows:
        result_rows = "<tr><td>✅ No plagiarism found!</td></tr>"

    return {
        "percent": plagiarism_percent,
        "table_html": result_rows
    }
