import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Matamaal Production Tracking System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal Kashmiri Theme CSS (dark green #1B4332, beige #F5F5DC, gold #DAA520)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600&display=swap');
html, body, [class*="css"] {
  font-family: 'Noto Sans', sans-serif;
}
.main {
  background-color: #F5F5DC;
  color: #1B4332;
  padding: 1.5rem;
}
.stApp {
  background-color: #F5F5DC;
}
.sidebar .sidebar-content {
  background-color: #E8F4E8;
}
.stButton > button {
  background-color: #1B4332;
  color: white;
  border: 2px solid #DAA520;
  border-radius: 8px;
  height: 45px;
  font-size: 16px;
  font-weight: 600;
  padding: 0 20px;
}
.stButton > button:hover {
  background-color: #2A5A42;
  border-color: #DAA520;
}
.stTextInput > div > div > input, 
.stNumberInput > div > div > input, 
.stSelectbox > div > div > select,
.stMultiSelect > div > div > select {
  height: 45px;
  font-size: 16px;
  border-radius: 8px;
  border: 2px solid #DAA520;
  padding: 0 12px;
}
h1 {
  color: #1B4332;
  font-size: 2.5rem;
  font-weight: 600;
}
h2 {
  color: #1B4332;
  font-size: 1.8rem;
  border-bottom: 2px solid #DAA520;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}
h3 {
  color: #1B4332;
  font-size: 1.4rem;
}
.stMetric > label {
  font-size: 14px;
  font-weight: 600;
  color: #1B4332;
}
.stDataFrame {
  border-radius: 8px;
  border: 1px solid #DAA520;
}
</style>
""", unsafe_allow_html=True)

MENU_DATA = {
    "Appetizers": ["Paneer Kanti", "Nadur Monje", "Kaladi Kulcha", "Aloo Churma", "Omelette Kanti", "Kabargah", "Wazwan Mutton Seekh", "Wazwan Chicken Seekh", "Mutton Seekh Kanti", "Chicken Seekh Kanti", "Chicken Lahabdar Kebab"],
    "Veg": ["Paneer Roganjosh", "Paneer Kaliya", "Dum Aloo", "Kashmiri Rajma", "Nadur Yakhni", "Tchok Wangun", "Monje Haak", "Palak Nadur"],
    "Non Veg": ["Mutton Roganjosh", "Masc", "Mutton Yakhni", "Mutton Kaliya", "Chicken Yakhni", "Chicken Roganjosh", "Gaad with Vegetables", "Tchok Charwan"],
    "Wazwan": ["Tamatar Tchaman", "Mutton Rista", "Mutton Goshtaba", "Mutton Marchwangan Korma", "Harissa", "Waza Kokur", "Chicken Marchwangan Korma", "Chicken Dhaniwal Korma", "Methi Maaz"],
    "Breads": ["Kashmiri Kulcha", "Desi Ghee Kulcha", "Lavasa", "Girda / Tchot", "Katlam", "Telvor", "Sheermal", "Bagherkhani", "Madur Khatayi", "Gyev Tchot", "Routh"]
}

UNITS = ["kg", "portion", "pieces"]

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

def load_production():
    try:
        return pd.read_csv('production_data.csv').to_dict('records')
    except:
        return []

def save_production(data):
    pd.DataFrame(data).to_csv('production_data.csv', index=False)

def init_session():
    if "users" not in st.session_state:
        st.session_state.users = load_users()
    if "production_data" not in st.session_state:
        st.session_state.production_data = load_production()
    if "user" not in st.session_state:
        st.session_state.user = None
    if "assigned_categories" not in st.session_state:
        st.session_state.assigned_categories = []


def login_ui():
    st.markdown("## Login")
    st.divider()
    
    with st.container(border=True):
        st.markdown("### Enter Details")
        col1, col2, col1 = st.columns([2,3,2])
        with col2:
            name = st.text_input("Full Name", placeholder="Enter your full name")
            role = st.selectbox("Role", ["Cook", "Admin"])
            
            if st.button("Login", use_container_width=True, type="primary"):
                if name.strip():
                    users = st.session_state.users.copy()
                    if name.strip() in users:
                        user_data = users[name.strip()]
                        st.session_state.user = {"name": name.strip(), "role": user_data["role"]}
                        st.session_state.assigned_categories = user_data.get("categories", [])
                        st.success(f"Welcome back {name.strip()}, logged in as {user_data['role']}.")
                    else:
                        user_data = {"role": role}
                        if role == "Cook":
                            cats = st.multiselect("Assign Categories", list(MENU_DATA.keys()), default=list(MENU_DATA.keys())[:2])
                            user_data["categories"] = cats
                            st.session_state.assigned_categories = cats
                        users[name.strip()] = user_data
                        st.session_state.users = users
                        save_users(users)
                        st.session_state.user = {"name": name.strip(), "role": role}
                        st.success(f"New user {name.strip()} created and logged in!")
                    st.rerun()
                else:
                    st.error("Please enter your name")

def cook_dashboard():
    st.markdown("## Production Entry")
    st.divider()
    
    if not st.session_state.assigned_categories:
        st.warning("No assigned categories. Contact admin.")
        st.stop()
    
    with st.container(border=True):
        menu_df = pd.DataFrame([
            {"item_name": item, "category": cat} for cat, items in MENU_DATA.items() for item in items
        ])
        assigned_cats = st.session_state.assigned_categories
        
        col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
        with col1:
            category = st.selectbox("Category", assigned_cats, key="cook_cat")
        with col2:
            items = menu_df[menu_df["category"] == category]["item_name"].tolist()
            item = st.selectbox("Item", items, key="cook_item")
        with col3:
            unit = st.selectbox("Unit", UNITS, key="cook_unit")
        with col4:
            qty = st.number_input("Qty", min_value=0.0, step=0.1, key="cook_qty")
        
        if st.button("Add Entry", use_container_width=True, type="primary"):
            if qty > 0 and item:
                entry = {
                    "item_name": item,
                    "category": category,
                    "quantity": qty,
                    "unit": unit,
                    "created_by": st.session_state.user["name"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.production_data.append(entry)
                save_production(st.session_state.production_data)
                st.success("Entry added!")
                st.rerun()

def admin_dashboard():
    st.markdown("## Admin Dashboard")
    st.divider()
    
    tab1, tab2 = st.tabs(["Production Entries", "Manage Users"])
    
    with tab1:
        if not st.session_state.production_data:
            st.info("No entries yet.")
            st.stop()
        
        st.markdown("### Entries")
        st.dataframe(pd.DataFrame(st.session_state.production_data)[['item_name', 'category', 'quantity', 'unit', 'created_by', 'timestamp']], hide_index=True, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Refresh", type="secondary", use_container_width=True):
                st.session_state.production_data = load_production()
                st.rerun()
        with col2:
            if st.button("Clear All", type="primary", use_container_width=True):
                st.session_state.production_data = []
                save_production([])
                st.success("All data cleared!")
                st.rerun()
    
    with tab2:
        st.markdown("### Users")
        users_df = pd.DataFrame([
            {"Name": name, "Role": data["role"], "Categories": ", ".join(data.get("categories", []))} 
            for name, data in st.session_state.users.items() if data["role"] == "Cook"
        ])
        if not users_df.empty:
            st.dataframe(users_df, hide_index=True, use_container_width=True)
        else:
            st.info("No cooks yet.")
        
        st.markdown("**Add Cook**")
        col_new1, col_new2 = st.columns(2)
        with col_new1:
            new_cook = st.text_input("Cook Name")
        with col_new2:
            new_cats = st.multiselect("Categories", list(MENU_DATA.keys()))
        if st.button("Add Cook", type="primary", use_container_width=True):
            if new_cook.strip() and new_cats:
                st.session_state.users[new_cook.strip()] = {"role": "Cook", "categories": new_cats}
                save_users(st.session_state.users)
                st.success("Cook added!")
                st.rerun()
        
        if st.button("Save Changes", type="secondary", use_container_width=True):
            save_users(st.session_state.users)
            st.success("Users updated!")

def main():
    init_session()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## User Panel")
        if st.session_state.user:
            st.markdown(f"**{st.session_state.user['role']}**: {st.session_state.user['name']}")
            if st.button("Logout", use_container_width=True):
                for key in ["user", "assigned_categories"]:
                    del st.session_state[key]
                st.rerun()
        st.divider()
        if st.session_state.production_data:
            st.metric("Total Entries", len(st.session_state.production_data))
    
    # Main content
    if not st.session_state.user:
        login_ui()
    elif st.session_state.user["role"] == "Cook":
        cook_dashboard()
    else:
        admin_dashboard()

if __name__ == "__main__":
    main()

