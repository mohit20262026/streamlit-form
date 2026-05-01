import streamlit as st
import pandas as pd
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
 
# ---------- CSS (UNCHANGED) ----------
hide_streamlit_style = """
<style>
/* KEEPING YOUR ORIGINAL CSS EXACTLY SAME */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {padding-top: 2rem;}
.header-cell {
    background-color: #2d2d2d;
    color: white;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}
.data-cell {
    height: 70px;
    display: flex;
    align-items: center;
    border: 1px solid #e0e0e0;
}
.center-data {justify-content: center;}
.left-data {justify-content: flex-start; padding-left: 20px;}
.done-cell {
    background: linear-gradient(135deg, #11998e, #38ef7d);
    color: white;
    width: 100%;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
 
# ---------- SESSION STATE ----------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Zone": ["Zone-1"] * 6,
        "Store": ["NSP"] * 6,
        "Captain": ["AMIT"] * 6,
        "AisleBay": [1016, 10987, 19363, 23476, 78365, 87523],
        "Dept_Name": ["Toothpaste", "Rice", "Frozen", "Pulses", "Eggs", "Coldrink"],
        "Flag": [1, 1, 1, 1, 0, 0]
    })
 
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "Zone-1"
 
if "loading" not in st.session_state:
    st.session_state.loading = False
 
# ---------- LOAD DATA ----------
def load_data():
    df = st.session_state.df.copy()
    df["Checked"] = df["Flag"] == 1
    return df
 
# ---------- SAVE DATA ----------
def save_data(df):
    st.session_state.df = df.copy()
 
# ---------- MAIN ----------
df = load_data()
 
zones = sorted(df["Zone"].unique())
st.session_state.selected_zone = zones[0]
 
zone_df = df[df["Zone"] == st.session_state.selected_zone].copy()
 
store = zone_df["Store"].iloc[0]
captain = zone_df["Captain"].iloc[0]
 
total = len(zone_df)
done = len(zone_df[zone_df["Flag"] == 1])
pending = len(zone_df[zone_df["Flag"] == 0])
 
# ---------- HEADER (SAME STYLE) ----------
st.markdown(f"""
<div style="background:#f5f5f5;padding:20px;border-radius:12px;">
<h3>📍 Zone: {st.session_state.selected_zone} | 🏬 Store: {store} | 👤 Captain: {captain}</h3>
<p>📊 Total: {total} | ✅ Done: {done} | ⏳ Pending: {pending}</p>
</div>
""", unsafe_allow_html=True)
 
st.markdown("## Aisle Bay Checklist")
 
# ---------- TABLE HEADER ----------
col_h1, col_h2, col_h3 = st.columns([1, 3, 1.5])
 
with col_h1:
    st.markdown('<div class="header-cell">Aisle Bay</div>', unsafe_allow_html=True)
 
with col_h2:
    st.markdown('<div class="header-cell">Department</div>', unsafe_allow_html=True)
 
with col_h3:
    st.markdown('<div class="header-cell">Action</div>', unsafe_allow_html=True)
 
# ---------- TABLE ----------
for idx, row in zone_df.iterrows():
    col1, col2, col3 = st.columns([1, 3, 1.5])
 
    with col1:
        st.markdown(f'<div class="data-cell center-data">{row["AisleBay"]}</div>', unsafe_allow_html=True)
 
    with col2:
        st.markdown(f'<div class="data-cell left-data">{row["Dept_Name"]}</div>', unsafe_allow_html=True)
 
    with col3:
        if row["Flag"] == 0:
            if st.button("✓ Tick", key=f"tick_{idx}", use_container_width=True):
                st.session_state.loading = True
                df.loc[idx, "Flag"] = 1
                save_data(df)
                st.rerun()
        else:
            st.markdown(
                '<div class="data-cell center-data"><div class="done-cell">✓ DONE</div></div>',
                unsafe_allow_html=True
            )
 
# ---------- LOADING ----------
if st.session_state.loading:
    with st.spinner("Updating..."):
        time.sleep(1)
        st.session_state.loading = False
