import pandas as pd
import numpy as np
import io
import chardet
import streamlit as st

# 분석에 필요한 필수 컬럼 정의
REQUIRED_COLUMNS = ['접수일시', 'VOC유형대', '관리지사', '계약번호', '상호']

def load_voc_data(uploaded_file):
    """Loads and returns a pandas DataFrame from an uploaded CSV file."""
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            result = chardet.detect(bytes_data)
            encoding = result['encoding'] if result['encoding'] else 'utf-8'
            
            df = pd.read_csv(io.BytesIO(bytes_data), encoding=encoding)
            
            # 필수 컬럼 검증
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                st.error(f"⚠️ 필수 컬럼이 누락되었습니다: {', '.join(missing_cols)}")
                st.info("파일의 헤더(첫 줄) 이름을 확인해 주세요.")
                return None
                
            return df
        except Exception as e:
            raise Exception(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    return None

def preprocess_voc_data(df):
    """Preprocesses the VOC DataFrame with richer analysis features."""
    if df is None or df.empty:
        return None
    
    df = df.copy()
    
    # 1. Date & Time Processing
    if '접수일시' in df.columns:
        df['접수일시'] = pd.to_datetime(df['접수일시'], errors='coerce')
        df['월'] = df['접수일시'].dt.to_period('M').astype(str)
        df['일'] = df['접수일시'].dt.strftime('%Y-%m-%d')
        df['시간대'] = df['접수일시'].dt.hour
    
    # 2. Currency Cleaning
    if '월정료(VAT미포함)' in df.columns:
        df['월정료_숫자'] = df['월정료(VAT미포함)'].astype(str).str.replace(',', '').str.strip()
        df['월정료_숫자'] = pd.to_numeric(df['월정료_숫자'], errors='coerce').fillna(0)
    else:
        df['월정료_숫자'] = 0

    # 3. Rich Churn Categorization
    def categorize_churn_rich(row):
        text = str(row.get('등록내용', '')) + " " + str(row.get('VOC유형', ''))
        if '휴업' in text or '폐업' in text: return '휴/폐업'
        if '타사' in text or '경쟁' in text or '이동' in text: return '타사 이동'
        if '관리' in text or '불만' in text or '느림' in text or 'AS' in text: return '관리/품질 불만'
        if '가격' in text or '비싸' in text or '요금' in text: return '가격/혜택 불만'
        if '위약금' in text: return '위약금 문의'
        if '노후' in text or '낡아' in text or '교체' in text: return '시설 노후'
        if '단순' in text or '불필요' in text: return '단순 해지'
        return '기타/미분류'

    df['해지사유_상세'] = df.apply(categorize_churn_rich, axis=1)

    # 4. Data Formatting
    if '계약번호' in df.columns:
        df['계약번호'] = df['계약번호'].astype(str).str.replace('\.0$', '', regex=True)
    
    # 5. Service Grouping
    if '서비스소' in df.columns:
        df['서비스그룹'] = df['서비스소'].fillna('기타')
    else:
        df['서비스그룹'] = '알수없음'

    return df

def get_summary_metrics(df):
    """Calculates comprehensive metrics."""
    if df is None or df.empty:
        return {}
    
    haeji_df = df[df['VOC유형대'] == '해지'] if 'VOC유형대' in df.columns else pd.DataFrame()
    
    total_voc = len(df)
    churn_voc = len(haeji_df)
    revenue_at_risk = haeji_df['월정료_숫자'].sum()
    
    # Growth or Churn Ratio
    churn_ratio = (churn_voc / total_voc * 100) if total_voc > 0 else 0
    
    return {
        "total_voc": total_voc,
        "churn_voc": churn_voc,
        "revenue_at_risk": revenue_at_risk,
        "churn_ratio": churn_ratio,
        "top_branch": df['관리지사'].mode()[0] if '관리지사' in df.columns and not df['관리지사'].mode().empty else "N/A"
    }
