import streamlit as st
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# --- 1. INITIAL SETUP & API CONFIGURATION ---

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("AIMLAPI_KEY")

# Set up Streamlit page configuration
st.set_page_config(
    page_title="AuthentiText",
    page_icon="✨",
    layout="centered"
)

# Initialize the AIMLAPI client
if not API_KEY:
    st.error("AIMLAPI_KEY not found. Please add it to your .env file.")
    st.stop()

client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=API_KEY,
)
MODEL = "gpt-3.5-turbo"

# --- 2. BACKEND LOGIC (API CALLS) ---

def get_ai_score_and_analysis(text_to_analyze: str) -> dict:
    """
    Analyzes text and returns a detailed JSON object with score, reason, and improvements.
    """
    prompt = f"""
    You are an expert AI writing analyst. Your task is to analyze the following text and provide a detailed breakdown of its likelihood of being AI-generated.

    Analyze the text based on factors like:
    1.  **Perplexity & Burstiness:** Is the sentence structure too uniform or predictable?
    2.  **Voice & Tone:** Does it lack a distinct, human personality?
    3.  **Vocabulary:** Is the word choice overly complex or unnaturally formal?

    Provide your response in a strict JSON format with the following keys:
    - "score": A number between 0 and 100 indicating the probability it was written by AI.
    - "reason": A brief, one-sentence summary of your analysis.
    - "improvements": A list of JSON objects, where each object has two keys: "point" (e.g., "Lacks Personal Voice") and "explanation" (a short sentence describing the issue). Provide at least 2-3 improvement points.

    Text to analyze:
    \"\"\"
    {text_to_analyze}
    \"\"\"
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
        return None

def humanize_text(text_to_humanize: str, style_name: str, custom_styles: dict) -> str:
    """
    Rewrites text in a specified style, handling both predefined and custom styles.
    """
    if style_name in custom_styles:
        example = custom_styles[style_name]
        prompt = f"""
        You are a writing style chameleon. Your task is to rewrite the "Original Text" to perfectly match the tone, voice, and style of the "Style Example" provided.

        --- Style Example ---
        {example}
        ---

        --- Original Text to Rewrite ---
        {text_to_humanize}
        ---

        Rewrite the "Original Text" below, adopting the style from the example. Do not add any commentary.
        """
    else: # It's a predefined style
        prompt = f"""
        You are a text humanizer and expert writer. Rewrite the following text to sound natural and human, adopting the specified style. Make it pass as if written by a person with that specific tone. Do not add any commentary.

        Style to adopt: {style_name}

        Original Text:
        \"\"\"
        {text_to_humanize}
        \"\"\"

        Rewritten Humanized Text:
        """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.75,
            top_p=0.9,
            max_tokens=2048
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"An error occurred during humanization: {e}")
        return "Error: Could not humanize the text."

# --- 3. SESSION STATE MANAGEMENT ---

# Initialize session state variables to store data across reruns
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'humanized_text' not in st.session_state:
    st.session_state.humanized_text = None
if 'custom_styles' not in st.session_state:
    st.session_state.custom_styles = {}

# --- 4. USER INTERFACE (STREAMLIT) ---

# Header Section
st.markdown("<h1 style='text-align: center; color: #2C3E50;'>AuthentiText</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>From Robotic to Realistic. Analyze and Humanize Your Content.</p>", unsafe_allow_html=True)
st.divider()

# Input Area
original_text = st.text_area("Paste your text here to begin...", height=225, placeholder="The utilization of advanced artificial intelligence paradigms facilitates the creation of highly efficient and automated content generation systems...")

if st.button("Analyze Text", type="primary", use_container_width=True):
    if original_text:
        with st.spinner('Analyzing your text... This may take a moment.'):
            analysis_data = get_ai_score_and_analysis(original_text)
            st.session_state.analysis_results = analysis_data
            st.session_state.humanized_text = None # Clear previous humanized text
    else:
        st.warning("Please paste some text to analyze.")

# Analysis Results Section (only shows after analysis)
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    score = results.get('score', 0)
    
    st.subheader("Analysis Results")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Determine color for the metric delta
        delta_color = "inverse" if score > 70 else ("off" if score > 40 else "normal")
        st.metric(label="AI-Generated Score", value=f"{score}%", 
                  delta=f"High Likelihood" if score > 70 else ("Moderate" if score > 40 else "Low Likelihood"),
                  delta_color=delta_color)

    with col2:
        st.markdown("**Points for Improvement:**")
        improvements = results.get('improvements', [])
        if improvements:
            for item in improvements:
                st.markdown(f"- **{item.get('point', 'N/A')}:** {item.get('explanation', 'N/A')}")
        else:
            st.markdown("No specific improvement points were identified.")
            
    st.divider()
    
    # Humanizer Section
    st.subheader("Make it Human")
    
    PREDEFINED_STYLES = [
        "Conversational & Casual",
        "Respectful & Formal",
        "Persuasive & Confident",
        "Storytelling & Engaging",
        "Academic & Scholarly",
        "Explanatory & Simple",
        "Humorous & Witty",
    ]
    
    # Combine predefined and custom styles for the dropdown
    available_styles = PREDEFINED_STYLES + list(st.session_state.custom_styles.keys())
    selected_style = st.selectbox("Choose a Humanizing Style", options=available_styles)

    with st.expander("Or, Define a New Custom Style by Example"):
        style_name = st.text_input("Give your style a name (e.g., 'My Blog Voice')")
        style_example = st.text_area("Paste an example of the writing style you want...", height=150)
        if st.button("Save Custom Style"):
            if style_name and style_example:
                st.session_state.custom_styles[style_name] = style_example
                st.success(f"Custom style '{style_name}' saved! It is now available in the dropdown.")
            else:
                st.warning("Please provide both a name and an example for your custom style.")
    
    if st.button("✨ Humanize Text", type="primary", use_container_width=True):
        with st.spinner('Humanizing... The AI is finding its voice.'):
            humanized_result = humanize_text(original_text, selected_style, st.session_state.custom_styles)
            st.session_state.humanized_text = humanized_result

# Humanized Output Section (only shows after humanizing)
if st.session_state.humanized_text:
    st.subheader("Your Humanized Text")
    st.code(st.session_state.humanized_text, language=None)