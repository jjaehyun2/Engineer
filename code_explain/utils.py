# utils.py
import os
from dotenv import load_dotenv

def load_environment():
    """환경 변수를 로드합니다."""
    load_dotenv()
    # 로컬 모델을 사용하므로 API 키는 필요 없지만,
    # 다른 환경 변수가 필요하면 여기서 로드
    return None

def read_code_file(file_path):
    """파일에서 코드를 읽습니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return None

def identify_language(file_path):
    """파일 확장자를 기반으로 프로그래밍 언어를 식별합니다."""
    extension = os.path.splitext(file_path)[1].lower()
    language_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.go': 'Go',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.ts': 'TypeScript'
        # 필요에 따라 더 추가할 수 있습니다
    }
    return language_map.get(extension, '알 수 없음')