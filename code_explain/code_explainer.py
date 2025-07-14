import requests
import time
import json
import logging
import os

# logging configuration
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CodeExplainer:
    """class for explaining code using an Ollama model"""

    def __init__(self, model_name="qwen2.5-coder", ollama_base_url="http://localhost:11434"):
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url
        self.api_url = f"{ollama_base_url}/api/generate"

        logger.info(f"CodeExplainer initialized with model: {model_name}")

        # Check model availability
        try:
            response = requests.get(f"{ollama_base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model.get("name") for model in models]

                if model_name not in model_names:
                    logger.warning(f"Model {model_name} is not available locally. It will be downloaded on first use.")
            else:
                logger.warning(f"Failed to check model availability: {response.status_code}")
        except Exception as e:
            logger.warning(f"Error checking model availability: {str(e)}")

    def explain_code(self, code, language=None, timeout=120):
        """Analyze the code and generate an explanation"""
        lang_info = f"The code is written in {language}. " if language else ""

        prompt = f"""
            You are a professional code reviewer and software engineer.

            Please analyze and explain the following {language or "code"} with **clarity and conciseness**. 
            Structure your response in clean markdown with headings and bullet points. 
            Avoid repeating information across sections.

            ## 1. Purpose
            - What is the main goal or function of this code?

            ## 2. Key Components
            - List important functions, classes, or modules and describe their roles.

            ## 3. Logic Flow
            - Describe the control flow or main steps of the program.

            ## 4. Notable Features
            - Mention any clever, unique, or advanced techniques used.

            ## 5. Suggestions for Improvement
                - Recommend any enhancements, such as:
                - Code readability improvements
                - Performance optimizations
                - More Pythonic / idiomatic practices
                - Refactoring opportunities
                - Better error handling or logging

            Please write in a **concise and helpful** style that would benefit someone maintaining or learning from this code.

            ```{language or ""}
            {code}
            ```
        """

        try:
            start_time = time.time()

            # 1. Save prompt to file
            prompt_file = os.path.join(os.getcwd(), "temp_prompt.txt")
            with open(prompt_file, "w", encoding="utf-8") as f:
                f.write(prompt)
            logger.info(f"Saved prompt to {prompt_file}")

            # 2. Non-streaming
            try:
                logger.info("1. Non-streaming API 테스트")
                test_response = requests.post(
                    self.api_url,
                    json={
                        "model": self.model_name,
                        "prompt": "Say hello world",
                        "stream": False
                    },
                    timeout=10
                )
                logger.info(f"Status code: {test_response.status_code}")
                logger.info(f"Raw response: {test_response.text[:500]}")
            except Exception as e:
                logger.error(f"Non-streaming API 테스트 실패: {str(e)}")

            # 3. Streaming API call
            logger.info("2. 스트리밍 API 호출 시작")
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=timeout
            )

            logger.info(f"응답 상태 코드: {response.status_code}")

            # 4. response
            full_response = ""
            response_chunks = []

            for i, line in enumerate(response.iter_lines()):
                if line:
                    decoded_line = line.decode('utf-8')

                    if i < 5:
                        logger.info(f"Raw line {i}: {decoded_line}")

                    response_chunks.append(decoded_line)

                    try:
                        json_line = json.loads(decoded_line)
                        chunk = json_line.get("response", "")
                        full_response += chunk
                    except json.JSONDecodeError as je:
                        logger.warning(f"JSON 파싱 오류: {je}, 라인: {decoded_line[:100]}")
                    except Exception as e:
                        logger.warning(f"응답 처리 중 오류: {str(e)}")

            # 5. Save response to file
            raw_response_file = os.path.join(os.getcwd(), "raw_response.txt")
            with open(raw_response_file, "w", encoding="utf-8") as f:
                f.write("\n".join(response_chunks))
            logger.info(f"원시 응답을 {raw_response_file}에 저장했습니다")

            elapsed_time = time.time() - start_time
            logger.info(f"Code explanation generated in {elapsed_time:.2f} seconds")

            return full_response if full_response else "응답이 비어 있습니다. 자세한 내용은 로그를 확인하세요."

        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {timeout} seconds")
            return "요청 시간이 초과되었습니다. 더 짧은 코드로 다시 시도해보세요."

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return f"API 요청 중 오류가 발생했습니다: {str(e)}"

        except Exception as e:
            logger.error(f"Error explaining code: {str(e)}")
            return f"코드 설명 중 오류가 발생했습니다: {str(e)}"
