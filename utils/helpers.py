import pandas as pd

def dataset_info(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Memory (MB)": round(df.memory_usage().sum()/1024**2, 2)
    }


def missing_value_report(df):
    report = df.isnull().sum().reset_index()
    report.columns = ["Column", "Missing Values"]
    report["Percentage"] = (report["Missing Values"] / len(df)) * 100
    report = report.sort_values("Missing Values", ascending=False)
    # Ensure string columns are explicitly string type for Streamlit compatibility
    report["Column"] = report["Column"].astype(str)
    return report


# ===== STREAMLIT ARROW ERROR FIX =====
def fix_streamlit_types(df):
    """
    Fix DataFrame types to be compatible with Streamlit/PyArrow.
    Explicitly converts object columns to string to avoid type inference issues.
    """
    # First, ensure all object columns are string
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)
    
    # Handle numeric columns - ensure consistent dtypes
    for col in df.columns:
        if df[col].dtype == 'float64':
            # Keep float as is - PyArrow handles floats well
            continue
        elif df[col].dtype == 'int64':
            # Keep int as is - PyArrow handles ints well
            continue
    
    return df
