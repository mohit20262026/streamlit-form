import streamlit as st
import pandas as pd
import textwrap
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Zone Task Manager",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- CSS (YOUR ORIGINAL - UNCHANGED) ----------
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
        }

        .data-cell {
            height: 70px !important;
            display: flex !important;
            align-items: center !important;
            border: 1px solid #e0e0e0 !important;
            background-color: white !important;
        }
        /* Remove gap between columns completely */
        div[data-testid="column"] {
            padding: 0px !important;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 0px !important;
        }

        .center-data {
            justify-content: center !important;
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
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------- HARDCODED DATA ----------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Zone": ["Zone-1"] * 6,
        "Store": ["NSP"] * 6,
        "Captain": ["AMIT"] * 6,
        "AisleBay": [1016, 10987, 19363, 23476, 78365, 87523],
        "Dept_Name": ["Toothpaste", "Rice", "Frozen", "Pulses", "Eggs", "Coldrink"],
        "Flag": [1, 1, 1, 1, 0, 0]
    })

df = st.session_state.df

# ---------- ZONE ----------
selected_zone = "Zone-1"
zone_df = df[df["Zone"] == selected_zone].copy()

# ---------- STATS ----------
store = zone_df["Store"].iloc[0]
captain = zone_df["Captain"].iloc[0]

total = len(zone_df)
done = len(zone_df[zone_df["Flag"] == 1])
pending = len(zone_df[zone_df["Flag"] == 0])

# ---------- HEADER CARD (SAME LOOK) ----------
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
    border-radius:16px;
    padding:20px 25px;
    margin-bottom:25px;
    box-shadow:0 10px 25px rgba(0,0,0,0.05);
    border: 1px solid #d0d0d0;
">
<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
<div style="display:flex; gap:140px;">

<div>
<div style="color:#666; font-size:18px; font-weight:700;">📍 ZONE</div>
<div style="color:#333; font-size:22px; font-weight:700;">{selected_zone}</div>
</div>

<div>
<div style="color:#666; font-size:18px; font-weight:700;">🏬 STORE</div>
<div style="color:#333; font-size:22px; font-weight:700;">{store}</div>
</div>

<div>
<div style="color:#666; font-size:18px; font-weight:700;">👤 CAPTAIN</div>
<div style="color:#333; font-size:22px; font-weight:700;">{captain}</div>
</div>

</div>

<div style="display:flex; gap:15px; background: rgba(0,0,0,0.05); padding:10px 18px; border-radius:12px;">

<div style="text-align:center;">
<div style="font-size:12px;">📊 TOTAL</div>
<div style="font-size:24px; font-weight:800;">{total}</div>
</div>

<div style="text-align:center;">
<div style="font-size:12px;">✅ DONE</div>
<div style="font-size:24px; font-weight:800; color:#22c55e;">{done}</div>
</div>

<div style="text-align:center;">
<div style="font-size:12px;">⏳ PENDING</div>
<div style="font-size:24px; font-weight:800; color:#f59e0b;">{pending}</div>
</div>

</div>
</div>
</div>
""", unsafe_allow_html=True)

st.subheader("Aisle Bay Checklist")

# ---------- TABLE HEADER ----------
col_h1, col_h2, col_h3 = st.columns([1, 3, 1.2], gap="small")

with col_h1:
    st.markdown('<div class="header-cell">Aisle Bay</div>', unsafe_allow_html=True)

with col_h2:
    st.markdown('<div class="header-cell">Department</div>', unsafe_allow_html=True)

with col_h3:
    st.markdown('<div class="header-cell">Action</div>', unsafe_allow_html=True)

# ---------- TABLE ROWS ----------
for idx, row in zone_df.iterrows():
    col1, col2, col3 = st.columns([1, 3, 1.2], gap="small")

    with col1:
        st.markdown(f'<div class="data-cell center-data">{row["AisleBay"]}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="data-cell left-data">{row["Dept_Name"]}</div>', unsafe_allow_html=True)

    with col3:
        if row["Flag"] == 0:
            if st.button("✓ Tick", key=f"tick_{idx}", use_container_width=True):
                df.loc[idx, "Flag"] = 1
                st.session_state.df = df
                st.rerun()
        else:
            st.markdown(
                '<div class="data-cell center-data"><div class="done-cell">✓ DONE</div></div>',
                unsafe_allow_html=True
            )
