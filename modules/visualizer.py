import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def plot_histogram(df, col):
    fig, ax = plt.subplots()
    sns.histplot(df[col].dropna(), kde=True, ax=ax)
    st.pyplot(fig)


def plot_boxplot(df, col):
    fig, ax = plt.subplots()
    sns.boxplot(x=df[col], ax=ax)
    st.pyplot(fig)


def plot_pie_chart(df, col):
    fig, ax = plt.subplots()
    df[col].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_ylabel('')
    st.pyplot(fig)


def plot_scatter(df, col1, col2):
    fig, ax = plt.subplots()
    ax.scatter(df[col1], df[col2], alpha=0.6)
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    st.pyplot(fig)


def plot_bar_chart(df, col):
    fig, ax = plt.subplots()
    df[col].value_counts().plot(kind='bar', ax=ax)
    ax.set_title(f'Count of {col}')
    ax.set_ylabel('Count')
    st.pyplot(fig)
