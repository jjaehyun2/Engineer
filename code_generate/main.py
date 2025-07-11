# code_generate/main.py
import argparse
import sys
import os

# 상위 디렉토리를 모듈 경로에 추가 (임포트를 위해 필요)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from code_generate import CodeGenerator


def main():
    """코드 생성기 명령줄 인터페이스"""

    parser = argparse.ArgumentParser(description='코드 생성기 - AI를 활용한 코드 생성 도구')

    # 서브 파서 설정
    subparsers = parser.add_subparsers(dest='command', help='실행할 명령')

    # 코드 생성 명령
    gen_parser = subparsers.add_parser('generate', help='코드 생성')
    gen_parser.add_argument('requirements', help='코드 요구사항', nargs='+')
    gen_parser.add_argument('--lang', '-l', default='python', help='프로그래밍 언어 (기본: python)')
    gen_parser.add_argument('--comment-lang', '-c', default='korean', choices=['korean', 'english'],
                            help='주석 언어 (기본: korean)')
    gen_parser.add_argument('--output', '-o', help='출력 파일 경로')

    # 함수 생성 명령
    func_parser = subparsers.add_parser('function', help='함수 생성')
    func_parser.add_argument('description', help='함수 설명', nargs='+')
    func_parser.add_argument('--lang', '-l', default='python', help='프로그래밍 언어 (기본: python)')
    func_parser.add_argument('--params', '-p', nargs='+', help='함수 매개변수 (형식: 이름:설명)')
    func_parser.add_argument('--return', '-r', dest='return_desc', help='반환값 설명')
    func_parser.add_argument('--comment-lang', '-c', default='korean', choices=['korean', 'english'],
                             help='주석 언어 (기본: korean)')
    func_parser.add_argument('--output', '-o', help='출력 파일 경로')

    # 코드 개선 명령
    improve_parser = subparsers.add_parser('improve', help='코드 개선')
    improve_parser.add_argument('file', help='개선할 코드 파일')
    improve_parser.add_argument('--instructions', '-i', nargs='+', help='개선 지시사항')
    improve_parser.add_argument('--lang', '-l', help='프로그래밍 언어')
    improve_parser.add_argument('--comment-lang', '-c', default='korean', choices=['korean', 'english'],
                                help='주석 언어 (기본: korean)')
    improve_parser.add_argument('--output', '-o', help='출력 파일 경로')

    # 템플릿 기반 생성 명령
    template_parser = subparsers.add_parser('template', help='템플릿 기반 코드 생성')
    template_parser.add_argument('template_name', help='템플릿 이름 (예: BASIC_SCRIPT, CLASS_TEMPLATE)')
    template_parser.add_argument('--replacements', '-r', nargs='+', help='대체할 텍스트 (형식: 원본:대체)')
    template_parser.add_argument('--lang', '-l', default='python', help='프로그래밍 언어 (기본: python)')
    template_parser.add_argument('--output', '-o', help='출력 파일 경로')

    # 대화형 모드 명령
    interactive_parser = subparsers.add_parser('interactive', help='대화형 모드')

    # 모델 경로 옵션 (모든 명령에 공통)
    parser.add_argument('--model', '-m', help='사용할 모델 파일 경로')

    # 파싱
    args = parser.parse_args()

    # 모델 초기화
    try:
        generator = CodeGenerator(model_path=args.model)
    except Exception as e:
        print(f"모델 초기화 오류: {e}")
        return 1

    # 명령어 처리
    if args.command == 'generate':
        requirements = ' '.join(args.requirements)
        code = generator.generate_code(
            requirements=requirements,
            language=args.lang,
            comment_language=args.comment_lang
        )
        output_result(code, args.output)

    elif args.command == 'function':
        description = ' '.join(args.description)

        # 매개변수 처리
        params = {}
        if args.params:
            for param in args.params:
                if ':' in param:
                    name, desc = param.split(':', 1)
                    params[name.strip()] = desc.strip()
                else:
                    params[param.strip()] = ''

        code = generator.generate_function(
            function_description=description,
            language=args.lang,
            parameters=params,
            return_description=args.return_desc,
            comment_language=args.comment_lang
        )
        output_result(code, args.output)

    elif args.command == 'improve':
        # 파일에서 코드 읽기
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            print(f"파일 읽기 오류: {e}")
            return 1

        instructions = ' '.join(args.instructions) if args.instructions else None

        improved = generator.improve_code(
            code=code,
            instructions=instructions,
            language=args.lang,
            comment_language=args.comment_lang
        )
        output_result(improved, args.output)

    elif args.command == 'template':
        # 대체 텍스트 처리
        replacements = {}
        if args.replacements:
            for replacement in args.replacements:
                if ':' in replacement:
                    orig, repl = replacement.split(':', 1)
                    replacements[orig.strip()] = repl.strip()

        code = generator.generate_from_template(
            template_name=args.template_name,
            replacements=replacements,
            language=args.lang
        )
        output_result(code, args.output)

    elif args.command == 'interactive':
        run_interactive_mode(generator)

    else:
        parser.print_help()
        return 1

    return 0


def output_result(code, output_file=None):
    """결과를 출력하거나 파일에 저장"""
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"코드가 '{output_file}' 파일에 저장되었습니다.")
        except Exception as e:
            print(f"파일 쓰기 오류: {e}")
            print("\n생성된 코드:")
            print("=" * 80)
            print(code)
            print("=" * 80)
    else:
        print("\n생성된 코드:")
        print("=" * 80)
        print(code)
        print("=" * 80)


def run_interactive_mode(generator):
    """대화형 모드 실행"""
    print("코드 생성기 대화형 모드를 시작합니다. (종료하려면 'exit' 또는 'quit' 입력)")
    print("명령어 목록: generate, function, improve, template, help")

    while True:
        try:
            command = input("\n명령어 > ").strip().lower()

            if command in ('exit', 'quit'):
                print("대화형 모드를 종료합니다.")
                break

            elif command == 'generate':
                requirements = input("코드 요구사항 > ")
                language = input("프로그래밍 언어 (기본: python) > ") or "python"
                comment_lang = input("주석 언어 (korean/english, 기본: korean) > ") or "korean"

                code = generator.generate_code(
                    requirements=requirements,
                    language=language,
                    comment_language=comment_lang
                )
                print("\n생성된 코드:")
                print("=" * 80)
                print(code)
                print("=" * 80)

            elif command == 'function':
                description = input("함수 설명 > ")
                language = input("프로그래밍 언어 (기본: python) > ") or "python"

                # 매개변수 입력
                params = {}
                while True:
                    param = input("매개변수 (형식: 이름:설명, 완료시 빈 줄) > ")
                    if not param:
                        break
                    if ':' in param:
                        name, desc = param.split(':', 1)
                        params[name.strip()] = desc.strip()
                    else:
                        params[param.strip()] = ''

                return_desc = input("반환값 설명 > ")
                comment_lang = input("주석 언어 (korean/english, 기본: korean) > ") or "korean"

                code = generator.generate_function(
                    function_description=description,
                    language=language,
                    parameters=params,
                    return_description=return_desc,
                    comment_language=comment_lang
                )
                print("\n생성된 함수:")
                print("=" * 80)
                print(code)
                print("=" * 80)

            elif command == 'improve':
                print("개선할 코드를 입력하세요. (완료시 빈 줄에서 Ctrl+D 또는 Ctrl+Z)")
                code_lines = []
                while True:
                    try:
                        line = input()
                        code_lines.append(line)
                    except EOFError:
                        break
                code = '\n'.join(code_lines)

                if not code.strip():
                    print("코드가 입력되지 않았습니다.")
                    continue

                instructions = input("개선 지시사항 > ")
                language = input("프로그래밍 언어 (선택사항) > ")
                comment_lang = input("주석 언어 (korean/english, 기본: korean) > ") or "korean"

                improved = generator.improve_code(
                    code=code,
                    instructions=instructions if instructions else None,
                    language=language if language else None,
                    comment_language=comment_lang
                )
                print("\n개선된 코드:")
                print("=" * 80)
                print(improved)
                print("=" * 80)

            elif command == 'template':
                template_name = input("템플릿 이름 > ")
                language = input("프로그래밍 언어 (기본: python) > ") or "python"

                # 대체 텍스트 입력
                replacements = {}
                while True:
                    replacement = input("대체 텍스트 (형식: 원본:대체, 완료시 빈 줄) > ")
                    if not replacement:
                        break
                    if ':' in replacement:
                        orig, repl = replacement.split(':', 1)
                        replacements[orig.strip()] = repl.strip()

                code = generator.generate_from_template(
                    template_name=template_name,
                    replacements=replacements,
                    language=language
                )
                print("\n생성된 코드:")
                print("=" * 80)
                print(code)
                print("=" * 80)

            elif command == 'help':
                print("사용 가능한 명령어:")
                print("  generate  : 요구사항에 따라 코드 생성")
                print("  function  : 함수 생성")
                print("  improve   : 코드 개선")
                print("  template  : 템플릿 기반 코드 생성")
                print("  help      : 도움말 표시")
                print("  exit/quit : 종료")

            else:
                print(f"알 수 없는 명령어: {command}")
                print("사용 가능한 명령어: generate, function, improve, template, help, exit/quit")

        except KeyboardInterrupt:
            print("\n대화형 모드를 종료합니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")


if __name__ == "__main__":
    sys.exit(main())