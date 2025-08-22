from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import sqlite3
import pandas as pd

# Load environment variables
load_dotenv()

# Get environment variables
api_key = os.getenv("OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("OPENAI_API_VERSION")

def user_panel():
    # Initialize Azure OpenAI Client
    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version
    )

    st.title("📊 SQL Query Assistant")

    # Maintain history in session
    if "history" not in st.session_state:
        st.session_state.history = []

    if "show_history" not in st.session_state:
        st.session_state.show_history = False

    # Sidebar toggle with dynamic label (single click works)
    st.session_state.show_history = st.sidebar.toggle(
        "Switch Panel",
        value=st.session_state.show_history,
        help="Toggle between query input and query history"
    )

    # -------------------------
    # Show Query History
    # -------------------------
    if st.session_state.show_history:
        st.subheader("🕒 Query History")
        if st.session_state.history:
            for i, record in enumerate(reversed(st.session_state.history), 1):
                with st.expander(f"Query {i}: {record['query']}"):
                    st.markdown("**Generated SQL by Model:**")
                    st.code(record['sql'], language="sql")
                    st.markdown("**Query Result:**")
                    st.dataframe(record['result'], height=300)
                    st.markdown("---")
        else:
            st.info("No queries run yet.")
        return  # stop here if showing history

    # -------------------------
    # Main Query Panel
    # -------------------------
    db_path = r"C:\Users\A7698\OneDrive - Axtria\Desktop\Python\Streamlit\uploaded_db.sqlite"
    conn = sqlite3.connect(db_path)

    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';",
        conn
    )["name"].tolist()

    schema_parts = []
    for table in tables:
        schema = pd.read_sql(f"PRAGMA table_info({table});", conn)
        cols = ", ".join([f"{row['name']} ({row['type']})" for _, row in schema.iterrows()])
        schema_parts.append(f"Table: {table}\nColumns: {cols}")
    schema_str = "\n\n".join(schema_parts)

    user_text = st.text_area("Enter your query in natural language", key="user_input")

    # ---- Temperature Slider in Sidebar ----
    temperature = st.sidebar.slider(
        "Set model temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1
    )

    if st.button("Generate SQL and Run"):
        if user_text.strip():
            prompt = f"""
            You are an expert SQL assistant. ONLY generate SELECT queries in SQLite.
            Use JOINs if necessary.

            Database schema:
            {schema_str}

            Natural language request: {user_text}

            Return ONLY a valid SQL SELECT query. If not suitable, respond:
            "⚠️ Only SELECT queries are allowed."
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )

            sql_query = response.choices[0].message.content.strip()
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            st.code(sql_query, language="sql")

            try:
                result_df = pd.read_sql(sql_query, conn)
                st.write("### Query Results")
                st.dataframe(result_df)

                # Save to history
                st.session_state.history.append({
                    "query": user_text,
                    "sql": sql_query,
                    "result": result_df
                })

                # Download option
                csv = result_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"Error running SQL: {e}")

    conn.close()
