import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image
import base64
import json

# --------------------------
# Load environment variables
# --------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# --------------------------
# Page Setup + Theme Toggle
# --------------------------
st.set_page_config(page_title="ORCA AI 🐬", page_icon="🐬", layout="wide")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

theme = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = theme

# Inject custom CSS for Ocean Theme
ocean_css = """
<style>
/* Background */
.stApp {
    background: linear-gradient(to bottom, #00416A, #00B4DB);
    color: white;
}

/* Center container */
.main-container {
    display: flex;
    justify-content: center;
}

/* Chatbox style */
.chat-box {
    background: rgba(255, 255, 255, 0.1);
    padding: 25px;
    border-radius: 20px;
    max-width: 750px;
    width: 100%;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
}

/* Text area */
textarea {
    background: rgba(0,0,0,0.2) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton>button {
    background-color: #0077B6;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #0096C7;
    color: white;
}
</style>
"""
st.markdown(ocean_css, unsafe_allow_html=True)

# --------------------------
# Session State Initialization
# --------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "upload_history" not in st.session_state:
    st.session_state.upload_history = []
if "image_history" not in st.session_state:
    st.session_state.image_history = []
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"

# --------------------------
# Title + Model Selector
# --------------------------
st.markdown("<h1 style='text-align: center;'>🐬 ORCA AI </h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='main-container'><div class='chat-box'>", unsafe_allow_html=True)

    # Model switcher
    model_choice = st.selectbox(
        "🔽 Choose your LLM model:",
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
    )
    st.session_state.model = model_choice

    # --------------------------
    # Feature Selector
    # --------------------------
    feature = st.selectbox(
        "Pick a feature:",
        ["Chatbot", "Upload (Text/Audio/Image)", "Image Generation"]
    )

    # --------------------------
    # Chatbot Mode
    # --------------------------
    if feature == "Chatbot":
        st.subheader("💬 Chat with ORCA AI")

        user_input = st.text_area("Type your message (any language 🌍):", height=100)

        if st.button("Send"):
            if user_input.strip():
                try:
                    messages = [{"role": "system", "content": "You are ORCA AI 🐬, a wise ocean-inspired multilingual assistant."}]
                    for msg in st.session_state.chat_history:
                        messages.append({"role": "user", "content": msg["user"]})
                        messages.append({"role": "assistant", "content": msg["bot"]})

                    messages.append({"role": "user", "content": user_input})

                    response = client.chat.completions.create(
                        model=st.session_state.model,
                        messages=messages
                    )
                    reply = response.choices[0].message.content

                    st.markdown(f"**ORCA AI:** {reply}")

                    st.session_state.chat_history.append({"user": user_input, "bot": reply})

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please enter a message!")

        # Chat history + download
        if st.session_state.chat_history:
            st.subheader("📜 Chat History")
            for msg in st.session_state.chat_history[::-1]:
                st.markdown(f"**You:** {msg['user']}")
                st.markdown(f"**ORCA AI:** {msg['bot']}")
                st.markdown("---")

            # Download buttons
            chat_json = json.dumps(st.session_state.chat_history, indent=2)
            chat_txt = "\n".join([f"You: {m['user']}\nORCA AI: {m['bot']}" for m in st.session_state.chat_history])

            st.download_button("⬇️ Download Chat (JSON)", chat_json, "chat_history.json")
            st.download_button("⬇️ Download Chat (TXT)", chat_txt, "chat_history.txt")

    # --------------------------
    # Upload Mode
    # --------------------------
    elif feature == "Upload (Text/Audio/Image)":
        st.subheader("📤 Upload File")
        uploaded_file = st.file_uploader("Upload txt, mp3, wav, jpg, png", 
                                         type=["txt", "png", "jpg", "jpeg", "mp3", "wav", "m4a"])
        if uploaded_file:
            file_type = uploaded_file.type
            file_content, img_b64 = None, None

            if "text" in file_type:  # text files
                file_content = uploaded_file.read().decode("utf-8")
                st.text_area("Preview:", file_content, height=150, disabled=True)

            elif "audio" in file_type:  # audio files
                with open("temp_audio.mp3", "wb") as f:
                    f.write(uploaded_file.read())
                with open("temp_audio.mp3", "rb") as audio:
                    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio)
                file_content = transcription.text
                st.text_area("🎙️ Transcription:", file_content, height=100, disabled=True)

            elif "image" in file_type:  # images
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_container_width=True)
                uploaded_file.seek(0)
                img_b64 = base64.b64encode(uploaded_file.read()).decode("utf-8")

            # Prompt
            user_prompt = st.text_area("✍️ What should ORCA AI do with this?", height=100)

            if st.button("Process"):
                if user_prompt.strip():
                    try:
                        if file_content:
                            response = client.chat.completions.create(
                                model=st.session_state.model,
                                messages=[{"role": "user", "content": f"{user_prompt}\n\nContent:\n{file_content}"}]
                            )
                            reply = response.choices[0].message.content
                            st.markdown(f"**ORCA AI:** {reply}")

                            st.session_state.upload_history.append({
                                "prompt": user_prompt,
                                "file": file_type,
                                "response": reply
                            })

                        elif img_b64:
                            response = client.chat.completions.create(
                                model=st.session_state.model,
                                messages=[{
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": user_prompt},
                                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                                    ]
                                }]
                            )
                            reply = response.choices[0].message.content
                            st.markdown(f"**ORCA AI:** {reply}")

                            st.session_state.upload_history.append({
                                "prompt": user_prompt,
                                "file": file_type,
                                "response": reply
                            })

                    except Exception as e:
                        st.error(f"Error: {e}")

        # Upload history
        if st.session_state.upload_history:
            st.subheader("📜 Upload History")
            for item in st.session_state.upload_history[::-1]:
                st.markdown(f"**Prompt:** {item['prompt']}")
                st.markdown(f"**File Type:** {item['file']}")
                st.markdown(f"**ORCA AI:** {item['response']}")
                st.markdown("---")

    # --------------------------
    # Image Generation Mode
    # --------------------------
    elif feature == "Image Generation":
        st.subheader("🎨 Generate Ocean-Inspired Image")
        img_prompt = st.text_area("Enter prompt for image:", height=100)

        if st.button("Generate"):
            if img_prompt.strip():
                try:
                    result = client.images.generate(
                        model="gpt-image-1",
                        prompt=img_prompt,
                        size="1024x1024"   
                    )

                    
                    img_url = result.data[0].url
                    st.image(img_url, caption="Generated Image", use_container_width=True)

                    # Save history
                    st.session_state.image_history.append({"prompt": img_prompt, "url": img_url})

                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.image_history:
            st.subheader("📜 Image History")
            for item in st.session_state.image_history[::-1]:
                st.markdown(f"**Prompt:** {item['prompt']}")
                st.image(item['url'], use_container_width=True)

            # Allow download of last image
            last_img = st.session_state.image_history[-1]
            st.download_button("⬇️ Download Last Image", last_img["url"], "generated.png")

    st.markdown("</div></div>", unsafe_allow_html=True)
