def fill_null_values(df, col, method, constant=None):

    if method == "Mean":
        df[col] = df[col].fillna(df[col].mean())

    elif method == "Median":
        df[col] = df[col].fillna(df[col].median())

    elif method == "Mode":
        df[col] = df[col].fillna(df[col].mode()[0])

    elif method == "Forward Fill":
        df[col] = df[col].fillna(method="ffill")

    elif method == "Backward Fill":
        df[col] = df[col].fillna(method="bfill")

    elif method == "Constant":
        df[col] = df[col].fillna(constant)

    return df


def drop_null_rows(df):
    return df.dropna()


def drop_null_columns(df):
    return df.dropna(axis=1)
