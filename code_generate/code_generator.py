# code_generator.py
import os
import re
from llama_cpp import Llama
# from utils import load_environment


class CodeGenerator:
    def __init__(self, model_path=None):
        """
        CodeGenerator 초기화

        Args:
            model_path: GGUF 모델 파일 경로 (기본값: models 폴더의 첫 번째 .gguf 파일)
        """
        if model_path is None:
            # models 디렉토리에서 .gguf 파일 자동 탐색
            models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
            gguf_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]

            if not gguf_files:
                raise FileNotFoundError("models 디렉토리에 .gguf 모델 파일이 없습니다.")

            model_path = os.path.join(models_dir, gguf_files[0])
            print(f"모델을 자동으로 선택했습니다: {model_path}")

        # 모델 설정 - 메모리와 성능에 따라 조정 가능
        self.model = Llama(
            model_path=model_path,
            n_ctx=4096,  # 컨텍스트 길이
            n_batch=512,  # 배치 크기
            n_gpu_layers=-1  # 가능한 모든 레이어를 GPU로 (GPU 없으면 CPU만 사용)
        )
        print("코드 생성을 위한 로컬 LLM 모델을 로드했습니다.")

    def _generate_response(self, prompt, max_tokens=2048, temperature=0.2):
        """내부 응답 생성 함수"""
        try:
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["Human:", "User:"],  # 응답 종료 토큰
                echo=False  # 프롬프트 제외하고 응답만 반환
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            return f"오류가 발생했습니다: {str(e)}"

    def generate_code(self, requirements, language="python", comment_language="korean", additional_instructions=None):
        """
        주어진 요구사항에 따라 코드를 생성합니다.

        Args:
            requirements: 코드 생성을 위한 요구사항 설명
            language: 생성할 코드의 프로그래밍 언어 (기본값: python)
            comment_language: 주석 언어 ("korean" 또는 "english")
            additional_instructions: 코드 스타일, 구조 등에 관한 추가 지시사항

        Returns:
            생성된 코드
        """
        # 언어별 프롬프트 설정
        if comment_language.lower() == "english":
            instruction = f"Create {language} code that meets the following requirements."
            code_standards = "The code should be executable, efficient, and readable."
            comment_instr = "Include English comments and follow best practices."
            additional = f"\nAdditional instructions: {additional_instructions}" if additional_instructions else ""
            requirements_header = "Requirements:"
            generated_code = "Generated Code:"
        else:  # korean
            instruction = f"다음 요구사항에 맞는 {language} 코드를 생성해주세요."
            code_standards = "코드는 실행 가능하고, 효율적이며, 가독성이 좋아야 합니다."
            comment_instr = "한국어 주석을 포함하고, 모범 사례를 따르는 코드를 작성해주세요."
            additional = f"\n추가 지시사항: {additional_instructions}" if additional_instructions else ""
            requirements_header = "요구사항:"
            generated_code = "생성된 코드:"

        prompt = f"""### 지시사항: {instruction}
        {code_standards}
        {comment_instr}{additional}
        {requirements_header}
        {requirements}
        {generated_code}{language} """
        response = self._generate_response(prompt, max_tokens=2048, temperature=0.2)

        # 코드 블록 마커가 있으면 제거
        code_pattern = r"```(?:\w+)?\s*([\s\S]*?)```"
        code_match = re.search(code_pattern, response)
        if code_match:
            return code_match.group(1).strip()

        return response.strip()

    def generate_function(self, function_description, language="python", parameters=None, return_description=None,
                          comment_language="korean"):
        """
        함수를 생성합니다.

        Args:
            function_description: 함수의 기능 설명
            language: 프로그래밍 언어 (기본값: python)
            parameters: 함수 매개변수 설명 (딕셔너리 또는 리스트)
            return_description: 반환 값 설명
            comment_language: 주석 언어 ("korean" 또는 "english")

        Returns:
            생성된 함수 코드
        """
        # 매개변수 문자열 생성
        params_text = ""
        if parameters:
            if isinstance(parameters, dict):
                params = [f"{name}: {desc}" for name, desc in parameters.items()]
                params_text = "\n- " + "\n- ".join(params)
            elif isinstance(parameters, list):
                params_text = "\n- " + "\n- ".join(parameters)
            else:
                params_text = f"\n- {parameters}"

        # 반환값 설명 생성
        return_text = f"\n\n반환값: {return_description}" if return_description else ""
        if comment_language.lower() == "english":
            return_text = f"\n\nReturn: {return_description}" if return_description else ""

        # 언어별 프롬프트 설정
        if comment_language.lower() == "english":
            instruction = f"Create a {language} function that does the following:"
            params_header = "Parameters:" if params_text else ""
            function_header = "Function:"
        else:  # korean
            instruction = f"다음 기능을 수행하는 {language} 함수를 작성해주세요:"
            params_header = "매개변수:" if params_text else ""
            function_header = "함수:"

        prompt = f"""### 지시사항: {instruction}
        {function_description}{return_text}

        {params_header}{params_text}

        ### {function_header}
        ```{language}
        """

        response = self._generate_response(prompt, max_tokens=1024, temperature=0.2)

        # 코드 블록 마커가 있으면 제거
        code_pattern = r"```(?:\w+)?\s*([\s\S]*?)```"
        code_match = re.search(code_pattern, response)
        if code_match:
            return code_match.group(1).strip()

        return response.strip()

    def improve_code(self, code, instructions=None, language=None, comment_language="korean"):
        """
        기존 코드를 개선합니다.

        Args:
            code: 개선할 코드
            instructions: 개선 방향에 대한 지시사항
            language: 코드의 프로그래밍 언어
            comment_language: 주석 및 설명 언어 ("korean" 또는 "english")

        Returns:
            개선된 코드
        """
        lang_text = language if language else ('코드' if comment_language.lower() == "korean" else 'code')

        # 언어별 프롬프트 설정
        if comment_language.lower() == "english":
            instruction = f"Improve the following {lang_text}."
            if instructions:
                instruction = f"Improve the following {lang_text} based on these instructions: {instructions}"
            original_code = "Original code:"
            improved_code = "Improved code:"
        else:  # korean
            instruction = f"다음 {lang_text}를 개선해주세요."
            if instructions:
                instruction = f"다음 지시사항에 따라 {lang_text}를 개선해주세요: {instructions}"
            original_code = "원본 코드:"
            improved_code = "개선된 코드:"

        prompt = f"""### 지시사항: {instruction}

            ### {original_code}
            {code}
            {improved_code}
            """

        response = self._generate_response(prompt, max_tokens=2048, temperature=0.2)

        # 코드 블록 마커가 있으면 제거
        code_pattern = r"``````"
        code_match = re.search(code_pattern, response)
        if code_match:
            return code_match.group(1).strip()

        return response.strip()

    def generate_from_template(self, template_name, replacements=None, language="python"):
        """
        템플릿을 기반으로 코드를 생성합니다.

        Args:
            template_name: 사용할 템플릿 이름 (예: 'BASIC_SCRIPT', 'CLASS_TEMPLATE')
            replacements: 템플릿에서 대체할 키-값 딕셔너리 (예: {'ClassName': 'MyClass'})
            language: 프로그래밍 언어 (기본값: python)

        Returns:
            생성된 코드
        """
        # 언어별 템플릿 모듈 가져오기
        try:
            if language.lower() == "python":
                from .templates.python_templates import BASIC_SCRIPT, CLASS_TEMPLATE, UNITTEST_TEMPLATE
                templates = {
                    'BASIC_SCRIPT': BASIC_SCRIPT,
                    'CLASS_TEMPLATE': CLASS_TEMPLATE,
                    'UNITTEST_TEMPLATE': UNITTEST_TEMPLATE
                }
            elif language.lower() in ["javascript", "js"]:
                from .templates.javascript_templates import (
                    BASIC_SCRIPT, CLASS_TEMPLATE, REACT_FUNCTIONAL_COMPONENT,
                    REACT_CLASS_COMPONENT, NODE_MODULE, JEST_TEST_TEMPLATE, ASYNC_FUNCTION
                )
                templates = {
                    'BASIC_SCRIPT': BASIC_SCRIPT,
                    'CLASS_TEMPLATE': CLASS_TEMPLATE,
                    'REACT_FUNCTIONAL_COMPONENT': REACT_FUNCTIONAL_COMPONENT,
                    'REACT_CLASS_COMPONENT': REACT_CLASS_COMPONENT,
                    'NODE_MODULE': NODE_MODULE,
                    'JEST_TEST_TEMPLATE': JEST_TEST_TEMPLATE,
                    'ASYNC_FUNCTION': ASYNC_FUNCTION
                }
            else:
                return f"템플릿이 지원되지 않는 언어입니다: {language}"

            # 템플릿 가져오기
            template = templates.get(template_name.upper())
            if not template:
                return f"템플릿을 찾을 수 없습니다: {template_name}"

            # 대체
            if replacements:
                for key, value in replacements.items():
                    template = template.replace(key, value)

            return template

        except Exception as e:
            return f"템플릿 처리 중 오류 발생: {str(e)}"
