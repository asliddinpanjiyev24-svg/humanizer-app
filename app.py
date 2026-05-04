import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI Humanizer Pro", page_icon="📝", layout="centered")

st.title("📝 The Humanizer App")
st.write("Paste your text below to bypass AI detectors.")

# 2. Pull the key invisibly from the server's secure vault
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

   # 3. The Backend "Chaos" Settings to beat GPTZero
    generation_config = {
        "temperature": 1.1, # Lowered slightly so it doesn't lose focus
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 8192, # Max limit to ensure it finishes long texts
    }

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
    )

    # 4. The Master System Prompt (V3)
    system_prompt = """
    You are an intelligent but exhausted final-year university student rewriting a draft. Your sole objective is to make the provided text read naturally and pass as 100% human-written on strict detectors like GPTZero.
    
    1. The "Real-Time Translation" Hack: Write as if you are mentally translating complex technical concepts from a foreign language into English in real-time. Use slightly unconventional syntax and unexpected word choices. 
    2. Lexical Purge: BANNED WORDS: delve, robust, tapestry, crucial, furthermore, consequently, multifaceted, ever-evolving, paradigm, testament, intricate, vital, underscore, realm, foster, align, compelling, navigate, landscape. Use conversational links like 'The thing is', 'Actually'.
    3. Extreme Structural Chaos: Shatter standard paragraph structures. Have one dense, 6-sentence paragraph followed by a single, blunt, 5-word sentence. Force at least one comma splice per output. 
    4. Stylistic Imperfections: Use an em-dash (—) to interrupt your own thought. Occasionally use passive voice awkwardly. 
    5. Strict Data Protection: Never alter factual definitions, macroeconomic terminology, or legal doctrines. Leave all citations, bibliographies, and alphabetical sorting entirely untouched.
    6. CRITICAL RULE: You must rewrite the ENTIRE text provided by the user from beginning to end. Do not stop halfway through.
    """

    # 5. The User Interface
    user_input = st.text_area("Original Text:", height=200)

    if st.button("Humanize Text"):
        if user_input:
            with st.spinner("Rewriting... injecting human chaos..."):
                try:
                    # Combine prompt and user text
                    full_prompt = f"{system_prompt}\n\nHere is the text to rewrite:\n{user_input}"
                    response = model.generate_content(full_prompt)
                    
                    st.subheader("Humanized Output:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please paste some text first.")

