import streamlit as st
import pandas as pd

from modules.loader import load_data
from modules.cleaner import fill_null_values, drop_null_rows, drop_null_columns
from modules.filters import apply_numeric_filter, apply_category_filter
from modules.analysis import get_summary, value_counts
from modules.visualizer import plot_histogram, plot_boxplot, plot_pie_chart, plot_scatter, plot_bar_chart
from utils.helpers import dataset_info, missing_value_report, fix_streamlit_types

# =========================
# PREMIUM UI CSS
# =========================
def load_css():
    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg,#0f172a,#1e293b);
        color:white;
    }

    [data-testid="stSidebar"] {
        background:#111827;
    }

    .card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(8px);
        border-radius:16px;
        padding:20px;
        margin-bottom:20px;
        box-shadow:0 4px 20px rgba(0,0,0,0.25);
    }

    .stButton>button {
        background: linear-gradient(90deg,#38bdf8,#0ea5e9);
        color:white;
        border:none;
        border-radius:10px;
        font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)

load_css()

# =========================
# HEADER
# =========================
st.markdown("""
<h1 style='text-align:center;'>🧹 Smart Data Cleaner</h1>
<p style='text-align:center;color:#94a3b8;'>
Clean • Analyze • Transform • Download
</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload CSV / Excel", type=["csv","xlsx"])

if uploaded_file:

    df = load_data(uploaded_file)

    # FIX ARROW ERROR
    df = fix_streamlit_types(df)

    # ===== DATASET INFO =====
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Dataset Info")
    st.write(dataset_info(df))
    st.dataframe(fix_streamlit_types(df).head())
    st.markdown('</div>', unsafe_allow_html=True)

    # ===== MISSING VALUES =====
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("❗ Missing Values Report")
    st.dataframe(missing_value_report(df))
    st.markdown('</div>', unsafe_allow_html=True)

    # ===== CLEANING =====
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧠 Null Value Cleaning")

    col = st.selectbox("Select Column", df.columns)
    method = st.selectbox("Method",
                          ["Mean","Median","Mode","Forward Fill","Backward Fill","Constant"])

    constant = None
    if method == "Constant":
        constant = st.text_input("Constant Value")

    if st.button("Apply Cleaning"):
        df = fill_null_values(df, col, method, constant)
        st.success("Cleaning Applied")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Drop Null Rows"):
            df = drop_null_rows(df)
    with c2:
        if st.button("Drop Null Columns"):
            df = drop_null_columns(df)

    st.markdown('</div>', unsafe_allow_html=True)

    # ===== FILTER =====
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔎 Filter Data")

    num_cols = df.select_dtypes(include=["number"]).columns

    if len(num_cols) > 0:
        fcol = st.selectbox("Numeric Column", num_cols)
        minv, maxv = float(df[fcol].min()), float(df[fcol].max())

        rng = st.slider("Range", minv, maxv, (minv,maxv))
        df = apply_numeric_filter(df, fcol, rng[0], rng[1])

    st.dataframe(fix_streamlit_types(df).head())
    st.markdown('</div>', unsafe_allow_html=True)

    # ===== SUMMARY =====
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Summary")
    st.dataframe(fix_streamlit_types(get_summary(df)))
    st.markdown('</div>', unsafe_allow_html=True)

    # ===== VISUALIZATION =====
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Visualizations")

    # Get numeric and categorical columns
    num_cols = df.select_dtypes(include=["number"]).columns
    cat_cols = df.select_dtypes(include=["object"]).columns

    # Create tabs for different visualization types
    tab1, tab2, tab3 = st.tabs(["📈 Histogram & Boxplot", "🥧 Categorical Charts", "📍 Scatter Plot"])
    
    with tab1:
        if len(num_cols) > 0:
            vcol = st.selectbox("Select Numeric Column", num_cols, key="hist_box")
            col_left, col_right = st.columns(2)
            with col_left:
                st.write("**Histogram**")
                plot_histogram(df, vcol)
            with col_right:
                st.write("**Boxplot**")
                plot_boxplot(df, vcol)
    
    with tab2:
        if len(cat_cols) > 0:
            cat_col = st.selectbox("Select Categorical Column", cat_cols)
            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Pie Chart"])
            if chart_type == "Bar Chart":
                plot_bar_chart(df, cat_col)
            else:
                plot_pie_chart(df, cat_col)
        else:
            st.info("No categorical columns available")
    
    with tab3:
        if len(num_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                scatter_col1 = st.selectbox("X-axis", num_cols, key="scatter_x")
            with col2:
                scatter_col2 = st.selectbox("Y-axis", num_cols, key="scatter_y")
            plot_scatter(df, scatter_col1, scatter_col2)
        else:
            st.info("Need at least 2 numeric columns for scatter plot")

    st.markdown('</div>', unsafe_allow_html=True)

    # ===== DOWNLOAD =====
    st.download_button(
        "⬇️ Download Cleaned CSV",
        df.to_csv(index=False).encode("utf-8"),
        "cleaned_data.csv"
    )
