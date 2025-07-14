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
    
    if args.file:
        file_path = args.file
        try:
            if not os.path.exists(file_path):
                print(f"can't find file: {file_path}")
                return 1
                
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                
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
            
            explanation = explainer.explain_code(code, language)
            
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
        print("Starting the code explanation. Type 'exit' or 'quit' to exit.")
        
    while True:
        print("\nEnter your code (end input with an empty line, or type 'exit' or 'quit' to exit):")
        code_lines = []
        try:
            first_line = input()
            if first_line.strip().lower() in ['exit', 'quit']:
                print("Exiting the code explanation tool.")
                return 0
            code_lines.append(first_line)
            while True:
                line = input()
                if line.strip().lower() in ['exit', 'quit']:
                    print("Exiting the code explanation.")
                    return 0
                if line == "":
                    break
                code_lines.append(line)
        except EOFError:
            break

        code = "\n".join(code_lines).strip()
        if not code:
            continue

        print("\n analyzing code...\n")
        explanation = explainer.explain_code(code)
        print("\n" + "="*50 + "\n")
        print(explanation)
        print("\n" + "="*50)

    return 0

if __name__ == "__main__":
    sys.exit(main())
