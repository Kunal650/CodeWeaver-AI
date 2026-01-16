"""
CodeWeaver AI - Modern Chat Interface
A professional AI coding assistant with RAG capabilities.
"""

import streamlit as st
import os
import re
from datetime import datetime

# Page Configuration - Must be first Streamlit command
st.set_page_config(
    page_title="CodeWeaver AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# VS Code Theme - Custom CSS Injection
# =============================================================================

def inject_custom_css():
    """
    Inject VS Code-style CSS to create an IDE-like experience.
    Hides default Streamlit elements and applies dark theme styling.
    """
    st.markdown("""
    <style>
        /* ============================================
           VS CODE THEME - HIDE DEFAULT ELEMENTS
           ============================================ */
        
        /* Hide Deploy button */
        .stDeployButton {
            display: none !important;
        }
        
        /* Hide Hamburger menu */
        #MainMenu {
            visibility: hidden !important;
        }
        
        /* Hide header */
        header {
            visibility: hidden !important;
        }
        
        /* Hide footer */
        footer {
            visibility: hidden !important;
        }
        
        /* ============================================
           VS CODE STYLE - CODE BLOCKS
           ============================================ */
        
        /* Code block styling - VS Code editor look */
        pre, code {
            font-family: 'Consolas', 'Courier New', 'Monaco', 'Menlo', monospace !important;
            font-size: 14px !important;
            line-height: 1.5 !important;
        }
        
        /* Code block container */
        .stCodeBlock {
            background-color: #1e1e1e !important;
            border: 1px solid #3c3c3c !important;
            border-radius: 6px !important;
        }
        
        /* Syntax highlighting - VS Code Dark+ theme colors */
        .stCodeBlock code {
            background-color: #1e1e1e !important;
            color: #d4d4d4 !important;
        }
        
        /* Code block with line numbers feel */
        pre {
            background-color: #1e1e1e !important;
            border: 1px solid #3c3c3c !important;
            border-radius: 6px !important;
            padding: 12px 16px !important;
        }
        
        /* ============================================
           VS CODE STYLE - CHAT INPUT
           ============================================ */
        
        /* Chat input dark border */
        .stChatInput {
            border-color: #3c3c3c !important;
        }
        
        .stChatInput > div {
            background-color: #252526 !important;
            border: 1px solid #3c3c3c !important;
            border-radius: 8px !important;
        }
        
        .stChatInput input, .stChatInput textarea {
            background-color: #252526 !important;
            color: #d4d4d4 !important;
            border: none !important;
        }
        
        .stChatInput input:focus, .stChatInput textarea:focus {
            border-color: #007acc !important;
            box-shadow: 0 0 0 1px #007acc !important;
        }
        
        /* ============================================
           VS CODE STYLE - SCROLLBARS
           ============================================ */
        
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1e1e1e;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #424242;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #4f4f4f;
        }
        
        /* ============================================
           VS CODE STYLE - SIDEBAR
           ============================================ */
        
        [data-testid="stSidebar"] {
            background-color: #252526 !important;
            border-right: 1px solid #3c3c3c !important;
        }
        
        /* Activity bar accent */
        [data-testid="stSidebar"]::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #007acc 0%, #0e639c 100%);
        }
        
    </style>
    """, unsafe_allow_html=True)


# Call inject_custom_css at the top of the app
inject_custom_css()

# =============================================================================
# Custom CSS for Dark Theme & Professional Styling
# =============================================================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #12121a 50%, #0d0d14 100%);
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.3rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: -1px;
    }
    
    .sub-header {
        color: #6b7280;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111118 0%, #0d0d12 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.1);
    }
    
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1.5rem;
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(30, 41, 59, 0.6) 100%);
        border: 1px solid rgba(71, 85, 105, 0.3);
        margin-right: 2rem;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 10px !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
    }
    
    pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Input styling */
    .stTextInput input, .stTextArea textarea {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.4);
        border: 2px dashed rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 1rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #818cf8;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
        margin: 1.5rem 0;
    }
    
    /* Chat input at bottom */
    .stChatInput {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Spinner */
    .stSpinner > div {
        border-color: #6366f1 !important;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.4rem 1rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35) !important;
    }
    
    /* Enhanced code block styling for IDE look */
    .stCodeBlock {
        background: #0d1117 !important;
        border-radius: 8px !important;
        border: 1px solid #30363d !important;
        margin: 0.5rem 0 !important;
    }
    
    .stCodeBlock pre {
        background: #0d1117 !important;
        padding: 1rem !important;
    }
    
    /* Code header bar */
    .code-header {
        background: linear-gradient(135deg, #21262d 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-bottom: none;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #8b949e;
    }
    
    .code-language {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .code-language-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #6366f1;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# Utility Functions
# =============================================================================

def extract_code_blocks(text: str) -> list:
    """
    Extract code blocks from markdown-formatted text.
    Returns list of tuples: (language, code, full_match)
    """
    # Pattern to match ```language\ncode\n```
    pattern = r'```(\w*)\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    blocks = []
    for lang, code in matches:
        # Default to python if no language specified
        language = lang.lower() if lang else 'python'
        # Map common variations
        lang_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'jsx': 'javascript',
            'tsx': 'typescript',
            'sh': 'bash',
            'shell': 'bash',
            '': 'python'
        }
        language = lang_map.get(language, language)
        blocks.append((language, code.strip()))
    
    return blocks


def detect_primary_language(code: str) -> str:
    """Detect the programming language from code content."""
    # Simple heuristics for language detection
    if 'def ' in code or 'import ' in code or 'class ' in code and ':' in code:
        return 'python'
    elif 'function ' in code or 'const ' in code or 'let ' in code or '=>' in code:
        return 'javascript'
    elif 'fn ' in code or 'let mut' in code or '::' in code:
        return 'rust'
    elif 'func ' in code or 'package ' in code:
        return 'go'
    elif '<html' in code.lower() or '</div>' in code:
        return 'html'
    elif 'SELECT ' in code.upper() or 'FROM ' in code.upper():
        return 'sql'
    else:
        return 'python'  # Default


def render_file_tree(files: list) -> str:
    """
    Generate an ASCII-style tree structure for uploaded files.
    Similar to the Linux 'tree' command output.
    
    Args:
        files: List of uploaded file objects with .name attribute
    
    Returns:
        Formatted ASCII tree string
    """
    if not files:
        return "📂 (No files uploaded)"
    
    # Get file names and organize by extension
    file_names = sorted([f.name for f in files])
    
    # Build tree structure
    tree_lines = ["📂 **Project Context**"]
    
    # Group files by extension for better visualization
    extensions = {}
    for name in file_names:
        ext = name.split('.')[-1] if '.' in name else 'other'
        if ext not in extensions:
            extensions[ext] = []
        extensions[ext].append(name)
    
    # Emoji mapping for file types
    ext_emoji = {
        'py': '🐍',
        'js': '📜',
        'jsx': '⚛️',
        'ts': '📘',
        'tsx': '⚛️',
        'html': '🌐',
        'css': '🎨',
        'json': '📋',
        'md': '📝',
        'txt': '📄',
        'other': '📁'
    }
    
    total_files = len(file_names)
    current_idx = 0
    
    for ext, names in extensions.items():
        emoji = ext_emoji.get(ext, '📄')
        for i, name in enumerate(names):
            current_idx += 1
            is_last = current_idx == total_files
            prefix = "└── " if is_last else "├── "
            tree_lines.append(f"{prefix}{emoji} `{name}`")
    
    # Add summary
    tree_lines.append("")
    tree_lines.append(f"**{total_files} file(s)** in context")
    
    return "\n".join(tree_lines)


def parse_multi_file_response(response: str) -> list:
    """
    Parse AI response for multi-file markers (### filename.ext).
    Returns list of tuples: (filename, language, code)
    """
    # Pattern to match ### filename.ext followed by code block
    pattern = r'###\s+([\w\-\.\/]+)\s*\n```(\w*)\n(.*?)```'
    matches = re.findall(pattern, response, re.DOTALL)
    
    files = []
    for filename, lang, code in matches:
        # Determine language from extension if not specified
        if not lang:
            ext = filename.split('.')[-1] if '.' in filename else ''
            ext_to_lang = {
                'py': 'python',
                'js': 'javascript',
                'jsx': 'javascript',
                'ts': 'typescript',
                'tsx': 'typescript',
                'html': 'html',
                'css': 'css',
                'json': 'json',
                'md': 'markdown',
                'sql': 'sql',
                'sh': 'bash',
                'rs': 'rust',
                'go': 'go',
                'java': 'java',
                'cpp': 'cpp',
                'c': 'c'
            }
            lang = ext_to_lang.get(ext, 'python')
        
        files.append((filename.strip(), lang.lower(), code.strip()))
    
    return files


def render_response_with_code(response: str):
    """
    Render AI response with proper syntax highlighting and download buttons.
    Supports multi-file responses with tabbed display.
    """
    # First, check for multi-file response (### filename.ext markers)
    multi_files = parse_multi_file_response(response)
    
    if multi_files and len(multi_files) > 1:
        # Multi-file response - use tabs
        st.markdown("### 📁 Project Files")
        st.markdown(f"*{len(multi_files)} files generated*")
        
        # Create tabs for each file
        tab_names = [f"📄 {f[0]}" for f in multi_files]
        tabs = st.tabs(tab_names)
        
        for idx, (tab, (filename, lang, code)) in enumerate(zip(tabs, multi_files)):
            with tab:
                # File info header
                st.markdown(f'''
                <div class="code-header" style="margin-bottom: 0;">
                    <div class="code-language">
                        <span class="code-language-dot"></span>
                        <span>{filename}</span>
                    </div>
                    <span style="color: #6b7280; font-size: 0.75rem;">{lang.upper()}</span>
                </div>
                ''', unsafe_allow_html=True)
                
                # Code with syntax highlighting
                st.code(code, language=lang)
                
                # Download button for this file
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.download_button(
                        label=f"📥 Download",
                        data=code,
                        file_name=filename,
                        mime="text/plain",
                        key=f"download_multi_{idx}_{hash(code)}"
                    )
        
        # Remove the parsed multi-file parts and show remaining text
        remaining = re.sub(r'###\s+[\w\-\.\/]+\s*\n```\w*\n.*?```', '', response, flags=re.DOTALL)
        if remaining.strip():
            st.markdown("---")
            st.markdown(remaining.strip())
        
        return
    
    # Single file or regular code blocks
    code_blocks = extract_code_blocks(response)
    
    if code_blocks:
        # Split response by code blocks and render each part
        parts = re.split(r'```\w*\n.*?```', response, flags=re.DOTALL)
        
        for i, part in enumerate(parts):
            # Render text part
            if part.strip():
                # Clean up any stray ### markers
                clean_part = re.sub(r'###\s+[\w\-\.\/]+\s*$', '', part, flags=re.MULTILINE)
                if clean_part.strip():
                    st.markdown(clean_part.strip())
            
            # Render corresponding code block if exists
            if i < len(code_blocks):
                lang, code = code_blocks[i]
                
                # Check if there's a filename marker before this block
                filename_match = re.search(r'###\s+([\w\-\.\/]+)\s*$', part, re.MULTILINE)
                if filename_match:
                    display_name = filename_match.group(1)
                    download_filename = display_name
                else:
                    display_name = lang.upper()
                    file_ext = {
                        'python': '.py',
                        'javascript': '.js',
                        'typescript': '.ts',
                        'html': '.html',
                        'css': '.css',
                        'sql': '.sql',
                        'bash': '.sh',
                        'rust': '.rs',
                        'go': '.go',
                        'java': '.java',
                        'cpp': '.cpp',
                        'c': '.c'
                    }.get(lang, '.txt')
                    download_filename = f"codeweaver_output{file_ext}"
                
                # Code header
                st.markdown(f'''
                <div class="code-header">
                    <div class="code-language">
                        <span class="code-language-dot"></span>
                        <span>{display_name}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Render code with syntax highlighting
                st.code(code, language=lang)
                
                # Download button
                st.download_button(
                    label=f"📥 Download {display_name}",
                    data=code,
                    file_name=download_filename,
                    mime="text/plain",
                    key=f"download_{i}_{hash(code)}"
                )
    else:
        # No code blocks, just render as markdown
        st.markdown(response)


def generate_project_documentation() -> str:
    """
    Generate a markdown documentation file from the chat history.
    Compiles all user prompts and AI code responses into a single document.
    
    Returns:
        Formatted markdown string.
    """
    from datetime import datetime as dt
    
    # Header
    doc = f"""# CodeWeaver AI - Project Documentation

Generated on: {dt.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Session Summary

This document contains the complete interaction history from your CodeWeaver AI session, including all prompts and generated code.

---

"""
    
    # Process chat history
    for idx, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            doc += f"## 💬 User Request #{(idx // 2) + 1}\n\n"
            doc += f"{message['content']}\n\n"
        else:
            doc += f"### 🧬 CodeWeaver Response\n\n"
            doc += f"{message['content']}\n\n"
            doc += "---\n\n"
    
    # Footer
    doc += """
---

## Notes

- This documentation was automatically generated by CodeWeaver AI
- Code blocks are formatted with proper syntax highlighting when viewed in a markdown editor
- For best results, open this file in VS Code, GitHub, or any markdown-compatible viewer

---

*Powered by CodeWeaver AI - Your Intelligent Coding Companion*
"""
    
    return doc


# =============================================================================
# Session State Initialization
# =============================================================================

def init_session_state():
    """Initialize all session state variables."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("GOOGLE_API_KEY", "")
    
    if "brain" not in st.session_state:
        st.session_state.brain = None
    
    if "memory" not in st.session_state:
        st.session_state.memory = None
    
    if "files_uploaded" not in st.session_state:
        st.session_state.files_uploaded = False
    
    if "memory_stats" not in st.session_state:
        st.session_state.memory_stats = None
    
    if "enable_refiner" not in st.session_state:
        st.session_state.enable_refiner = False


# =============================================================================
# Backend Initialization
# =============================================================================

def initialize_backend(api_key: str):
    """
    Initialize the CodeBrain and CodeMemory with the provided API key.
    
    BYOK Security: API key is passed directly to CodeBrain, not saved to environment.
    The key exists only in session memory (RAM) for the duration of the session.
    
    Args:
        api_key: The Gemini API key (user's key or admin .env key)
    
    Returns:
        True if initialization successful, False otherwise.
    """
    try:
        # Import backend modules
        from backend import CodeBrain, CodeMemory
        
        # Get selected model from session state (default to Flash)
        selected_model = st.session_state.get("selected_model", "gemini-2.5-flash")
        
        # Initialize brain with BYOK support and model selection
        # Security: Key is passed in memory, not saved to environment/disk
        st.session_state.brain = CodeBrain(api_key=api_key, model_name=selected_model)
        
        # Initialize memory (for RAG) with the same key
        st.session_state.memory = CodeMemory(api_key=api_key)
        
        return True
        
    except Exception as e:
        st.error(f"❌ Failed to initialize: {str(e)}")
        return False


# =============================================================================
# Sidebar
# =============================================================================

def render_sidebar():
    """Render the sidebar with API key input and file upload."""
    with st.sidebar:
        # Logo/Brand
        st.markdown("## 🧬 CodeWeaver")
        st.markdown("---")
        
        # API Key Section - BYOK Architecture
        st.markdown("### 🔑 API Configuration")
        
        # BYOK: API Key input (password type for security)
        user_api_key = st.text_input(
            "🔑 Enter Your Gemini API Key",
            type="password",
            value=st.session_state.get("user_api_key", ""),
            placeholder="Paste your API key here",
            help="Your key is stored in session memory only - never saved to disk"
        )
        
        # Security info and link
        st.markdown("""
        <div style="
            font-size: 0.75rem;
            color: #9ca3af;
            margin-top: -0.5rem;
        ">
            ⚠️ Get your free key at <a href="https://aistudio.google.com" target="_blank" style="color: #60a5fa;">aistudio.google.com</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Store user key in session state (RAM only - never saved to disk)
        if user_api_key != st.session_state.get("user_api_key", ""):
            st.session_state.user_api_key = user_api_key
            st.session_state.brain = None  # Reset brain to use new key
            st.session_state.memory = None
        
        # Determine which key to use (BYOK priority)
        effective_key = st.session_state.get("user_api_key", "") or st.session_state.get("api_key", "")
        
        # Initialize button
        if effective_key and st.session_state.brain is None:
            if st.button("🚀 Connect", use_container_width=True):
                with st.spinner("Initializing AI..."):
                    if initialize_backend(effective_key):
                        st.success("✅ Connected!")
                        st.rerun()
        
        # Show connection status
        if st.session_state.brain:
            key_source = "Your Key" if st.session_state.get("user_api_key") else "Admin Key"
            st.success(f"✅ AI Connected ({key_source})")
        elif effective_key:
            st.info("Click 'Connect' to initialize")
        else:
            st.warning("⚠️ API Key required")
        
        st.markdown("---")
        
        # File Upload Section
        st.markdown("### 📁 Project Files")
        
        uploaded_files = st.file_uploader(
            "Upload your code files",
            type=["py", "js", "jsx", "ts", "tsx", "md", "txt", "json", "css", "html"],
            accept_multiple_files=True,
            help="Upload project files for context-aware assistance"
        )
        
        if uploaded_files and st.session_state.memory:
            if st.button("📥 Process Files", use_container_width=True):
                with st.spinner("Processing files..."):
                    try:
                        # Reset file positions for re-reading
                        for f in uploaded_files:
                            f.seek(0)
                        
                        stats = st.session_state.memory.ingest_files(uploaded_files)
                        st.session_state.files_uploaded = True
                        st.session_state.memory_stats = stats
                        
                        st.success(f"✅ Processed {stats['files_processed']} files!")
                        
                        if stats['files_skipped'] > 0:
                            st.warning(f"⚠️ Skipped {stats['files_skipped']} unsupported files")
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        # Show memory stats
        if st.session_state.memory_stats:
            stats = st.session_state.memory_stats
            st.markdown("---")
            st.markdown("### 📊 Memory Stats")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Files", stats['files_processed'])
            with col2:
                st.metric("Chunks", stats['chunks_created'])
            
            # Project Context Map - ASCII tree visualization
            if stats['processed_files']:
                with st.expander("� Current Context Map", expanded=True):
                    # Create file objects with name attribute for render_file_tree
                    class FileObj:
                        def __init__(self, name):
                            self.name = name
                    
                    file_objects = [FileObj(f) for f in stats['processed_files']]
                    tree_output = render_file_tree(file_objects)
                    st.markdown(tree_output)
        
        st.markdown("---")
        
        # AI Settings
        st.markdown("### 🎛️ AI Settings")
        
        # Model Selector
        model_options = {
            "⚡ Flash (Fastest)": "gemini-2.5-flash",
            "🧠 Pro (Smartest)": "gemini-2.5-pro",
        }
        
        # Get current model from session state or default
        current_model_label = st.session_state.get("selected_model_label", "⚡ Flash (Fastest)")
        
        selected_model_label = st.radio(
            "🧠 AI Model Power",
            options=list(model_options.keys()),
            index=list(model_options.keys()).index(current_model_label),
            help="Flash: Fast & efficient for simple tasks. Pro: Most capable for complex architecture."
        )
        
        # Store in session state if changed
        if selected_model_label != st.session_state.get("selected_model_label"):
            st.session_state.selected_model_label = selected_model_label
            st.session_state.selected_model = model_options[selected_model_label]
            # Reset brain to use new model
            if st.session_state.brain:
                st.session_state.brain = None
                st.info("💡 Model changed. Click 'Connect' to reinitialize with the new model.")
        
        # Model description
        if "Pro" in selected_model_label:
            st.markdown("""
            <div style="font-size: 0.75rem; color: #fbbf24; margin-bottom: 0.5rem;">
                🧠 Best for: Complex architecture, multi-file projects, debugging hard problems
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="font-size: 0.75rem; color: #34d399; margin-bottom: 0.5rem;">
                ⚡ Best for: Quick scripts, simple tasks, faster responses
            </div>
            """, unsafe_allow_html=True)
        
        # Smart Refiner Toggle
        enable_refiner = st.toggle(
            "🔄 Smart Refiner",
            value=st.session_state.enable_refiner,
            help="Enable self-correction loop for higher quality code. Slower but produces more accurate, error-free code."
        )
        
        if enable_refiner != st.session_state.enable_refiner:
            st.session_state.enable_refiner = enable_refiner
        
        if st.session_state.enable_refiner:
            st.markdown("""
            <div style="
                background: rgba(99, 102, 241, 0.1);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 8px;
                padding: 0.5rem;
                font-size: 0.8rem;
                color: #a5b4fc;
            ">
                ✨ Code will be reviewed and refined for errors, security issues, and best practices.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Vision-to-Code Section
        st.markdown("### 📷 Vision to Code")
        
        uploaded_image = st.file_uploader(
            "Upload UI Screenshot (Vision to Code)",
            type=["png", "jpg", "jpeg"],
            help="Upload a UI screenshot and CodeWeaver will generate the HTML/CSS/React code to recreate it pixel-perfectly."
        )
        
        if uploaded_image:
            # Display the uploaded image
            st.image(uploaded_image, caption="Uploaded UI Screenshot", use_container_width=True)
            
            # Store in session state
            st.session_state.uploaded_image = uploaded_image
            
            # Optional additional instructions
            vision_instructions = st.text_area(
                "Additional Instructions (Optional)",
                placeholder="e.g., 'Use React', 'Add dark mode', 'Make it responsive'",
                height=70
            )
            
            if st.button("🎨 Generate Code from Screenshot", use_container_width=True):
                if st.session_state.brain:
                    with st.spinner("🔍 Analyzing screenshot and generating code..."):
                        # Read image data
                        uploaded_image.seek(0)
                        image_bytes = uploaded_image.read()
                        
                        # Call the vision analysis function
                        result = st.session_state.brain.analyze_image(image_bytes, vision_instructions)
                        
                        # Add to chat history
                        user_msg = f"📷 [Vision-to-Code] Analyze this UI screenshot: {uploaded_image.name}"
                        if vision_instructions:
                            user_msg += f"\nInstructions: {vision_instructions}"
                        
                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": user_msg
                        })
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": result
                        })
                        
                        st.success("✅ Code generated! Check the chat.")
                        st.rerun()
                else:
                    st.warning("⚠️ Please connect to AI first (enter API key and click Connect)")
        
        st.markdown("---")
        
        # Actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.session_state.memory and st.button("🧹 Clear Memory", use_container_width=True):
            st.session_state.memory.clear_memory()
            st.session_state.memory_stats = None
            st.session_state.files_uploaded = False
            st.success("Memory cleared!")
            st.rerun()
        
        st.markdown("---")
        
        # Auto-Test Generator Section
        st.markdown("### 🐞 Auto-Test Generator")
        
        # File input for testing
        test_target_file = st.text_input(
            "Python file to test",
            placeholder="e.g., utils.py or /path/to/file.py",
            label_visibility="collapsed",
            key="test_target_input"
        )
        
        if st.button("🐞 Gen & Run Tests", use_container_width=True, help="Generate and run pytest tests"):
            if st.session_state.brain:
                if test_target_file.strip():
                    try:
                        import os
                        from backend import FileEditor, CodeBrain
                        
                        filepath = test_target_file.strip()
                        
                        # Read the source file
                        if os.path.exists(filepath):
                            with open(filepath, 'r', encoding='utf-8') as f:
                                code = f.read()
                        elif st.session_state.memory and hasattr(st.session_state.memory, 'documents'):
                            # Try to find in uploaded files
                            code = None
                            for doc in st.session_state.memory.documents:
                                if doc.metadata.get('source', '').endswith(filepath):
                                    code = doc.page_content
                                    break
                            if not code:
                                st.error(f"❌ File not found: {filepath}")
                                st.stop()
                        else:
                            st.error(f"❌ File not found: {filepath}")
                            st.stop()
                        
                        with st.spinner("🔍 Analyzing code and generating tests..."):
                            # Generate test code
                            test_response = st.session_state.brain.generate_tests(code, filepath)
                            
                            # Extract Python code from response
                            import re
                            code_match = re.search(r'```python\n(.*?)```', test_response, re.DOTALL)
                            if code_match:
                                test_code = code_match.group(1)
                            else:
                                test_code = test_response
                            
                            # Create test filename
                            basename = os.path.basename(filepath)
                            name, ext = os.path.splitext(basename)
                            test_filename = f"test_{name}.py"
                            test_filepath = os.path.join(os.path.dirname(filepath) or ".", test_filename)
                            
                            # Save test file using FileEditor
                            save_result = FileEditor.safe_write_file(test_filepath, test_code)
                            
                            if save_result["success"]:
                                st.success(f"✅ Created: `{test_filename}`")
                                
                                # Run the tests
                                with st.spinner("🧪 Running pytest..."):
                                    test_result = CodeBrain.run_tests(test_filepath)
                                
                                # Display results
                                if test_result["success"]:
                                    # All tests passed - green box
                                    st.markdown(f"""
                                    <div style="
                                        background: rgba(16, 185, 129, 0.15);
                                        border: 2px solid #10b981;
                                        border-radius: 10px;
                                        padding: 1rem;
                                        margin: 0.5rem 0;
                                    ">
                                        <h4 style="color: #10b981; margin: 0;">✅ All Tests Passed!</h4>
                                        <p style="color: #a7f3d0; margin: 0.5rem 0;">
                                            🟢 {test_result['passed']} passed
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.toast("✅ All tests passed!", icon="✅")
                                else:
                                    # Tests failed - red box
                                    st.markdown(f"""
                                    <div style="
                                        background: rgba(239, 68, 68, 0.15);
                                        border: 2px solid #ef4444;
                                        border-radius: 10px;
                                        padding: 1rem;
                                        margin: 0.5rem 0;
                                    ">
                                        <h4 style="color: #ef4444; margin: 0;">❌ Tests Failed</h4>
                                        <p style="color: #fca5a5; margin: 0.5rem 0;">
                                            🟢 {test_result['passed']} passed | 
                                            🔴 {test_result['failed']} failed
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Show test output
                                    with st.expander("📋 Test Output", expanded=True):
                                        st.code(test_result["output"], language="text")
                                    
                                    # Auto-prompt to fix
                                    st.warning("🔧 Generating fix suggestions...")
                                    
                                    fix_prompt = f"""The following tests FAILED:

{test_result['output']}

ORIGINAL CODE ({filepath}):
```python
{code}
```

Analyze the test failures and fix the code. Provide the corrected version."""
                                    
                                    fix_response = st.session_state.brain.generate_code(fix_prompt)
                                    
                                    # Add to chat for visibility
                                    st.session_state.chat_history.append({
                                        "role": "user",
                                        "content": f"🐞 [Auto-Test] Fix code based on test failures for `{filepath}`"
                                    })
                                    st.session_state.chat_history.append({
                                        "role": "assistant",
                                        "content": fix_response
                                    })
                                    
                                    st.info("💡 Fix suggestions added to chat. Review and apply.")
                            else:
                                st.error(f"❌ Could not save test file: {save_result['message']}")
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a Python file path")
            else:
                st.warning("⚠️ Connect to AI first")
        
        st.markdown("""
        <div style="font-size: 0.75rem; color: #6b7280;">
            Enter filename → Generates tests → Runs pytest → Shows results
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

        
        # Export Project Section
        st.markdown("### 📦 Export")
        
        # License key check placeholder (commented out for now)
        # def check_license_key(key: str) -> bool:
        #     """Validate user's license key for premium features."""
        #     # TODO: Implement license validation logic
        #     # valid_keys = fetch_valid_keys_from_server()
        #     # return key in valid_keys
        #     return True
        
        # is_licensed = check_license_key(st.session_state.get("license_key", ""))
        is_licensed = True  # Placeholder - license check disabled
        
        # Get chat history length
        chat_len = len(st.session_state.get("chat_history", []))
        
        if chat_len > 0:
            # Generate markdown on-the-fly for download
            markdown_content = generate_project_documentation()
            
            st.download_button(
                label="📦 Export to Markdown",
                data=markdown_content,
                file_name="Project_Documentation.md",
                mime="text/markdown",
                use_container_width=True,
                key=f"export_md_btn_{chat_len}"  # Dynamic key to force refresh
            )
            
            st.markdown(f"""
            <div style="
                font-size: 0.75rem;
                color: #6b7280;
                margin-top: 0.5rem;
            ">
                📝 {chat_len} messages ready to export
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background: rgba(107, 114, 128, 0.1);
                border: 1px solid rgba(107, 114, 128, 0.2);
                border-radius: 8px;
                padding: 0.75rem;
                font-size: 0.8rem;
                color: #6b7280;
                text-align: center;
            ">
                💬 Start a conversation to enable export
            </div>
            """, unsafe_allow_html=True)
        
        # One-Click README Generation
        st.markdown("---")
        st.markdown("### 📄 Auto Documentation")
        
        if st.session_state.files_uploaded and st.session_state.memory_stats:
            if st.button("📄 Generate README.md", use_container_width=True, help="Analyze your codebase and generate a professional README"):
                if st.session_state.brain and st.session_state.memory:
                    with st.spinner("📝 Analyzing codebase and generating README..."):
                        try:
                            # Get the uploaded files content from memory
                            code_files = {}
                            if hasattr(st.session_state.memory, 'documents') and st.session_state.memory.documents:
                                for doc in st.session_state.memory.documents:
                                    filename = doc.metadata.get('source', 'unknown')
                                    content = doc.page_content
                                    if filename not in code_files:
                                        code_files[filename] = content
                                    else:
                                        code_files[filename] += "\n" + content
                            
                            # Generate README
                            readme_content = st.session_state.brain.generate_readme(code_files)
                            
                            # Store in session state for display
                            st.session_state.generated_readme = readme_content
                            st.success("✅ README.md generated!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("⚠️ Please connect to AI first")
            
            # Display generated README if available
            if st.session_state.get("generated_readme"):
                st.markdown("---")
                with st.expander("📄 Generated README.md", expanded=True):
                    st.markdown(st.session_state.generated_readme)
                
                # Download button
                st.download_button(
                    label="⬇️ Download README.md",
                    data=st.session_state.generated_readme,
                    file_name="README.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key="download_readme_btn"
                )
        else:
            st.markdown("""
            <div style="
                background: rgba(107, 114, 128, 0.1);
                border: 1px solid rgba(107, 114, 128, 0.2);
                border-radius: 8px;
                padding: 0.75rem;
                font-size: 0.8rem;
                color: #6b7280;
                text-align: center;
            ">
                📁 Upload code files to generate README
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Git Control Center
        st.markdown("### 🐙 Version Control")
        
        try:
            from git import Repo, InvalidGitRepositoryError, GitCommandError
            
            try:
                # Try to get the repo from current working directory
                repo = Repo(os.getcwd())
                
                # Git Status Button
                if st.button("📄 Status", use_container_width=True, help="Show changed files (git status)"):
                    try:
                        # Get status
                        changed = [item.a_path for item in repo.index.diff(None)]
                        staged = [item.a_path for item in repo.index.diff("HEAD")]
                        untracked = repo.untracked_files
                        
                        with st.expander("📄 Git Status", expanded=True):
                            if staged:
                                st.markdown("**Staged Changes:**")
                                for f in staged:
                                    st.markdown(f"• 🟢 `{f}`")
                            
                            if changed:
                                st.markdown("**Modified (not staged):**")
                                for f in changed:
                                    st.markdown(f"• 🟡 `{f}`")
                            
                            if untracked:
                                st.markdown("**Untracked Files:**")
                                for f in untracked[:10]:  # Limit to 10
                                    st.markdown(f"• ⚪ `{f}`")
                                if len(untracked) > 10:
                                    st.markdown(f"*...and {len(untracked) - 10} more*")
                            
                            if not staged and not changed and not untracked:
                                st.success("✅ Working tree clean - nothing to commit")
                                
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                
                # Git Commit Section
                commit_msg = st.text_input(
                    "Commit Message",
                    placeholder="feat: add new feature",
                    label_visibility="collapsed"
                )
                
                if st.button("💾 Commit", use_container_width=True, help="Stage all and commit"):
                    if commit_msg.strip():
                        try:
                            # Stage all changes
                            repo.git.add(A=True)
                            # Commit
                            repo.index.commit(commit_msg)
                            st.toast("✅ Committed successfully!", icon="✅")
                            st.success(f"✅ Committed: `{commit_msg}`")
                        except GitCommandError as e:
                            st.error(f"❌ Git error: {str(e)}")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter a commit message")
                
                # Git Push Button
                if st.button("🚀 Push", use_container_width=True, help="Push to remote"):
                    try:
                        origin = repo.remote(name='origin')
                        push_info = origin.push()
                        st.toast("🚀 Pushed successfully!", icon="🚀")
                        st.success("✅ Pushed to remote!")
                    except GitCommandError as e:
                        error_msg = str(e)
                        if "rejected" in error_msg:
                            st.error("❌ Push rejected. Pull first: `git pull`")
                        elif "Could not read from remote" in error_msg:
                            st.error("❌ Remote not accessible. Check your credentials.")
                        else:
                            st.error(f"❌ Push failed: {error_msg}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                
                # Show current branch
                try:
                    current_branch = repo.active_branch.name
                    st.markdown(f"""
                    <div style="font-size: 0.75rem; color: #6b7280; margin-top: 0.5rem;">
                        📍 Branch: <code>{current_branch}</code>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    pass
                    
            except InvalidGitRepositoryError:
                st.warning("⚠️ No Git repo found")
                st.markdown("""
                <div style="font-size: 0.8rem; color: #6b7280;">
                    Run <code>git init</code> to initialize
                </div>
                """, unsafe_allow_html=True)
                
        except ImportError:
            st.info("ℹ️ GitPython not installed. Run: `pip install GitPython`")
        
        st.markdown("---")
        
        # About
        st.markdown("### ℹ️ About")
        st.markdown("""
        **CodeWeaver AI** is your intelligent 
        coding companion powered by Google's 
        Gemini AI with RAG capabilities.
        
        **Features:**
        - 💬 Natural language coding
        - 📁 Codebase understanding
        - 🔍 Context-aware responses
        - ⚡ Code generation & debug
        - 🔄 Self-correction loop
        - 📦 Export to Markdown
        """)


# =============================================================================
# Chat Interface
# =============================================================================

def render_chat_message(role: str, content: str):
    """Render a single chat message with styling."""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You</strong><br><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🧬 CodeWeaver</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(content)


def render_chat():
    """Render the main chat interface."""
    # Header
    st.markdown('<h1 class="main-header">CodeWeaver AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your Intelligent Coding Companion with RAG • Powered by Gemini</p>', unsafe_allow_html=True)
    
    # Check if ready
    if not st.session_state.brain:
        st.markdown("---")
        
        # Welcome card
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
        ">
            <h2 style="color: #e2e8f0; margin-bottom: 1rem;">👋 Welcome to CodeWeaver AI</h2>
            <p style="color: #94a3b8; font-size: 1.1rem;">
                To get started, enter your Google API Key in the sidebar and click Connect.
            </p>
            <p style="color: #6b7280; margin-top: 1rem;">
                Get your free API key from 
                <a href="https://makersuite.google.com/app/apikey" target="_blank" style="color: #818cf8;">
                    Google AI Studio →
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💻</div>
                <div style="color: #e2e8f0; font-weight: 600;">Code Generation</div>
                <div style="color: #6b7280; font-size: 0.85rem; margin-top: 0.5rem;">
                    Generate clean, documented code
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📁</div>
                <div style="color: #e2e8f0; font-weight: 600;">RAG Context</div>
                <div style="color: #6b7280; font-size: 0.85rem; margin-top: 0.5rem;">
                    Upload files for smart context
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🐛</div>
                <div style="color: #e2e8f0; font-weight: 600;">Debug & Fix</div>
                <div style="color: #6b7280; font-size: 0.85rem; margin-top: 0.5rem;">
                    Find and fix bugs instantly
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        return
    
    st.markdown("---")
    
    # Context indicator
    if st.session_state.files_uploaded:
        st.markdown("""
        <div style="
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            margin-bottom: 1rem;
            display: inline-block;
        ">
            <span style="color: #10b981;">📚 Context Active</span>
            <span style="color: #6b7280;"> — AI will use your uploaded files for context</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        for idx, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🧬"):
                    # Use simple markdown for history to avoid duplicate download buttons
                    st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about coding...", key="chat_input"):
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant", avatar="🧬"):
            # Show appropriate spinner message
            if st.session_state.enable_refiner:
                spinner_msg = "🧬 CodeWeaver is thinking & refining..."
            else:
                spinner_msg = "🧬 CodeWeaver is thinking..."
            
            with st.spinner(spinner_msg):
                try:
                    # Retrieve context if files are uploaded
                    context = ""
                    if st.session_state.memory and st.session_state.files_uploaded:
                        context = st.session_state.memory.retrieve_context(prompt)
                    
                    # Generate response with optional refinement
                    response = st.session_state.brain.generate_code(
                        prompt, 
                        context, 
                        enable_refiner=st.session_state.enable_refiner
                    )
                    
                    # Check for agentic file editing commands
                    if "[APPLY_TO_FILE:" in response:
                        from backend import FileEditor
                        import re
                        
                        # Extract file path and code
                        file_match = re.search(r'\[APPLY_TO_FILE:\s*([^\]]+)\]', response)
                        if file_match:
                            filepath = file_match.group(1).strip()
                            
                            # Extract the code block after the marker
                            code_match = re.search(r'```[\w]*\n(.*?)```', response, re.DOTALL)
                            if code_match:
                                code_content = code_match.group(1)
                                
                                # Use safe_write_file with backup
                                result = FileEditor.safe_write_file(filepath, code_content)
                                
                                if result["success"]:
                                    st.toast("✅ Changes Applied!", icon="✅")
                                    if result["backup_path"]:
                                        st.info(f"📂 Backup created: `{result['backup_path']}`")
                                    st.success(result["message"])
                                else:
                                    st.error(result["message"])
                    
                    # Render response with proper code highlighting and download
                    render_response_with_code(response)
                    
                    # Add to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    
    # Voice Input Section
    st.markdown("---")
    
    voice_col1, voice_col2 = st.columns([3, 1])
    
    with voice_col1:
        st.markdown("""
        <div style="font-size: 0.85rem; color: #9ca3af; margin-bottom: 0.5rem;">
            🎤 <strong>Voice Input</strong> — Speak your coding request
        </div>
        """, unsafe_allow_html=True)
    
    with voice_col2:
        st.markdown("""
        <div style="font-size: 0.75rem; color: #6b7280; text-align: right;">
            Click microphone → speak → release
        </div>
        """, unsafe_allow_html=True)
    
    # Audio input widget
    audio_input = st.audio_input("Record your voice command", key="voice_input", label_visibility="collapsed")
    
    if audio_input:
        # Process the recorded audio
        with st.spinner("🎤 Transcribing your voice..."):
            try:
                # Read audio bytes
                audio_bytes = audio_input.read()
                
                # Determine MIME type based on audio format (Streamlit uses WAV by default)
                mime_type = "audio/wav"
                
                # Transcribe using Gemini
                transcribed_text = st.session_state.brain.transcribe_audio(audio_bytes, mime_type)
                
                # Check if transcription was successful
                if transcribed_text and not transcribed_text.startswith("⚠️") and transcribed_text != "[UNCLEAR AUDIO]":
                    st.success(f"🎤 **You said:** {transcribed_text}")
                    
                    # Process the transcribed text as a prompt
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": f"🎤 [Voice] {transcribed_text}"
                    })
                    
                    # Generate response
                    with st.chat_message("assistant", avatar="🧬"):
                        with st.spinner("🧬 CodeWeaver is thinking..."):
                            context = ""
                            if st.session_state.memory and st.session_state.files_uploaded:
                                context = st.session_state.memory.retrieve_context(transcribed_text)
                            
                            response = st.session_state.brain.generate_code(
                                transcribed_text, 
                                context, 
                                enable_refiner=st.session_state.enable_refiner
                            )
                            
                            render_response_with_code(response)
                            
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": response
                            })
                    
                    st.rerun()
                else:
                    st.warning(f"Could not transcribe audio: {transcribed_text}")
                    
            except Exception as e:
                st.error(f"🎤 Voice processing error: {str(e)}")


# =============================================================================
# Main Application
# =============================================================================

def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render main chat interface
    render_chat()


if __name__ == "__main__":
    main()
