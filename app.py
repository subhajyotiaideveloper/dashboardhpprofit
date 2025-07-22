import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="HP Profitability Dashboard", layout="wide")

st.title("HP Profitability Dashboard")

# Load and clean CSV
def load_data():
    # Skip first two rows, use third row as header
    df = pd.read_csv("HP-Profitablility-_TWR-_-AIO_.csv", header=2)
    # Clean column names
    df.columns = df.columns.str.strip()
    # Remove unnamed columns and empty columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='all')
    return df

df = load_data()

# Debug: Show actual columns
st.sidebar.write("Loaded columns:", list(df.columns))

# Sidebar filters
if 'CAT' in df.columns:
    cat_options = df['CAT'].dropna().unique()
    selected_cat = st.sidebar.multiselect('Select Category', cat_options, default=cat_options)
    filtered_df = df[df['CAT'].isin(selected_cat)]
else:
    st.error("'CAT' column not found. Please check the CSV structure.")
    filtered_df = df

st.subheader("Summary Table")
st.dataframe(filtered_df)

# Show key metrics (example: total NDP, average targets)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total NDP", filtered_df['NDP'].replace({',':'', ' ':'', '₹':''}, regex=True).astype(float).sum())
with col2:
    st.metric("Avg. 0.6% ON ACH 100% Month Target", filtered_df['0.6% ON ACH 100% Month Target'].replace({',':'', ' ':'', '₹':''}, regex=True).astype(float).mean())
with col3:
    st.metric("Avg. RD CPC PGM", filtered_df['RD CPC PGM (AIO-0.3%, TWR-2.8%)'].replace({',':'', ' ':'', '₹':''}, regex=True).astype(float).mean())

# Bar chart: NDP by Model
st.subheader("NDP by Model")
chart_df = filtered_df.copy()
chart_df['NDP'] = chart_df['NDP'].replace({',':'', ' ':'', '₹':''}, regex=True).astype(float)
st.bar_chart(chart_df.set_index('Model')['NDP'])

# Download button
st.download_button('Download filtered data as CSV', chart_df.to_csv(index=False), 'filtered_data.csv', 'text/csv')
