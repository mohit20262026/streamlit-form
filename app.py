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

# ---------- CSS ----------
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
        
        .stButton > button {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 5px 16px !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(255,107,107,0.4) !important;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------- HARDCODED DATA (STATIC TESTING) ----------
if "df" not in st.session_state:
    data = [
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Toothpaste", "AisleBay": 1016, "Flag": 1},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Rice", "AisleBay": 10987, "Flag": 1},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Frozen", "AisleBay": 19363, "Flag": 1},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Pulses", "AisleBay": 23476, "Flag": 1},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Eggs", "AisleBay": 78365, "Flag": 0},
        {"Zone": "Zone-1", "Store": "NSP", "Captain": "AMIT", "Dept_Name": "Coldrink", "AisleBay": 87523, "Flag": 0},
    ]
    st.session_state.df = pd.DataFrame(data)

if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "Zone-1"

if "loading" not in st.session_state:
    st.session_state.loading = False

# ---------- NAVBAR (KEEPING ORIGINAL RATIO) ----------
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

col_nav_main, col_nav_empty = st.columns([2, 3])
with col_nav_main:
    nav_left, nav_right = st.columns([1.5, 1])
    with nav_left:
        st.markdown(f'<div style="display: flex; align-items: center; gap: 10px;"><img src="{LOGO_URL}" width="28"><span style="font-size: 18px; font-weight: 600; background: linear-gradient(135deg, #FF6B6B, #FF8E53); -webkit-background-clip: text; background-clip: text; color: transparent;">Zone Manager</span></div>', unsafe_allow_html=True)
    with nav_right:
        st.selectbox("Select Zone", ["-- Select Zone --", "Zone-1"], index=1, label_visibility="collapsed")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ---------- STATS CARD (KEEPING ORIGINAL RATIO) ----------
col_stats_main, col_stats_empty = st.columns([2, 3])
with col_stats_main:
    df = st.session_state.df
    zone_df = df[df["Zone"] == st.session_state.selected_zone].copy()
    
    if not zone_df.empty:
        total, done, pending = len(zone_df), len(zone_df[zone_df["Flag"] == 1]), len(zone_df[zone_df["Flag"] == 0])
        html = f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #f5f5f5, #e8e8e8); border-radius:12px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #d0d0d0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid #dcdcdc; padding-bottom: 10px;">
                <div><div style="color: #666; font-size: 11px; font-weight: 700;">📍 ZONE</div><div style="color: #333; font-size: 15px; font-weight: 700;">Zone-1</div></div>
                <div><div style="color: #666; font-size: 11px; font-weight: 700;">🏬 STORE</div><div style="color: #333; font-size: 15px; font-weight: 700;">NSP</div></div>
                <div><div style="color: #666; font-size: 11px; font-weight: 700;">👤 CAPTAIN</div><div style="color: #333; font-size: 15px; font-weight: 700;">AMIT</div></div>
            </div>
            <div style="display: flex; justify-content: space-around; background: rgba(0,0,0,0.03); padding: 10px; border-radius: 8px;">
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">📊 TOTAL</div><div style="color: #333; font-weight: 800; font-size: 18px;">{total}</div></div>
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">✅ DONE</div><div style="color: #22c55e; font-weight: 800; font-size: 18px;">{done}</div></div>      
                <div style="text-align:center;"><div style="color: #666; font-size: 10px; font-weight: 600;">⏳ PENDING</div><div style="color: #f59e0b; font-weight: 800; font-size: 18px;">{pending}</div></div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

# ---------- CHECKLIST SECTION (HALVED LENGTH) ----------
st.subheader("Aisle Bay Checklist")

if st.session_state.loading:
    st.markdown('<div class="loading-container"><div class="loading-spinner"></div><p>Updating...</p></div>', unsafe_allow_html=True)
    time.sleep(0.4)
    st.session_state.loading = False

for idx, row in zone_df.iterrows():
    # CHANGED RATIO: [1, 4] makes the content column much narrower (half length)
    col_item_main, col_item_empty = st.columns([1, 4])
    
    with col_item_main:
        # Department Name
        st.markdown(f'<div style="font-size: 15px; font-weight: 700; color: #2d2d2d; margin-bottom: 8px; margin-top: 10px; padding-left: 8px; border-left: 4px solid #FF6B6B;">{row["Dept_Name"]}</div>', unsafe_allow_html=True)

        # Aisle and Button Row
        c_left, c_right = st.columns([1, 1.2])
        with c_left:
            st.markdown(f'<div style="height: 36px; display: flex; align-items: center; justify-content: center; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 13px; font-weight: 600; color: #333;">{row["AisleBay"]}</div>', unsafe_allow_html=True)
        
        with c_right:
            if row["Flag"] == 0:
                if st.button("✓ Tick", key=f"tick_{idx}", use_container_width=True):
                    st.session_state.loading = True
                    st.session_state.df.at[idx, "Flag"] = 1
                    st.rerun()
            else:
                st.markdown('<div style="height: 36px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; border-radius: 6px; font-weight: bold; font-size: 11px;">✓ DONE</div>', unsafe_allow_html=True)
        
        # Divider matching the halved length
        st.markdown("<hr style='margin: 12px 0 5px 0; border: 0.5px solid #e0e0e0; width: 100%;'>", unsafe_allow_html=True)
        
