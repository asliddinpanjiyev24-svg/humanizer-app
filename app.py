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
        "rate_warning": "⏱️ **Note:** If you hit a rate limit, just wait a minute and retry.",
        "input_label": "Original Text:",
        "button": "Humanize Text",
        "spinner": "Injecting human chaos...",
        "output_label": "Humanized Output (Click icon to copy):",
        "empty_warning": "Please paste some text first.",
        "target_lang": "English"
    },
    "Русский": {
        "title": "📝 Приложение Humanizer",
        "subtitle": "Вставьте текст ниже, чтобы обойти ИИ-детекторы.",
        "word_warning": "⚠️ **Примечание:** Для эффективности не более 2000 слов.",
        "rate_warning": "⏱️ **Лимит:** Если возникнет ошибка, подождите минуту.",
        "input_label": "Оригинальный текст:",
        "button": "Гуманизировать",
        "spinner": "Добавление человеческого хаоса...",
        "output_label": "Результат (Нажмите для копирования):",
        "empty_warning": "Пожалуйста, сначала вставьте текст.",
        "target_lang": "Russian"
    },
    "O'zbekcha": {
        "title": "📝 Humanizer Ilovasi",
        "subtitle": "AI detektorlarini aylanib o'tish uchun matn kiriting.",
        "word_warning": "⚠️ **Eslatma:** 2000 so'zdan oshmasligi tavsiya etiladi.",
        "rate_warning": "⏱️ **Chegara:** Xato bo'lsa, bir daqiqa kuting.",
        "input_label": "Asl matn:",
        "button": "Insoniylashtirish",
        "spinner": "Insoniy tartibsizlik qo'shilmoqda...",
        "output_label": "Natija (Nusxa olish uchun bosing):",
        "empty_warning": "Iltimos, avval matnni kiriting.",
        "target_lang": "Uzbek"
    }
}

selected_lang = st.selectbox("🌐 Select Language:", ["English", "Русский", "O'zbekcha"])
t = ui_texts[selected_lang]

st.title(t["title"])
st.info(t["word_warning"])

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# We are sticking to Lite to ensure your high daily quota remains intact
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    generation_config={
        "temperature": 1.3, # Pushed higher for maximum word variety
        "top_p": 0.98,      # Allows for more "rare" word choices
        "top_k": 80,        # Higher variety in word selection
        "max_output_tokens": 8192,
    },
)

# 6. REFINED CHAOS PROMPT V4
system_prompt = f"""
You are a highly intelligent but extremely stressed university student rewriting a draft at 3 AM. You MUST pass 100% as a human. 

1. THE "BURSTINESS" RULE: Detectors look for uniform sentence lengths. You must destroy this. Use one very long, rambling sentence with multiple clauses, immediately followed by a 2-word sentence. Use "..." to indicate a pause in thought.
2. LOW-PROBABILITY WORD CHOICE: Avoid the "logical" next word. Instead of 'important', use 'pivotal' or 'non-negotiable'. Instead of 'improve', use 'sharpen' or 'overhaul'.
3. THE "SECOND LANGUAGE" FLAVOR: Write as if you are thinking in a different language and translating into {t['target_lang']} on the fly. This creates unique phrasing that detectors cannot predict.
4. BANNED AI-ISMS: Never use: delve, robust, tapestry, crucial, furthermore, multifaceted, ever-evolving, landscape, realm, foster, align, compelling, navigate. If you use these, you fail.
5. GRAMMATICAL LOOSENESS: Use a semicolon correctly once, then follow it with a conversational phrase like "you know?" or "anyway." Use an em-dash (—) to cut yourself off mid-thought.
6. NO INTRODUCTIONS: Do not say "Okay, here is the text." Provide ONLY the rewritten text.
7. DATA PROTECTION: Do not touch legal citations, macroeconomic data points, or factual names. Leave lists and bibliographies exactly as they are.
8. TOTAL REWRITE: Every single sentence of the user's input must be transformed into this new {t['target_lang']} style.
"""

user_input = st.text_area(t["input_label"], height=250)

if st.button(t["button"]):
    if user_input:
        with st.spinner(t["spinner"]):
            try:
                # We wrap the input to ensure the model focuses on the prompt
                full_prompt = f"{system_prompt}\n\n[START OF ORIGINAL TEXT]\n{user_input}\n[END OF ORIGINAL TEXT]"
                response = model.generate_content(full_prompt)
                
                st.subheader(t["output_label"])
                st.code(response.text, language=None)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning(t["empty_warning"])
