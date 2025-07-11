import os
from dotenv import load_dotenv

def load_environment():
    """환경 변수를 로드합니다."""
    # 프로젝트 루트 디렉토리 경로
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(root_dir, '.env')
    # .env 파일이 존재하면 로드
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print(".env 파일을 로드했습니다.")
    else:
        print(".env 파일을 찾을 수 없습니다. 환경 변수가 이미 설정되어 있는지 확인하세요.")
