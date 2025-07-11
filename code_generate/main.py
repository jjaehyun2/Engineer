import sys
import os
import argparse
from pathlib import Path

# 프로젝트 루트 디렉토리를 파이썬 경로에 추가
sys.path.append(str(Path(__file__).resolve().parent.parent))

from code_generate.code_generator import CodeGenerator

def main():
    parser = argparse.ArgumentParser(description="코드 생성 도구")
    parser.add_argument("--file", "-f", help="요구사항이 작성된 파일 경로")
    parser.add_argument("--output", "-o", help="생성된 코드를 저장할 파일 경로")
    parser.add_argument("--language", "-l", help="생성할 코드 언어 (예: python, javascript)")
    parser.add_argument("--model", "-m", default="qwen2.5-coder", help="사용할 모델 이름 (기본값: qwen2.5-coder)")
    parser.add_argument("--url", default="http://localhost:11434", help="Ollama API URL (기본값: http://localhost:11434)")
    
    args = parser.parse_args()
    
    model_name = args.model
    ollama_url = args.url
    language = args.language
    
    generator = CodeGenerator(model_name=model_name, ollama_base_url=ollama_url)
    
    # 파일에서 요구사항을 읽는 경우
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                prompt = f.read()
                
            print(f"파일에서 요구사항을 읽었습니다: {args.file}")
            print("\n코드 생성 중...\n")
            
            generated_code = generator.generate_code(prompt, language)
            
            print("\n" + "="*50 + "\n")
            print(generated_code)
            print("\n" + "="*50)
            
            # 결과를 파일에 저장
            if args.output:
                try:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        # 코드 블록 마크다운 제거하고 저장
                        code_content = generated_code
                        if "```" in generated_code:
                            code_blocks = generated_code.split("```")
                            if len(code_blocks) >= 3:
                                # 첫 번째 코드 블록 내용만 추출
                                code_content = code_blocks[1]
                                if code_content.startswith(language or ""):
                                    # 언어 표시 제거 (```python 등)
                                    code_content = code_content.split("\n", 1)[1] if "\n" in code_content else ""
                        
                        f.write(code_content)
                    print(f"\n생성된 코드를 '{args.output}' 파일에 저장했습니다.")
                except Exception as e:
                    print(f"파일 저장 중 오류 발생: {str(e)}")
                
        except Exception as e:
            print(f"오류 발생: {str(e)}")
            return 1
    else:
        # 대화형 모드
        print("코드 생성 도구를 시작합니다. 종료하려면 'exit' 또는 'quit'를 입력하세요.")
        
        while True:
            print("\n요구사항을 입력하세요 (종료: exit 또는 quit):")
            prompt_lines = []
            
            # 첫 번째 줄 읽기
            try:
                first_line = input()
                if first_line.lower() in ['exit', 'quit']:
                    break
                    
                prompt_lines.append(first_line)
                
                # 나머지 요구사항 읽기
                while True:
                    line = input()
                    if not line:  # 빈 줄이면 입력 종료
                        break
                    prompt_lines.append(line)
                    
            except EOFError:
                pass  # Ctrl+D 또는 Ctrl+Z로 입력 종료
                
            prompt = "\n".join(prompt_lines)
            if not prompt.strip():
                continue
                
            # 언어 확인
            if not language:
                try:
                    language_input = input("생성할 코드의 언어를 입력하세요 (예: python, javascript, 생략 가능): ")
                    language = language_input.strip() if language_input.strip() else None
                except EOFError:
                    language = None
                    
            print("\n코드 생성 중...\n")
            generated_code = generator.generate_code(prompt, language)
            
            print("\n" + "="*50 + "\n")
            print(generated_code)
            print("\n" + "="*50)
            
            # 언어 리셋 (다음 요청을 위해)
            language = args.language
    
    return 0

if __name__ == "__main__":
    sys.exit(main())