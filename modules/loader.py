import pandas as pd

def load_data(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, encoding="utf-8")
    else:
        df = pd.read_excel(uploaded_file)
    return df
