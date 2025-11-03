# checklist_monitor.py
"""
CheckList – Professional Equipment Monitoring Platform
Enhanced with modern features and refined design

Run: streamlit run checklist_monitor.py
"""

from pathlib import Path
from datetime import datetime, time, timedelta
import json
import shutil
import tempfile
import zipfile
import os

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -------------------- Configuration --------------------
APP_TITLE = "CheckList"
APP_SUBTITLE = "Equipment Monitoring Platform"
PAGE_ICON = "◆"
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- Enhanced Professional Design --------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #fafbfc;
        --bg-tertiary: #f4f6f8;
        --surface: #ffffff;
        --surface-hover: #f8f9fa;
        --accent-primary: #2563eb;
        --accent-secondary: #1e40af;
        --accent-light: #eff6ff;
        --accent-lighter: #dbeafe;
        --text-primary: #111827;
        --text-secondary: #4b5563;
        --text-muted: #9ca3af;
        --border: #e5e7eb;
        --border-strong: #d1d5db;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --info: #3b82f6;
        --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --spacing-xs: 0.375rem;
        --spacing-sm: 0.625rem;
        --spacing-md: 0.875rem;
        --spacing-lg: 1.25rem;
        --spacing-xl: 1.75rem;
        --spacing-2xl: 2.5rem;
    }
    
    * {
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
    }
    
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        color: var(--accent-primary) !important;
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.5rem !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: var(--accent-light) !important;
        border-color: var(--accent-primary) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .app-header {
        background: var(--surface);
        border-bottom: 1px solid var(--border);
        padding: 0.75rem 1.5rem;
        margin: -5rem -5rem 1.5rem;
        position: sticky;
        top: 0;
        z-index: 999;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.97);
        box-shadow: var(--shadow-xs);
    }
    
    .header-content {
        max-width: 1600px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-logo {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .logo-icon {
        font-size: 1.5rem;
        color: var(--accent-primary);
        font-weight: 700;
    }
    
    .logo-text h1 {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.02em;
    }
    
    .logo-text p {
        margin: 0;
        font-size: 0.65rem;
        color: var(--text-muted);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    .header-actions {
        display: flex;
        gap: 0.75rem;
        align-items: center;
    }
    
    .header-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.75rem;
        background: var(--accent-light);
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--accent-primary);
        border: 1px solid var(--accent-lighter);
    }
    
    .status-dot {
        width: 6px;
        height: 6px;
        background: var(--success);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    
    .time-badge {
        font-size: 0.7rem;
        color: var(--text-secondary);
        padding: 0.375rem 0.75rem;
        background: var(--bg-secondary);
        border-radius: var(--radius-sm);
        font-weight: 500;
        border: 1px solid var(--border);
    }
    
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border);
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.25rem 1rem;
    }
    
    .sidebar-header {
        padding: 1rem;
        margin: -1.25rem -1rem 1rem;
        background: var(--surface);
        border-bottom: 1px solid var(--border);
    }
    
    .sidebar-section {
        padding: 1rem 0;
        border-bottom: 1px solid var(--border);
    }
    
    .sidebar-section:last-child {
        border-bottom: none;
    }
    
    .sidebar-title {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
        padding: 0 0.5rem;
    }
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stRadio"] > label {
        background: transparent !important;
        padding: 0.625rem 0.75rem !important;
        border-radius: var(--radius-sm) !important;
        margin-bottom: 0.25rem !important;
        border: 1px solid transparent !important;
        transition: all 0.15s ease !important;
        cursor: pointer;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stRadio"] > label:hover {
        background: var(--surface) !important;
        border-color: var(--border) !important;
    }
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stRadio"] > label[data-checked="true"] {
        background: var(--accent-primary) !important;
        color: white !important;
        border-color: var(--accent-primary) !important;
        font-weight: 600 !important;
    }
    
    .main .block-container {
        padding: 1.5rem 2rem 3rem;
        max-width: 1600px;
    }
    
    .page-header {
        margin-bottom: 1.75rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    .page-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 0.375rem 0;
        letter-spacing: -0.02em;
    }
    
    .page-subtitle {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin: 0;
        font-weight: 400;
    }
    
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        box-shadow: var(--shadow-xs);
        margin-bottom: 1.25rem;
        transition: all 0.2s ease;
    }
    
    .card:hover {
        box-shadow: var(--shadow-sm);
        border-color: var(--border-strong);
    }
    
    .card-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0 0 1rem 0;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.25rem;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-primary);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.25s ease;
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--accent-primary);
        transform: translateY(-2px);
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    .metric-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    
    .metric-trend {
        font-size: 0.7rem;
        color: var(--success);
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    .stButton > button {
        background: var(--accent-primary);
        color: white;
        border: none;
        border-radius: var(--radius-sm);
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.75rem;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-xs);
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        background: var(--accent-secondary);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        color: var(--text-primary);
        padding: 0.625rem;
        transition: all 0.2s ease;
        font-size: 0.8rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 3px var(--accent-light);
        outline: none;
    }
    
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stDateInput > label,
    .stNumberInput > label,
    .stSlider > label {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.375rem;
    }
    
    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        overflow: hidden;
        font-size: 0.75rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.25rem;
        background: transparent;
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-secondary);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--surface);
        color: var(--accent-primary);
        border-bottom: 2px solid var(--accent-primary);
    }
    
    .stSuccess {
        background: #f0fdf4;
        border: 1px solid #86efac;
        border-left: 4px solid var(--success);
        border-radius: var(--radius-sm);
        padding: 0.875rem;
        color: #166534;
        font-size: 0.8rem;
    }
    
    .stWarning {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 4px solid var(--warning);
        border-radius: var(--radius-sm);
        padding: 0.875rem;
        color: #92400e;
        font-size: 0.8rem;
    }
    
    .stError {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-left: 4px solid var(--error);
        border-radius: var(--radius-sm);
        padding: 0.875rem;
        color: #991b1b;
        font-size: 0.8rem;
    }
    
    .stInfo {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 4px solid var(--info);
        border-radius: var(--radius-sm);
        padding: 0.875rem;
        color: #1e40af;
        font-size: 0.8rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.875rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        padding: 0.875rem;
        background: var(--bg-secondary);
        border-radius: var(--radius-sm);
        border: 1px solid var(--border);
        transition: all 0.2s ease;
    }
    
    .stat-item:hover {
        background: var(--surface);
        border-color: var(--border-strong);
        box-shadow: var(--shadow-sm);
    }
    
    .stat-label {
        font-size: 0.65rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.375rem;
        font-weight: 600;
    }
    
    .stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .form-section {
        background: var(--bg-secondary);
        padding: 1.25rem;
        border-radius: var(--radius-md);
        border: 1px solid var(--border);
        margin-bottom: 1rem;
    }
    
    .form-section-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border);
    }
    
    .stProgress > div > div > div {
        background: var(--accent-primary);
    }
    
    .streamlit-expanderHeader {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-primary);
        background: var(--bg-secondary);
        border-radius: var(--radius-sm);
        border: 1px solid var(--border);
    }
    
    .stDownloadButton > button {
        background: var(--success) !important;
    }
    
    .stDownloadButton > button:hover {
        background: #059669 !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-strong);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .metric-grid {
            grid-template-columns: 1fr;
        }
        .app-header {
            padding: 0.625rem 1rem;
        }
        .header-actions {
            display: none;
        }
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- Core Functions --------------------
BASE_DIR = Path.cwd()
LOG_DIR = BASE_DIR / "logs"
BACKUP_DIR = BASE_DIR / "backups"
META_FILE = BASE_DIR / "equipment_meta.json"
LOG_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

WIDE_COLUMNS = [
    "timestamp", "date", "hour",
    "equipment_type", "equipment_id",
    "pressure", "temperature", "flow_rate",
    "valve_status", "leak_observed", "tank_level",
    "operator", "note", "created_at", "version", "alarm_flag"
]

PLACEHOLDER_IDS = list(range(1, 11))

PARAM_SPECS = {
    "Pipeline": {
        "pressure": ("float", "psi", 0.0, 3000.0),
        "temperature": ("float", "°C", -40.0, 200.0),
        "flow_rate": ("float", "bbl/hr", 0.0, 100000.0),
        "valve_status": ("categorical", "state", None, None),
        "leak_observed": ("categorical", "yesno", None, None),
        "tank_level": ("float", "m", 0.0, 50.0)
    },
    "Vessel": {
        "pressure": ("float", "psi", 0.0, 5000.0),
        "temperature": ("float", "°C", -40.0, 400.0),
        "tank_level": ("float", "m", 0.0, 50.0),
        "vapor_o2": ("float", "%", 0.0, 100.0)
    },
    "Tank": {
        "tank_level": ("float", "m", 0.0, 50.0),
        "temperature": ("float", "°C", -20.0, 120.0),
        "valve_status": ("categorical", "state", None, None)
    },
    "Separator": {
        "pressure": ("float", "psi", 0.0, 5000.0),
        "oil_level": ("float", "m", 0.0, 10.0),
        "gas_flow_rate": ("float", "m³/hr", 0.0, 200000.0)
    }
}

EQUIPMENT_TYPES = list(PARAM_SPECS.keys())

def equipment_filename(equipment_type: str, equipment_id: int) -> Path:
    safe = equipment_type.replace(" ", "_")
    return LOG_DIR / f"{safe}_{int(equipment_id)}.csv"

def load_meta():
    if not META_FILE.exists():
        return {}
    try:
        return json.loads(META_FILE.read_text())
    except Exception:
        return {}

def save_meta(meta: dict):
    META_FILE.write_text(json.dumps(meta, indent=2))

meta = load_meta()

def init_equipment(equipment_type: str, equipment_id: int):
    fn = equipment_filename(equipment_type, equipment_id)
    if not fn.exists():
        pd.DataFrame(columns=WIDE_COLUMNS).to_csv(fn, index=False)
    key = f"{equipment_type}_{equipment_id}"
    if key not in meta:
        params = {}
        for p, spec in PARAM_SPECS.get(equipment_type, {}).items():
            dtype, unit, mn, mx = spec
            params[p] = {"dtype": dtype, "unit": unit, "min": mn, "max": mx}
        meta[key] = {
            "equipment_type": equipment_type,
            "equipment_id": int(equipment_id),
            "params": params,
            "created": datetime.utcnow().isoformat()
        }
        save_meta(meta)
    return fn

def load_equipment_log(equipment_type: str, equipment_id: int) -> pd.DataFrame:
    fn = equipment_filename(equipment_type, equipment_id)
    if not fn.exists():
        init_equipment(equipment_type, equipment_id)
    try:
        df = pd.read_csv(fn, parse_dates=["timestamp"])
    except Exception:
        df = pd.read_csv(fn)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    return df

def append_equipment_row(equipment_type: str, equipment_id: int, row: dict):
    fn = init_equipment(equipment_type, equipment_id)
    for c in WIDE_COLUMNS:
        if c not in row:
            row[c] = None
    df_row = pd.DataFrame([row], columns=WIDE_COLUMNS)
    header = not fn.exists() or fn.stat().st_size == 0
    df_row.to_csv(fn, mode='a', header=header, index=False)
    return True

def validate_row(equipment_type: str, row: dict):
    msgs = []
    specs = PARAM_SPECS.get(equipment_type, {})
    ok = True
    for p, spec in specs.items():
        dtype, unit, mn, mx = spec
        val = row.get(p)
        if val is None or (isinstance(val, str) and str(val).strip() == ""):
            msgs.append(f"{p} is empty")
            ok = False
            continue
        if dtype == "float":
            try:
                v = float(val)
                if mn is not None and v < mn:
                    msgs.append(f"{p}: {v} below min {mn}")
                    ok = False
                if mx is not None and v > mx:
                    msgs.append(f"{p}: {v} above max {mx}")
                    ok = False
            except Exception:
                msgs.append(f"{p}: not numeric")
                ok = False
    return ok, msgs

def detect_anomalies(equipment_type: str, df: pd.DataFrame, param: str, z_thresh: float = 3.0, window: int = 24):
    if df.empty or param not in df.columns:
        return pd.Series([False] * len(df), index=df.index)
    s = pd.to_numeric(df[param], errors='coerce')
    if s.isna().all():
        return pd.Series([False] * len(df), index=df.index)
    anomalies = pd.Series(False, index=df.index)
    key = f"{equipment_type}_{int(df['equipment_id'].iloc[0])}" if 'equipment_id' in df.columns and not df.empty else None
    mm = load_meta()
    static_min = static_max = None
    if key and key in mm and param in mm[key]['params']:
        pmeta = mm[key]['params'][param]
        static_min, static_max = pmeta.get('min'), pmeta.get('max')
    if static_min is not None:
        anomalies |= (s < static_min)
    if static_max is not None:
        anomalies |= (s > static_max)
    if s.dropna().shape[0] >= max(5, min(window, 5)):
        roll_mean = s.rolling(window=min(window, len(s)), min_periods=1).mean()
        roll_std = s.rolling(window=min(window, len(s)), min_periods=1).std().replace(0, np.nan)
        z = (s - roll_mean) / roll_std
        anomalies |= z.abs() > z_thresh
    return anomalies.fillna(False)

# -------------------- Session State --------------------
if "viz_selection" not in st.session_state:
    st.session_state.viz_selection = {"type": None, "id": None, "param": None}
if "show_details" not in st.session_state:
    st.session_state.show_details = False

# -------------------- Header --------------------
current_time = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
    <div class="app-header">
        <div class="header-content">
            <div class="header-logo">
                <div class="logo-icon">◆</div>
                <div class="logo-text">
                    <h1>CheckList</h1>
                    <p>Equipment Monitoring</p>
                </div>
            </div>
            <div class="header-actions">
                <div class="time-badge">{current_time}</div>
                <div class="header-badge">
                    <div class="status-dot"></div>
                    <span>Online</span>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    
    files = list(LOG_DIR.glob("*.csv"))
    backups = len(list(BACKUP_DIR.glob("*.csv")))
    
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 0.75rem;">
            <div style="font-size: 0.65rem; color: var(--text-muted); 
                        text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.375rem;">
                System Overview
            </div>
            <div style="display: flex; gap: 0.5rem; justify-content: center;">
                <div style="padding: 0.375rem 0.75rem; background: var(--accent-light); 
                            border-radius: var(--radius-sm); font-size: 0.7rem; font-weight: 600; 
                            color: var(--accent-primary);">
                    {len(files)} Files
                </div>
                <div style="padding: 0.375rem 0.75rem; background: var(--bg-tertiary); 
                            border-radius: var(--radius-sm); font-size: 0.7rem; font-weight: 600; 
                            color: var(--text-secondary);">
                    {backups} Backups
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
    
    nav = st.radio(
        "nav",
        ["Dashboard", "Data Entry", "Analytics", "Import Data", "Settings", "Administration"],
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Quick Stats</div>', unsafe_allow_html=True)
    
    total_records = 0
    for f in files:
        try:
            df = pd.read_csv(f)
            total_records += len(df)
        except:
            pass
    
    st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Equipment Types</div>
                <div class="stat-value">{len(EQUIPMENT_TYPES)}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Total Records</div>
                <div class="stat-value">{total_records}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Quick Actions</div>', unsafe_allow_html=True)
    
    if st.button("Initialize Sample", key="sidebar_init", use_container_width=True):
        init_equipment("Pipeline", 1)
        st.success("Pipeline 1 initialized")
    
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Pages --------------------
if nav == "Dashboard":
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Dashboard</h1>
            <p class="page-subtitle">Real-time equipment monitoring overview</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    total_equips = len(files)
    
    st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Active Equipment</div>
                <div class="metric-value">{total_equips}</div>
                <div class="metric-trend">↑ {total_equips} tracked</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Equipment Types</div>
                <div class="metric-value">{len(EQUIPMENT_TYPES)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Records</div>
                <div class="metric-value">{total_records}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Backups</div>
                <div class="metric-value">{backups}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Recent Activity
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card"><h3 class="card-title">Recent Activity</h3></div>', unsafe_allow_html=True)
        
        latest_rows = []
        with st.spinner("Loading..."):
            for f in files:
                try:
                    df = pd.read_csv(f)
                    if 'timestamp' in df.columns:
                        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                    if df.empty:
                        continue
                    if 'timestamp' in df.columns and df['timestamp'].notna().any():
                        idx = df['timestamp'].idxmax()
                        r = df.loc[[idx]].copy()
                    else:
                        r = df.tail(1).copy()
                    latest_rows.append(r)
                except:
                    continue
        
        if latest_rows:
            try:
                df_latest = pd.concat(latest_rows, ignore_index=True)
                if 'timestamp' in df_latest.columns:
                    df_latest['timestamp'] = pd.to_datetime(df_latest['timestamp'], errors='coerce')
                    df_latest = df_latest.sort_values('timestamp', ascending=False, na_position='last')
                show_cols = [c for c in ['timestamp','equipment_type','equipment_id','operator'] if c in df_latest.columns]
                st.dataframe(df_latest[show_cols].head(15), use_container_width=True, height=500)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.info("No entries available")
    
    with col2:
        st.markdown('<div class="card"><h3 class="card-title">Equipment Distribution</h3></div>', unsafe_allow_html=True)
        
        eq_counts = {}
        for eq_type in EQUIPMENT_TYPES:
            count = len(list(LOG_DIR.glob(f"{eq_type.replace(' ', '_')}_*.csv")))
            if count > 0:
                eq_counts[eq_type] = count
        
        if eq_counts:
            for eq_type, count in eq_counts.items():
                pct = (count / total_equips * 100) if total_equips > 0 else 0
                st.markdown(f"""
                    <div style="margin-bottom: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span style="font-size: 0.75rem; font-weight: 600;">{eq_type}</span>
                            <span style="font-size: 0.75rem; color: var(--text-muted);">{count}</span>
                        </div>
                        <div style="background: var(--bg-tertiary); height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="background: var(--accent-primary); height: 100%; width: {pct}%;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

elif nav == "Data Entry":
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Data Entry</h1>
            <p class="page-subtitle">Record equipment readings</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="card"><h3 class="card-title">Equipment Selection</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        equipment_type = st.selectbox("Equipment Type", options=EQUIPMENT_TYPES, key="entry_type")
    
    with col2:
        equipment_id = st.selectbox("Equipment ID", options=PLACEHOLDER_IDS, key="entry_id")
    
    with col3:
        st.markdown('<div style="padding-top: 1.6rem;"></div>', unsafe_allow_html=True)
        if st.button("Initialize", use_container_width=True):
            init_equipment(equipment_type, equipment_id)
            st.success(f"Initialized {equipment_type} {equipment_id}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form("entry_form", clear_on_submit=False):
        st.markdown('<div class="form-section"><h4 class="form-section-title">Entry Details</h4>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date = st.date_input("Date", value=datetime.now().date())
            hour = st.selectbox("Hour", [f"{h:02d}:00" for h in range(24)])
            hour_int = int(hour.split(":")[0])
        
        with col2:
            operator = st.text_input("Operator", value="Operator 1")
            version = st.text_input("Version", value="v1.0")
        
        with col3:
            note = st.text_area("Notes", placeholder="Optional...", height=100)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-section"><h4 class="form-section-title">Parameters</h4>', unsafe_allow_html=True)
        
        param_cols = st.columns(3)
        param_widgets = {}
        specs = PARAM_SPECS.get(equipment_type, {})
        
        for i, (pname, pspec) in enumerate(specs.items()):
            dtype, unit, mn, mx = pspec
            col = param_cols[i % 3]
            label = f"{pname.title()} ({unit})" if unit else pname.title()
            
            if dtype == "float":
                val = col.text_input(label, value="", placeholder=f"{mn}-{mx}" if mn else "", key=f"param_{pname}")
                param_widgets[pname] = val
            else:
                if pname.lower() == "valve_status":
                    param_widgets[pname] = col.selectbox(label, options=["Open", "Closed", "Partially Open"], key=f"param_{pname}")
                elif pname.lower() == "leak_observed":
                    param_widgets[pname] = col.selectbox(label, options=["No", "Yes", "Suspected"], key=f"param_{pname}")
                else:
                    param_widgets[pname] = col.text_input(label, key=f"param_{pname}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Save Entry", use_container_width=True)
        
        if submitted:
            ts = datetime.combine(date, time(hour_int, 0, 0))
            row = {k: None for k in WIDE_COLUMNS}
            row.update({
                "timestamp": ts.isoformat(),
                "date": ts.date().isoformat(),
                "hour": hour_int,
                "equipment_type": equipment_type,
                "equipment_id": int(equipment_id),
                "operator": operator,
                "note": note,
                "created_at": datetime.utcnow().isoformat(),
                "version": version,
                "alarm_flag": False
            })
            
            for k, v in param_widgets.items():
                if v is None or (isinstance(v, str) and v.strip() == ""):
                    row[k] = None
                else:
                    spec = PARAM_SPECS[equipment_type][k]
                    if spec[0] == "float":
                        try:
                            row[k] = float(v) if v.strip() else None
                        except:
                            row[k] = v
                    else:
                        row[k] = v
            
            ok, messages = validate_row(equipment_type, row)
            append_equipment_row(equipment_type, equipment_id, row)
            
            if not ok:
                st.warning("Warnings: " + "; ".join(messages))
            else:
                st.success(f"Entry saved for {equipment_type} {equipment_id}")

elif nav == "Analytics":
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Analytics Dashboard</h1>
            <p class="page-subtitle">Visualize trends and detect anomalies</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card"><h3 class="card-title">Configuration</h3>', unsafe_allow_html=True)
        
        equipment_type = st.selectbox("Equipment Type", options=EQUIPMENT_TYPES, key="viz_type")
        equipment_id = st.selectbox("Equipment ID", options=PLACEHOLDER_IDS, key="viz_id")
        
        try:
            df = load_equipment_log(equipment_type, equipment_id)
            if not df.empty and 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        except Exception as e:
            st.error(f"Failed: {e}")
            df = pd.DataFrame()
        
        if df.empty:
            st.info("No data available")
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()
        
        candidate_cols = [c for c in df.columns if c not in ["timestamp","date","hour","equipment_type","equipment_id","operator","note","created_at","version","alarm_flag"]]
        
        if not candidate_cols:
            st.warning("No parameters found")
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()
        
        param = st.selectbox("Parameter", options=candidate_cols, key="viz_param")
        
        st.markdown("---")
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        min_dt = df['timestamp'].min().date() if not df['timestamp'].isna().all() else datetime.now().date()
        max_dt = df['timestamp'].max().date() if not df['timestamp'].isna().all() else datetime.now().date()
        
        start_date = st.date_input("Start Date", value=max(min_dt, max_dt - timedelta(days=7)), min_value=min_dt, max_value=max_dt)
        end_date = st.date_input("End Date", value=max_dt, min_value=min_dt, max_value=max_dt)
        
        st.markdown("---")
        
        z_thresh = st.slider("Threshold", 1.0, 5.0, 3.0, 0.5)
        window = st.slider("Window (hrs)", 3, 168, 24)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.spinner("Generating..."):
            try:
                sdt = datetime.combine(start_date, time(0,0,0))
                edt = datetime.combine(end_date, time(23,59,59))
                mask = (df['timestamp'] >= sdt) & (df['timestamp'] <= edt)
                dff = df.loc[mask].sort_values('timestamp').reset_index(drop=True)
                
                if dff.empty:
                    st.info("No records in range")
                else:
                    dff['_val'] = pd.to_numeric(dff[param], errors='coerce')
                    has_numeric = dff['_val'].notna().any()
                    anomalies = detect_anomalies(equipment_type, dff, param, z_thresh=z_thresh, window=window) if has_numeric else pd.Series([False]*len(dff))
                    dff['anomaly'] = anomalies
                    
                    if has_numeric:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=dff['timestamp'], y=dff['_val'], mode='lines+markers', name=param, line=dict(color='#2563eb', width=2.5)))
                        
                        if dff['anomaly'].any():
                            fig.add_trace(go.Scatter(x=dff.loc[dff['anomaly'],'timestamp'], y=dff.loc[dff['anomaly'],'_val'], mode='markers', name='Anomaly', marker=dict(color='#ef4444', size=12, symbol='x')))
                        
                        fig.update_layout(title=f"{equipment_type} {equipment_id} — {param}", xaxis_title="Time", yaxis_title=param, template="plotly_white", height=450, font=dict(family='Montserrat'))
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        col_a, col_b, col_c, col_d = st.columns(4)
                        col_a.metric("Mean", f"{dff['_val'].mean():.2f}")
                        col_b.metric("Std", f"{dff['_val'].std():.2f}")
                        col_c.metric("Min", f"{dff['_val'].min():.2f}")
                        col_d.metric("Anomalies", f"{dff['anomaly'].sum()}")
                        
                        if dff['_val'].dropna().shape[0] > 1:
                            hist = px.histogram(dff, x='_val', nbins=30, title=f"{param} Distribution", color_discrete_sequence=['#2563eb'])
                            hist.update_layout(template="plotly_white", font=dict(family='Montserrat'), height=350)
                            st.plotly_chart(hist, use_container_width=True)
                    
                    st.markdown('<div class="card"><h3 class="card-title">Data Preview</h3>', unsafe_allow_html=True)
                    display_cols = ['timestamp', param, 'anomaly']
                    st.dataframe(dff[display_cols].tail(25), use_container_width=True, height=400)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    csv_data = dff.to_csv(index=False).encode('utf-8')
                    st.download_button("Export Data", data=csv_data, file_name=f"export_{equipment_type}_{equipment_id}.csv", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

elif nav == "Import Data":
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Import Data</h1>
            <p class="page-subtitle">Upload CSV files</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
            <h3 class="card-title">CSV Format</h3>
            <p style="font-size: 0.8rem; color: var(--text-secondary);">Required columns: timestamp, equipment_type, equipment_id, parameter, value</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded = st.file_uploader("Choose CSV", type=['csv'])
    
    if uploaded:
        try:
            lf = pd.read_csv(uploaded)
            required = {'timestamp','equipment_type','equipment_id','parameter','value'}
            
            if not required.issubset(set(lf.columns)):
                st.error(f"Missing columns: {list(lf.columns)}")
            else:
                st.markdown('<div class="card"><h3 class="card-title">Preview</h3>', unsafe_allow_html=True)
                st.dataframe(lf.head(15), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("Confirm Import", use_container_width=True):
                    pivot = lf.pivot_table(index=['timestamp','equipment_type','equipment_id'], columns='parameter', values='value', aggfunc='first').reset_index()
                    count = 0
                    progress = st.progress(0)
                    
                    for idx, r in pivot.iterrows():
                        row = {k: None for k in WIDE_COLUMNS}
                        row.update({
                            'timestamp': r['timestamp'],
                            'equipment_type': r['equipment_type'],
                            'equipment_id': int(r['equipment_id']),
                            'created_at': datetime.utcnow().isoformat(),
                            'version': 'imported'
                        })
                        
                        for p in PARAM_SPECS.get(r['equipment_type'], {}).keys():
                            if p in pivot.columns:
                                row[p] = r.get(p)
                        
                        append_equipment_row(r['equipment_type'], int(r['equipment_id']), row)
                        count += 1
                        progress.progress(min(count / len(pivot), 1.0))
                    
                    st.success(f"Imported {count} rows")
        except Exception as e:
            st.error(f"Import failed: {e}")

elif nav == "Settings":
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Settings</h1>
            <p class="page-subtitle">Configure parameters</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card"><h3 class="card-title">Selection</h3>', unsafe_allow_html=True)
        etype = st.selectbox("Equipment Type", options=EQUIPMENT_TYPES)
        eid = st.selectbox("Equipment ID", options=PLACEHOLDER_IDS)
        
        if st.button("Initialize", use_container_width=True):
            init_equipment(etype, eid)
            st.success(f"Initialized {etype} {eid}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        key = f"{etype}_{eid}"
        mm = load_meta()
        pmeta = mm.get(key, {}).get('params', {}) if key in mm else {}
        
        if not pmeta:
            st.info("No metadata. Initialize first.")
        else:
            st.markdown('<div class="card"><h3 class="card-title">Parameters</h3>', unsafe_allow_html=True)
            
            for p, v in pmeta.items():
                st.markdown(f"**{p}** ({v.get('unit')})")
                c1, c2 = st.columns(2)
                mn = c1.text_input(f"Min {p}", value=str(v.get('min') if v.get('min') else ""), key=f"min_{p}")
                mx = c2.text_input(f"Max {p}", value=str(v.get('max') if v.get('max') else ""), key=f"max_{p}")
                
                try:
                    mm[key]['params'][p]['min'] = float(mn) if mn.strip() else None
                except:
                    mm[key]['params'][p]['min'] = None
                try:
                    mm[key]['params'][p]['max'] = float(mx) if mx.strip() else None
                except:
                    mm[key]['params'][p]['max'] = None
            
            if st.button("Save Config", use_container_width=True):
                save_meta(mm)
                st.success("Saved")
            st.markdown('</div>', unsafe_allow_html=True)

elif nav == "Administration":
    st.markdown("""
        <div class="page-header">
            <h1 class="page-title">Administration</h1>
            <p class="page-subtitle">System management</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Files", "Backups"])
    
    with tab1:
        st.markdown('<div class="card"><h3 class="card-title">Equipment Files</h3>', unsafe_allow_html=True)
        
        if files:
            sel = st.selectbox("Select File", options=[f.name for f in files])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Backup", use_container_width=True):
                    fn = LOG_DIR / sel
                    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                    dest = BACKUP_DIR / f"{fn.stem}_{ts}.csv"
                    shutil.copy(fn, dest)
                    st.success(f"Backed up")
            
            with col2:
                with open(LOG_DIR / sel, "rb") as fh:
                    st.download_button("Download", data=fh, file_name=sel, use_container_width=True)
        else:
            st.info("No files")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        if st.button("Export All as ZIP", use_container_width=True):
            if any(LOG_DIR.glob("*.csv")):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
                    with zipfile.ZipFile(tmp.name, "w") as z:
                        for f in LOG_DIR.glob("*.csv"):
                            z.write(f, arcname=f.name)
                    with open(tmp.name, "rb") as fh:
                        st.download_button("Download ZIP", data=fh, file_name=f"logs_{datetime.now().strftime('%Y%m%d')}.zip", use_container_width=True)
                    try:
                        os.unlink(tmp.name)
                    except:
                        pass
            else:
                st.warning("No data")

# Footer
st.markdown("""
    <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border); text-align: center;">
        <div style="font-size: 0.7rem; color: var(--text-muted);">
            CheckList v2.0 • Equipment Monitoring Platform • AI-DPRS © 2024
        </div>
    </div>
""", unsafe_allow_html=True)
