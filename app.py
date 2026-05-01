import streamlit as st
import pandas as pd
import time
 
# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Zone Task Manager",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ---------- CRITICAL CSS FOR ROW LAYOUT - DESKTOP + MOBILE BOTH ROW ----------
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stAppHeader {display: none;}
        .stDeployButton {display: none;}
        .stToolbar {display: none;}
        .stStatusWidget {display: none;}
        .stApp > header {display: none !important;}
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0rem !important;
            margin-top: 0rem !important;
        }
       
        .loading-spinner {
            display: inline-block;
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255,107,107,0.3);
            border-radius: 50%;
            border-top-color: #FF6B6B;
            animation: spin 1s ease-in-out infinite;
        }
       
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
 
        .loading-container {
            text-align: center;
            padding: 50px;
        }
       
        .stats-card {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
       
        /* FORCE ROW LAYOUT ON BOTH DESKTOP AND MOBILE */
        @media (max-width: 768px) {
            /* Override Streamlit's column behavior completely */
            .stHorizontalBlock {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
            }
           
            /* Force all columns to stay horizontal */
            div[data-testid="column"] {
                flex: 1 !important;
                min-width: auto !important;
                width: auto !important;
            }
        }
       
        /* Checklist container - uses CSS Grid for true row layout */
        .checklist-grid {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
       
        .checklist-item {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            align-items: center;
            gap: 15px;
            padding: 12px 10px;
            background: white;
            border-radius: 10px;
            border: 1px solid #e5e7eb;
            margin-bottom: 8px;
        }
       
        /* Mobile pe bhi same grid, koi change nahi */
        @media (max-width: 768px) {
            .checklist-item {
                grid-template-columns: 2fr 1fr 1fr;
                gap: 10px;
                padding: 10px 8px;
            }
           
            .checklist-item .dept-name {
                font-size: 14px;
            }
           
            .checklist-item .aisle-bay {
                font-size: 13px;
            }
           
            .checklist-item button {
                font-size: 12px;
                padding: 6px 10px;
            }
        }
       
        .dept-name {
            font-weight: 700;
            color: #1f2937;
            border-left: 4px solid #FF6B6B;
            padding-left: 12px;
        }
       
        .aisle-bay {
            background: #f3f4f6;
            padding: 8px;
            text-align: center;
            border-radius: 8px;
            font-weight: 600;
            color: #374151;
        }
       
        .done-badge {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 8px;
            text-align: center;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13px;
        }
       
        .stButton > button {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            width: 100% !important;
        }
       
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(255,107,107,0.4) !important;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
 
# ---------- HARDCODED DATA ----------
@st.cache_data
def get_initial_data():
    data = [
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Toothpaste", "AisleBay": 1016, "Flag": 1},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Rice", "AisleBay": 10987, "Flag": 1},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Frozen", "AisleBay": 19363, "Flag": 1},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Pulses", "AisleBay": 23476, "Flag": 1},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Eggs", "AisleBay": 78365, "Flag": 0},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Coldrink", "AisleBay": 87523, "Flag": 0},
    ]
    return pd.DataFrame(data)
 
# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = get_initial_data()
 
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "Zone-1"
 
if "loading" not in st.session_state:
    st.session_state.loading = False
 
# ---------- NAVBAR ----------
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
 
col_nav_main, col_nav_empty = st.columns([2, 3])
with col_nav_main:
    nav_left, nav_right = st.columns([1.5, 1])
    with nav_left:
        st.markdown(f'<div style="display: flex; align-items: center; gap: 10px;"><img src="{LOGO_URL}" width="28"><span style="font-size: 18px; font-weight: 600; background: linear-gradient(135deg, #FF6B6B, #FF8E53); -webkit-background-clip: text; background-clip: text; color: transparent;">Zone Manager</span></div>', unsafe_allow_html=True)
    with nav_right:
        selected = st.selectbox("Select Zone", ["-- Select Zone --", "Zone-1"],
                               index=1, label_visibility="collapsed", key="zone_selector")
        if selected != st.session_state.selected_zone:
            st.session_state.selected_zone = selected
            st.rerun()
 
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
 
# ---------- STATS CARD ----------
col_stats_main, col_stats_empty = st.columns([2, 3])
with col_stats_main:
    df = st.session_state.df
    if st.session_state.selected_zone != "-- Select Zone --":
        zone_df = df[df["Zone"] == st.session_state.selected_zone].copy()
    else:
        zone_df = pd.DataFrame()
 
    if not zone_df.empty and st.session_state.selected_zone != "-- Select Zone --":
        store = zone_df.iloc[0]["Store"] if len(zone_df) > 0 else "N/A"
        captain = zone_df.iloc[0]["Captain"] if len(zone_df) > 0 else "N/A"
        total, done, pending = len(zone_df), len(zone_df[zone_df["Flag"] == 1]), len(zone_df[zone_df["Flag"] == 0])
        html = f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #f5f5f5, #e8e8e8); border-radius:12px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #d0d0d0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid #dcdcdc; padding-bottom: 10px;">
                <div><div style="color: #666; font-size: 11px; font-weight: 700;">📍 ZONE</div><div style="color: #333; font-size: 15px; font-weight: 700;">{st.session_state.selected_zone}</div></div>
                <div><div style="color: #666; font-size: 11px; font-weight: 700;">🏬 STORE</div><div style="color: #333; font-size: 15px; font-weight: 700;">{store}</div></div>
                <div><div style="color: #666; font-size: 11px; font-weight: 700;">👤 CAPTAIN</div><div style="color: #333; font-size: 15px; font-weight: 700;">{captain}</div></div>
            </div>
            <div style="display: flex; justify-content: space-around; background: rgba(0,0,0,0.03); padding: 10px; border-radius: 8px;">
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">📊 TOTAL</div><div style="color: #333; font-weight: 800; font-size: 18px;">{total}</div></div>
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">✅ DONE</div><div style="color: #22c55e; font-weight: 800; font-size: 18px;">{done}</div></div>      
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">⏳ PENDING</div><div style="color: #f59e0b; font-weight: 800; font-size: 18px;">{pending}</div></div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
 
# ---------- CHECKLIST SECTION - EXACT ROW LAYOUT ----------
if st.session_state.selected_zone != "-- Select Zone --" and not zone_df.empty:
    st.subheader("Aisle Bay Checklist")
   
    if st.session_state.loading:
        st.markdown('<div class="loading-container"><div class="loading-spinner"></div><p>Updating...</p></div>', unsafe_allow_html=True)
        time.sleep(0.4)
        st.session_state.loading = False
        st.rerun()
   
    # Using CSS Grid for perfect row layout on all devices
    st.markdown('<div class="checklist-grid">', unsafe_allow_html=True)
   
    for idx, row in zone_df.iterrows():
        if row["Flag"] == 0:
            # Pending item with button
            button_key = f"tick_{row['Dept_Name']}_{row['AisleBay']}_{idx}"
           
            # Start grid item
            st.markdown(f'''
            <div class="checklist-item">
                <div class="dept-name">{row['Dept_Name']}</div>
                <div class="aisle-bay">{row['AisleBay']}</div>
                <div id="btn-container-{idx}" style="width:100%"></div>
            </div>
            ''', unsafe_allow_html=True)
           
            # Add actual button using Streamlit (will appear in the third column)
            col1, col2, col3 = st.columns([2, 1, 1])
            with col3:
                if st.button("✓ Tick", key=button_key, use_container_width=True):
                    st.session_state.df.loc[idx, "Flag"] = 1
                    st.session_state.loading = True
                    st.rerun()
           
            # Hide the Streamlit columns but keep button functional
            st.markdown('''
            <style>
            div[data-testid="column"]:has(button) {
                margin-top: -65px !important;
                margin-bottom: 0 !important;
            }
            .stButton button {
                position: relative;
                z-index: 10;
            }
            </style>
            ''', unsafe_allow_html=True)
           
        else:
            # Completed item with DONE badge
            st.markdown(f'''
            <div class="checklist-item">
                <div class="dept-name">{row['Dept_Name']}</div>
                <div class="aisle-bay">{row['AisleBay']}</div>
                <div class="done-badge">✓ DONE</div>
            </div>
            ''', unsafe_allow_html=True)
   
    st.markdown('</div>', unsafe_allow_html=True)
 
else:
    if st.session_state.selected_zone == "-- Select Zone --":
        st.info("👈 Please select a zone from the dropdown to view tasks")
    else:
        st.info("No tasks found for the selected zone")
