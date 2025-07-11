import requests
import json
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeExplainer:
    def __init__(self, model_name="qwen2.5-coder", ollama_base_url="http://localhost:11434"):
        """
        코드 설명 클래스 초기화
        
        Args:
            model_name (str): 사용할 Ollama 모델 이름
            ollama_base_url (str): Ollama API 서버 URL
        """
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url
        self.api_url = f"{ollama_base_url}/api/generate"
        logger.info(f"CodeExplainer initialized with model: {model_name}")
        
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
    
    def explain_code(self, code, language=None, timeout=300):
        """
        코드를 분석하고 설명 생성
        
        Args:
            code (str): 설명할 코드
            language (str, optional): 코드 언어 (예: "python", "javascript")
            timeout (int): 요청 타임아웃 시간(초)
            
        Returns:
            str: 코드에 대한 설명
        """
        if not code.strip():
            return "설명할 코드가 없습니다."
        
        lang_info = f"{language} " if language else ""
        prompt = f"""다음 {lang_info}코드를 상세히 분석하고 설명해주세요:
        {code}
        다음 형식으로 설명해주세요 :
        1. 코드의 목적과 기능 2. 주요 로직 설명 3. 함수와 변수의 역할 4. 주의할 점이나 개선할 수 있는 부분"""

        try:
            start_time = time.time()
            response = requests.post(self.api_url, json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": True
            }, timeout=timeout)

            response.raise_for_status()
            result = response.json()
            elapsed_time = time.time() - start_time
            logger.info(f"Code explanation generated in {elapsed_time:.2f} seconds")
            return result["response"]
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {timeout} seconds")
            return "요청 시간이 초과되었습니다. 더 짧은 코드로 다시 시도해보세요."
        except Exception as e:
            logger.error(f"Error explaining code: {str(e)}")
            return f"코드 설명 중 오류가 발생했습니다: {str(e)}"