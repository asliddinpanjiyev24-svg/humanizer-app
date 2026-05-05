import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI Humanizer Pro", page_icon="📝", layout="centered")

# 2. Multilingual UI Dictionary
ui_texts = {
    "English": {
        "title": "📝 The Humanizer App (Gemma Edition)",
        "subtitle": "Bypass AI detectors with 14,000+ daily request capacity.",
        "word_warning": "⚠️ **Note:** Stay under 2,000 words for the best results.",
        "rate_warning": "✅ **Status:** Using High-Quota Gemma Model (14.4k requests/day).",
        "input_label": "Original Text:",
        "button": "Humanize Text",
        "spinner": "Injecting human chaos...",
        "output_label": "Humanized Output (Click icon to copy):",
        "empty_warning": "Please paste some text first.",
        "target_lang": "English"
    },
    "Русский": {
        "title": "📝 Humanizer (Версия Gemma)",
        "subtitle": "Обход ИИ-детекторов с лимитом 14 000+ запросов в день.",
        "word_warning": "⚠️ **Примечание:** Для лучшего результата не более 2000 слов.",
        "rate_warning": "✅ **Статус:** Используется модель Gemma (14.4к запросов/день).",
        "input_label": "Оригинальный текст:",
        "button": "Гуманизировать",
        "spinner": "Добавление человеческого хаоса...",
        "output_label": "Результат (Нажмите для копирования):",
        "empty_warning": "Пожалуйста, сначала вставьте текст.",
        "target_lang": "Russian"
    },
    "O'zbekcha": {
        "title": "📝 Humanizer (Gemma Talqini)",
        "subtitle": "AI detektorlarini kunlik 14 000+ so'rov limiti bilan aylanib o'ting.",
        "word_warning": "⚠️ **Eslatma:** Eng yaxshi natija uchun 2000 so'zdan oshirmang.",
        "rate_warning": "✅ **Holat:** Yuqori quvvatli Gemma modeli ishlatilmoqda.",
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
st.success(t["rate_warning"])

# 3. API Configuration
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Using Gemma 3 27B - High intelligence + High Quota
model = genai.GenerativeModel(
    model_name="gemma-3-27b", 
    generation_config={
        "temperature": 1.25, 
        "top_p": 0.95,
        "top_k": 50,
        "max_output_tokens": 8192,
    },
)

# 4. Refined System Prompt (The "Burstiness" Protocol)
system_prompt = f"""
You are an intelligent but exhausted final-year university student. Your goal is to rewrite the text so it passes 100% as human.

1. BURSTINESS: Mix extremely short sentences with very long, multi-clause sentences. This "uneven" rhythm is how humans write. 
2. LOW PREDICTABILITY: Avoid the most obvious word choices. Instead of "shows," use "unpacks" or "highlights." Instead of "important," use "non-negotiable."
3. NO AI TRANSITIONS: Strictly BAN these words: delve, robust, tapestry, crucial, furthermore, multifaceted, landscape, realm, foster, align, navigate. Use conversational links like 'Honestly', 'The thing is', 'Basically'.
4. STYLISTIC FLAWS: Use an em-dash (—) once to interrupt a thought. Use a rhetorical question.
5. NO CHATTER: Do not explain anything. Do not say "Here is the rewrite." Output ONLY the transformed text.
6. DATA INTEGRITY: Never alter legal citations, macroeconomic terms, or bibliographies. 
7. LANGUAGE: Rewrite the ENTIRE text in {t['target_lang']}.
"""

# 5. UI Logic
user_input = st.text_area(t["input_label"], height=250)

if st.button(t["button"]):
    if user_input:
        with st.spinner(t["spinner"]):
            try:
                full_prompt = f"{system_prompt}\n\nREWRITE THIS TEXT:\n{user_input}"
                response = model.generate_content(full_prompt)
                
                st.subheader(t["output_label"])
                st.code(response.text, language=None)
            except Exception as e:
                st.error(f"Error: {e}. If it's a 404, check the model name in your region.")
    else:
        st.warning(t["empty_warning"])
