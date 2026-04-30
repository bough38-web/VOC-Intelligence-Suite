import streamlit as st

def apply_custom_styles():
    """Applies a high-end, professional SaaS aesthetic."""
    st.markdown("""
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

        :root {
            --primary: #2563eb;
            --primary-glow: rgba(37, 99, 235, 0.4);
            --accent: #00f2ff;
            --bg-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }

        * {
            font-family: 'Pretendard', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at top right, #1e293b, #0f172a);
            color: var(--text-main);
        }

        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.8) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Metric Cards with Neon Glow */
        .metric-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .metric-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
        }
        .metric-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary);
            box-shadow: 0 8px 30px var(--primary-glow);
        }
        .metric-label {
            color: var(--text-dim);
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .metric-value {
            color: white;
            font-size: 2.2rem;
            font-weight: 800;
            margin-top: 0.5rem;
            text-shadow: 0 0 20px var(--primary-glow);
        }

        /* Styled Section Headers */
        .section-header {
            font-size: 1.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 2rem 0 1.5rem 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .section-header i {
            color: var(--accent);
            font-style: normal;
        }

        /* Glass Containers */
        .glass-container {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 2rem;
            margin-bottom: 2rem;
        }

        /* Custom Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            white-space: pre-wrap;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 12px 12px 0 0;
            color: var(--text-dim);
            font-weight: 600;
            border: none;
            padding: 0 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--primary) !important;
            color: white !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
        
        /* Hide default elements */
        #MainMenu, footer, header { visibility: hidden; }
        </style>
    """, unsafe_allow_html=True)
