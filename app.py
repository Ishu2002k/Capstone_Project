import streamlit as st
from admin import admin_panel
from user import user_panel
from visualize import visualize_panel

# App Title and Branding
st.set_page_config(initial_sidebar_state="collapsed",page_title="Axtria Data Platform", page_icon="📊", layout = "wide")

# --- Fix ghost strip when collapsed ---
hide_sidebar_style = """
    <style>
        section[data-testid="stSidebar"][aria-expanded="false"] {
            width: 0px !important;
            min-width: 0px !important;
            margin-left: -20px !important; /* removes leftover strip */
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #d9fdd3; /* Light green */
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0); /* Transparent header */
}
[data-testid="stSidebar"] {
    background-color: #f0fff0; /* Optional: light green sidebar */
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

st.image("axtria_logo.png", width=160)
st.markdown("<h2 style='text-align: center; color: #2E86C1;'>📊 GenAI SQL Assitant</h2>", unsafe_allow_html=True)
st.write("---")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"  # default to role selection

# --- Home Page (Role Selection) ---
if st.session_state.page == "home":
    st.markdown("### 🔑 Please select your role")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👨‍💼 Admin", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()

    with col2:
        if st.button("👤 User", use_container_width=True):
            st.session_state.page = "user"
            st.rerun()
    
    with col3:
        if st.button("📊 Visualize Data", use_container_width=True):
            st.session_state.page = "visualize"
            st.rerun()

# --- Admin Page ---
elif st.session_state.page == "admin":
    st.sidebar.button("⬅️ Back to Home", on_click=lambda: st.session_state.update(page="home"))
    admin_panel()

# --- User Page ---
elif st.session_state.page == "user":
    st.sidebar.button("⬅️ Back to Home", on_click=lambda: st.session_state.update(page="home"))
    st.markdown("### 👤 User Dashboard")
    user_panel()

# --- Visualization Page ---
elif st.session_state.page == "visualize":
    st.sidebar.button("⬅️ Back to Home", on_click=lambda: st.session_state.update(page="home"))
    st.markdown("### 📊 Data Visualization Dashboard")
    visualize_panel("uploaded_db.sqlite")  # ⬅️ database file path






















# import streamlit as st
# from admin import admin_panel
# from user import user_panel
# from visualize import visualize_panel

# # App Title and Branding
# st.set_page_config(
#     initial_sidebar_state="collapsed",
#     page_title="Axtria Data Platform",
#     page_icon="📊",
#     layout="wide"
# )

# # --- Fix ghost strip when collapsed ---
# hide_sidebar_style = """
#     <style>
#         section[data-testid="stSidebar"][aria-expanded="false"] {
#             width: 0px !important;
#             min-width: 0px !important;
#             margin-left: -20px !important; /* default for desktops */
#         }

#         /* For tablets */
#         @media (max-width: 1024px) {
#             section[data-testid="stSidebar"][aria-expanded="false"] {
#                 margin-left: -20px !important;
#             }
#         }

#         /* For mobile */
#         @media (max-width: 768px) {
#             section[data-testid="stSidebar"][aria-expanded="false"] {
#                 margin-left: -30px !important;
#             }
#         }

#         /* For very small devices */
#         @media (max-width: 480px) {
#             section[data-testid="stSidebar"][aria-expanded="false"] {
#                 margin-left: -50px !important;
#             }
#         }
#     </style>
# """
# st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# # --- Fixed header + responsive design ---
# custom_css = """
# <style>
# /* Fixed Header */
# .fixed-header {
#     position: fixed;
#     top: 0;
#     left: 0;
#     width: 100%;
#     background-color: #d9fdd3;
#     z-index: 1;
#     padding: 8px 1rem;
#     text-align: center;
#     border-bottom: 2px solid #ccc;
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
# }

# /* Responsive image */
# .fixed-header img {
#     max-width: 160px;
#     width: 40%;
#     height: auto;
# }


# /* Responsive title */
# .fixed-header h2 {
#     color: #2E86C1;
#     margin: 0;
#     font-size: clamp(1rem, 2.5vw, 1.8rem);
#     text-align: center;
# }

# /* Padding so content does not overlap header */
# [data-testid="stAppViewContainer"] {
#     padding-top: 140px !important;
#     background-color: #d9fdd3;
# }

# /* Transparent Streamlit default header */
# [data-testid="stHeader"] {
#     background: rgba(0,0,0,0);
#     height: 0px;
# }

# /* Sidebar full height */
# section[data-testid="stSidebar"] {
#     position: fixed !important;   /* make it stick independently */
#     top: 0 !important;           /* start at very top */
#     left: 0 !important;          /* stick to left */
#     bottom: 0 !important;
#     height: 100vh !important;
#     background-color: #f0fff0;
#     z-index: 999;                /* keep it above content but below header if needed */
# }



# /* --- RESPONSIVENESS --- */

# /* Tablets and below */
# @media (max-width: 1024px) {
#     .fixed-header {
#         flex-direction: column;
#         padding: 10px;
#     }
#     .fixed-header img {
#         max-width: 120px;
#         width: 50%;
#     }
#     .fixed-header h2 {
#         font-size: 1.4rem;
#     }
#     [data-testid="stAppViewContainer"] {
#         padding-top: 120px !important;
#     }
# }

# /* Mobile screens */
# @media (max-width: 600px) {
#     .fixed-header {
#         padding: 8px;
#     }
#     .fixed-header img {
#         max-width: 100px;
#         width: 60%;
#     }
#     .fixed-header h2 {
#         font-size: 1.2rem;
#     }
#     [data-testid="stAppViewContainer"] {
#         padding-top: 100px !important;
#     }
# }
# </style>
# """
# st.markdown(custom_css, unsafe_allow_html=True)

# # --- Fixed Header Content ---
# st.markdown(
#     """
#     <div class="fixed-header">
#         <img src="https://images.yourstory.com/cs/wordpress/2015/07/axtria_logo.jpg?fm=png&auto=format" alt="Axtria Logo">
#         <h2>📊 GenAI SQL Assistant</h2>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# # Initialize session state
# if "page" not in st.session_state:
#     st.session_state.page = "home"  # default to role selection

# # --- Home Page (Role Selection) ---
# if st.session_state.page == "home":
#     st.markdown("### 🔑 Please select your role")
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         if st.button("👨‍💼 Admin", use_container_width=True):
#             st.session_state.page = "admin"
#             st.rerun()

#     with col2:
#         if st.button("👤 User", use_container_width=True):
#             st.session_state.page = "user"
#             st.rerun()

#     with col3:
#         if st.button("📊 Visualize Data", use_container_width=True):
#             st.session_state.page = "visualize"
#             st.rerun()

# # --- Admin Page ---
# elif st.session_state.page == "admin":
#     st.sidebar.button("⬅️ Back to Home", on_click=lambda: st.session_state.update(page="home"))
#     admin_panel()

# # --- User Page ---
# elif st.session_state.page == "user":
#     st.sidebar.button("⬅️ Back to Home", on_click=lambda: st.session_state.update(page="home"))
#     st.markdown("### 👤 User Dashboard")
#     user_panel()

# # --- Visualization Page ---
# elif st.session_state.page == "visualize":
#     st.sidebar.button("⬅️ Back to Home", on_click=lambda: st.session_state.update(page="home"))
#     visualize_panel("uploaded_db.sqlite")  # ⬅️ database file path
