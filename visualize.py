# import sqlite3
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# import seaborn as sns

# def visualize_panel(db_path="uploaded_db.sqlite"):
#     st.title("📊 Smart Table Visualization")

#     conn = sqlite3.connect(db_path)
#     tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)["name"].tolist()
#     if not tables:
#         st.warning("⚠️ No tables found in the database.")
#         conn.close()
#         return

#     table_name = st.selectbox("Select a table", tables)
#     if not table_name:
#         conn.close()
#         return

#     df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
#     st.subheader("📋 Data Preview")
#     st.dataframe(df.head())
#     st.subheader("📊 Summary Statistics")
#     st.write(df.describe(include="all"))

#     numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
#     numeric_cols = [col for col in numeric_cols if df[col].nunique() > 1]

#     if len(numeric_cols) >= 2:
#         st.subheader("📈 Plot Numeric Columns")
#         col_pair = st.selectbox(
#             "Select columns to plot",
#             [(x, y) for x in numeric_cols for y in numeric_cols if x != y],
#             format_func=lambda x: f"{x[0]} vs {x[1]}"
#         )
#         chart_type = st.selectbox("Choose chart type", ["Scatter", "Line", "Bar"])
#         x_col, y_col = col_pair
#         fig, ax = plt.subplots()
#         if chart_type == "Scatter":
#             sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
#         elif chart_type == "Line":
#             sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
#         elif chart_type == "Bar":
#             sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
#         ax.set_title(f"{x_col} vs {y_col}")
#         st.pyplot(fig)
#     else:
#         st.info("ℹ️ Not enough numeric columns for plotting.")

#     conn.close()


import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def visualize_panel(db_path="uploaded_db.sqlite"):
    st.title("📊 Smart Table Visualization with Safe Plots")

    # Connect to SQLite DB
    conn = sqlite3.connect(db_path)

    # Fetch available tables
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)["name"].tolist()
    if not tables:
        st.warning("⚠️ No tables found in the database.")
        conn.close()
        return

    # Table selection
    table_name = st.selectbox("Select a table", tables)
    if not table_name:
        conn.close()
        return

    # Load table
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    # Show basic info
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())
    st.subheader("📊 Summary Statistics")
    st.write(df.describe(include="all"))

    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    # Heuristics to avoid meaningless plots
    safe_numeric_cols = []
    for col in numeric_cols:
        nunique = df[col].nunique()
        total = len(df)
        if nunique > 1 and nunique < 0.9 * total:
            if df[col].max() / (df[col].min() + 1e-5) < 1e4:
                safe_numeric_cols.append(col)

    plotted_cols = set()

    if safe_numeric_cols:
        st.subheader("📈 Suggested Bivariate Plots")
        corr_matrix = df[safe_numeric_cols].corr().abs()
        threshold = 0.2
        suggested_pairs = [
            (x, y) for x in safe_numeric_cols for y in safe_numeric_cols
            if x != y and corr_matrix.loc[x, y] >= threshold
        ]

        if suggested_pairs:
            col_pair = st.selectbox(
                "Select columns to plot",
                suggested_pairs,
                format_func=lambda x: f"{x[0]} vs {x[1]}"
            )
            chart_type = st.selectbox("Choose chart type", ["Scatter", "Line", "Bar"])
            x_col, y_col = col_pair

            fig, ax = plt.subplots()
            if chart_type == "Scatter":
                sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "Line":
                sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "Bar":
                sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
            ax.set_title(f"{x_col} vs {y_col}")
            st.pyplot(fig)

            plotted_cols.update([x_col, y_col])
        else:
            st.info("ℹ️ No safe numeric column pairs have meaningful correlation for plotting.")

        # Univariate histograms for remaining numeric columns
        unplotted_cols = [col for col in safe_numeric_cols if col not in plotted_cols]
        if unplotted_cols:
            st.subheader("📊 Univariate Histograms")
            for col in unplotted_cols:
                fig, ax = plt.subplots()
                sns.histplot(df[col], kde=True, ax=ax, color="skyblue")
                ax.set_title(f"Distribution of {col}")
                st.pyplot(fig)

    else:
        st.info("ℹ️ No safe numeric columns available for plotting.")

    conn.close()
