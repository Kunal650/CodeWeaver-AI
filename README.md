# 🧬 CodeWeaver AI

**Your Intelligent Coding Companion powered by Google's Gemini AI**

A professional AI coding assistant with RAG (Retrieval Augmented Generation) capabilities for context-aware code generation, debugging, and documentation.

![CodeWeaver AI](https://img.shields.io/badge/Powered%20by-Gemini%20AI-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)

---

## ✨ Features

- 💬 **Natural Language Coding** - Describe what you want, get production-ready code
- 📁 **Codebase Understanding** - Upload your project files for context-aware assistance
- 🔍 **RAG-Powered Context** - Retrieves relevant code snippets from your uploaded files
- ⚡ **Code Generation & Debug** - Generate, explain, debug, and optimize code
- 🔄 **Smart Refiner** - Self-correction loop for higher quality output
- 📦 **Export to Markdown** - Download your entire session as documentation
- 🔐 **BYOK Security** - Bring Your Own API Key (never saved to disk)

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CodeWeaver_AI.git
cd CodeWeaver_AI
```

### 2. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key

### 3. Run Locally

#### Option A: Using the Setup Script (Windows)

```bash
# Run the setup script (creates venv and installs dependencies)
setup_venv.bat

# Start the app
run_app.bat
```

#### Option B: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Create .env file for admin key
echo GOOGLE_API_KEY=your_api_key_here > .env

# Run the app
streamlit run main.py
```

### 4. Open in Browser

Navigate to: **http://localhost:8501**

---

## 🔑 API Key Configuration

You have two options:

| Method                 | Description                                                                       |
| ---------------------- | --------------------------------------------------------------------------------- |
| **BYOK (Recommended)** | Enter your API key directly in the sidebar. Key is stored in session memory only. |
| **Admin Mode**         | Add `GOOGLE_API_KEY=your_key` to `.env` file for persistent access.               |

---

## 📁 Project Structure

```
CodeWeaver_AI/
├── main.py              # Streamlit frontend
├── backend.py           # AI logic (CodeBrain + CodeMemory)
├── requirements.txt     # Python dependencies
├── packages.txt         # Linux dependencies (for cloud)
├── .env.template        # Environment template
├── .env                 # Your API key (gitignored)
├── run_app.bat          # Windows launcher
├── run_app.sh           # Linux/Mac launcher
└── README.md            # This file
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the main file path: `main.py`
5. (Optional) Add `GOOGLE_API_KEY` to Secrets if using Admin Mode

> **Note:** Users can bring their own API key via the sidebar, so admin key is optional.

---

## ⚠️ DISCLAIMER

**THIS IS AN AI-POWERED CODE GENERATION TOOL**

By using CodeWeaver AI, you acknowledge and agree that:

1. **Review All Code** - AI-generated code may contain bugs, security vulnerabilities, or logical errors. Always review and test code before using in production.

2. **No Warranty** - This software is provided "as is" without warranty of any kind. The developers are not responsible for any damages arising from the use of generated code.

3. **Not a Replacement** - This tool is designed to assist developers, not replace human judgment. Critical systems should always involve human review.

4. **API Costs** - You are responsible for any API usage costs incurred through your Google API key.

5. **Data Privacy** - Code you upload or generate may be sent to Google's Gemini API for processing. Do not upload sensitive or proprietary code without understanding the implications.

6. **License Compliance** - Ensure any generated code complies with your project's licensing requirements.

---

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **RAG**: LangChain + FAISS
- **Embeddings**: Google Generative AI Embeddings

---

## 📄 License

This project is for educational and personal use. See LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

**Made with ❤️ and AI**
