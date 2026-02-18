def apply_numeric_filter(df, col, minv, maxv):
    return df[(df[col] >= minv) & (df[col] <= maxv)]


def apply_category_filter(df, col, values):
    return df[df[col].isin(values)]
