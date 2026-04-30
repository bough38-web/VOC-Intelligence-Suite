#!/bin/bash

echo "🚀 Data Intel PRO VOC 대시보드를 시작합니다..."

# 1. 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "📦 가상환경을 생성하는 중입니다 (최초 1회)..."
    python3 -m venv venv
fi

# 2. 가상환경 활성화
source venv/bin/activate

# 3. 필수 라이브러리 설치 (인터넷 연결 필요)
echo "📥 필수 라이브러리를 확인 및 설치 중입니다..."
pip install --quiet streamlit pandas plotly chardet openpyxl

# 4. 앱 실행
echo "✨ 대시보드를 실행합니다. 잠시만 기다려 주세요..."
streamlit run app/main.py
