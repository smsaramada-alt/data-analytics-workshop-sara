import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="TikTok Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 TikTok Performance Dashboard")
st.caption("Digital Marketing Analytics | Organic Content Performance")

# Load dataset
df = pd.read_csv("data/tiktok_performance.csv")

st.subheader("Dataset Preview")
st.write(f"Total posts: {len(df)}")

st.dataframe(df.head(10), use_container_width=True)
