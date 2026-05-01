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

# ---------- CSS (UNCHANGED) ----------
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
        
        /* Loading Spinner */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
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
    # Data exactly as shown in your images
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
    st.session_state.selected_zone = None

if "loading" not in st.session_state:
    st.session_state.loading = False

# ---------- NAVBAR ----------
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Navbar restricted to [2, 3] ratio for alignment
col_main, col_empty_space = st.columns([2, 3])

with col_main:
    nav_col_left, nav_col_right = st.columns([1.5, 1])
    with nav_col_left:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="{LOGO_URL}" width="28">
                <span style="font-size: 18px; font-weight: 600; background: linear-gradient(135deg, #FF6B6B, #FF8E53);
                    -webkit-background-clip: text; background-clip: text; color: transparent;">Zone Manager</span>
            </div>
        """, unsafe_allow_html=True)

    with nav_col_right:
        # Static options for testing
        zone_options = ["-- Select Zone --", "Zone-1"]
        selected_zone_val = st.selectbox("Select Zone", zone_options, index=1, label_visibility="collapsed")
        
        if selected_zone_val != "-- Select Zone --":
            st.session_state.selected_zone = selected_zone_val
        else:
            st.session_state.selected_zone = None

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

if st.session_state.selected_zone is None:
    st.stop()

# Loading Spinner logic
if st.session_state.loading:
    st.markdown('<div class="loading-container"><div class="loading-spinner"></div><p>Processing...</p></div>', unsafe_allow_html=True)
    time.sleep(0.5)
    st.session_state.loading = False

# Filter data based on selection
df = st.session_state.df
zone_df = df[df["Zone"] == st.session_state.selected_zone].copy()

# ---------- CONSTRAINED STATS CARD ----------
col_stats, col_stats_empty = st.columns([2, 3])

with col_stats:
    if not zone_df.empty:
        store = zone_df["Store"].iloc[0]
        captain = zone_df["Captain"].iloc[0]
        total = len(zone_df)
        done = len(zone_df[zone_df["Flag"] == 1])
        pending = len(zone_df[zone_df["Flag"] == 0])

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

# ---------- CHECKLIST SECTION ----------
st.subheader("Aisle Bay Checklist")

for idx, row in zone_df.iterrows():
    col_item, col_item_empty = st.columns([2, 3])
    
    with col_item:
        # Department Name
        st.markdown(f"""
            <div style="font-size: 16px; font-weight: 700; color: #2d2d2d; margin-bottom: 8px; margin-top: 10px; padding-left: 8px; border-left: 4px solid #FF6B6B;">
                {row['Dept_Name']}
            </div>
        """, unsafe_allow_html=True)

        # Aisle and Button Row
        c_left, c_right = st.columns([1, 1.2])
        with c_left:
            st.markdown(f"""
                <div style="height: 38px; display: flex; align-items: center; justify-content: center; background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; font-size: 14px; font-weight: 600; color: #333;">
                    {row['AisleBay']}
                </div>
            """, unsafe_allow_html=True)
        
        with c_right:
            if row["Flag"] == 0:
                if st.button("✓ Tick", key=f"tick_{idx}", use_container_width=True):
                    st.session_state.loading = True
                    # Update the dataframe in session state
                    st.session_state.df.at[idx, "Flag"] = 1
                    st.rerun()
            else:
                st.markdown("""
                    <div style="height: 38px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; border-radius: 6px; font-weight: bold; font-size: 12px;">
                        ✓ DONE
                    </div>
                """, unsafe_allow_html=True)
        
        # Matching Shortened Divider
        st.markdown("<hr style='margin: 15px 0 5px 0; border: 0.5px solid #e0e0e0; width: 100%;'>", unsafe_allow_html=True)
