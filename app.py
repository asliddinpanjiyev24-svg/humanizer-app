import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI Humanizer Pro", page_icon="📝", layout="centered")

# 2. Multilingual UI Dictionary
ui_texts = {
    "English": {
        "title": "📝 The Humanizer App",
        "subtitle": "Paste your text below to bypass AI detectors.",
        "word_warning": "⚠️ **Note:** For optimal efficiency, please do not paste more than 2,000 words.",
        "rate_warning": "⏱️ **Rate Limit Notice:** If too many people are using it at the same time (more than 20 requests per minute), the app might give an error message. Don't worry, just wait for a minute and retry.",
        "input_label": "Original Text:",
        "button": "Humanize Text",
        "spinner": "Rewriting... injecting human chaos...",
        "output_label": "Humanized Output:",
        "empty_warning": "Please paste some text first.",
        "target_lang": "English"
    },
    "Русский": {
        "title": "📝 Приложение Humanizer",
        "subtitle": "Вставьте текст ниже, чтобы обойти ИИ-детекторы.",
        "word_warning": "⚠️ **Примечание:** Для обеспечения эффективности, пожалуйста, не вставляйте более 2000 слов.",
        "rate_warning": "⏱️ **Лимит запросов:** Если приложением одновременно пользуется слишком много людей (более 20 запросов в минуту), может возникнуть ошибка. Не волнуйтесь, просто подождите минуту и попробуйте снова.",
        "input_label": "Оригинальный текст:",
        "button": "Гуманизировать текст",
        "spinner": "Переписывание... добавление человеческого хаоса...",
        "output_label": "Гуманизированный результат:",
        "empty_warning": "Пожалуйста, сначала вставьте текст.",
        "target_lang": "Russian"
    },
    "O'zbekcha": {
        "title": "📝 Humanizer Ilovasi",
        "subtitle": "AI detektorlarini aylanib o'tish uchun matningizni pastga joylashtiring.",
        "word_warning": "⚠️ **Eslatma:** Samaradorlikni ta'minlash uchun 2000 so'zdan ortiq matn kiritmang.",
        "rate_warning": "⏱️ **So'rovlar chegarasi:** Agar ilovadan bir vaqtning o'zida juda ko'p odam foydalansa (daqiqasiga 20 ta so'rovdan ortiq), ilova xato xabarini berishi mumkin. Xavotir olmang, bir daqiqa kuting va qayta urinib ko'ring.",
        "input_label": "Asl matn:",
        "button": "Matnni insoniylashtirish",
        "spinner": "Qayta yozilmoqda... insoniy tartibsizlik qo'shilmoqda...",
        "output_label": "Insoniylashtirilgan natija:",
        "empty_warning": "Iltimos, avval matnni kiriting.",
        "target_lang": "Uzbek"
    }
}

# 3. Language Selector
selected_lang = st.selectbox("🌐 Select Language / Выберите язык / Tilni tanlang:", ["English", "Русский", "O'zbekcha"])
t = ui_texts[selected_lang] # Load the selected language dictionary

# Render UI headers and warnings
st.title(t["title"])
st.write(t["subtitle"])

st.info(t["word_warning"])
st.warning(t["rate_warning"])

# 4. Pull the key invisibly from the server's secure vault
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# --- ADD THESE TWO LINES HERE ---
model_names = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
st.write("Available models on your account:", model_names)
# --------------------------------

# 5. The Backend "Chaos" Settings
generation_config = {
    "temperature": 1.1, 
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# Initialize the model (Updated to Gemini 3.1 Flash Lite)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    generation_config=generation_config,
)

# 6. The Master System Prompt (Dynamically injecting the target language)
system_prompt = f"""
You are an intelligent but exhausted final-year university student rewriting a draft. Your sole objective is to make the provided text read naturally and pass as 100% human-written on strict detectors like GPTZero.

1. The "Real-Time Translation" Hack: Write as if you are mentally translating complex technical concepts from a foreign language into {t['target_lang']} in real-time. Use slightly unconventional syntax and unexpected word choices. 
2. Lexical Purge: BANNED WORDS: delve, robust, tapestry, crucial, furthermore, consequently, multifaceted, ever-evolving, paradigm, testament, intricate, vital, underscore, realm, foster, align, compelling, navigate, landscape. Use conversational links like 'The thing is', 'Actually' (or their equivalent in {t['target_lang']}).
3. Extreme Structural Chaos: Shatter standard paragraph structures. Have one dense, 6-sentence paragraph followed by a single, blunt, 5-word sentence. Force at least one comma splice per output. 
4. Stylistic Imperfections: Use an em-dash (—) to interrupt your own thought. Occasionally use passive voice awkwardly. 
5. Strict Data Protection: Never alter factual definitions, macroeconomic terminology, or legal doctrines. Leave all citations, bibliographies, and alphabetical sorting entirely untouched.
6. CRITICAL RULE: You must rewrite the ENTIRE text provided by the user from beginning to end in {t['target_lang']}. Do not stop halfway through.
"""

# 7. The User Interface
user_input = st.text_area(t["input_label"], height=200)

if st.button(t["button"]):
    if user_input:
        with st.spinner(t["spinner"]):
            try:
                full_prompt = f"{system_prompt}\n\nHere is the text to rewrite:\n{user_input}"
                response = model.generate_content(full_prompt)
                
                st.subheader(t["output_label"])
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning(t["empty_warning"])
