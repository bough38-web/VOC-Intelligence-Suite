import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ensure the app directory is in the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from core.handlers import load_voc_data, preprocess_voc_data, get_summary_metrics
from ui.styles import apply_custom_styles
from ui.components import styled_header, metric_card, glass_container_start, glass_container_end

# Page Config
st.set_page_config(
    page_title="Data Intel PRO | Enterprise VOC Intelligence",
    page_icon="💎",
    layout="wide"
)

apply_custom_styles()

df = None

# Sidebar Content
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h1 style='color: #00f2ff; font-size: 1.5rem; font-weight: 900;'>DATA INTEL PRO</h1>
            <p style='color: #94a3b8; font-size: 0.8rem;'>Enterprise Intelligence System</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    sidebar_file = st.file_uploader("VOC 데이터 업로드 (.csv)", type=["csv"], key="sidebar_up")
    if sidebar_file:
        raw_df = load_voc_data(sidebar_file)
        if raw_df is not None:
            df = preprocess_voc_data(raw_df)

# Logic for Empty State
if df is None:
    st.markdown("""
        <div style='text-align: center; padding: 80px 0 20px 0;'>
            <h1 style='font-size: 4rem; font-weight: 900; margin-bottom: 10px;'>VOC Intelligence</h1>
            <p style='font-size: 1.4rem; color: #94a3b8; margin-bottom: 40px;'>시계열 분석 및 해지 방어 최적화 솔루션</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        main_file = st.file_uploader("분석할 VOC 파일을 드래그하여 놓으세요", type=["csv"], key="main_up")
        if main_file:
            raw_df = load_voc_data(main_file)
            if raw_df is not None:
                df = preprocess_voc_data(raw_df)
                if df is not None:
                    st.rerun() # 즉시 대시보드 전환
    
    # Features Section
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        glass_container_start()
        st.markdown("### 📈 시계열 트렌드")
        st.write("월별/일별 VOC 발생 추이를 한눈에 파악하고 미래 수요를 예측합니다.")
        glass_container_end()
    with col2:
        glass_container_start()
        st.markdown("### 🏢 조직 성과 분석")
        st.write("지사별, 담당자별 처리 현황을 분석하여 운영 효율성을 극대화합니다.")
        glass_container_end()
    with col3:
        glass_container_start()
        st.markdown("### ⚠️ 리스크 관리")
        st.write("해지 사유를 자동 분류하고 고위험 고객을 식별하여 선제적으로 대응합니다.")
        glass_container_end()
    
    if df is None:
        st.stop()

# Filter Logic (Sidebar)
with st.sidebar:
    st.markdown("### 🔍 상세 필터")
    if '관리지사' in df.columns:
        branches = ["전체 지사"] + sorted(df['관리지사'].dropna().unique().tolist())
        sel_branch = st.selectbox("지사 필터", branches)
        if sel_branch != "전체 지사":
            df = df[df['관리지사'] == sel_branch]
    
    if '서비스그룹' in df.columns:
        services = ["전체 서비스"] + sorted(df['서비스그룹'].dropna().unique().tolist())
        sel_service = st.selectbox("서비스 필터", services)
        if sel_service != "전체 서비스":
            df = df[df['서비스그룹'] == sel_service]

# Main Dashboard Content
metrics = get_summary_metrics(df)
styled_header("인텔리전스 개요", "💎")

m1, m2, m3, m4 = st.columns(4)
with m1: metric_card("전체 분석 건수", f"{metrics['total_voc']:,}")
with m2: metric_card("해지 요청 건수", f"{metrics['churn_voc']:,}")
with m3: metric_card("위험 노출 매출", f"₩{metrics['revenue_at_risk']:,.0f}")
with m4: metric_card("해지 전환율", f"{metrics['churn_ratio']:.1f}%")

# Tabs
tabs = st.tabs(["📊 트렌드 분석", "🛡️ 해지 위험 분석", "🏢 조직/담당자 성과", "🔍 데이터 인사이트"])

with tabs[0]:
    styled_header("VOC 시계열 추이", "📈")
    glass_container_start()
    trend_data = df.groupby('월').size().reset_index(name='건수')
    fig_trend = px.area(trend_data, x='월', y='건수', 
                       title="월별 VOC 발생 트렌드",
                       color_discrete_sequence=['#2563eb'],
                       template="plotly_dark")
    fig_trend.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                           xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'))
    st.plotly_chart(fig_trend, use_container_width=True)
    glass_container_end()

with tabs[1]:
    col1, col2 = st.columns([1, 1])
    haeji_df = df[df['VOC유형대'] == '해지'] if 'VOC유형대' in df.columns else pd.DataFrame()
    
    with col1:
        styled_header("핵심 해지 사유", "⚠️")
        if not haeji_df.empty:
            reason_data = haeji_df['해지사유_상세'].value_counts().reset_index()
            reason_data.columns = ['사유', '건수']
            fig_reason = px.bar(reason_data, x='건수', y='사유', orientation='h',
                               color='건수', color_continuous_scale='Reds',
                               template="plotly_dark")
            fig_reason.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_reason, use_container_width=True)
        else:
            st.info("해지 관련 데이터가 없습니다.")
        
    with col2:
        styled_header("서비스별 해지 분포", "📦")
        if not haeji_df.empty:
            svc_data = haeji_df['서비스그룹'].value_counts().reset_index()
            svc_data.columns = ['서비스', '건수']
            fig_svc = px.pie(svc_data.head(8), values='건수', names='서비스', 
                            hole=0.5, template="plotly_dark")
            fig_svc.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_svc, use_container_width=True)
        else:
            st.info("해지 관련 데이터가 없습니다.")

    styled_header("고액 해지 위험 리스트 (Top 20)", "🚩")
    if not haeji_df.empty:
        st.dataframe(haeji_df.sort_values('월정료_숫자', ascending=False).head(20)[['접수일시', '상호', '서비스그룹', '월정료(VAT미포함)', '해지사유_상세', '처리자']], use_container_width=True)
    else:
        st.info("표시할 위험 리스트가 없습니다.")

with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        styled_header("지사별 리텐션 퍼포먼스", "🏢")
        branch_data = df['관리지사'].value_counts().reset_index().head(10)
        branch_data.columns = ['지사', 'VOC수']
        fig_branch = px.bar(branch_data, x='지사', y='VOC수', color='VOC수', color_continuous_scale='GnBu')
        st.plotly_chart(fig_branch, use_container_width=True)
    with c2:
        styled_header("담당자별 처리량 TOP 10", "🏆")
        leaderboard = df['처리자'].value_counts().reset_index().head(10)
        leaderboard.columns = ['담당자', '처리건수']
        st.table(leaderboard)

with tabs[3]:
    styled_header("심층 데이터 탐색", "🧪")
    glass_container_start()
    st.markdown("### 데이터 상관 관계 및 분포")
    if not df.empty:
        st.write(df.describe())
        st.markdown("---")
        st.markdown("### 원본 데이터 (Raw Data)")
        st.dataframe(df, use_container_width=True)
    glass_container_end()
