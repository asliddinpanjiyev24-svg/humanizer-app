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
        "rate_warning": "⏱️ **Rate Limit Notice:** If you hit a limit, please wait a minute and retry.",
        "input_label": "Original Text:",
        "button": "Humanize Text",
        "spinner": "Rewriting... injecting human chaos...",
        "output_label": "Humanized Output (Click the icon on the right to copy):",
        "empty_warning": "Please paste some text first.",
        "target_lang": "English"
    },
    "Русский": {
        "title": "📝 Приложение Humanizer",
        "subtitle": "Вставьте текст ниже, чтобы обойти ИИ-детекторы.",
        "word_warning": "⚠️ **Примечание:** Для обеспечения эффективности, пожалуйста, не вставляйте более 2000 слов.",
        "rate_warning": "⏱️ **Лимит запросов:** Если возникнет ошибка, подождите минуту и попробуйте снова.",
        "input_label": "Оригинальный текст:",
        "button": "Гуманизировать текст",
        "spinner": "Переписывание... добавление человеческого хаоса...",
        "output_label": "Результат (Нажмите на иконку справа, чтобы скопировать):",
        "empty_warning": "Пожалуйста, сначала вставьте текст.",
        "target_lang": "Russian"
    },
    "O'zbekcha": {
        "title": "📝 Humanizer Ilovasi",
        "subtitle": "AI detektorlarini aylanib o'tish uchun matningizni pastga joylashtiring.",
        "word_warning": "⚠️ **Eslatma:** Samaradorlikni ta'minlash uchun 2000 so'zdan ortiq matn kiritmang.",
        "rate_warning": "⏱️ **So'rovlar chegarasi:** Agar xato yuz bersa, bir daqiqa kuting va qayta urinib ko'ring.",
        "input_label": "Asl matn:",
        "button": "Matnni insoniylashtirish",
        "spinner": "Qayta yozilmoqda... insoniy tartibsizlik qo'shilmoqda...",
        "output_label": "Natija (Nusxa olish uchun o'ngdagi belgini bosing):",
        "empty_warning": "Iltimos, avval matnni kiriting.",
        "target_lang": "Uzbek"
    }
}

selected_lang = st.selectbox("🌐 Select Language / Выберите язык / Tilni tanlang:", ["English", "Русский", "O'zbekcha"])
t = ui_texts[selected_lang]

st.title(t["title"])
st.write(t["subtitle"])
st.info(t["word_warning"])
st.warning(t["rate_warning"])

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Using Gemini 1.5 Flash for better "Human" nuance vs. Lite
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 1.2, # Slightly higher for more randomness
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    },
)

# 6. Refined Master System Prompt
system_prompt = f"""
You are an intelligent but exhausted final-year university student rewriting a draft. Your sole objective is to make the provided text read naturally and pass as 100% human-written on strict detectors.

1. PERPLEXITY & BURSTINESS: Humans vary their sentence length and word choice unpredictably. Mix very long, complex sentences with short, punchy ones. Use "low-frequency" synonyms occasionally.
2. The "Real-Time Translation" Hack: Write as if you are mentally translating from a foreign language into {t['target_lang']}. Use slightly unconventional (but correct) syntax.
3. Lexical Purge: STICK TO THE BANNED WORDS LIST. NEVER use: delve, robust, tapestry, crucial, furthermore, consequently, multifaceted, ever-evolving, paradigm, testament, intricate, vital, underscore, realm, foster, align, compelling, navigate, landscape. Use 'Basically', 'The thing is', 'Actually' instead.
4. Stylistic Imperfections: Use an em-dash (—) to interrupt yourself. Use "I mean" or "think about it" to create a conversational flow. 
5. NO CHATTER: Do not explain yourself. Do not say "Here is the rewrite." Provide ONLY the text.
6. DATA PROTECTION: Never alter factual definitions, legal doctrines, or citations. Keep bibliographies and alphabetical sorting exactly as they are.
7. CRITICAL: Rewrite the ENTIRE text from start to finish in {t['target_lang']}.
"""

user_input = st.text_area(t["input_label"], height=200)

if st.button(t["button"]):
    if user_input:
        with st.spinner(t["spinner"]):
            try:
                full_prompt = f"{system_prompt}\n\nTEXT TO REWRITE:\n{user_input}"
                response = model.generate_content(full_prompt)
                st.subheader(t["output_label"])
                st.code(response.text, language=None)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning(t["empty_warning"])
