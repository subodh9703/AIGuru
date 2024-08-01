import streamlit as st
import openai
from dotenv import load_dotenv
import os
import streamlit.components.v1 as components
import tempfile

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_content(prompt, content_type):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or use "gpt-3.5-turbo"
        messages=[{"role": "user", "content": f"Generate a {content_type}: {prompt}"}]
    )
    return response.choices[0].message['content'].strip()

def generate_image(description):
    response = openai.Image.create(
        prompt=description,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

def generate_html(content, headings, images):
    html_content = "<html><head><title>Generated Content</title></head><body>"
    for heading, image in zip(headings, images):
        html_content += f"<h2>{heading}</h2>"
        html_content += f"<img src='{image}' alt='{heading}'><br>"
    html_content += f"<p>{content}</p>"
    html_content += "</body></html>"
    return html_content

# Streamlit UI
st.title("AI-Powered Content Generator")

# Dropdown to select content type
content_type = st.selectbox("Select Content Type:", ["Article", "Blog Post", "Report", "Story"])

# Text area for entering the prompt
prompt = st.text_area("Enter a Prompt:", height=150)

if st.button("Generate Content"):
    with st.spinner("Generating content..."):
        content = generate_content(prompt, content_type)
        
        # Summarize content into headings
        headings_summary = generate_content(f"Summarize the following content into headings:\n\n{content}", content_type)
        headings = headings_summary.split('\n')[:4]  # Limit to 4 headings

        images = [generate_image(heading) for heading in headings]

        st.subheader("Generated Headings and Images:")
        for heading, image in zip(headings, images):
            st.write(f"**{heading}**")
            st.image(image, caption=heading)

        html_content = generate_html(content, headings, images)
        
        st.subheader("Generated HTML Content:")
        st.code(html_content, language='html')

        st.download_button(
            label="Download HTML",
            data=html_content,
            file_name="generated_content.html",
            mime="text/html"
        )

        # Save HTML content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            tmp_file.write(html_content.encode('utf-8'))
            tmp_file_path = tmp_file.name
        
        # Load HTML content in an iframe
        st.subheader("Preview Generated HTML")
        components.iframe(f'file://{tmp_file_path}', height=600, scrolling=True)
