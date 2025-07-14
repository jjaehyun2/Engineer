import sys
import os
import argparse
from pathlib import Path

# Add project root directory to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from code_generate.code_generator import CodeGenerator

def main():
    parser = argparse.ArgumentParser(description="Code Generation Tool")
    parser.add_argument("--file", "-f", help="Path to the requirements file")
    parser.add_argument("--output", "-o", help="Path to save the generated code")
    parser.add_argument("--language", "-l", help="Programming language to generate (e.g., python, javascript)")
    parser.add_argument("--model", "-m", default="qwen2.5-coder", help="Model name to use (default: qwen2.5-coder)")
    parser.add_argument("--url", default="http://localhost:11434", help="Ollama API URL (default: http://localhost:11434)")
    
    args = parser.parse_args()
    
    model_name = args.model
    ollama_url = args.url
    language = args.language
    
    generator = CodeGenerator(model_name=model_name, ollama_base_url=ollama_url)
    
    # If reading requirements from a file
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                prompt = f.read()
                
            print(f"Read requirements from file: {args.file}")
            print("\nGenerating code...\n")
            
            generated_code = generator.generate_code(prompt, language)
            
            print("\n" + "="*50 + "\n")
            print(generated_code)
            print("\n" + "="*50)
            
            # Save result to file
            if args.output:
                try:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        code_content = generated_code
                        if "```" in generated_code:
                            code_blocks = generated_code.split("```")
                            if len(code_blocks) >= 3:
                                code_content = code_blocks[1]
                                if code_content.startswith(language or ""):
                                    code_content = code_content.split("\n", 1)[1] if "\n" in code_content else ""
                        
                        f.write(code_content)
                    print(f"\nGenerated code saved to '{args.output}'.")
                except Exception as e:
                    print(f"Error while saving file: {str(e)}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return 1
    else:
        print("Starting code generation tool. Type 'exit' or 'quit' to exit.")
        
        while True:
            print("\nEnter your requirements (end input with an empty line, or type 'exit' or 'quit' to exit):")
            code_lines = []

            try:
                first_line = input()
                if first_line.lower() in ['exit', 'quit']:
                    print("Exiting the code generation tool.")
                    break
                code_lines.append(first_line)
                
                while True:
                    line = input()
                    if not line:  
                        break
                    code_lines.append(line)
                    
            except EOFError:
                pass  
                
            prompt = "\n".join(code_lines)
            if not prompt.strip():
                continue
                

            if not language:
                try:
                    language_input = input("Enter the programming language to generate (e.g., python, javascript, optional): ")
                    language = language_input.strip() if language_input.strip() else None
                except EOFError:
                    language = None
                    
            print("\nGenerating code...\n")
            generated_code = generator.generate_code(prompt, language)
            
            print("\n" + "="*50 + "\n")
            print(generated_code)
            print("\n" + "="*50)
            
            language = args.language
    
    return 0

if __name__ == "__main__":
    sys.exit(main())