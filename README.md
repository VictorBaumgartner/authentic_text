AuthentiText 📝
Overview 🌟
AuthentiText is a Streamlit-based web application designed to analyze and humanize text, transforming robotic or AI-generated content into natural, engaging, and authentic writing. It uses the OpenAI API to evaluate text authenticity with a "Human Score" and provides suggestions for improvement, while also offering a humanization feature to rewrite text in various styles.
Features ✨

Text Analysis 🔍: Assesses text for human-like qualities with a strict scoring system (0-100% Human Score).
Text Humanization ✍️: Rewrites text to sound natural and relatable in predefined or custom styles.
Dual Theme Support 🎨: Offers light and dark themes with customizable CSS for a modern UI.
Custom Styles 🎭: Allows users to define and save custom writing styles with examples.
Actionable Feedback 💡: Provides detailed feedback and improvement suggestions based on analysis.

Installation 🛠️
Prerequisites 📋

Python 3.8+
An OpenAI API key (stored in a .env file or Streamlit secrets)

Setup 🚀

Clone the repository:git clone <repository-url>
cd authentiText


Install dependencies:pip install -r requirements.txt


Create a .env file in the project root and add your OpenAI API key:AIMLAPI_KEY=your_api_key_here


Run the application:streamlit run app.py



Usage 🎮

Input Text ✏️: Paste your text into the text area on the main interface.
Analyze Text 🔎: Click "Analyze Text" to get a Human Score and feedback.
Humanize Text 🌱: Select a style (e.g., Conversational, Formal) and click "Humanize Text" to rewrite the text.
Custom Styles 🎨: Use the expander to define and save a new style with a name and example.
Re-Analyze 🔄: Review the humanized text and analyze it again for a new Human Score.

Configuration ⚙️

API Key 🔑: Required and loaded from .env or Streamlit secrets.
Model 🤖: Uses gpt-3.5-turbo for analysis and humanization.
Themes 🌗: Switch between "Bright" and "Dark" via the sidebar settings.

File Structure 📂

app.py: Main application script containing UI and backend logic.
.env: Environment file for API key (not included in version control).
requirements.txt: List of Python dependencies.

Contributing 🤝
Feel free to fork the repository, submit issues, or create pull requests for enhancements or bug fixes.
License 📜
[MIT License] - See the LICENSE file for details.
Contact 📧
For questions or support, reach out via the project repository or email.

Made by VIK 🎉
