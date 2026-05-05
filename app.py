import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI Humanizer Pro", page_icon="📝", layout="centered")

# 2. Multilingual UI Dictionary
ui_texts = {
    "English": {
        "title": "📝 The Humanizer App (Pro Edition)",
        "subtitle": "Bypass AI detectors with high-capacity stable models.",
        "word_warning": "⚠️ **Note:** For maximum quality, stay under 2,000 words.",
        "rate_warning": "✅ **Status:** High-Quota Stable Model Active (14.4k requests/day).",
        "input_label": "Original Text:",
        "button": "Humanize Text",
        "spinner": "Applying human chaos...",
        "output_label": "Humanized Output (Click icon to copy):",
        "empty_warning": "Please paste some text first.",
        "target_lang": "English"
    },
    "Русский": {
        "title": "📝 Humanizer (Pro версия)",
        "subtitle": "Обход ИИ-детекторов с высокой пропускной способностью.",
        "word_warning": "⚠️ **Примечание:** Для лучшего качества не более 2000 слов.",
        "rate_warning": "✅ **Статус:** Модель со стабильной квотой активна.",
        "input_label": "Оригинальный текст:",
        "button": "Гуманизировать",
        "spinner": "Добавление человеческого хаоса...",
        "output_label": "Результат (Нажмите для копирования):",
        "empty_warning": "Пожалуйста, сначала вставьте текст.",
        "target_lang": "Russian"
    },
    "O'zbekcha": {
        "title": "📝 Humanizer (Pro talqini)",
        "subtitle": "AI detektorlarini yuqori quvvatli modellar bilan aylanib o'ting.",
        "word_warning": "⚠️ **Eslatma:** Yuqori sifat uchun 2000 so'zdan oshirmang.",
        "rate_warning": "✅ **Holat:** Yuqori kotalik barqaror model faol.",
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

# Using gemma-2-27b-it for high quota + high intelligence
# This model is specifically tuned to follow instructions better than the 'Lite' versions
model = genai.GenerativeModel(
    model_name="gemma-2-27b-it", 
    generation_config={
        "temperature": 1.2, 
        "top_p": 0.95,
        "top_k": 60,
        "max_output_tokens": 8192,
    },
)

# 4. The Ghostwriter Protocol V5 (Optimized for GPTZero/Detectors)
system_prompt = f"""
You are an intelligent but exhausted university student rewriting a draft. You MUST pass 100% as human on strict detectors.

1. INTENTIONAL IMPERFECTION: Real humans aren't perfect. Use an em-dash (—) to cut yourself off mid-sentence. Occasionally start a sentence with "I mean," or "Like," or "Actually," to break the machine rhythm.
2. THE "BURSTINESS" FACTOR: Vary your sentence lengths drastically. Follow a massive, three-line complex sentence with a tiny, three-word blunt one. This "uneven" heartbeat is the #1 human signal.
3. LEXICAL REPLACEMENT: Never use common AI words: delve, robust, tapestry, crucial, furthermore, multifaceted, landscape, realm, foster, align, navigate. Use 'Honestly', 'Basically', or 'The thing is'.
4. THE REAL-TIME TRANSLATION HACK: Write as if you are mentally translating concepts into {t['target_lang']} on the fly. This creates slightly unique, unpredictable phrasing that detectors cannot catch.
5. NO CHATTER: Do not explain your process. Do not say "Here is your rewrite." Provide ONLY the transformed text.
6. DATA PROTECTION: Leave all legal citations, macroeconomic terms, names, and bibliographies completely untouched.
7. TOTAL REWRITE: Transform the ENTIRE provided text from beginning to end in {t['target_lang']}.
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
                # st.code provides the built-in copy button
                st.code(response.text, language=None)
            except Exception as e:
                st.error(f"Error: {e}. If this is a 404, please try switching the model name to 'gemma-2-9b-it' in the code.")
    else:
        st.warning(t["empty_warning"])
