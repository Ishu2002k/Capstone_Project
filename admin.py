import sqlite3
import pandas as pd
import streamlit as st

def admin_panel():
    st.title("🔐 Admin Panel")

    # -------------------------
    # Password Protection
    # -------------------------
    PASSWORD = "admin_123"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.subheader("Login Required")
        password_input = st.text_input("Enter password:", type="password")
        if st.button("Login"):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Logged in successfully!")
                st.rerun()  # Refresh to hide login
            else:
                st.error("❌ Wrong password. Try again.")
        return

    # -------------------------
    # Admin Panel (After Login)
    # -------------------------
    st.subheader("📂 Upload Files to SQLite Database")

    # Logout button
    if st.button("🔓 Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # Connect to SQLite database
    conn = sqlite3.connect("uploaded_db.sqlite")

    # Upload CSV/Excel files
    uploaded_files = st.file_uploader(
        "Upload CSV or Excel files",
        type=["csv", "xlsx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            base_name = file.name.split(".")[0]

            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
                table_name = base_name
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                st.success(f"✅ Uploaded {file.name} as table `{table_name}`")

            else:  # Excel with multiple sheets
                xls = pd.ExcelFile(file)
                for sheet in xls.sheet_names:
                    df = xls.parse(sheet)
                    table_name = f"{base_name}_{sheet}".strip().replace(" ", "_")
                    df.to_sql(table_name, conn, if_exists="replace", index=False)
                    st.success(f"✅ Uploaded sheet '{sheet}' from {file.name} as table `{table_name}`")
        st.rerun()  # Refresh to show new tables immediately

    # Function to fetch tables
    def fetch_tables():
        return pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

    tables = fetch_tables()
    st.subheader("📋 Tables in Database")
    st.dataframe(tables)

    # Delete table
    if not tables.empty:
        table_to_delete = st.selectbox("Select a table to delete", tables["name"])
        if st.button("❌ Delete Table"):
            conn.execute(f"DROP TABLE IF EXISTS {table_to_delete};")
            conn.commit()
            st.warning(f"Table `{table_to_delete}` has been deleted!")
            st.rerun()  # Refresh to update list and selectbox

    conn.close()



