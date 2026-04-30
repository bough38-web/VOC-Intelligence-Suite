import streamlit as st

def styled_header(title, icon="📊"):
    """Renders a styled header with an icon."""
    st.markdown(f"""
        <div class="section-header">
            <span>{icon}</span> {title}
        </div>
    """, unsafe_allow_html=True)

def metric_card(label, value, prefix="", suffix=""):
    """Renders a premium metric card."""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{prefix}{value}{suffix}</div>
        </div>
    """, unsafe_allow_html=True)

def glass_container_start():
    """Starts a glassmorphism container."""
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)

def glass_container_end():
    """Ends a glassmorphism container."""
    st.markdown('</div>', unsafe_allow_html=True)
