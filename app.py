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
 
# ---------- OLD CSS STYLE (EXACT SAME) ----------
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
        flex: 1;
    }
 
    /* 4. BUTTON & DONE BADGE STYLES */
    .action-container {
        flex: 1;
        display: flex;
        align-items: center;
    }
   
    /* Streamlit Button Override - Match Done badge exactly */
    .stButton {
        width: 100%;
        display: block;
    }
   
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
        color: white !important;
        border: none !important;
        width: 44% !important;
        height: 38px !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        cursor: pointer !important;
        transition: opacity 0.2s !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        position: absolute;
        top: -60px;
        left: 195px;
        line-height: 1 !important;
    }
   
    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }
   
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
 
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
        width: 100%;
    }
   
    /* Stats Card Styles */
    .stats-card {
        background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #d0d0d0;
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
 
# ---------- HANDLE TICK CLICK ----------
if "tick_id" in st.query_params:
    idx_to_update = int(st.query_params["tick_id"])
    st.session_state.df.loc[idx_to_update, "Flag"] = 1
    st.query_params.clear()
    st.rerun()
 
# ---------- NAVBAR ----------
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
 
df_temp = st.session_state.df
store_title = df_temp.iloc[0]["Store"] if not df_temp.empty else "N/A"
 
with st.container():
    st.markdown(f'''
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
<img src="{LOGO_URL}" width="26">
<span style="font-size: 20px; font-weight: 700; background: linear-gradient(135deg, #FF6B6B, #FF8E53); -webkit-background-clip: text; background-clip: text; color: transparent; white-space: nowrap;">Store - {store_title}</span>
</div>
    ''', unsafe_allow_html=True)
   
    selected_zone_val = st.selectbox(
        "Select Zone",
        ["-- Select Zone --", "Zone-1"],
        index=1,
        label_visibility="collapsed",
        key="zone_selector"
    )
    if selected_zone_val != st.session_state.selected_zone:
        st.session_state.selected_zone = selected_zone_val
        st.rerun()
 
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
 
# ---------- STATS CARD ----------
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
<div class="stats-card">
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
<div style="display: flex; justify-content: space-around; background: rgba(0,0,0,0.03); padding: 10px; border-radius: 8px;">
<div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">📊 TOTAL</div><div style="color: #333; font-weight: 800; font-size: 18px;">{total}</div></div>
<div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">✅ DONE</div><div style="color: #22c55e; font-weight: 800; font-size: 18px;">{done}</div></div>      
<div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">⏳ PENDING</div><div style="color: #f59e0b; font-weight: 800; font-size: 18px;">{pending}</div></div>
</div>
</div>
        """
        st.markdown(html, unsafe_allow_html=True)
 
# ---------- CHECKLIST SECTION ----------
col_main, _ = st.columns([1.5, 3])
 
with col_main:
    if st.session_state.selected_zone != "-- Select Zone --" and not zone_df.empty:
        st.subheader("Tasks")
       
        # Show loading spinner if updating
        if st.session_state.loading:
            with st.spinner("Updating..."):
                time.sleep(0.5)
                st.session_state.loading = False
       
        for idx, row in zone_df.iterrows():
            if row["Flag"] == 0:
                # Pending task - with button properly aligned
                st.markdown(f'''
<div class="checklist-item">
<div class="dept-row">{row['Dept_Name']}</div>
<div class="details-row">
<div class="aisle-bay-label">{row['AisleBay']}</div>
<div class="action-container">
<div id="btn_container_{idx}" style="width:100%"></div>
</div>
</div>
</div>
                ''', unsafe_allow_html=True)
               
                # Streamlit button (now properly aligned with Done badge)
                button_key = f"tick_{row['Dept_Name']}_{row['AisleBay']}_{idx}"
                if st.button("✓ Tick", key=button_key, use_container_width=True):
                    st.session_state.df.loc[idx, "Flag"] = 1
                    st.session_state.loading = True
                    st.rerun()
                   
            else:
                # Completed task - Done badge
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
   
    else:
        if st.session_state.selected_zone == "-- Select Zone --":
            st.info("👈 Please select a zone from the dropdown to view tasks")
        else:
            st.info("No tasks found for the selected zone")
