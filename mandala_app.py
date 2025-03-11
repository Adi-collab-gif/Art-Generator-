import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image
import base64

def generate_mandala(prompt, api_key):
    """Generate a mandala image using OpenAI's DALL-E 3 model."""
    try:
        client = OpenAI(api_key=api_key)
        
        # Create a more detailed prompt for the mandala
        detailed_prompt = f"Create a stunning black and white mandala art inspired by the word '{prompt}'. The design should be intricate, symmetrical, and highly detailed with a clear circular pattern. Pure black and white only, no gray tones."
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=detailed_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            style="vivid"
        )
        
        image_url = response.data[0].url
        
        # Get the image from the URL
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        
        return img, image_url
    
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None, None

def get_image_download_link(img, filename, text):
    """Generate a download link for the image."""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}.png">{text}</a>'
    return href

def main():
    st.set_page_config(page_title="Mandala Art Generator", layout="centered")
    
    st.title("Black & White Mandala Art Generator")
    st.write("Enter a single word of inspiration to create a unique mandala design.")
    
    # Create sidebar for API key
    st.sidebar.title("Configuration")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    st.sidebar.markdown("""
    ### About this app
    This app generates black and white mandala art using OpenAI's DALL-E 3 model.
    
    You need to provide your own API key to use the app. Your key is not stored and is only used to generate images.
    
    ### How to use
    1. Enter your OpenAI API key in the sidebar
    2. Type a single word for inspiration
    3. Click 'Generate Mandala'
    4. Download your image using the button below the generated image
    """)
    
    # Main area for generation
    inspiration_word = st.text_input("Inspiration Word:", placeholder="Enter a single word (e.g., ocean, nature, cosmos)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        generate_btn = st.button("Generate Mandala")
    
    if generate_btn:
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        elif not inspiration_word:
            st.error("Please enter an inspiration word.")
        else:
            with st.spinner("Creating your mandala art..."):
                image, image_url = generate_mandala(inspiration_word, api_key)
                
                if image:
                    st.success("Mandala generated successfully!")
                    st.image(image, caption=f"Mandala inspired by '{inspiration_word}'", use_column_width=True)
                    
                    # Generate download link
                    download_filename = f"mandala_{inspiration_word}"
                    st.markdown(get_image_download_link(image, download_filename, "Download Mandala Image"), unsafe_allow_html=True)
                    
                    # Display the prompt used for transparency
                    with st.expander("View the prompt used to generate this image"):
                        st.write(f"Create a stunning black and white mandala art inspired by the word '{inspiration_word}'. The design should be intricate, symmetrical, and highly detailed with a clear circular pattern. Pure black and white only, no gray tones.")

if __name__ == "__main__":
    main()