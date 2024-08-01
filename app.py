import streamlit as st
import openai
import requests

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def generate_content(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

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

prompt = st.text_area("Enter a Prompt:", height=150)

if st.button("Generate Content"):
    with st.spinner("Generating content..."):
        content = generate_content(prompt)
        headings = generate_content(f"Summarize the following content into headings:\n\n{content}").split('\n')
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
