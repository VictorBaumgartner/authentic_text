# AuthentiText

## Overview
AuthentiText is a Streamlit-based web application designed to analyze and humanize text, transforming robotic or AI-generated content into natural, engaging, and authentic writing. It uses the OpenAI API to evaluate text authenticity with a "Human Score" and provides suggestions for improvement, while also offering a humanization feature to rewrite text in various styles.

## Features
- **Text Analysis**: Assesses text for human-like qualities with a strict scoring system (0-100% Human Score).
- **Text Humanization**: Rewrites text to sound natural and relatable in predefined or custom styles.
- **Dual Theme Support**: Offers light and dark themes with customizable CSS for a modern UI.
- **Custom Styles**: Allows users to define and save custom writing styles with examples.
- **Actionable Feedback**: Provides detailed feedback and improvement suggestions based on analysis.

## Installation

### Prerequisites
- Python 3.8+
- An OpenAI API key (stored in a `.env` file or Streamlit secrets)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd authentiText
