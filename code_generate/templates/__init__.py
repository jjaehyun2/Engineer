# templates/__init__.py
from .python_templates import *
from .javascript_templates import *

__all__ = [
    # Python templates
    'BASIC_SCRIPT', 'CLASS_TEMPLATE', 'UNITTEST_TEMPLATE',

    # JavaScript templates
    'BASIC_SCRIPT', 'CLASS_TEMPLATE', 'REACT_FUNCTIONAL_COMPONENT',
    'REACT_CLASS_COMPONENT', 'NODE_MODULE', 'JEST_TEST_TEMPLATE',
    'ASYNC_FUNCTION'
]