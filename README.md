# 🎨 Logo Designer Bot

**Logo Designer Bot** is an intelligent Streamlit application that helps you generate high-quality, brand-aligned logo designs based on your unique branding preferences. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and DALL·E 3, this tool creates polished, scalable logos suitable for real-world use across websites, packaging, and digital platforms.

## Folder Structure

```
Logo-Designer-Bot/
├── logo-designer-bot.py
├── README.md
└── requirements.txt
```

* **logo-designer-bot.py**: The main Streamlit app.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Visual Branding Input**
  Capture brand identity across name, style, audience, tone, iconography, and visual preferences — all through a clean multi-column form layout.

* **AI-Driven Prompt Generation**
  A branding agent converts your preferences into a detailed logo prompt, adhering to strict guidelines for professional, centered, vector-style logos.

* **DALL·E-Powered Logo Generation**
  A visual identity agent uses the prompt to generate a crisp, HD-quality logo image (white or transparent background, no mockups or decorative noise).

* **Error-Free Brand Name Handling**
  The app ensures accurate spelling, layout, and formatting based strictly on your provided inputs — no placeholder names, abbreviations, or fake text.

* **Downloadable Output**
  Instantly preview and download your generated logo as a `.png` file for use in design decks, brand kits, or digital platforms.

* **Clean Streamlit UI**
  Built with Streamlit for an intuitive, responsive, and distraction-free experience — minimal styling, maximum focus.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Logo-Designer-Bot.git
   cd Logo-Designer-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   # or
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run logo-designer-bot.py
   ```

2. **In your browser**:

   * Enter your OpenAI API key in the sidebar.
   * Fill out the logo branding form across 3 sections: Brand Basics, Visual Style, Tone & Purpose.
   * Click **🎨 Generate Logo**.
   * View your AI-generated logo.
   * Use the **📥 Download Logo** button to save the image as a `.png` file.

## Code Overview

* **`render_logo_preferences()`**: Collects structured branding input across tone, visuals, and audience.
* **`generate_logo()`**:

  * Uses a `Logo Prompt Generator` agent to turn branding input into a detailed prompt.
  * Sends it to a `Logo Designer` agent powered by DALL·E to create the final image.
* **`render_sidebar()`**: Collects and stores the OpenAI API key in session state.
* **`main()`**: Sets up the layout, handles logo generation, preview, and file download.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest improvements, or open a pull request. Make sure your changes are clean, purposeful, and aligned with the branding principles of the app.