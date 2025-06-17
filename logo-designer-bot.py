from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.dalle import DalleTools

import requests, tempfile
import streamlit as st 

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    st.sidebar.markdown("---")

def render_logo_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Brand Basics
    with col1:
        st.subheader("🏷️ Brand Basics")
        brand_name = st.text_input("Brand Name", placeholder="e.g., Luxoride, GreenBloom")
        brand_type = st.selectbox(
            "What type of brand is this?",
            ["Tech Startup", "Fashion Label", "Health & Wellness", "Food & Beverage", "Education", 
             "Non-Profit", "Finance", "Personal Brand", "Other"]
        )
        tagline = st.text_input("Tagline (optional)", placeholder="e.g., Drive Freely. Live Boldly.")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Urban millennials, small businesses")

    # Column 2: Visual Style
    with col2:
        st.subheader("🎨 Visual Style")
        logo_style = st.multiselect(
            "Preferred Logo Style",
            ["Minimalist", "Vintage", "Bold & Geometric", "Playful", "Elegant & Luxurious", 
             "Modern & Techy", "Hand-drawn", "Mascot-based", "Symbolic", "Typographic"]
        )
        color_palette = st.multiselect(
            "Preferred Color Palette",
            ["Blues", "Greens", "Reds", "Monochrome", "Pastels", "Earth tones", 
             "Neon/High contrast", "Muted neutrals"]
        )
        logo_type = st.selectbox(
            "Logo Composition Preference",
            ["Symbol-only", "Text-only", "Combination of symbol and text"]
        )
        icon_elements = st.text_input("Any specific icons or elements you'd like to include?", placeholder="e.g., leaf, rocket, book")

    # Column 3: Tone & Purpose
    with col3:
        st.subheader("🧭 Tone & Purpose")
        brand_tone = st.selectbox(
            "What tone should the logo convey?",
            ["Professional", "Friendly", "Innovative", "Trustworthy", "Luxury", "Adventurous", "Minimal"]
        )
        usage_context = st.multiselect(
            "Where will the logo be used?",
            ["Website", "Mobile App", "Packaging", "Business Cards", "Social Media", "Merchandise", "All of the above"]
        )
        competitors = st.text_input("Any brands you admire or want to differentiate from?", placeholder="e.g., Tesla, Canva, Patagonia")
        uniqueness_note = st.text_input("Anything that makes your brand unique?", placeholder="e.g., Sustainability, community-first model")

    # Assemble branding profile
    branding_profile = f"""
    **Brand Basics:**
    - Brand Name: {brand_name}
    - Brand Type: {brand_type}
    - Tagline: {tagline if tagline else 'Not provided'}
    - Target Audience: {target_audience if target_audience else 'Not specified'}

    **Visual Style Preferences:**
    - Logo Style: {', '.join(logo_style) if logo_style else 'Not specified'}
    - Color Palette: {', '.join(color_palette) if color_palette else 'Not specified'}
    - Logo Composition: {logo_type}
    - Icon Elements: {icon_elements if icon_elements else 'None specified'}

    **Tone & Purpose:**
    - Brand Tone: {brand_tone}
    - Usage Context: {usage_context}
    - Competitor References: {competitors if competitors else 'None specified'}
    - Unique Aspects: {uniqueness_note if uniqueness_note else 'None specified'}
    """

    return branding_profile

def generate_logo(user_logo_preferences: str) -> str:
    logo_prompt_agent = Agent(
        name="Logo Prompt Generator",
        role="Creates a highly specific and design-appropriate logo prompt based on branding inputs",
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        instructions=[
            "You are a branding assistant that transforms a detailed branding profile into a highly specific prompt for generating a professional logo using an image generation model.",
            
            "Strictly follow these visual and technical constraints for logo design:",
            "- The output must describe a **single, clean logo design only** — not a badge sheet, multi-option layout, or mockup.",
            "- The background must be **white or transparent** (this must be stated clearly in the prompt).",
            "- The logo must be **centered**, with no surrounding borders, badges, scenery, framing lines, or alignment guides.",
            "- The logo must be suitable for **professional branding** — vector-style, clean lines, scalable, and flat (not photorealistic).",
            
            "From the branding profile, extract and use the following:",
            "- Brand Name (use it **exactly as provided** — no abbreviation, generic substitutes, or spelling errors)",
            "- Brand Type and Target Audience (guide tone and aesthetic)",
            "- Logo Style and Color Palette",
            "- Logo Composition Preference (symbol-only, text-only, or combination)",
            "- Icon Elements (only those explicitly mentioned; avoid clutter)",
            "- Brand Tone (e.g., elegant, playful, bold)",
            "- Unique Aspects (for visual metaphor inspiration)",
            "- Competitor References (for differentiation)",
            "- Usage Context (ensure legibility across print, digital, and small-size use cases)",

            "Additional restrictions to enforce:",
            "- Do NOT invent placeholder words, branding slogans, or filler labels (e.g., 'Health & Wellness', 'Ritual', 'Branding Hands').",
            "- Do NOT add unrelated numeric or alphabetic codes (e.g., 'BSA', '509').",
            "- Do NOT generate rows of alternate icons, tag-style badges, or variant marks.",
            "- Do NOT include or invent taglines unless the branding profile specifically says to include it.",
            "- Avoid **any spelling or typographic errors** in brand name or tagline. Double-check casing and spacing.",

            "At the end of the logo prompt you generate, **append a short visual instruction warning block** like this:"
            "Design must include only one centered logo. Do not include multiple versions, extra icons, mockups, or decorative borders. Use a white or transparent background only. Do not include any placeholder or filler text. All spelling must be correct."

            "Return only the final logo prompt as a plain string — do NOT include JSON, markdown, or explanations."
        ]
    )

    logo_prompt = logo_prompt_agent.run(user_logo_preferences).content

    logo_designer_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        tools=[DalleTools(api_key=st.session_state.openai_api_key, quality='hd', style='natural')],
        description="You are a visual identity assistant that generates professional, brand-focused logo designs.",
        instructions=(
            "You are designing a **single brand logo** — not an illustration, multi-option layout, badge sheet, or product mockup."
            "When given a logo design prompt, use the `create_image` tool to generate a clean, high-resolution, centered, presentation-ready logo."
            "**Strict output requirements:**"
            "- The image must contain **exactly one logo design** — no additional layout variations, badges, or sub-symbols."
            "- The background must be **pure white or transparent** — no gradients, textures, drop shadows, or scene context."
            "- The logo must be **perfectly centered** — no auxiliary lines, label text, or offset composition."
            "- Do NOT generate any real-world mockups (e.g., signs, walls, T-shirts, business cards, etc.)."
            "- The style must be a **clean, flat, vector-style logo** — scalable and modern with bold, simplified forms."
            "- Include **only** the brand name and tagline (if specified), exactly as stated in the prompt — no filler text, codes (e.g., 'BSA'), or made-up branding."
            "- All text must be **accurately spelled** — including capitalization, spacing, and punctuation."
            "- Do not include multiple visual options, bottom rows of variants, or related symbol groups — **only one final logo** in the output."
            "**Your mission:** Create a crisp, minimal, high-quality logo image suitable for brand guidelines, websites, packaging, or app use. Nothing else."
        ),
        markdown=True,
        show_tool_calls=True,
    )

    logo_designer_response = logo_designer_agent.run(logo_prompt)
    logo_url = logo_designer_response.images[0].url

    return logo_url

def main() -> None:
    # Page config
    st.set_page_config(page_title="Logo Designer Bot", page_icon="🎨", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🎨 Logo Designer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Logo Designer Bot — a smart branding tool that captures your style, tone, and vision to generate polished, distinctive logos that help your brand stand out from the crowd.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_logo_preferences = render_logo_preferences()

    st.markdown("---")

    if st.button("🎨 Generate Logo"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        else:
            with st.spinner("Designing your logo..."):
                try:
                    logo_url = generate_logo(user_logo_preferences)
                    response = requests.get(logo_url)
                    
                    if response.status_code == 200:
                        # Save to temporary file
                        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                        tmp_file.write(response.content)
                        tmp_file.flush()

                        # Store logo locally in session
                        st.session_state.logo_url = logo_url
                        st.session_state.logo_path = tmp_file.name

                        st.success("Logo generated successfully!")
                    else:
                        st.error("Failed to download logo image.")
                except Exception as e:
                    st.error(f"Logo generation failed: {e}")

    # Display and allow download if available
    if "logo_path" in st.session_state and "logo_url" in st.session_state:
        st.markdown("## 🖼️ Your Designed Logo")
        st.image(st.session_state.logo_url)
        with open(st.session_state.logo_path, "rb") as file:
            st.download_button(
                label="📥 Download Logo",
                data=file,
                file_name="generated_logo.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()


