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

# Aesthetic theme CSS (dark green + beige)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap');
html, body, [class*="css"]  {
  font-family: 'Noto Sans', sans-serif;
}
.main { 
  background: linear-gradient(135deg, #F5F5DC 0%, #E8F5E8 100%); 
  color: #1B5E20;
  padding: 2rem;
}
.stApp { 
  background-color: #F5F5DC; 
}
.sidebar .sidebar-content { 
  background: linear-gradient(to bottom, #E8F5E8, #D4E4D4); 
}
.stButton > button { 
  background: linear-gradient(45deg, #1B5E20, #2E7D32); 
  color: white; 
  border-radius: 20px; 
  height: 60px; 
  font-size: 20px; 
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(27,94,32,0.3);
}
.stButton > button:hover {
  background: linear-gradient(45deg, #2E7D32, #4CAF50);
  transform: translateY(-2px);
}
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > select { 
  height: 60px; 
  font-size: 22px; 
  border-radius: 15px;
  border: 2px solid #D4E4D4;
  padding: 0 15px;
}
h1 { 
  color: #1B5E20; 
  font-size: 3.5rem; 
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
h2 { 
  color: #2E7D32; 
  font-size: 2.2rem;
  border-bottom: 3px solid #D4E4D4;
  padding-bottom: 0.5rem;
}
h3 { 
  color: #1B5E20;
  font-size: 1.8rem;
}
.stMetric > label {
  font-size: 18px;
  font-weight: 600;
  color: #1B5E20;
}
.stDataFrame {
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(27,94,32,0.15);
}
.block-container {
  padding-top: 2rem;
  padding-bottom: 2rem;
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
    st.markdown("### 👤 Login to Matamaal Production System")
    st.divider()
    
    with st.container():
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            st.markdown("---")
            name = st.text_input("**Full Name**", placeholder="Enter your full name", label_visibility="collapsed")
            role = st.selectbox("**Role**", ["Cook", "Admin"], label_visibility="collapsed")
            st.markdown("---")
            
            col_btn_left, col_btn_right = st.columns([1,3])
            with col_btn_left:
                st.empty()
            with col_btn_right:
                if st.button("🚀 LOGIN", use_container_width=True):
                    if name.strip():
                        users = st.session_state.users.copy()
                        if name.strip() in users:
                            # Returning user
                            user_data = users[name.strip()]
                            st.session_state.user = {"name": name.strip(), "role": user_data["role"]}
                            st.session_state.assigned_categories = user_data.get("categories", [])
                            st.success(f"✅ Welcome back {name.strip()}, logged in as **{user_data['role']}**")
                        else:
                            # New user
                            user_data = {"role": role}
                            if role == "Cook":
                                cats = st.multiselect("**Assigned Categories**", list(MENU_DATA.keys()), default=list(MENU_DATA.keys())[:2])
                                user_data["categories"] = cats
                                st.session_state.assigned_categories = cats
                            users[name.strip()] = user_data
                            st.session_state.users = users
                            save_users(users)
                            st.session_state.user = {"name": name.strip(), "role": role}
                            st.success(f"👋 New user **{name.strip()}** created and logged in!")
                        st.rerun()
                    else:
                        st.error("Please enter your name")
            st.markdown("---")

def cook_dashboard():
    st.markdown("<h2>Production Entry Dashboard</h2>", unsafe_allow_html=True)
    
    if not st.session_state.assigned_categories:
        st.warning("No assigned categories. Contact admin.")
        return
    
    menu_df = pd.DataFrame([
        {"item_name": item, "category": cat} for cat, items in MENU_DATA.items() for item in items
    ])
    assigned_cats = st.session_state.assigned_categories
    
    col_cat, col_item, col_qty = st.columns([1,2,1])
    with col_cat:
        category = st.selectbox("Select Category", assigned_cats, key="cook_cat")
    items = menu_df[menu_df["category"] == category]["item_name"].tolist()
    with col_item:
        item = st.selectbox("Select Item", items, key="cook_item")
    col_unit, col_qty = st.columns([1,1])
    with col_unit:
        unit = st.selectbox("Unit", UNITS, key="cook_unit")
    with col_qty:
        qty = st.number_input("Quantity", min_value=0.0, step=0.1, key="cook_qty")
    
    if st.button("➕ Add Entry", use_container_width=True, type="primary"):
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
            st.success("✅ Entry added!")
            st.rerun()

def admin_dashboard():
    st.markdown("<h2>🍽️ Admin Dashboard</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 All Production Entries", "👥 Manage Users"])
    
    with tab1:
        if not st.session_state.production_data:
            st.info("No production entries yet.")
        else:
            df = pd.DataFrame(st.session_state.production_data)
            st.dataframe(df[['item_name', 'category', 'quantity', 'unit', 'created_by', 'timestamp']], use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Refresh Data", type="secondary"):
                    st.session_state.production_data = load_production()
                    st.rerun()
            with col2:
                if st.button("🗑️ Clear All Data", type="primary"):
                    st.session_state.production_data = []
                    save_production([])
                    st.success("All data cleared!")
                    st.rerun()
    
    with tab2:
        st.markdown("### Assign Categories to Cooks")
        users_df = pd.DataFrame([
            {"Name": name, "Role": data["role"], "Categories": ", ".join(data.get("categories", []))} 
            for name, data in st.session_state.users.items() if data["role"] == "Cook"
        ])
        st.dataframe(users_df, use_container_width=True)
        
        # Edit categories
        new_cook = st.text_input("New Cook Name")
        new_cats = st.multiselect("Assign Categories", list(MENU_DATA.keys()))
        col_add, col_save = st.columns(2)
        if col_add.button("Add Cook"):
            if new_cook and new_cats:
                st.session_state.users[new_cook] = {"role": "Cook", "categories": new_cats}
                save_users(st.session_state.users)
                st.success("Cook added!")
                st.rerun()
        
        # Update existing (simple)
        if st.button("Save Changes", type="primary"):
            save_users(st.session_state.users)
            st.success("Users updated!")

def main():
    init_session()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## User Panel")
        if st.session_state.user:
            st.success(f"**{st.session_state.user['role']}**: {st.session_state.user['name']}")
            if st.button("Logout", use_container_width=True):
                for key in ["user", "assigned_categories"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        st.markdown("---")
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

