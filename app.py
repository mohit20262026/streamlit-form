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

# ---------- CLEANED & CORRECTED COMPLETE CSS BLOCK ----------
# ---------- UNIFIED HTML/CSS LAYOUT ----------
hide_streamlit_style = """
    <style>
        /* 1. HIDE DEFAULTS */
        #MainMenu, footer, header, .stAppHeader, .stDeployButton, .stToolbar, .stStatusWidget {
            visibility: hidden; display: none !important;
        }
        
        .block-container { padding: 1rem !important; }

        /* 2. CARD BOX */
        .checklist-item {
            background: white;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            padding: 12px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
            width: 100%;
        }

        .dept-row {
            font-weight: 700;
            color: #1f2937;
            font-size: 16px;
            margin-bottom: 12px;
            border-left: 4px solid #FF6B6B;
            padding-left: 10px;
        }

        /* 3. ROW 2 LAYOUT (BAY & BUTTON) */
        .details-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }

        .aisle-bay-label {
            background: #f3f4f6;
            height: 38px;
            border-radius: 8px;
            font-weight: 600;
            color: #4b5563;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 1; /* Takes 50% width */
        }

        /* 4. CLICKABLE BUTTON & DONE BADGE (IDENTICAL STYLING) */
        .action-container {
            flex: 1; /* Takes 50% width */
        }

        .html-tick-btn {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            color: white !important;
            text-decoration: none !important;
            height: 38px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: opacity 0.2s;
        }

        .html-tick-btn:hover { opacity: 0.9; }

        .done-badge {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            height: 38px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
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
# ---------- NAVBAR (VERTICAL FOR MOBILE) ----------
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Get the Store Name from the first row of your data
df_temp = st.session_state.df
store_title = df_temp.iloc[0]["Store"] if not df_temp.empty else "N/A"

nav_container = st.container()

with nav_container:
    # 1. Logo and Store Name (e.g., NSP)
    st.markdown(f'''
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <img src="{LOGO_URL}" width="26">
            <span style="
                font-size: 20px; 
                font-weight: 700; 
                background: linear-gradient(135deg, #FF6B6B, #FF8E53);
                -webkit-background-clip: text; 
                background-clip: text; 
                color: transparent; 
                white-space: nowrap;
            ">Store - {store_title}</span>
        </div>
    ''', unsafe_allow_html=True)

    # 2. Zone Dropdown
    selected_zone_val = st.selectbox(
        "Select Zone",
        ["-- Select Zone --", "Zone-1"],
        index=1,
        label_visibility="collapsed",
        key="nav_zone_selector_vertical"
    )
    
    if selected_zone_val != st.session_state.selected_zone:
        st.session_state.selected_zone = selected_zone_val
        st.rerun()

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
 
# ---------- STATS CARD ----------
# ---------- STATS CARD (2-ITEM LAYOUT) ----------
# We use a narrower width [1.5, 3] to keep it compact on desktop/mobile
col_stats_main, col_stats_empty = st.columns([1.5, 3])
with col_stats_main:
    df = st.session_state.df
    if st.session_state.selected_zone != "-- Select Zone --":
        zone_df = df[df["Zone"] == st.session_state.selected_zone].copy()
    else:
        zone_df = pd.DataFrame()

    if not zone_df.empty:
        captain = zone_df.iloc[0]["Captain"]
        total, done, pending = len(zone_df), len(zone_df[zone_df["Flag"] == 1]), len(zone_df[zone_df["Flag"] == 0])
        
        html = f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #f5f5f5, #e8e8e8); border-radius:12px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #d0d0d0;">
            <!-- Top Row: Only 2 Items now (Zone and Captain) -->
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid #dcdcdc; padding-bottom: 10px;">
                <div>
                    <div style="color: #666; font-size: 11px; font-weight: 700;">📍 ZONE</div>
                    <div style="color: #333; font-size: 15px; font-weight: 700;">{st.session_state.selected_zone}</div>
                </div>
                <div>
                    <div style="color: #666; font-size: 11px; font-weight: 700;">👤 CAPTAIN</div>
                    <div style="color: #333; font-size: 15px; font-weight: 700;">{captain}</div>
                </div>
            </div>
            <!-- Bottom Row: Metrics remain the same -->
            <div style="display: flex; justify-content: space-around; background: rgba(0,0,0,0.03); padding: 10px; border-radius: 8px;">
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">📊 TOTAL</div><div style="color: #333; font-weight: 800; font-size: 18px;">{total}</div></div>
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">✅ DONE</div><div style="color: #22c55e; font-weight: 800; font-size: 18px;">{done}</div></div>      
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">⏳ PENDING</div><div style="color: #f59e0b; font-weight: 800; font-size: 18px;">{pending}</div></div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

# ---------- CHECKLIST SECTION - CORRECTED ALIGNMENT ----------
# --- 1. CLICK HANDLER (Place this at the very top of your code) ---
# This catches the ID from the URL, updates the DF, then clears the URL
if "tick_id" in st.query_params:
    idx_to_update = int(st.query_params["tick_id"])
    st.session_state.df.loc[idx_to_update, "Flag"] = 1
    st.query_params.clear() # Removes the parameter to prevent repeat triggers
    st.rerun()

# --- 2. UPDATED CHECKLIST SECTION ---
col_main, _ = st.columns([1.5, 3])

with col_main:
    if st.session_state.selected_zone != "-- Select Zone --" and not zone_df.empty:
        st.subheader("Tasks")

        for idx, row in zone_df.iterrows():
            if row["Flag"] == 0:
                # PURE HTML BUTTON (using <a> tag for click functionality)
                st.markdown(f'''
                <div class="checklist-item">
                    <div class="dept-row">{row['Dept_Name']}</div>
                    <div class="details-row">
                        <div class="aisle-bay-label">{row['AisleBay']}</div>
                        <div class="action-container">
                            <a href="/?tick_id={idx}" target="_self" class="html-tick-btn">✓ Tick</a>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                # PURE HTML DONE BADGE
                st.markdown(f'''
                <div class="checklist-item">
                    <div class="dept-row">{row['Dept_Name']}</div>
                    <div class="details-row">
                        <div class="aisle-bay-label">{row['AisleBay']}</div>
                        <div class="action-container">
                            <div class="done-badge">✓ DONE</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
