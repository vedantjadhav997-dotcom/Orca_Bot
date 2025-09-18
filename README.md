# 🐬 ORCA AI

**ORCA AI** is a sleek, ocean-themed AI assistant built with **Streamlit** and **OpenAI’s GPT models**.  
It allows users to **chat in any language**, **upload files for AI analysis**, and **generate images** with a minimal, elegant interface.

---

## 🌊 Features

### 1. Chatbot
- Chat with ORCA AI in **any language**.  
- Context-aware conversations with **history tracking**.  
- Download chat history in **JSON** or **TXT** formats.  
- Switch between LLM models: `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`.  

### 2. File Upload & Processing
- Upload **text**, **audio**, or **image files**: `.txt`, `.mp3`, `.wav`, `.m4a`, `.png`, `.jpg`, `.jpeg`.  
- **Text files:** Preview and analyze.  
- **Audio files:** Automatic transcription with **Whisper API**.  
- **Images:** Upload and ask ORCA AI to describe or analyze.  
- Maintains **history of uploaded files and AI responses**.  

### 3. Image Generation
- Generate high-quality, **ocean-inspired images**.  
- Enter a creative prompt and receive an AI-generated image.  
- History tracking with **preview** and **download** options.  

### 4. Theme & UI
- **Dark mode toggle** for comfortable viewing.  
- Ocean-themed gradient background with **glassmorphic chat box**.  
- Minimal, modern design for intuitive use.  

---

## ⚙️ Technologies Used
- **Python**  
- **Streamlit** – Frontend UI  
- **OpenAI API** – GPT models & Whisper transcription  
- **Pillow** – Image handling  
- **dotenv** – Environment variable management  
- **base64 & json** – Data encoding and storage  

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ORCA-AI.git
cd ORCA-AI