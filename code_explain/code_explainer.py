import os
import sys
from llama_cpp import Llama


class CodeExplainer:
    def __init__(self, model_path=None):
        if model_path is None:
            # 모델 경로를 설정합니다
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(os.path.dirname(current_dir), "models")

            # 모델 디렉토리에서 .gguf 파일 찾기
            model_files = [f for f in os.listdir(model_dir) if f.endswith('.gguf')]
            if not model_files:
                raise FileNotFoundError("모델 파일을 찾을 수 없습니다. models 디렉토리에 .gguf 파일이 있는지 확인하세요.")

            # 첫 번째 모델 파일 사용
            model_path = os.path.join(model_dir, model_files[0])

        print(f"로컬 LLM 모델을 로드합니다: {os.path.basename(model_path)}...")

        # 모델 초기화 (매개변수 최적화)
        self.model = Llama(
            model_path=model_path,
            n_ctx=2048,  # 컨텍스트 크기
            n_batch=512,  # 배치 크기
            n_gpu_layers=0,  # GPU 없으면 0, 있으면 -1
            verbose=False,  # 디버그 출력 끄기
        )

    def explain_code(self, code, language=None):
        """
        코드를 분석하고 설명합니다.

        Args:
            code (str): 설명할 코드
            language (str, optional): 프로그래밍 언어. None이면 자동 감지

        Returns:
            str: 코드 설명
        """
        lang_str = f"{language} " if language else ""
        prompt = (
            f"아래 {lang_str}코드를 분석하고 한국어로 명확하게 설명해주세요.\n\n"
            f"코드:\n{code}\n\n"
            "다음 구조로 설명해주세요: "
            "1. 코드 개요: 이 코드가 무엇을 하는지 간략히 설명 "
            "2. 주요 기능 및 구성 요소: 중요한 부분들을 설명 "
            "3. 실행 흐름: 코드가 어떻게 실행되는지 순서대로 설명 "
            "4. 개선 가능성: 더 나은 구현 방법 제안 (있는 경우)\n"
            "설명:"
        )
        print("\n처리 중입니다. 이 작업은 하드웨어에 따라 시간이 걸릴 수 있습니다...\n")
        output = self.model(
            prompt,
            max_tokens=512,
            temperature=0.2,
            top_p=0.9,
            repeat_penalty=1.2,
            stop=["```"],
            echo = False
        )
        explanation = output['choices']['text'].strip()
        explanation = self._remove_repetitions(explanation)
        return explanation

    def _remove_repetitions(self, text):
        """반복되는 문단을 제거합니다"""
        lines = text.split('\n')
        unique_lines = []
        for line in lines:
            # 이미 2번 이상 나타난 줄은 건너뜁니다
            if line.strip() and unique_lines.count(line) < 2:
                unique_lines.append(line)
        return '\n'.join(unique_lines)


def main():
    # 코드 설명기 초기화
    try:
        explainer = CodeExplainer()
    except Exception as e:
        print(f"오류: {e}")
        sys.exit(1)
    # 코드 입력 받기
    print("설명할 코드를 직접 입력하세요 (입력 완료 후 Ctrl+D 또는 Ctrl+Z를 누르세요):")
    code_lines = []
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        pass
    code = '\n'.join(code_lines)
    if not code.strip():
        print("코드가 입력되지 않았습니다.")
        sys.exit(1)
    # 언어 입력 받기
    language = input("프로그래밍 언어를 입력하세요 (자동 감지하려면 Enter): ")
    if not language.strip():
        language = None
    # 코드 설명
    try:
        explanation = explainer.explain_code(code, language)
        print("\n=== 코드 설명 ===\n")
        print(explanation)
    except Exception as e:
        print(f"코드 설명 중 오류가 발생했습니다: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
