# templates/python_templates.py

# 기본 Python 파일 템플릿
BASIC_SCRIPT = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    # 여기에 메인 코드를 작성하세요
    pass

if __name__ == "__main__":
    main()
"""

# 클래스 템플릿
CLASS_TEMPLATE = """class ClassName:
    def __init__(self):
        # 초기화 코드
        pass

    def method_name(self):
        # 메서드 구현
        pass
"""

# 단위 테스트 템플릿
UNITTEST_TEMPLATE = """import unittest

class TestClassName(unittest.TestCase):
    def setUp(self):
        # 테스트 설정
        pass

    def test_method(self):
        # 테스트 로직
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
"""