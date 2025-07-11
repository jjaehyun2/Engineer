# code_explain/main.py
import argparse
import sys
from .code_explainer import CodeExplainer


def main():
    # 명령줄 인수 파싱
    parser = argparse.ArgumentParser(description='코드 설명 도구')
    parser.add_argument('--model', '-m', help='사용할 모델 파일 경로')
    parser.add_argument('--detail', '-d', choices=['low', 'medium', 'high'],
                        default='medium', help='설명의 상세 수준 (기본: medium)')
    args = parser.parse_args()

    # 코드 설명기 초기화
    try:
        explainer = CodeExplainer(model_path=args.model)
    except Exception as e:
        print(f"오류: {e}")
        sys.exit(1)

    # 코드 입력 받기
    print("설명할 코드를 직접 입력하세요 (입력 완료 후 새 줄에 'END' 를 입력하세요):")
    code_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        code_lines.append(line)

    code = '\n'.join(code_lines)

    if not code.strip():
        print("코드가 입력되지 않았습니다.")
        sys.exit(1)

    # 언어 입력 받기
    language = input("프로그래밍 언어를 입력하세요 (자동 감지하려면 Enter): ")
    if not language.strip():
        language = None

    # 코드 설명 - detail 인수 제거 (또는 CodeExplainer 클래스 수정)
    try:
        explanation = explainer.explain_code(code, language)  # args.detail 인수 제거
        print("\n=== 코드 설명 ===\n")
        print(explanation)
    except Exception as e:
        print(f"코드 설명 중 오류가 발생했습니다: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()