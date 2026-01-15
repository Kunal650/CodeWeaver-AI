"""
CodeWeaver AI - Backend Logic
The brain behind the AI coding assistant.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Google Generative AI
try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "google-generativeai package not found. "
        "Please install it with: pip install google-generativeai"
    )


# =============================================================================
# Token Management Utilities
# =============================================================================

# Token limit configuration
MAX_CONTEXT_TOKENS = 30000
TOKENS_PER_CHAR_ESTIMATE = 0.25  # Rough estimate: ~4 chars per token


def count_tokens(text: str) -> int:
    """
    Count the approximate number of tokens in a text string.
    Uses character-based estimation for efficiency.
    
    Args:
        text: The text to count tokens for.
    
    Returns:
        Approximate token count.
    """
    if not text:
        return 0
    
    # Use character-based estimation (faster than API call)
    # Rough estimate: ~4 characters per token for code/English
    estimated_tokens = int(len(text) * TOKENS_PER_CHAR_ESTIMATE)
    
    return estimated_tokens


def truncate_to_token_limit(text: str, max_tokens: int) -> str:
    """
    Truncate text to fit within a token limit.
    
    Args:
        text: The text to truncate.
        max_tokens: Maximum number of tokens allowed.
    
    Returns:
        Truncated text if needed.
    """
    current_tokens = count_tokens(text)
    
    if current_tokens <= max_tokens:
        return text
    
    # Calculate the character limit based on token estimate
    char_limit = int(max_tokens / TOKENS_PER_CHAR_ESTIMATE)
    
    # Truncate from the beginning (keep recent context)
    truncated = "...[Earlier context truncated for token limit]...\n\n" + text[-char_limit:]
    
    return truncated


class CodeBrain:
    """
    The intelligent brain of CodeWeaver AI.
    Handles all AI-powered code generation and analysis.
    """

    # System prompt that defines CodeWeaver's personality and behavior
    SYSTEM_PROMPT = """You are CodeWeaver, a Principal Software Architect and 10x Engineer. Your Rules:

1. No Placeholders: Never use comments like '# ... rest of code'. Write the full, functional code every time.

2. Production Ready: All code must include error handling (try/except), type hinting, and DocStrings.

3. Modular: If the solution requires multiple files, specify the filename at the top of the code block like ### filename.py.

4. Modern Stack: Always use the latest stable versions of libraries (e.g., Functional React components, not Class components).

5. Self-Correction: If you detect a potential security risk (like SQL injection), fix it and explain the fix.

6. Tone: Concise, technical, and direct. Do not apologize. Just solve."""

    def __init__(self, api_key: str = None):
        """
        Initialize the CodeBrain with Google Generative AI.
        
        Supports BYOK (Bring Your Own Key) architecture:
        - If api_key is provided, uses that key (User Mode)
        - If api_key is None/empty, falls back to .env file (Admin Mode)
        
        Args:
            api_key: Optional API key provided by user. Never saved to disk.
        """
        # BYOK: Use provided key, or fall back to environment variable
        if api_key and api_key.strip():
            self.api_key = api_key.strip()
            self._key_source = "user"  # For logging/debugging only
        else:
            self.api_key = os.getenv("GOOGLE_API_KEY", "")
            self._key_source = "env"
        
        self._validate_api_key()
        self._configure_ai()
        self._initialize_model()

    def _validate_api_key(self) -> None:
        """
        Validate that the API key is present and not a placeholder.
        
        Raises:
            ValueError: If API key is missing or invalid.
        """
        if not self.api_key:
            raise ValueError(
                "API key not provided. Please enter your Gemini API key in the sidebar, "
                "or add GOOGLE_API_KEY to your .env file."
            )
        
        if self.api_key == "your_google_api_key_here":
            raise ValueError(
                "Please replace the placeholder API key with your actual key. "
                "Get one from: https://aistudio.google.com/app/apikey"
            )

    def _configure_ai(self) -> None:
        """Configure the Google Generative AI with the API key."""
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            raise ConnectionError(f"Failed to configure Google AI: {str(e)}")

    def _initialize_model(self) -> None:
        """
        Initialize the Gemini model with generation configuration.
        Uses gemini-2.0-flash as the latest free version.
        """
        try:
            # Generation configuration for optimal code output
            generation_config = genai.GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
            )

            # Initialize the model with gemini-2.5-flash
            self.model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                generation_config=generation_config,
                system_instruction=self.SYSTEM_PROMPT
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize AI model: {str(e)}")

    def generate_code(self, user_prompt: str, context: str = "", enable_refiner: bool = False, conversation_history: list = None) -> str:
        """
        Generate code based on user's request and optional codebase context.
        
        Includes token management to prevent context length errors.
        
        Args:
            user_prompt: The user's code generation request.
            context: Optional context from the codebase (existing code, file contents, etc.)
            enable_refiner: If True, applies self-correction loop for higher quality output.
            conversation_history: Optional list of previous messages for context truncation.
        
        Returns:
            The AI-generated response with explanation and code.
        
        Raises:
            RuntimeError: If code generation fails.
        """
        try:
            # Build the full prompt with context if provided
            full_prompt = self._build_prompt(user_prompt, context)
            
            # Token limit check and truncation
            prompt_tokens = count_tokens(full_prompt)
            
            if prompt_tokens > MAX_CONTEXT_TOKENS:
                print(f"⚠️ Prompt exceeds token limit ({prompt_tokens} > {MAX_CONTEXT_TOKENS}). Truncating context...")
                
                # Truncate the context first
                if context:
                    truncated_context = truncate_to_token_limit(
                        context, 
                        MAX_CONTEXT_TOKENS - count_tokens(user_prompt) - 1000  # Reserve space for prompt
                    )
                    full_prompt = self._build_prompt(user_prompt, truncated_context)
                else:
                    # Truncate the prompt itself if no context
                    full_prompt = truncate_to_token_limit(full_prompt, MAX_CONTEXT_TOKENS)
                
                print(f"   Truncated to ~{count_tokens(full_prompt)} tokens")
            
            # Generate initial response from the model
            response = self.model.generate_content(full_prompt)
            
            # Extract the text response
            if response and response.text:
                initial_code = response.text
                
                # Apply self-correction loop if enabled
                if enable_refiner:
                    refined_code = self.refine_code(initial_code, user_prompt)
                    return refined_code
                else:
                    return initial_code
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
                
        except genai.types.BlockedPromptException:
            return "⚠️ The request was blocked due to safety filters. Please rephrase your request."
        
        except genai.types.StopCandidateException as e:
            return f"⚠️ Generation stopped early: {str(e)}"
        
        except Exception as e:
            error_msg = str(e)
            
            # Handle common API errors with helpful messages
            if "quota" in error_msg.lower():
                return "⚠️ API quota exceeded. Please wait a moment and try again."
            elif "invalid" in error_msg.lower() and "key" in error_msg.lower():
                return "⚠️ Invalid API key. Please check your GOOGLE_API_KEY in the .env file."
            elif "not found" in error_msg.lower():
                return "⚠️ Model not available. The service may be temporarily unavailable."
            elif "context" in error_msg.lower() and "length" in error_msg.lower():
                return "⚠️ Context too long. Please clear some chat history or reduce file uploads."
            else:
                return f"⚠️ An error occurred: {error_msg}"

    def refine_code(self, original_code: str, user_prompt: str) -> str:
        """
        Self-correction loop to ensure high-quality code output.
        Analyzes and refines the generated code for errors and improvements.
        
        Args:
            original_code: The initially generated code/response.
            user_prompt: The original user request for context.
        
        Returns:
            The refined, higher-quality code response.
        """
        # Reviewer system prompt for code analysis
        reviewer_prompt = f"""You are a Code Reviewer. Analyze the following code based on the user's request. 
If there are syntax errors, security vulnerabilities, or logical flaws, rewrite the code to fix them. 
If the code is perfect, return it as is.

ORIGINAL USER REQUEST:
{user_prompt}

CODE TO REVIEW:
{original_code}

INSTRUCTIONS:
1. Check for syntax errors and fix them
2. Identify any security vulnerabilities (SQL injection, XSS, etc.)
3. Look for logical flaws or edge cases not handled
4. Ensure best practices are followed
5. Verify the code fulfills the user's request
6. If improvements are made, briefly note what was fixed at the end

Provide the refined code below:"""

        try:
            # Use efficient token management - only refine if code looks substantial
            if len(original_code) < 50:  # Skip refinement for short responses
                return original_code
            
            # Generate refined response
            response = self.model.generate_content(reviewer_prompt)
            
            if response and response.text:
                return response.text
            else:
                # If refinement fails, return original
                return original_code
                
        except Exception as e:
            # If refinement fails, return original code
            print(f"Refinement failed: {str(e)}")
            return original_code

    def _build_prompt(self, user_prompt: str, context: str = "") -> str:
        """
        Build the complete prompt with context.
        
        Args:
            user_prompt: The user's request.
            context: Optional codebase context.
        
        Returns:
            The formatted prompt string.
        """
        if context:
            return f"""CODEBASE CONTEXT:
```
{context}
```

USER REQUEST:
{user_prompt}

Please analyze the context and fulfill the user's request."""
        else:
            return user_prompt

    def explain_code(self, code: str) -> str:
        """
        Explain the given code in detail.
        
        Args:
            code: The source code to explain.
        
        Returns:
            Detailed explanation of the code.
        """
        prompt = f"""Please analyze and explain the following code in detail:

```
{code}
```

Provide:
1. A brief overview of what the code does
2. Line-by-line explanation of key parts
3. Any potential issues or improvements
4. Best practices recommendations"""
        
        return self.generate_code(prompt)

    def debug_code(self, code: str, error_message: str = "") -> str:
        """
        Debug the given code and suggest fixes.
        
        Args:
            code: The buggy source code.
            error_message: Optional error message.
        
        Returns:
            Debug analysis and corrected code.
        """
        prompt = f"""Debug the following code:

CODE:
```
{code}
```

ERROR MESSAGE: {error_message if error_message else "No specific error provided"}

Please provide:
1. Identified issues and bugs
2. Root cause analysis
3. Corrected code with fixes
4. Explanation of what was wrong and how it was fixed"""
        
        return self.generate_code(prompt)

    def optimize_code(self, code: str) -> str:
        """
        Optimize the given code for performance and readability.
        
        Args:
            code: The source code to optimize.
        
        Returns:
            Optimization analysis and improved code.
        """
        prompt = f"""Optimize the following code for better performance and readability:

```
{code}
```

Please provide:
1. Performance analysis of the current code
2. Identified optimization opportunities
3. Optimized version of the code
4. Explanation of improvements made"""
        
        return self.generate_code(prompt)

    def chat(self, message: str, history: list = None) -> str:
        """
        Have a conversation about coding topics.
        
        Args:
            message: The user's message.
            history: Optional conversation history.
        
        Returns:
            AI response to the message.
        """
        if history is None:
            history = []
        
        # Build conversation context
        context_parts = []
        for h in history[-5:]:  # Keep last 5 exchanges for context
            context_parts.append(f"User: {h.get('user', '')}")
            context_parts.append(f"Assistant: {h.get('assistant', '')}")
        
        conversation_context = "\n".join(context_parts)
        
        if conversation_context:
            prompt = f"""Previous conversation:
{conversation_context}

Current message: {message}

Please respond helpfully to the user's current message, taking into account the conversation history."""
        else:
            prompt = message
        
        return self.generate_code(prompt)


# =============================================================================
# CodeMemory - RAG System for Project Understanding
# =============================================================================

class CodeMemory:
    """
    RAG (Retrieval Augmented Generation) system for understanding project files.
    Uses FAISS vector store and LangChain for local, free retrieval.
    """
    
    # Supported file extensions for ingestion
    SUPPORTED_EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.md', '.txt', '.json', '.css', '.html'}
    
    def __init__(self, api_key: str = None):
        """
        Initialize the CodeMemory with embeddings and vector store.
        
        Args:
            api_key: Google API key for embeddings (uses env var if not provided).
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.vector_store = None
        self.documents = []
        self.chunk_size = 1000
        self.chunk_overlap = 200
        
        self._initialize_embeddings()
    
    def _initialize_embeddings(self) -> None:
        """Initialize the Google Generative AI embeddings model."""
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=self.api_key
            )
        except ImportError:
            raise ImportError(
                "langchain-google-genai not found. "
                "Install with: pip install langchain-google-genai"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize embeddings: {str(e)}")
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename."""
        import os
        return os.path.splitext(filename)[1].lower()
    
    def _is_supported_file(self, filename: str) -> bool:
        """Check if the file type is supported for ingestion."""
        return self._get_file_extension(filename) in self.SUPPORTED_EXTENSIONS
    
    def _read_file_content(self, uploaded_file) -> tuple:
        """
        Read content from an uploaded file.
        
        Args:
            uploaded_file: Streamlit UploadedFile object.
        
        Returns:
            Tuple of (content, filename) or (None, None) if failed.
        """
        try:
            filename = uploaded_file.name
            
            if not self._is_supported_file(filename):
                return None, filename
            
            # Read file content
            content = uploaded_file.read()
            
            # Decode bytes to string
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            
            return content, filename
            
        except Exception as e:
            print(f"Error reading file {uploaded_file.name}: {str(e)}")
            return None, uploaded_file.name
    
    def _split_into_chunks(self, text: str, filename: str) -> list:
        """
        Split text into overlapping chunks for embedding.
        
        Args:
            text: The text content to split.
            filename: Source filename for metadata.
        
        Returns:
            List of document chunks with metadata.
        """
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from langchain.schema import Document
        except ImportError:
            from langchain_core.documents import Document
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        # Configure the text splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split the text
        chunks = splitter.split_text(text)
        
        # Create Document objects with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": filename,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            )
            documents.append(doc)
        
        return documents
    
    def ingest_files(self, uploaded_files: list) -> dict:
        """
        Ingest multiple uploaded files into the vector store.
        
        Args:
            uploaded_files: List of Streamlit UploadedFile objects.
        
        Returns:
            Dictionary with ingestion statistics.
        """
        try:
            from langchain_community.vectorstores import FAISS
        except ImportError:
            try:
                from langchain.vectorstores import FAISS
            except ImportError:
                raise ImportError(
                    "FAISS not found. Install with: pip install faiss-cpu"
                )
        
        stats = {
            "files_processed": 0,
            "files_skipped": 0,
            "chunks_created": 0,
            "skipped_files": [],
            "processed_files": []
        }
        
        all_documents = []
        
        for uploaded_file in uploaded_files:
            content, filename = self._read_file_content(uploaded_file)
            
            if content is None:
                stats["files_skipped"] += 1
                stats["skipped_files"].append(filename)
                continue
            
            # Split content into chunks
            chunks = self._split_into_chunks(content, filename)
            all_documents.extend(chunks)
            
            stats["files_processed"] += 1
            stats["chunks_created"] += len(chunks)
            stats["processed_files"].append(filename)
        
        # Create or update vector store
        if all_documents:
            try:
                if self.vector_store is None:
                    # Create new vector store
                    self.vector_store = FAISS.from_documents(
                        documents=all_documents,
                        embedding=self.embeddings
                    )
                else:
                    # Add to existing vector store
                    self.vector_store.add_documents(all_documents)
                
                self.documents.extend(all_documents)
                
            except Exception as e:
                raise RuntimeError(f"Failed to create vector store: {str(e)}")
        
        return stats
    
    def retrieve_context(self, query: str, k: int = 3) -> str:
        """
        Retrieve relevant code context for a query with re-ranking.
        
        Optimized for token efficiency:
        - Limits to Top 3 most relevant chunks (re-ranked by similarity)
        - Enforces token limits to prevent context overflow
        
        Args:
            query: The user's question or code request.
            k: Number of relevant chunks to retrieve (default: 3 for efficiency).
        
        Returns:
            Formatted string of relevant code context within token limits.
        """
        if self.vector_store is None:
            return ""
        
        try:
            # Search for similar documents with scores for re-ranking
            # Request more results initially for re-ranking
            results_with_scores = self.vector_store.similarity_search_with_score(query, k=min(k * 2, 10))
            
            if not results_with_scores:
                return ""
            
            # Re-rank: Sort by similarity score (lower is better for FAISS L2 distance)
            sorted_results = sorted(results_with_scores, key=lambda x: x[1])
            
            # Take only Top 3 most relevant chunks
            top_results = sorted_results[:3]
            
            # Format the context
            context_parts = []
            seen_sources = set()
            total_chars = 0
            max_context_chars = int(MAX_CONTEXT_TOKENS / TOKENS_PER_CHAR_ESTIMATE * 0.5)  # Reserve 50% for response
            
            for doc, score in top_results:
                source = doc.metadata.get("source", "unknown")
                content = doc.page_content
                
                # Check if adding this chunk would exceed limit
                if total_chars + len(content) > max_context_chars:
                    # Truncate and stop
                    remaining = max_context_chars - total_chars
                    if remaining > 100:
                        context_parts.append(content[:remaining] + "\n...[truncated for token limit]")
                    break
                
                # Add source header if new file
                if source not in seen_sources:
                    header = f"\n--- From: {source} (relevance: {1/(1+score):.2f}) ---"
                    context_parts.append(header)
                    seen_sources.add(source)
                    total_chars += len(header)
                
                context_parts.append(content)
                total_chars += len(content)
            
            context_str = "\n".join(context_parts)
            
            # Final token check and truncation if needed
            if count_tokens(context_str) > MAX_CONTEXT_TOKENS // 2:
                context_str = truncate_to_token_limit(context_str, MAX_CONTEXT_TOKENS // 2)
            
            return context_str
            
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return ""
    
    def get_all_sources(self) -> list:
        """Get list of all ingested file sources."""
        sources = set()
        for doc in self.documents:
            sources.add(doc.metadata.get("source", "unknown"))
        return sorted(list(sources))
    
    def clear_memory(self) -> None:
        """Clear all ingested documents and reset the vector store."""
        self.vector_store = None
        self.documents = []
    
    def get_stats(self) -> dict:
        """Get current memory statistics."""
        return {
            "total_documents": len(self.documents),
            "total_sources": len(self.get_all_sources()),
            "sources": self.get_all_sources(),
            "has_vector_store": self.vector_store is not None
        }


# =============================================================================
# Singleton Instances
# =============================================================================

_brain_instance = None
_memory_instance = None


def get_brain() -> CodeBrain:
    """
    Get or create the CodeBrain singleton instance.
    
    Returns:
        The CodeBrain instance.
    """
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = CodeBrain()
    return _brain_instance


def get_memory() -> CodeMemory:
    """
    Get or create the CodeMemory singleton instance.
    
    Returns:
        The CodeMemory instance.
    """
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = CodeMemory()
    return _memory_instance


# Backward compatibility aliases
CodeWeaverBackend = CodeBrain
get_backend = get_brain
