import os
import sys
import argparse
from pathlib import Path

# 프로젝트 루트 디렉토리를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from code_explain.code_explainer import CodeExplainer

def main():
    parser = argparse.ArgumentParser(description="코드 설명 도구")
    parser.add_argument("file", nargs="?", help="설명할 코드가 담긴 파일 경로")
    parser.add_argument("--model", "-m", default="qwen2.5-coder", help="사용할 모델 이름 (기본값: qwen2.5-coder)")
    parser.add_argument("--url", default="http://localhost:11434", help="Ollama API URL (기본값: http://localhost:11434)")
    
    args = parser.parse_args()
    
    model_name = args.model
    ollama_url = args.url

    explainer = CodeExplainer(model_name=model_name, ollama_base_url=ollama_url)
    
    # 파일 경로가 제공된 경우
    if args.file:
        file_path = args.file
        try:
            # 파일이 존재하는지 확인
            if not os.path.exists(file_path):
                print(f"can't find file: {file_path}")
                return 1
                
            # 파일에서 코드 읽기
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                
            # 파일 확장자에서 언어 추측
            extension = os.path.splitext(file_path)[1].lower()
            language_map = {
                '.py': 'Python',
                '.js': 'JavaScript',
                '.java': 'Java',
                '.cpp': 'C++',
                '.c': 'C',
                '.go': 'Go',
                '.rs': 'Rust',
                '.ts': 'TypeScript',
                '.php': 'PHP',
                '.rb': 'Ruby',
                '.cs': 'C#',
                '.swift': 'Swift',
                '.kt': 'Kotlin',
            }
            language = language_map.get(extension)
            
            # 코드 설명 생성
            explanation = explainer.explain_code(code, language)
            
            # 결과 출력
            print("\n" + "="*50 + "\n")
            print(f"file: {file_path}")
            print(f"language: {language if language else 'auto-detected'}")
            print("\n" + "="*50 + "\n")
            print(explanation)
            print("\n" + "="*50)
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 1
    else:
        # 대화형 모드
        print("Starting the code explanation tool. Type 'exit' or 'quit' to exit.")
        print("Enter your code and press Enter on an empty line, then Ctrl+D (Unix) or Ctrl+Z (Windows) to generate an explanation.")
        
        while True:
            print("\nEnter your code (type 'exit' or 'quit' to exit):")
            code_lines = []
            
            try:
                while True:
                    line = input()
                    # 종료 조건 추가: 줄 중간에 exit 또는 quit 입력 시 종료
                    if line.strip().lower() in ['exit', 'quit']:
                        print("Exiting the code explanation tool.")
                        return 0
                    if line == "":
                        # 빈 줄이면 입력 종료
                        break
                    code_lines.append(line)
            except EOFError:
                # Ctrl+D (Unix), Ctrl+Z (Windows) 입력 시 종료
                pass  
            
            code = "\n".join(code_lines)
            if not code.strip():
                continue
                
            print("\n analyzing code...\n")
            explanation = explainer.explain_code(code)
            
            print("\n" + "="*50 + "\n")
            print(explanation)
            print("\n" + "="*50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
