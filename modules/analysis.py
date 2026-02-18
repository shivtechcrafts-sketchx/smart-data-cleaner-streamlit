def get_summary(df):
    summary = df.describe(include="all")
    # Convert all columns to string to ensure Streamlit/PyArrow compatibility
    for col in summary.columns:
        if summary[col].dtype == 'object':
            summary[col] = summary[col].astype(str)
    return summary


def value_counts(df, col):
    return df[col].value_counts()
