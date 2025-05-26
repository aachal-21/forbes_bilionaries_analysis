# This code is intended to be run in an environment where Streamlit is installed.
# Ensure you have streamlit installed by running: pip install streamlit

try:
    import streamlit as st
except ModuleNotFoundError:
    raise ModuleNotFoundError("Streamlit is not installed. Please run `pip install streamlit` to use this app.")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Forbes Billionaires 2022 Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload the Forbes Billionaires CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.dataframe(df.head())

    # Cleaning
    df['networth'] = df['networth'].replace('[$B]', '', regex=True).astype('float64')

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    st.subheader("Net Worth Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean", f"${df.networth.mean():.2f}B")
    col2.metric("Median", f"${df.networth.median():.2f}B")
    col3.metric("Min", f"${df.networth.min():.2f}B")
    col4.metric("Max", f"${df.networth.max():.2f}B")

    st.subheader("Net Worth Distribution")
    fig1, ax1 = plt.subplots()
    sns.histplot(df['networth'], kde=True, ax=ax1)
    st.pyplot(fig1)

    st.subheader("Net Worth Boxplot")
    fig2, ax2 = plt.subplots()
    sns.boxplot(x=df['networth'], ax=ax2)
    st.pyplot(fig2)

    st.subheader("Top 10 Richest Billionaires")
    top_10 = df.groupby('name')['networth'].sum().nlargest(10)
    st.bar_chart(top_10)

    st.subheader("Billionaires by Country")
    country_counts = df['country'].value_counts()
    st.bar_chart(country_counts.head(20))

    st.subheader("Net Worth by Country")
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.stripplot(x='country', y='networth', data=df, ax=ax3)
    plt.xticks(rotation=90)
    st.pyplot(fig3)

    st.subheader("Industry Distribution")
    industry_counts = df['industry'].value_counts()
    st.bar_chart(industry_counts.head(20))

    st.subheader("Average Net Worth by Industry")
    industry_avg = df.groupby('industry')['networth'].mean().nlargest(10)
    st.bar_chart(industry_avg)

    st.subheader("Age Analysis")
    col5, col6 = st.columns(2)
    col5.metric("Average Age", f"{df.age.mean():.2f} years")
    col6.metric("Median Age", f"{df.age.median():.2f} years")

    st.subheader("Oldest Billionaire")
    st.write(df.loc[df['age'].idxmax()][['name', 'age', 'networth']])

    st.subheader("Youngest Billionaire")
    st.write(df.loc[df['age'].idxmin()][['name', 'age', 'networth']])

else:
    st.info("Please upload a CSV file to begin analysis.")
