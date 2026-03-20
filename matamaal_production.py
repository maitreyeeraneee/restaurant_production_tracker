import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Restaurant Production Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Restaurant Theme CSS (dark green #1B4332, beige #F5F5DC, soft gold #DAA520)
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
    st.markdown("### 🔐 Login")
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
    st.markdown("### ➕ Production Entry")
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
    st.markdown("###  Admin Dashboard")
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Production Entries", "Manage Users", "Edit Cook Entries", "History & Analytics"])
    
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
        st.markdown("### Manage Users")
        users_list = [{"Name": name, "Role": data["role"], "Categories": ", ".join(data.get("categories", []))} 
                      for name, data in st.session_state.users.items()]
        users_df = pd.DataFrame(users_list)
        if users_df.empty:
            st.info("No users yet.")
        else:
            st.dataframe(users_df, hide_index=True, use_container_width=True)
        
        st.markdown("---")
        
        # Edit/Delete each user
        for idx, row in users_df.iterrows():
            name = row["Name"]
            if name in st.session_state.users:
                data = st.session_state.users[name]
                with st.expander(f" Edit /  Delete {name} ({data['role']})", expanded=False):
                    col_role, col_cats = st.columns([1, 4])
                    with col_role:
                        role_idx = 0 if data["role"] == "Cook" else 1
                        new_role = st.selectbox("Role", ["Cook", "Admin"], index=role_idx, key=f"role_edit_{name}")
                    with col_cats:
                        is_cook = new_role == "Cook"
                        new_cats = st.multiselect("Categories", list(MENU_DATA.keys()), 
                                                  default=data.get("categories", []) if is_cook else [],
                                                  key=f"cats_edit_{name}")
                    col_up, col_del = st.columns(2)
                    with col_up:
                        if st.button(" Update", key=f"update_user_{name}"):
                            st.session_state.users[name] = {"role": new_role, "categories": new_cats}
                            save_users(st.session_state.users)
                            st.success(f"Updated {name}!")
                            st.rerun()
                    with col_del:
                        if st.button(" Delete", key=f"delete_user_{name}"):
                            if st.session_state.user and st.session_state.user["name"] == name:
                                st.warning("Cannot delete logged-in user!")
                            else:
                                del st.session_state.users[name]
                                save_users(st.session_state.users)
                                st.success(f"Deleted {name}!")
                                st.rerun()
        
        # Add new user
        st.markdown("### ➕ Add New User")
        col_new1, col_new2, col_new3 = st.columns([1.5, 1.5, 3])
        with col_new1:
            new_name = st.text_input("Name")
        with col_new2:
            new_role = st.selectbox("Role", ["Cook", "Admin"])
        with col_new3:
            new_cats = st.multiselect("Categories", list(MENU_DATA.keys()))
        if st.button("Add User", type="primary", use_container_width=True):
            if new_name.strip():
                if new_role == "Admin" or new_cats:
                    st.session_state.users[new_name.strip()] = {"role": new_role, "categories": new_cats}
                    save_users(st.session_state.users)
                    st.success("User added!")
                    st.rerun()
                else:
                    st.error("Assign categories for Cook.")
            else:
                st.error("Enter name.")

    with tab3:
        st.markdown("### Edit Cook Entries")
        if not st.session_state.production_data:
            st.info("No production entries yet.")
            st.stop()
        
        df = pd.DataFrame(st.session_state.production_data)
        if df.empty:
            st.info("No entries.")
        else:
            cooks = sorted(df['created_by'].unique())
            selected_cook = st.selectbox("Select Cook", cooks)
            
            cook_entries = df[df['created_by'] == selected_cook]
            if cook_entries.empty:
                st.info(f"No entries for {selected_cook}")
            else:
                st.markdown(f"**Entries by {selected_cook}**")
                st.dataframe(cook_entries[['item_name', 'category', 'quantity', 'unit', 'timestamp']], hide_index=True, use_container_width=True)
                
                st.markdown("---")
                
                # Edit/Delete each entry
                for idx, entry in cook_entries.iterrows():
                    with st.expander(f" Edit / Delete: {entry['item_name']} ({entry['quantity']} {entry['unit']})", expanded=False):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            new_category = st.selectbox("Category", list(MENU_DATA.keys()), index=list(MENU_DATA.keys()).index(entry['category']), key=f"cat_{idx}")
                        with col2:
                            menu_items = MENU_DATA[new_category]
                            new_item = st.selectbox("Item", menu_items, index=menu_items.index(entry['item_name']), key=f"item_{idx}")
                        with col3:
                            new_qty = st.number_input("Quantity", value=float(entry['quantity']), step=0.1, key=f"qty_{idx}")
                        with col4:
                            new_unit = st.selectbox("Unit", UNITS, index=UNITS.index(entry['unit']), key=f"unit_{idx}")
                        
                        col_edit, col_delete = st.columns(2)
                        with col_edit:
                            if st.button(" Update", key=f"edit_entry_{idx}"):
                                # Update in session_data
                                for i, e in enumerate(st.session_state.production_data):
                                    if e['timestamp'] == entry['timestamp'] and e['created_by'] == selected_cook:
                                        st.session_state.production_data[i] = {
                                            **e,
                                            'item_name': new_item,
                                            'category': new_category,
                                            'quantity': new_qty,
                                            'unit': new_unit
                                        }
                                        break
                                save_production(st.session_state.production_data)
                                st.success("Entry updated!")
                                st.rerun()
                        with col_delete:
                            if st.button(" Delete", key=f"del_entry_{idx}"):
                                st.session_state.production_data = [e for e in st.session_state.production_data if not (e['timestamp'] == entry['timestamp'] and e['created_by'] == selected_cook)]
                                save_production(st.session_state.production_data)
                                st.success("Entry deleted!")
                                st.rerun()
    
    with tab4:
        st.subheader("History & Analytics")
        if not st.session_state.production_data:
            st.info("No data available")
        else:
            df = pd.DataFrame(st.session_state.production_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filters
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                start_date = st.date_input("Start Date", value=df['timestamp'].dt.date.min())
            with col2:
                end_date = st.date_input("End Date", value=datetime.now().date())
            with col3:
                items = sorted(df['item_name'].unique())
                selected_item = st.selectbox("Item", ["All"] + items)
            with col4:
                sort_by = st.selectbox("Sort by", ["timestamp", "quantity", "item_name"])
            
            # Filter
            filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]
            if selected_item != "All":
                filtered_df = filtered_df[filtered_df['item_name'] == selected_item]
            
            # Sort
            filtered_df = filtered_df.sort_values(sort_by, ascending=False)
            
            if filtered_df.empty:
                st.info("No entries match the filters")
            else:
                st.markdown("**Filtered Entries**")
                st.dataframe(filtered_df[['item_name', 'category', 'quantity', 'unit', 'created_by', 'timestamp']], hide_index=True, use_container_width=True)
                
                col_tot1, col_tot2 = st.columns(2)
                with col_tot1:
                    st.metric("Total Quantity", filtered_df['quantity'].sum())
                
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV", 
                    data=csv, 
                    file_name=f"production_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )
                
                # Monthly Insights
                st.markdown("**Monthly Summary**")
                monthly = filtered_df.groupby(filtered_df['timestamp'].dt.to_period('M').astype(str))[['item_name', 'category', 'quantity']].agg({'quantity': 'sum'}).reset_index()
                st.dataframe(monthly, hide_index=True, use_container_width=True)

def main():
    init_session()
    
    # Header
    st.markdown("# Restaurant Production Tracker")
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 👤 User Panel")
        if st.session_state.user:
            st.markdown(f"**{st.session_state.user['role']}**: {st.session_state.user['name']}")
            if st.button(" Logout", use_container_width=True):
                for key in ["user", "assigned_categories"]:
                    del st.session_state[key]
                st.rerun()
        st.divider()
        if st.session_state.production_data:
            st.metric("📊 Total Entries", len(st.session_state.production_data))
    
    # Main content
    if not st.session_state.user:
        login_ui()
    elif st.session_state.user["role"] == "Cook":
        cook_dashboard()
    else:
        admin_dashboard()

if __name__ == "__main__":
    main()

