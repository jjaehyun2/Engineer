import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeGenerator:
    def __init__(self, model_name="qwen2.5-coder", ollama_base_url="http://localhost:11434"):
        """
        코드 생성 클래스 초기화
        
        Args:
            model_name (str): 사용할 Ollama 모델 이름
            ollama_base_url (str): Ollama API 서버 URL
        """
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url
        self.api_url = f"{ollama_base_url}/api/generate"
        logger.info(f"CodeGenerator initialized with model: {model_name}")
        
        # 모델이 준비되었는지 확인
        self._check_model_availability()
        
    def _check_model_availability(self):
        """모델이 로컬에 있는지 확인하고, 없으면 다운로드될 것임을 알림"""
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
        프롬프트를 기반으로 코드 생성
        
        Args:
            prompt (str): 코드 생성을 위한 요구사항 설명
            language (str, optional): 생성할 코드 언어 (예: "python", "javascript")
            timeout (int): 요청 타임아웃 시간(초)
            
        Returns:
            str: 생성된 코드
        """
        if not prompt.strip():
            return "코드 생성에 필요한 요구사항이 없습니다."
            
        lang_instruction = f"{language} 프로그래밍 언어로 " if language else ""
        system_prompt = f"""다음 요구사항에 맞는 {lang_instruction}코드를 생성해주세요. 
코드만 출력하고, 코드는 반드시 마크다운 코드 블록(```) 안에 작성해주세요.
코드는 실행 가능하고, 최적화된 방식으로 작성해주세요.
주석을 포함하여 코드의 이해를 도와주세요."""

        full_prompt = f"{system_prompt}\n\n요구사항: {prompt}"
        
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
            return "요청 시간이 초과되었습니다. 더 간단한 요구사항으로 다시 시도해보세요."
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            return f"코드 생성 중 오류가 발생했습니다: {str(e)}"