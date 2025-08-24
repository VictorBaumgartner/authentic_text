import streamlit as st
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# --- 1. INITIAL SETUP & API CONFIGURATION ---

load_dotenv()
API_KEY = os.getenv("AIMLAPI_KEY") or st.secrets.get("AIMLAPI_KEY")

st.set_page_config(
    page_title="AuthentiText",
    page_icon="✨",
    layout="centered"
)

if not API_KEY:
    st.error("AIMLAPI_KEY not found. Please add it to your .env file locally or as a secret on Streamlit Cloud.")
    st.stop()

client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=API_KEY,
)
MODEL = "gpt-3.5-turbo"


# --- 2. DUAL-THEME CUSTOM CSS ---
# (No changes here, remains the same)
light_theme_css = """
:root {
    --bg-color: #F8F9FA; --card-bg-color: #FFFFFF; --text-color: #2C3E50;
    --subtle-text-color: #6c757d; --accent-color: #1ABC9C; --accent-hover-color: #16A085;
    --border-color: #EAECEE; --metric-bg-color: #F8F9FA;
}
"""
dark_theme_css = """
:root {
    --bg-color: #17202A; --card-bg-color: #2C3E50; --text-color: #ECF0F1;
    --subtle-text-color: #95A5A6; --accent-color: #1ABC9C; --accent-hover-color: #1DD1A1;
    --border-color: #34495E; --metric-bg-color: #34495E;
}
"""
general_styles = """
    /* (CSS is the same as the previous version) */
    .stApp { background-color: var(--bg-color); }
    .main-container { background: var(--card-bg-color); border-radius: 16px; padding: 2.5rem; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1); border: 1px solid var(--border-color); color: var(--text-color); }
    h1, h2, h3 { font-family: 'Lora', serif; color: var(--text-color) !important; }
    p, .stMarkdown { color: var(--subtle-text-color) !important; }
    .stTextArea textarea { background-color: var(--bg-color); color: var(--text-color); min-height: 250px; border-radius: 8px; border: 1px solid var(--border-color); font-family: 'Inter', sans-serif; }
    .stTextArea textarea:focus { border-color: var(--accent-color); box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent-color) 20%, transparent); }
    .stButton > button { background-color: var(--accent-color); color: white; font-weight: 600; padding: 0.75rem 1.5rem; border-radius: 8px; transition: background-color 0.3s, transform 0.2s; width: 100%; border: none; }
    .stButton > button:hover { background-color: var(--accent-hover-color); transform: translateY(-2px); color: white; border: none; }
    .stMetric { background-color: var(--metric-bg-color); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; text-align: center; }
    .stMetric > div { color: var(--text-color) !important; }
    hr { background: var(--border-color); }
"""
def load_css(theme_css):
    full_css = f"<style>{theme_css}{general_styles}</style>"
    st.markdown(full_css, unsafe_allow_html=True)


# --- 3. BACKEND LOGIC (API CALLS) ---

@st.cache_data(show_spinner=False)
def get_human_score_and_analysis(text_to_analyze: str) -> dict:
    # --- ENHANCED, GENERALIZED, AND RUTHLESS PROMPT ---
    prompt = f"""
    You are a world-class linguistic forensic analyst with an unmatched ability to detect AI-generated text, even when it’s highly polished and deceptively human-like. Your task is to scrutinize the provided text with extreme skepticism, identifying subtle cues that distinguish authentic human writing from AI output. Be ruthless in your judgment, assigning a conservative human-likeness score and leaning toward lower scores if any doubt exists.

    To guide your analysis, consider these generalized, topic-agnostic examples:

    --- AI-Generated Example (Hallmarks of AI) ---
    "The implementation of synergistic paradigms is a crucial component for leveraging core competencies. By strategically facilitating cross-platform integrations, organizations can unlock robust productivity gains and enhance stakeholder value. This data-driven approach ensures optimal outcomes across all operational verticals."
    *Analysis of AI example: This text relies on predictable corporate jargon ('synergistic paradigms', 'leveraging'), with uniform sentence structures and a neutral, impersonal tone lacking unique voice or emotional depth. It feels formulaic and robotic.*

    --- Human-Written Example (Hallmarks of Human) ---
    "Look, let's be honest—most of the 'productivity hacks' out there are just clever ways to procrastinate. I once spent a whole day color-coding my tasks instead of, you know, actually doing them. The real breakthrough for me wasn't some fancy system; it was just admitting that I needed to focus on one thing at a time. It’s not revolutionary, but it works."
    *Analysis of human example: This text has a distinct, conversational voice with varied sentence structures, a personal anecdote, and an opinionated tone. It feels authentic, relatable, and emotionally grounded.*

    Analyze the following text with a forensic lens, focusing on these critical dimensions:
    1. **Voice & Idiosyncrasy**: Does the text exhibit a unique personality, memorable phrasing, or context-specific tone, or does it rely on generic, high-probability word choices typical of AI?
    2. **Rhythm & Flow**: Are sentence structures varied and natural (burstiness), or are they uniform, monotonous, or overly polished?
    3. **Emotional Depth & Authenticity**: Does the text convey genuine emotion, opinion, or context-specific nuance, or is it overly neutral, superficial, or detached?
    4. **Word Choice & Predictability**: Does the text use creative, unexpected, or contextually appropriate words, or does it lean on clichéd, formulaic, or overly formal phrases?

    Handle ambiguous cases (e.g., human-edited AI text) by erring on the side of caution and assigning a lower score unless clear human hallmarks are present. Provide actionable suggestions to make the text more human-like.

    Return your analysis in strict JSON format with the following keys:
    - "human_score": A number between 0 and 100 (100 = unmistakably human, 0 = unmistakably AI). Be conservative.
    - "reason": A one-sentence summary of your expert judgment.
    - "improvements": A list of JSON objects, each with "point" (a specific issue) and "explanation" (how to address it).

    Text to analyze:
    \"\"\"
    {text_to_analyze}
    \"\"\"
    """
    try:
        response = client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": prompt}],
            temperature=0.1, # Low temperature for more deterministic analysis
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"error": "Failed to analyze the text. The API might be busy. Please try again."}


# (The rest of the file is IDENTICAL to the previous version)

@st.cache_data(show_spinner=False)
def humanize_text(text_to_humanize: str, style_name: str, custom_styles: dict) -> str:
    # This function is unchanged
    custom_example = custom_styles.get(style_name)
    if custom_example:
        prompt = f"""You are an expert human writer skilled at crafting natural, engaging, and authentic text. Your task is to rewrite the 'Original Text' to perfectly match the tone, style, vocabulary, and flow of the 'Style Example'. Ensure the rewritten text feels human, relatable, and polished, avoiding robotic, overly formal, or clichéd phrasing. Preserve the original meaning while infusing subtle personality and emotional nuance that aligns with the style example. Adapt the text to suit the intended audience implied by the style example, if applicable.

        --- Style Example ---\n{custom_example}\n---
        --- Original Text to Rewrite ---\n{text_to_humanize}\n---
        Rewritten Text:"""
    else:
        prompt = f"""You are an expert human writer with a talent for making text sound natural and engaging. Rewrite the following text in a '{style_name}' style to make it sound authentically human. Avoid robotic, overly formal, or clichéd language, and infuse the text with warmth, clarity, and subtle personality that suits the specified style. Preserve the original meaning while ensuring the text feels relatable and polished for its intended audience.

        Original Text: \"\"\"{text_to_humanize}\"\"\"
        Rewritten Humanized Text:"""
    try:
        response = client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": prompt}],
            temperature=0.75, top_p=0.9, max_tokens=2048
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Error: Could not humanize the text. Please try again."

# --- 4. SESSION STATE & THEME SELECTION ---
if 'theme' not in st.session_state: st.session_state.theme = "Bright"
st.sidebar.title("Settings")
selected_theme = st.sidebar.radio("Choose a theme", ["Bright", "Dark"], key="theme")
if selected_theme == "Dark": load_css(dark_theme_css)
else: load_css(light_theme_css)
if 'analysis_results' not in st.session_state: st.session_state.analysis_results = None
if 'humanized_text' not in st.session_state: st.session_state.humanized_text = None
if 'humanized_analysis' not in st.session_state: st.session_state.humanized_analysis = None
if 'custom_styles' not in st.session_state: st.session_state.custom_styles = {}

# --- 5. HELPER FUNCTION for displaying results ---
def display_analysis(analysis_data, title="Analysis Results"):
    # This function is unchanged
    if not analysis_data or "error" in analysis_data:
        st.error(analysis_data.get("error", "An unknown error occurred."))
        return
    st.subheader(title)
    score = analysis_data.get('human_score', 0)
    col1, col2 = st.columns([1, 2])
    with col1:
        delta_color = "normal" if score > 70 else ("off" if score > 40 else "inverse")
        st.metric(label="Human Score", value=f"{score}%",
                  delta="Sounds Human" if score > 70 else ("Needs Improvement" if score > 40 else "Sounds Robotic"),
                  delta_color=delta_color)
    with col2:
        st.markdown("**Actionable Feedback:**")
        improvements = analysis_data.get('improvements', [])
        if improvements:
            for item in improvements:
                st.markdown(f"💡 **{item.get('point', 'N/A')}:** *{item.get('explanation', 'N/A')}*")
        else:
            st.markdown("✅ Looks great! No specific improvement points identified.")

# --- 6. USER INTERFACE ---
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>AuthentiText</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Refine your writing from robotic to realistic.</p>", unsafe_allow_html=True)
    original_text = st.text_area("Paste your text here...", height=250, label_visibility="collapsed")
    if st.button("Analyze Text"):
        if original_text:
            with st.spinner('Analyzing your text...'):
                st.session_state.analysis_results = None; st.session_state.humanized_text = None; st.session_state.humanized_analysis = None
                st.session_state.analysis_results = get_human_score_and_analysis(original_text)
        else:
            st.warning("Please paste some text to analyze.")
    if st.session_state.analysis_results:
        st.divider()
        display_analysis(st.session_state.analysis_results, title="Initial Analysis")
        st.divider()
        st.subheader("Make it Human")
        PREDEFINED_STYLES = [
            "Conversational & Casual", "Respectful & Formal", "Persuasive & Confident",
            "Storytelling & Engaging", "Academic & Scholarly"
        ]
        available_styles = PREDEFINED_STYLES + list(st.session_state.custom_styles.keys())
        selected_style = st.selectbox("Choose a Humanizing Style", options=available_styles)
        with st.expander("Define a New Custom Style"):
            style_name = st.text_input("Style Name")
            style_example = st.text_area("Paste an example...", height=150)
            if st.button("Save Custom Style"):
                if style_name and style_example:
                    st.session_state.custom_styles[style_name] = style_example
                    st.success(f"Custom style '{style_name}' saved!")
                    st.experimental_rerun()
                else:
                    st.warning("Please provide both a name and an example.")
        if st.button("✨ Humanize Text"):
            with st.spinner('Humanizing... The AI is finding its voice.'):
                st.session_state.humanized_text = humanize_text(original_text, selected_style, st.session_state.custom_styles)
                st.session_state.humanized_analysis = None
    if st.session_state.humanized_text:
        st.divider()
        st.subheader("Your Humanized Text")
        st.text_area("Result", value=st.session_state.humanized_text, height=250, key="output_text")
        if st.button("Analyze Humanized Text"):
            with st.spinner('Re-analyzing the new text...'):
                st.session_state.humanized_analysis = get_human_score_and_analysis(st.session_state.humanized_text)
    if st.session_state.humanized_analysis:
        st.divider()
        display_analysis(st.session_state.humanized_analysis, title="Humanized Text Analysis")
    st.markdown('</div>', unsafe_allow_html=True)