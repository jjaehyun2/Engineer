import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self, model_name="qwen2.5-coder", ollama_base_url="http://localhost:11434"):
        """
        Initialize the code generator class
        
        Args:
            model_name (str): Name of the Ollama model to use
            ollama_base_url (str): Ollama API server URL
        """
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url
        self.api_url = f"{ollama_base_url}/api/generate"
        logger.info(f"CodeGenerator initialized with model: {model_name}")
        
        # Check if the model is available
        self._check_model_availability()
        
    def _check_model_availability(self):
        """Check if the model is available locally, warn if it will be downloaded"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags")
            models = response.json().get("models", [])
            available_models = [model["name"] for model in models]
            
            if self.model_name not in available_models:
                logger.warning(f"Model {self.model_name} is not available locally. It will be downloaded on first use.")
            else:
                logger.info(f"Model {self.model_name} is available locally.")
        except Exception as e:
            logger.error(f"Failed to check model availability: {e}")
            logger.warning("Make sure Ollama server is running at: " + self.ollama_base_url)

    def generate_code(self, prompt, language=None, timeout=60):
        """
        Generate code based on the prompt
        
        Args:
            prompt (str): Description of requirements for code generation
            language (str, optional): Programming language for the generated code (e.g., "python", "javascript")
            timeout (int): Request timeout in seconds
            
        Returns:
            str: Generated code
        """
        if not prompt.strip():
            return "No requirements provided for code generation."
            
        lang_instruction = f"in {language} programming language " if language else ""
        include_comments = True  # Default to including comments unless specified otherwise
        comment_instruction = (
        "Include helpful inline comments to explain key logic and improve readability."
        if include_comments else
        "Do NOT include any comments, explanations, or annotations in the code."
)
        system_prompt = f"""
    You are an expert software engineer.
    Your task is to generate clean, optimized, and executable code {lang_instruction}that fulfills the user's requirements.
    You must strictly follow the user's requirements.  
    Prioritize fulfilling every detail mentioned by the user, even if there are simpler or more optimal alternatives.  
    Do not make assumptions or replace requested approaches with your own preferences.  
    Generate code exactly as specified, respecting all constraints and instructions.

    Guidelines:
    - Output **only the code**, and wrap it in a valid markdown code block using triple backticks (```).
    - The code must be **syntactically correct** and **ready to run**.
    - The code should follow **best practices** in structure and performance.
    - {comment_instruction}
    - Absolutely DO NOT include any explanations, comments, or text outside the code block unless explicitly requested.
    - If comments are not to be included, ensure the code contains ZERO comments or annotations.

    Example output format:
    '''{language or ""}
    <your code here>'''
        """

        full_prompt = f"{system_prompt}\n\nRequirements: {prompt}"
        
        try:
            start_time = time.time()
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            elapsed_time = time.time() - start_time
            logger.info(f"Code generation completed in {elapsed_time:.2f} seconds")
            
            return result["response"]
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {timeout} seconds")
            return "The request timed out. Please try again with a simpler requirement."
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            return f"An error occurred during code generation: {str(e)}"