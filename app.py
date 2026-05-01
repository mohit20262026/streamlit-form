import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import textwrap
import time
 
SHEET_NAME = "aislebay_data"
WORKSHEET_NAME = "Sheet1"
 
# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Zone Task Manager",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ---------- CSS WITH NEW COLORS, LOADING & HOVER ----------
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
       
        /* Shine Animation for Stats Card */
        @keyframes shine {
            0% {
                background-position: -100% 0;
            }
            100% {
                background-position: 200% 0;
            }
        }
       
        .stats-card {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
       
        .stats-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg,
                transparent,
                rgba(255,255,255,0.3),
                transparent);
            animation: shine 1.5s ease-in-out;
        }
       
        /* Blink Animations */
        @keyframes blinkRed {
            0% { border-color: #ff0000; box-shadow: 0 0 0px rgba(255,0,0,0.2); }
            50% { border-color: #ff4444; box-shadow: 0 0 20px rgba(255,0,0,0.8); }
            100% { border-color: #ff0000; box-shadow: 0 0 0px rgba(255,0,0,0.2); }
        }
       
        @keyframes blinkGreen {
            0% { border-color: #00ff00; box-shadow: 0 0 0px rgba(0,255,0,0.2); }
            50% { border-color: #44ff44; box-shadow: 0 0 20px rgba(0,255,0,0.8); }
            100% { border-color: #00ff00; box-shadow: 0 0 0px rgba(0,255,0,0.2); }
        }
       
        .blink-red {
            animation: blinkRed 0.5s ease-in-out 3;
        }
       
        .blink-green {
            animation: blinkGreen 0.5s ease-in-out 2;
        }
       
        /* Button Hover Effect */
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
       
        /* Card Hover Effect */
        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
       
        /* Table Row Hover */
        .grid-cell {
            transition: all 0.3s ease;
        }
       
        .grid-row:hover .grid-cell {
            background: rgba(255,107,107,0.05);
        }
       
        /* Select Box Hover */
        div[data-baseweb="select"] {
            transition: all 0.3s ease !important;
        }
       
        div[data-baseweb="select"]:hover {
            border-color: #FF6B6B !important;
            box-shadow: 0 0 10px rgba(255,107,107,0.2) !important;
        }
       
        /* TABLE HEADER CENTERING - DARK GRAY BACKGROUND */
        .stHorizontalBlock {
            gap: 0px !important;
        }
       
        /* Header styling with perfect centering */
        .header-cell {
            background-color: #2d2d2d !important;
            color: white !important;
            height: 70px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            border: 1px solid #e0e0e0 !important;
            font-weight: bold !important;
            font-size: 16px !important;
            margin: 0 !important;
            padding: 0 !important;
        }
       
        /* Data cell styling */
        .data-cell {
            height: 70px !important;
            display: flex !important;
            align-items: center !important;
            border: 1px solid #e0e0e0 !important;
            background-color: white !important;
            margin: 0 !important;
        }
       
        .center-data {
            justify-content: center !important;
            text-align: center !important;
        }
       
        .left-data {
            justify-content: flex-start !important;
            padding-left: 20px !important;
        }
       
        .done-cell {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
            color: white !important;
            width: 100%;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            font-weight: bold;
        }
       
        @media (max-width: 768px) {
            .stColumn {
                min-width: 100px !important;
            }
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
 
# ---------- SESSION STATE ----------
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = None
 
if "show_blink" not in st.session_state:
    st.session_state.show_blink = "red"
 
if "needs_selection" not in st.session_state:
    st.session_state.needs_selection = True
 
if "loading" not in st.session_state:
    st.session_state.loading = False
 
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
 
# ---------- CONNECTION ----------
def get_worksheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes,
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open(SHEET_NAME)
    return spreadsheet.worksheet(WORKSHEET_NAME)
 
# ---------- TEST BUTTON ----------
if st.sidebar.button("Test Google Sheet Connection"):
    ws = get_worksheet()
    ws.update_acell("H1", "Streamlit connection working")
    st.success("Connection test successful. Check cell H1 in your Google Sheet.")
 
# ---------- LOAD DATA ----------
@st.cache_data(ttl=5)
def load_data():
    ws = get_worksheet()
    records = ws.get_all_records()
    df = pd.DataFrame(records)
   
    if df.empty:
        st.error("Google Sheet is empty or not readable")
        st.stop()
   
    df["Flag"] = df["Flag"].fillna(0).astype(int)
    df["Checked"] = df["Flag"].eq(1)
    return df
 
# ---------- SAVE DATA ----------
def save_data(df):
    ws = get_worksheet()
    output = df.drop(columns=["Checked"], errors="ignore")
    output["Flag"] = output["Flag"].astype(int)
    ws.clear()
    ws.update([output.columns.tolist()] + output.values.tolist())
 
# ---------- MAIN ----------
df = load_data()
zones = sorted(df["Zone"].dropna().unique())
zone_options = ["-- Select Zone --"] + zones
 
# ---------- NAVBAR ----------
LOGO_URL = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
 
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
 
# Zone Selection - Navbar style
col1, col2, col3, col4, col5 = st.columns([0.5, 1.2, 2, 1.5, 1])
 
with col1:
    st.image(LOGO_URL, width=28)
   
with col2:
    st.markdown("""
        <span style="
            font-size: 18px;
            font-weight: 600;
            background: linear-gradient(135deg, #FF6B6B, #FF8E53);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        ">Zone Manager</span>
    """, unsafe_allow_html=True)
 
with col4:
    blink_class = ""
    if st.session_state.show_blink == "red" and st.session_state.needs_selection:
        blink_class = "blink-red"
    elif st.session_state.show_blink == "green":
        blink_class = "blink-green"
   
    if blink_class:
        st.markdown(f"""
            <style>
                div[data-baseweb="select"] {{
                    animation: {blink_class} 0.5s ease-in-out 3;
                }}
            </style>
        """, unsafe_allow_html=True)
   
    st.session_state.selected_zone = st.selectbox(
        "Select Zone",
        zone_options,
        index=0,
        label_visibility="collapsed",
        key="zone_selector"
    )
   
    if st.session_state.selected_zone != "-- Select Zone --":
        if st.session_state.selected_zone != st.session_state.selected_zone:
            st.session_state.selected_zone = st.session_state.selected_zone
            st.session_state.needs_selection = False
            st.session_state.show_blink = "green"
            st.session_state.data_loaded = False
            st.rerun()
    else:
        st.session_state.selected_zone = None
        st.session_state.needs_selection = True
 
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
 
if st.session_state.selected_zone == "-- Select Zone --":
    st.stop()
 
if st.session_state.selected_zone is None:
    st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; min-height: 400px; text-align: center;">
            <div>
                <h1 style="color: #FF6B6B; font-size: 48px;">🎯</h1>
                <h2>Please Select a Zone 👆</h2>
                <p>Choose a zone from the dropdown above</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()
 
# Loading Spinner
if st.session_state.loading:
    st.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading zone data...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.loading = False
 
zone_df = df[df["Zone"] == st.session_state.selected_zone].copy()
 
st.sidebar.success(f"📍 Zone: {st.session_state.selected_zone}")
st.sidebar.info(f"📊 Total Records: {len(df)}")
 
if not zone_df.empty:
    store = zone_df["Store"].iloc[0]
    captain = zone_df["Captain"].iloc[0]
   
    total = len(zone_df)
    done = len(zone_df[zone_df["Flag"] == 1])
    pending = len(zone_df[zone_df["Flag"] == 0])
   
    # Stats Cards with light gray header and shine animation
    html = f"""
    <div class="stats-card" style="
        background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
        border-radius:16px;
        padding:20px 25px;
        margin-bottom:25px;
        box-shadow:0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #d0d0d0;
    ">
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        flex-wrap:wrap;
        gap:20px;
    ">
    <div style="display:flex; gap:140px; flex-wrap:wrap;">
        <div>
            <div style="color: #666; font-size:18px; font-weight:700;">📍 ZONE</div>
            <div style="color: #333; font-size:22px; font-weight:700;">
                {st.session_state.selected_zone}
            </div>
        </div>
        <div>
            <div style="color: #666; font-size:18px; font-weight:700;">🏬 STORE</div>
            <div style="color: #333; font-size:22px; font-weight:700;">
                {store}
            </div>
        </div>
        <div>
            <div style="color: #666; font-size:18px; font-weight:700;">👤 CAPTAIN</div>
            <div style="color: #333; font-size:22px; font-weight:700;">
                {captain}
            </div>
        </div>
    </div>
    <div style="
        display:flex;
        gap:15px;
        background: rgba(0,0,0,0.05);
        padding:10px 18px;
        border-radius:12px;
    ">
        <div style="text-align:center;">
            <div style="color: #666; font-size:12px;">📊 TOTAL</div>
            <div style="color: #333; font-weight:800; font-size:24px;">{total}</div>
        </div>
        <div style="text-align:center;">
            <div style="color: #666; font-size:12px;">✅ DONE</div>
            <div style="color: #22c55e; font-weight:800; font-size:24px;">{done}</div>
        </div>      
        <div style="text-align:center;">
            <div style="color: #666; font-size:12px;">⏳ PENDING</div>
            <div style="color: #f59e0b; font-weight:800; font-size:24px;">{pending}</div>
        </div>
    </div>
    </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
   
    st.subheader("Aisle Bay Checklist")
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # LOOP THROUGH EACH ROW TO CREATE ULTRA-COMPACT CARDS
    for idx, row in zone_df.iterrows():
        # Using a main column group to constrain the total width of the content
        # [2, 3] ratio means the content only takes up about 40% of the screen width
        col_main, col_empty_space = st.columns([2, 3])

        with col_main:
            # 1. Department Name
            st.markdown(f"""
                <div style="
                    font-size: 16px; 
                    font-weight: 700; 
                    color: #2d2d2d; 
                    margin-bottom: 8px;
                    margin-top: 10px;
                    padding-left: 8px;
                    border-left: 4px solid #FF6B6B;
                ">
                    {row['Dept_Name']}
                </div>
            """, unsafe_allow_html=True)

            # 2. Row for Aisle Bay and Action Button
            col_left, col_right = st.columns([1, 1.2])

            with col_left:
                # Aisle Bay Box
                st.markdown(f"""
                    <div style="
                        height: 38px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background-color: white;
                        border: 1px solid #e0e0e0;
                        border-radius: 6px;
                        font-size: 14px;
                        font-weight: 600;
                        color: #333;
                    ">
                        {row['AisleBay']}
                    </div>
                """, unsafe_allow_html=True)

            with col_right:
                # Action Button or Done Status
                if row["Flag"] == 0:
                    if st.button("✓ Tick", key=f"tick_{idx}", use_container_width=True):
                        st.session_state.loading = True
                        df.loc[(df["Zone"] == st.session_state.selected_zone) & (df["AisleBay"] == row["AisleBay"]), "Flag"] = 1
                        save_data(df)
                        st.cache_data.clear()
                        st.rerun()
                else:
                    st.markdown(
                        f"""
                        <div style="
                            height: 38px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                            color: white;
                            border-radius: 6px;
                            font-weight: bold;
                            font-size: 12px;
                        ">
                            ✓ DONE
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # 3. Shortened Divider Line
            # This is now inside 'col_main', so its length matches the boxes above perfectly
            st.markdown("<hr style='margin: 15px 0 5px 0; border: 0.5px solid #e0e0e0; width: 100%;'>", unsafe_allow_html=True)

