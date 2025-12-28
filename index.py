# app.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Beautiful Data Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.header("Upload Your CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

st.sidebar.markdown("---")
st.sidebar.header("Settings")
show_data = st.sidebar.checkbox("Show raw data", value=True)
num_rows = st.sidebar.slider("Number of rows to view", min_value=5, max_value=50, value=10)

st.title("📊 Beautiful Data Explorer")
st.markdown("This is an interactive app to explore your dataset with beautiful charts.")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Dataset Overview")
    st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    if show_data:
        st.dataframe(df.head(num_rows))
    
    st.subheader("Interactive Plots")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Please upload a dataset with at least 2 numeric columns for plotting.")
    else:
        x_axis = st.selectbox("X-axis", numeric_cols)
        y_axis = st.selectbox("Y-axis", numeric_cols, index=1)
        color_col = st.selectbox("Color by (optional)", [None] + numeric_cols)
        
        # --- Create Altair chart ---
        chart = alt.Chart(df).mark_circle(size=60).encode(
            x=x_axis,
            y=y_axis,
            color=color_col if color_col != None else alt.value("steelblue"),
            tooltip=numeric_cols
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
else:
    st.info("Upload a CSV file to get started.")

# --- FOOTER ---
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")
