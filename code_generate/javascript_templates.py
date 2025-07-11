# templates/javascript_templates.py

# 기본 JavaScript 파일 템플릿
BASIC_SCRIPT = """'use strict';

function main() {
    // 여기에 메인 코드를 작성하세요
}

main();
"""

# 클래스 템플릿 (ES6)
CLASS_TEMPLATE = """class ClassName {
    constructor() {
        // 초기화 코드
    }

    methodName() {
        // 메서드 구현
    }
}
"""

# 함수형 컴포넌트 템플릿 (React)
REACT_FUNCTIONAL_COMPONENT = """import React from 'react';

function ComponentName(props) {
    return (
        <div>
            {/* 컴포넌트 내용 */}
        </div>
    );
}

export default ComponentName;
"""

# 클래스 컴포넌트 템플릿 (React)
REACT_CLASS_COMPONENT = """import React, { Component } from 'react';

class ComponentName extends Component {
    constructor(props) {
        super(props);
        this.state = {
            // 초기 상태
        };
    }

    render() {
        return (
            <div>
                {/* 컴포넌트 내용 */}
            </div>
        );
    }
}

export default ComponentName;
"""

# Node.js 모듈 템플릿
NODE_MODULE = """'use strict';

/**
 * 모듈 설명
 * @module ModuleName
 */

/**
 * 함수 설명
 * @param {type} paramName - 파라미터 설명
 * @returns {type} 반환값 설명
 */
function functionName(paramName) {
    // 함수 구현
}

module.exports = {
    functionName
};
"""

# 테스트 템플릿 (Jest)
JEST_TEST_TEMPLATE = """const moduleToTest = require('./moduleToTest');

describe('Module test suite', () => {
    test('should do something', () => {
        // 테스트 로직
        expect(true).toBe(true);
    });
});
"""

# 비동기 함수 템플릿
ASYNC_FUNCTION = """async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching ', error);
        throw error;
    }
}
"""