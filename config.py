"""
프로젝트 전역 설정
"""

# Ollama 설정
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5-coder"  # 기본 모델 설정

# 요청 설정
REQUEST_TIMEOUT = 60  # 초 단위

# 로깅 설정
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL 중 선택
